import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import random


def interactive_plot(x, y, c, img_list, use_log10=True):
    """ Modified from this: https://stackoverflow.com/questions/42867400/python-show-image-upon-hovering-over-a-point
    """
    cmap = plt.cm.RdYlGn
    if use_log10:
        c = np.log10(c)
    # create figure and plot scatter
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # line, = ax.plot(x,y, ls="", marker="o")
    line = plt.scatter(x, y, c=c, s=20, cmap="viridis")

    # create the annotations box
    image = plt.imread(img_list[0])
    im = OffsetImage(image, zoom=0.5)
    xybox = (150., 150.)
    ab = AnnotationBbox(im, (0, 0), xybox=xybox, xycoords='data', boxcoords="offset points", pad=0.3,
                        arrowprops=dict(arrowstyle="->"))
    # add it to the axes and make it invisible
    ax.add_artist(ab)
    ab.set_visible(False)

    def hover(event):
        # if the mouse is over the scatter points
        if line.contains(event)[0]:
            # find out the index within the array from the event
            indices = line.contains(event)[1]["ind"]
            if len(indices) > 1:
                ind = random.choice(indices)
            else:
                ind = indices[0]
            # get the figure size
            w, h = fig.get_size_inches() * fig.dpi
            ws = (event.x > w / 2.) * -1 + (event.x <= w / 2.)
            hs = (event.y > h / 2.) * -1 + (event.y <= h / 2.)
            # if event occurs in the top or right quadrant of the figure,
            # change the annotation box position relative to mouse.
            ab.xybox = (xybox[0] * ws, xybox[1] * hs)
            # make annotation box visible
            ab.set_visible(True)
            # place it at the position of the hovered scatter point
            ab.xy = (x[ind], y[ind])
            # set the image corresponding to that point
            im.set_data(plt.imread(img_list[ind]))
        else:
            # if the mouse is not over a scatter point
            ab.set_visible(False)
        fig.canvas.draw_idle()
    # add callback for mouse moves
    fig.canvas.mpl_connect('motion_notify_event', hover)
    fig = plt.gcf()
    fig.set_size_inches(12, 8)
    plt.show()


def run_interact_plot(tsne_filename, img_folder, activity_filename=None):
    if img_folder.endswith('/'):
        img_folder = img_folder[:-1]
    with open(tsne_filename) as f:
        lines = f.readlines()
    x = np.zeros(len(lines)-1)
    y = np.zeros(len(lines)-1)
    img_list = []
    for i, line in enumerate(lines[1:]):
        ll = line.split()
        img_list.append('{}/{}.png'.format(img_folder, ll[0]))
        x[i] = float(ll[1])
        y[i] = float(ll[2])
    c = np.zeros(len(x))
    if activity_filename is not None:
        with open(activity_filename) as f:
            lines = f.readlines()
        for i, line in enumerate(lines[1:]):
            c[i] = float(line.split()[-1])
    interactive_plot(x, y, c, img_list)



