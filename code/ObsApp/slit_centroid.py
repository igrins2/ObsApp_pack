from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import mpl_toolkits.axisartist as AA
from matplotlib.axes import Axes
import astropy.io.fits as pyfits
from mpl_slit_centroid import SW_centroid_finder
import scipy.ndimage as ni

from PySide6.QtWidgets import QFrame
                               
class MplFrame(QFrame):
    def __init__(self, parent, width, height, pixel_scale=1, cb_left_click=None):
        """
        cb_left_click : will take a xdata argument.
        """
        self.frame_profile = parent
        self.pixel_scale = pixel_scale

        self.cb_left_click = cb_left_click

        # canvas        
        self.ax = None
        self.canvas = None
        self.fig = Figure(figsize=(width, height), dpi=100)
        #self.ax = self.fig.add_subplot(111)            
        #self.fig.subplots_adjust(left=0.01,right=0.99,bottom=0.01, top=0.99) 
        self.canvas = FigureCanvas(self.fig)
        
        vbox_svc = QVBoxLayout(self.frame_profile)
        vbox_svc.addWidget(self.canvas)
        

    def plot(self, finder,
             sw_slit_star_stack=None):
        if sw_slit_star_stack is None:
            sw_slit_star_stack = []
            nn = 0
        else:
            sw_slit_star_stack, nn = sw_slit_star_stack

        print(sw_slit_star_stack)
        self.fig.clf()
        # ax = AA.Subplot(self.fig, 111)
        # self.fig.add_subplot(ax)
        ax = AA.Axes(self.fig, [0.02, 0.05, 1.-2*0.02, 0.7-2*0.05])
        ax2 = Axes(self.fig, [0.02, 0.7+0.05, 1.-2*0.02, 0.3-2*0.05],
                   sharex=ax)
        self.fig.add_axes(ax)
        self.fig.add_axes(ax2)

        ax2.set_axis_off()

        # self.ax = ax
        # ax.axis["left"].set_axis_direction("right")
        ax.axis[:].invert_ticklabel_direction()
        ax.axis[:].major_ticks.set_tick_out(True)
        ax.axis["left"].toggle(ticklabels=False)
        # self.fig.tight_layout()
        # ax.tick_params(direction="in")
        # ax.label_params(direction="in")

        # ax.plot([1, 2, 3])
        sw_slit0, sw_star0 = finder.plot(ax, pixel_scale=self.pixel_scale)

        sw_star_color = "green"
        sw_star_color1 = "0.8"
        sw_slit_list = [[sw_slit0]]  # to only select before tel move.
        sw_star_colors = [sw_star_color]
        sw_star_list = [sw_star0]

        for c, sw_slit, sw_star in sw_slit_star_stack:
            if c == "offset":
                sw_slit_list[-1].append(sw_slit)
                sw_star_list.append(sw_star)
                sw_star_colors.append(sw_star_color)
            else:
                sw_slit_list.append([])
                sw_star_color = sw_star_color1

        print(sw_slit_list)
        print("---", np.median(sw_slit_list[0]))
        ax2.axvline(np.median(sw_slit_list[0]), color="0.8",
                    linewidth=2)
        ax2.scatter(sw_star_list, range(len(sw_star_list)),
                    c=sw_star_colors, clip_on=False, s=4,
                    zorder=10)

        ax2.set_ylim(0, nn)
        self.canvas.draw()

        return sw_slit0, sw_star0



    def reset_image(self):
        self.fig.clf()
        self.fig.text(0.5, 0.5, 'N/A')
        self.canvas.draw()
        

    def update_image(self, imgdata, maskdata, cx, cy, pa, s=64,
                     sw_slit_star_stack=None):
        flat = None
        finder = SW_centroid_finder(imgdata, flat, maskdata, cx, cy,
                                    PA=pa, s=s)

        sw_slit, sw_star = self.plot(finder,
                                     sw_slit_star_stack=sw_slit_star_stack)
        return sw_slit, sw_star

'''
if __name__ == '__main__':
    
    def test(frame):
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

        stack = [["offset", 0.1, 0.3],
                 ["offset", 0.11, -0.2],
                 ["tel_move", None, None],
                 ["offset", 0.0911, -0.1]]

        frame.plot(finder, (stack, 10))

        # fig = plt.figure(1)
        # fig.clf()
        # ax = fig.add_subplot(111)

        # sw_slit, sw_star = finder.plot(ax, [])

        # return sw_slit, sw_star
        
    f = MplFrame(root, 3, 2)
    test(f)
'''