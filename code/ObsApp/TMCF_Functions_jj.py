import numpy as np
import scipy.ndimage as ni
from scipy.optimize import leastsq

def gaussian2d(fHeight,fCenterX,fCenterY,fWidth,fBackground):
    try:
        """ Return a gaussian function with a given parameters"""
        fWidth = float(fWidth)
        return lambda y,x: fHeight*np.exp(-(((fCenterX - x)/fWidth)**2 + ((fCenterY - y)/fWidth)**2)/2) + fBackground
    
    except ZeroDivisionError:
        pass
    except ValueError:
        pass
    except Exception as e:
        import traceback, sys
        traceback.print_exc(file=sys.stdout)


def moments2d(aData, mask=None):
    """ Return (fHeight,fCenterX,fCenterY,fWidth,fBackground) the Gaussian parameters
of a 2D distribution by calculating its moments"""

    try:
        ny, nx = aData.shape
        aY, aX = np.indices(aData.shape)

        if mask is not None:
            aData2 = np.ma.array(aData, mask=~mask)
        else:
            aData2 = aData
        fBackground = np.ma.median(aData2)
        aData2 = aData2 - fBackground
        mask_std = aData2 > 3.*np.std(aData2)

        if mask is not None:
            mask = mask & mask_std
        else:
            mask = mask_std

        aData = aData[mask]
        aY = aY[mask]
        aX = aX[mask]

        fTotal = aData.sum()
        if fTotal <= 0:
            return None
        fCenterX = (aX * aData).sum()/fTotal
        fCenterY = (aY * aData).sum()/fTotal

        fWidth = (((aY-fCenterY)**2+(aX-fCenterX)**2)**.5*aData).sum()/fTotal
        if fWidth <= 0:
            return None
        fHeight =  fTotal/(np.pi*fWidth)**2 #- fBackground
        return fHeight,fCenterX,fCenterY,fWidth,fBackground
    
    except ZeroDivisionError:
        pass
    except ValueError:
        pass
    except Exception as e:
        import traceback, sys
        traceback.print_exc(file=sys.stdout)


def fitgaussian2d(aData, aParams=None, mask=None,
                  fit_width=True):
    """ Return (fHeight,fCenterX,fCenterY,fWidth) the Gaussian parameters
of a 2D distribution found by a fit.
    If fit_width is False, width & background is fixed during the fit.
    """
    try:
        if aParams is None:
            aParams = np.array(moments2d(aData, mask))

        ny, nx = aData.shape
        aY, aX = np.indices(aData.shape)

        if mask is not None:
            aData = aData[mask]
            aY, aX = aY[mask], aX[mask]
        else:
            aData = aData.flat
            aY, aX = aY.flat, aX.flat


        if fit_width:
            def errorfunction_ls(p):
                _f = gaussian2d(*p)
                return _f(aY, aX) - aData

            r = leastsq(errorfunction_ls, aParams)[0]
        else:
            def errorfunction_ls(p):
                params = list(p) + list(aParams[-2:])

                # print(p)
                # print(list(p))
                # print(aParams)
                # print(aParams[-2:])
                # print(list(aParams[-2:]))
                # print(params)

                _f = gaussian2d(*params)
                return _f(aY, aX) - aData

            #print(errorfunction_ls, aParams)
            #20231007
            if aParams == None:
                return

            r_ = leastsq(errorfunction_ls, aParams[:-2])[0]
            r = list(r_) + list(aParams[-2:])

        # print(r)

        return r
    
    except Exception as e:
        import traceback, sys
        traceback.print_exc(file=sys.stdout)


def fitgaussian2d_mask(imgdata, mask, fit_width=False, ZOOMW=32):    #fit_witdh=false

    mask = ~mask

    dm = ni.median_filter(imgdata, 3)

    r_initial = moments2d(dm, mask=mask)
    #print("r_initial", r_initial)
    r_final = fitgaussian2d(dm, aParams=r_initial, mask=mask,
                                fit_width=fit_width)

    # print(r_final)
    return r_final


def fitgaussian2d_mask_fixed_width(imgdata, mask,
                                   width, ZOOMW=32):

    mask = ~mask

    dm = ni.median_filter(imgdata, 3)

    r_initial = moments2d(dm, mask=mask)

    # replace fwhm in r_initial with given width
    r_initial = list(r_initial)
    r_initial[-2] = width

    r_final = fitgaussian2d(dm, aParams=r_initial, mask=mask,
                                fit_width=False)

    # print(r_final)
    return r_final


def fitgaussian2d_mask_with_saturation(img, mask, fit_width=False):
    saturation_mask_ = (img>10000) | (img < 0) | ~np.isfinite(img)
    import scipy.ndimage as ni
    saturation_mask1 = ni.binary_closing(saturation_mask_, iterations=10)
    saturation_mask = ni.binary_dilation(saturation_mask1, iterations=2)

    #mask = ~mask
    msk = mask | saturation_mask
    r = fitgaussian2d_mask(img, mask=msk, fit_width=fit_width)
    #print(tmcf.moments2d(img, mask=msk))
    return r

def fitgaussian2d_mask_with_saturation_fixed_width(img, mask, width):
    saturation_mask_ = (img>10000) | (img < 0) | ~np.isfinite(img)
    import scipy.ndimage as ni
    saturation_mask1 = ni.binary_closing(saturation_mask_, iterations=10)
    saturation_mask = ni.binary_dilation(saturation_mask1, iterations=2)

    #mask = ~mask
    msk = mask | saturation_mask
    r = fitgaussian2d_mask_fixed_width(img, mask=msk, width=width)
    #print(tmcf.moments2d(img, mask=msk))
    return r

if __name__ == "__main__":
    import astropy.io.fits as pyfits
    #import pyfits

    f = pyfits.open("/IGRINS/FITS/SC/SDCS_20140316_0505.fits")

    r_final = fitgaussian2d_mask(f[0].data, False, ZOOMW=32)


    '''
    mask_ = f[0].data>20
    print(f)
    print(f[0])
    print(f[0].data)

    mask_ = ni.binary_closing(mask_)
    mask = ni.binary_erosion(mask_, iterations=1)

    slice_1y, slice_1x = slice(925, 1125), slice(915, 1115)
    d1 = f[0].data[slice_1y, slice_1x]
    msk1 = mask[slice_1y, slice_1x]

    slice_2y, slice_2x = slice(677, 877), slice(855, 1055)
    d2 = f[0].data[slice_2y, slice_2x]
    msk2 = mask[slice_2y, slice_2x]

    # median filtering to suppress CR/hotpixels
    d1m = ni.median_filter(d1, 3)
    d2m = ni.median_filter(d2, 3)

    fit_width=True

    r2_initial = moments2d(d2m,
                           mask=msk2)

    r2_final = fitgaussian2d(d2m,
                             aParams=r2_initial,
                             mask=msk2,
                             fit_width=fit_width)

    r1_initial = moments2d(d1m, mask=msk1)

    r1_final = fitgaussian2d(d1m,
                             aParams=r1_initial,
                             mask=msk1,
                             fit_width=fit_width)

    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    for ax, d, r_initial, r_final in [(ax1, d1, r1_initial, r1_final),
                                      (ax2, d2, r2_initial, r2_final)]:
        ax.imshow(d, origin="lower")
        ax.plot([r_initial[1]], [r_initial[2]], "wo", ms=10)
        ax.plot([r_final[1]], [r_final[2]], "r+", ms=10)
        ax.set(xlim=(-0.5, 200.5), ylim=(-0.5, 200.5))

    plt.show()
    '''
