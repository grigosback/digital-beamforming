#%%
import sys

sys.path.insert(0, "${workspaceRoot}/algorithms/")
sys.path.insert(0, "${workspaceRoot}/inits/")

from inits.initialization import *
from algorithms.music import doamusic_estimation
from matplotlib import pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

from PIL import Image, ImageDraw, ImageFilter
import imageio
import math
import matplotlib

matplotlib.use("Agg")

# get_ipython().run_line_magic("matplotlib", "qt")


def plotanim(Data, X, step=0.02, ylim=[]):
    plt.ion()
    fig, ax = plt.subplots(1, 1)
    plt.ylim((10 ** -3, Data.max()))
    plt.yscale("log")
    line, = ax.plot(X, Data[:, 0])
    fig.canvas.draw()
    for i in range(Data.shape[1]):
        plt.pause(step)
        line.set_ydata(Data[:, i])
        fig.canvas.draw()
    plt.ioff()


#%%
x_start = np.array([-15, 0, 15])  # Start coordinate for the transmitter in m
v = np.array([1, 0, 0])  # Transmitter velocity in m/s
fc = 436 * MHz
amp = 10
freq = 1300
sine = Sine_Wave(amp, freq, fc)

n_time = 200
n_theta = 200
t_array = np.linspace(0, 30, n_time)
p_mu = np.zeros((n_theta, n_time), dtype=complex)
track = np.zeros((2, n_time))
theta = np.linspace(-np.pi / 2, np.pi / 2, num=n_theta)
lambda_c = c / rx.fc
k = 2 * np.pi / (lambda_c)
a = np.empty((rx.m, theta.size), dtype=complex)

for ax in range(theta.size):
    for i in range(rx.m):
        a[i, ax] = np.e ** (1j * i * k * rx.d * np.sin(theta[ax]))

for j in range(n_time):
    t = t_array[j]
    tx = Transmitter(x_start, v, t, sine)
    track[:, j] = np.array([tx.r[0], tx.r[2]])
    s = doamusic_samples(tx, rx, simulation)
    p_mu[:, j] = doamusic_estimation(s, a)

#%%
plt.figure()
plt.plot(theta * 180 / np.pi, np.log10(abs(p_mu[:, 0])))
plt.show()


# %%
plotanim(p_mu, theta)


# %%
step = 0.02
plt.ion()
fig, ax = plt.subplots(2, 1, figsize=(16, 9), dpi=100)
# arr_satelite = mpimg.imread("satelite.png")
# imagebox = OffsetImage(arr_satelite, zoom=0.08)
# ab = AnnotationBbox(imagebox, (track[0, 0], track[1, 0]))
# ax[0].add_artist(ab)

# img = cv2.imread('satelite.png', cv2.IMREAD_UNCHANGED)
img = Image.open("satelite.png")
# img = img.resize((int(img.size[0]*0.2),int(img.size[1]*0.2)))
# ax.figimage(img, track[0, 0], track[1, 0])
imagebox = OffsetImage(img, zoom=0.08)
ab = AnnotationBbox(imagebox, (track[0, 0], track[1, 0]), frameon=False)
ax[0].add_artist(ab)

ax[1].set_ylim((10 ** -3, p_mu.max()))
ax[1].set_yscale("log")
line1, = ax[1].plot(theta, p_mu[:, 0])


ax[0].set_ylim((0, track[1, :].max() * (1 + 0.3)))
ax[0].set_xlim((track[0, :].min() * 1.1, track[0, :].max() * 1.1))

line2, = ax[0].plot(track[0, 0], track[1, 0], "o")
arrow = ax[0].arrow(0, 0, track[0, 0], track[1, 0], width=1)

fig.canvas.draw()

for i in range(p_mu.shape[1]):
    plt.pause(step)
    ab = AnnotationBbox(imagebox, (track[0, i], track[1, i]), frameon=False)
    ax[0].add_artist(ab)
    line1.set_ydata(p_mu[:, i])

    line2.set_xdata(track[0, i])
    line2.set_ydata(track[1, i])
    arrow.set_xy([[0, 0], [track[0, i], track[1, i]]])
    arrow.set_linewidth(1)
    fig.canvas.draw()


plt.ioff()


#%%
step = 0.02
plt.ion()
fig, ax = plt.subplots(1, 1)
plt.ylim((0, track[1, :].max() * (1 + 0.3)))
plt.xlim((track[0, :].min() * 1.1, track[0, :].max() * 1.1))
# plt.yscale("log")
line, = ax.plot(track[0, 0], track[1, 0], "o")
arrow = ax.arrow(0, 0, track[0, 0], track[1, 0], width=1)
fig.canvas.draw()
for i in range(p_mu.shape[1]):
    plt.pause(step)
    line.set_xdata(track[0, i])
    line.set_ydata(track[1, i])
    arrow.set_xy([[0, 0], [track[0, i] * 0.9, track[1, i] * 0.9]])
    arrow.set_linewidth(10)
    fig.canvas.draw()
plt.ioff()

#%%

