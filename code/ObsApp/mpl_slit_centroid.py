import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as pyfits
import scipy.ndimage as ni
from astropy.modeling import models, fitting


def sub_bg(d, msk):
    bg = np.median(d[msk])
    return d - bg


def zero_mask(d, msk):
    d2 = d.copy()
    d2[msk] = 0.
    return d2


def nan_mask(d, msk):
    d2 = d.copy()
    d2[msk] = np.nan
    return d2


def rot(pa, dx, dy):
    _pa = np.deg2rad(pa)
    dsl = - (dx*np.cos(_pa) - dy*np.sin(_pa))
    dsw = (dx*np.sin(_pa) + dy*np.cos(_pa))

    return dsl, dsw


def get_sorted_medianed(dsw, dd, sl_msk, median_size=5):
    swm, dm = dsw[sl_msk], dd[sl_msk]
    idx = np.argsort(swm)

    xx, yy = swm[idx], dm[idx]
    yym = ni.median_filter(yy, median_size)

    return xx, yym


class SW_centroid_finder():
    def __init__(self, data, flat, msk0, cx, cy,
                 s=64, PA=45.):
        self.data = data
        self.flat = flat
        self.msk0 = msk0
        self.cxcy = cx, cy
        self.s_size = s
        self.pa = PA
        # self.pixel_scale = pixel_scale

        iy0, ix0 = np.indices(data.shape)
        dy0, dx0 = iy0 - cy, ix0 - cx

        self.sl = (slice(int(cy)-s, int(cy)+s+1),
                   slice(int(cx)-s, int(cx)+s+1))

        dy, dx = dy0[self.sl], dx0[self.sl]

        self.dsl, self.dsw = rot(PA, dx, dy)

        k = int(s/4.)
        self.sl_msk = ((-k < self.dsl) & (self.dsl < k))

        self.dd = data[self.sl]

    def get_sw_slit(self):

        dsw = self.dsw
        dd = self.dd
        sl = self.sl
        sl_msk = self.sl_msk
        msk0 = self.msk0

        xx, yy = get_sorted_medianed(dsw, dd, sl_msk)

        # estimate the threshold
        m1 = np.percentile(dd[~(msk0[sl])], 10)
        m2 = np.percentile(dd[msk0[sl]], 50)
        m_thresh = .5*(m1 + m2)
        print("TTT", m1, m2, m_thresh)
        m_msk = yy < m_thresh
        return m_thresh, xx[m_msk], yy[m_msk]

    def find_sw_slit_centroid(self, xy_data=None):
        if xy_data is None:
            _m_thresh, x, y = self.get_sw_slit()
        else:
            x, y = xy_data

        # 1st attemp to fit
        p = np.polyfit(x, y, 2)
        p_root = np.poly1d(p).deriv(1).roots[0]

        return p_root

    def get_sw_star(self, m_thresh):

        sl = self.sl
        sl_msk = self.sl_msk
        dsw = self.dsw

        msk = ni.binary_dilation(ni.binary_opening(self.data < m_thresh))
        if self.flat is not None:
            d = self.data / self.flat
        else:
            d = self.data
        ds = d[sl]
        ds = nan_mask(ds, msk[sl])

        xx, yy = get_sorted_medianed(dsw, ds, sl_msk)

        mfinite = np.isfinite(yy)

        return xx, yy, mfinite

    def find_sw_star_model(self, xy_data=None):
        if xy_data is None:
            xx, yy, mfinite = self.get_sw_star()
            x, ym = xx[mfinite], yy[mfinite]

        else:
            x, ym = xy_data

        ymin = np.percentile(ym, 10)
        ymax = np.percentile(ym, 99)
        g_init1 = models.Gaussian1D(amplitude=ymax-ymin, mean=0, stddev=20.)
        # g_init1.fixed["stddev"] = True
        g_init1.amplitude.min = 0
        # g_init2 = models.Moffat1D(amplitude=1., x_0=0, gamma=20)
        # g_init3 = models.Voigt1D(amplitude_L=1., x_0=0, fwhm_L=20, fwhm_G=20)
        # c = models.Linear1D()


        fit_g = fitting.LevMarLSQFitter()
        # fit_g = fitting.SimplexLSQFitter()
        # g1 = fit_g(g_init1 + c, x, ym)
        c = models.Const1D(amplitude=ymin)
        c.fixed["amplitude"] = True

        g1 = fit_g(g_init1 + c, x, ym)

        # g2 = fit_g(g_init2 + c, x, ym)
        # g3 = fit_g(g_init3 + c, x, ym)
        return g1

    def find_sw_star_centroid(self, xy_data=None):
        # returns center of the slit and centroid of the star.
        g1 = self.find_sw_star_model(xy_data)
        return g1.mean_0.value

    def get_all(self):
        m_thresh, x, y = self.get_sw_slit()
        sl_slit = self.find_sw_slit_centroid((x, y))
        xx, yy, mfinite = self.get_sw_star(m_thresh)
        x, ym = xx[mfinite], yy[mfinite]
        sl_star = self.find_sw_star_centroid((x, ym))

        return sl_slit, sl_star

    def plot(self, ax, pixel_scale=1.):
        # self = finder
        m_thresh, x, y = self.get_sw_slit()
        sw_slit = self.find_sw_slit_centroid((x, y))
        xx, yy, mfinite = self.get_sw_star(m_thresh)
        x, ym = xx[mfinite], yy[mfinite]

        bins = np.arange(int(x.min()) - 0.5, int(x.max()) + 0.5, 1)
        v = np.histogram(x, weights=ym, bins=bins)[0]
        w = np.histogram(x, bins=bins)[0]

        vw = v/w
        # vw_mask = np.isfinite(vw)
        vw_mask = w > 10.
        vx = 0.5 * (bins[:-1] + bins[1:])

        # sw_star_model = self.find_sw_star_model((x, ym))
        sw_star_model = self.find_sw_star_model((vx[vw_mask],
                                                 vw[vw_mask]))
        sw_star = sw_star_model.mean_0.value

        import matplotlib.transforms as mtrans
        tr = mtrans.blended_transform_factory(ax.transData, ax.transAxes)

        ax.set_autoscaley_on(True)
        ax.plot(vx*pixel_scale,
                np.ma.array(vw, mask=~vw_mask).filled(np.nan),
                # vw,
                "-", zorder=5, lw=3,
                drawstyle='steps-mid')
        ax.set_autoscaley_on(False)
        ax.plot(xx*pixel_scale, yy, ".", color="r", alpha=0.2, zorder=3)
        ax.fill_betweenx([0, 1],
                         (sw_slit-4)*pixel_scale, (sw_slit+4)*pixel_scale,
                         transform=tr, facecolor="0.8", alpha=0.5, zorder=2)
        x1 = np.linspace(-32, 32, 128) # no pixel scale applied as this is
                                       # given to model
        ax.plot(x1*pixel_scale, sw_star_model(x1))
        # print("$$$", sw_star)
        ax.axvline(sw_star*pixel_scale, linestyle=":")
        ax.set_xlim(-32*pixel_scale, 32*pixel_scale)
        ylim = ax.get_ylim()
        ymax_cand1 = np.nanpercentile(vw, 99)
        ymax_cand2 = sw_star_model(x1).max()
        ax.set_ylim(ylim[0], np.max([ymax_cand1, ymax_cand2]))

        return sw_slit*pixel_scale, sw_star*pixel_scale