# %%
def image_array(i):
    print(i)
    tx = Transmitter(x_start, v, t_array[i], sine)
    fig, ax = plt.subplots(2, 1, figsize=(16, 9), dpi=150, num=0)
    img = Image.open("satelite.png")
    imagebox = OffsetImage(img, zoom=0.08)
    ab = AnnotationBbox(imagebox, (track[0, i], track[1, i]), frameon=False)
    ax[1].grid()
    ax[0].add_artist(ab)
    # ax[0].arrow(0,0,0,15,color='k',width=0.1)
    ax[0].annotate(
        "", xy=(0, 0), xytext=(0, 15), arrowprops=dict(arrowstyle="<-", linewidth=3)
    )
    ax[0].annotate(
        "", xy=(0, 0), xytext=(10, 0), arrowprops=dict(arrowstyle="<-", linewidth=3)
    )
    ax[0].annotate("x", xy=(9.5, 0.5))
    ax[0].annotate("z", xy=(0.5, 13.5))

    ax[1].set_ylim((p_mu.min(), p_mu.max()))
    ax[1].set_yscale("log")
    ax[1].set_ylabel(r"$|P_{MU}|$", size=15)
    ax[1].set_xlabel(r"$\theta$ [°]", size=15)
    line1, = ax[1].plot(theta * 180 / np.pi, p_mu[:, i])
    idx = np.argmax(p_mu[:, i])
    ax[1].plot(
        (theta[idx] * 180 / np.pi, theta[idx] * 180 / np.pi),
        (0, p_mu.max()),
        linestyle="--",
        color="r",
        linewidth=2,
    )
    ax[1].annotate(
        "%.2f°" % (theta[idx] * 180 / np.pi),
        xy=(theta[idx] * 180 / np.pi + 3, 10 ** 3),
        size=15,
    )
    # ax[1].annotate("pru", xy=(25, 1), size=15)

    ax[0].set_ylim((0, track[1, :].max() * (1 + 0.3)))
    ax[0].set_xlim((track[0, :].min() * 1.1, track[0, :].max() * 1.1))

    # line2, = ax[0].plot(track[0, i], track[1, i], "o")
    arrow = ax[0].arrow(
        0,
        0,
        track[0, i] * 0.9,
        track[1, i] * 0.9,
        width=0.15,
        length_includes_head=True,
        color="r",
    )

    # angle_plot = get_angle_plot(txs[i].doa.theta, 1)
    theta_deg = tx.doa.theta * 180 / np.pi
    if theta_deg < 0:
        arc = matplotlib.patches.Arc((0, 0), 10, 10, 0, 90, 90 - theta_deg)
        ax[0].add_patch(arc)  # To display the angle arc
        ax[0].annotate("%.2f" % theta_deg, xy=(0.5, 2.5), size=15)
    else:
        arc = matplotlib.patches.Arc((0, 0), 10, 10, 0, 90 - theta_deg, 90)
        ax[0].add_patch(arc)  # To display the angle arc
        ax[0].annotate("%.2f" % theta_deg, xy=(-2, 2.5), size=15)

    fig.canvas.draw()  # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image


#%%
kwargs_write = {"fps": 10.0, "quantizer": "nq"}
imageio.mimsave("./sim_tracking.gif", [image_array(i) for i in range(n_time)], fps=10)


#%%
i = 0
tx = Transmitter(x_start, v, t_array[i], sine)
fig, ax = plt.subplots(2, 1, figsize=(16, 9), dpi=100, num=0)
img = Image.open("satelite.png")
imagebox = OffsetImage(img, zoom=0.08)
ab = AnnotationBbox(imagebox, (track[0, i], track[1, i]), frameon=False)
ax[1].grid()
ax[0].add_artist(ab)
# ax[0].arrow(0,0,0,15,color='k',width=0.1)
ax[0].annotate(
    "", xy=(0, 0), xytext=(0, 15), arrowprops=dict(arrowstyle="<-", linewidth=3)
)
ax[0].annotate(
    "", xy=(0, 0), xytext=(10, 0), arrowprops=dict(arrowstyle="<-", linewidth=3)
)
ax[0].annotate("x [m]", xy=(9.5, 0.5))
ax[0].annotate("z [m]", xy=(0.5, 13.5))

ax[1].set_ylim((p_mu.min(), p_mu.max()))
ax[1].set_yscale("log")
ax[1].set_ylabel(r"$|P_{MU}|$", size=15)
ax[1].set_xlabel(r"$\theta$ [°]")
line1, = ax[1].plot(theta * 180 / np.pi, p_mu[:, i])
idx = np.argmax(p_mu[:, i])
ax[1].plot(
    (theta[idx] * 180 / np.pi, theta[idx] * 180 / np.pi),
    (0, p_mu.max()),
    linestyle="--",
    color="r",
    linewidth=2,
)
ax[1].annotate(
    "%.2f°" % (theta[idx] * 180 / np.pi),
    xy=(theta[idx] * 180 / np.pi + 3, 10 ** 3),
    size=15,
)
# ax[1].annotate("pru", xy=(25, 1), size=15)

ax[0].set_ylim((0, track[1, :].max() * (1 + 0.3)))
ax[0].set_xlim((track[0, :].min() * 1.1, track[0, :].max() * 1.1))

# line2, = ax[0].plot(track[0, i], track[1, i], "o")
arrow = ax[0].arrow(
    0,
    0,
    track[0, i] * 0.9,
    track[1, i] * 0.9,
    width=0.15,
    length_includes_head=True,
    color="r",
)

# angle_plot = get_angle_plot(txs[i].doa.theta, 1)
theta_deg = tx.doa.theta * 180 / np.pi
if theta_deg < 0:
    arc = matplotlib.patches.Arc((0, 0), 10, 10, 0, 90, 90 - theta_deg)
    ax[0].add_patch(arc)  # To display the angle arc
    ax[0].annotate("%.2f" % theta_deg, xy=(0.5, 2.5), size=15)
else:
    arc = matplotlib.patches.Arc((0, 0), 10, 10, 0, 90 - theta_deg, 90)
    ax[0].add_patch(arc)  # To display the angle arc
    ax[0].annotate("%.2f" % theta_deg, xy=(-2, 2.5), size=15)

fig.canvas.draw()  # draw the canvas, cache the renderer
image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))


# %%
tx.r

# %%