def test():
    f1 = pyfits.open("../../svc_examples/SDCS_20170903_0001.fits.fz")
    f2 = pyfits.open("../../svc_examples/SDCS_20170903_0002.fits.fz")

    flat = f1[2].data

    # use pregenerated mask here instead.
    msk0 = ni.binary_dilation(ni.binary_opening(f2[2].data < 100))

    # cx, cy = 1003, 1046
    cx, cy = 110, 147
    s = 64
    PA = 45

    data = f2[2].data

    finder = SW_centroid_finder(data, flat, msk0, cx, cy)

    fig = plt.figure(1)
    fig.clf()
    ax = fig.add_subplot(111)

    sw_slit, sw_star = finder.plot(ax)


def test_simul():
    cx, cy = 1004.5, 1047.6 # A
    # cx, cy = 1024.0, 1027.5 # A (center)
    s = 32
    PA = 45

    f = pyfits.open("test.fits")
    data = f[0].data
    msk0 = f[1].data > 0
    flat = None
    finder = SW_centroid_finder(data, flat, msk0, cx, cy)

    fig = plt.figure(1)
    fig.clf()
    ax = fig.add_subplot(111)

    sw_slit, sw_star = finder.plot(ax, 0.1)
    print(sw_slit)

# if False:
#     m_thresh, x, y = finder.get_sw_slit()
#     sl_slit = finder.find_sw_slit_centroid((x, y))
#     xx, yy, mfinite = finder.get_sw_star(m_thresh)
#     x, ym = xx[mfinite], yy[mfinite]
#     sl_star_model = finder.find_sw_star_model((x, ym))
#     sl_star = sl_star_model.mean_0.value

#     import matplotlib.transforms as mtrans
#     tr = mtrans.blended_transform_factory(ax.transData, ax.transAxes)

#     ax.plot(xx - sl_slit, yy, ".")
#     ax.set_autoscaley_on(False)
#     ax.fill_betweenx([0, 1], -4, 4,
#                      transform=tr, facecolor="0.8", alpha=0.5)
#     x1 = np.linspace(-32, 32, 128)
#     ax.plot(x1, sl_star_model(x1))
#     ax.axvline(sl_star, linestyle=":")
#     ax.set_xlim(-32, 32)

#     # from mpl_inner_title import add_inner_title

#     ax.set_title("dSW=0,23\"")
#     fig.tight_layout()
