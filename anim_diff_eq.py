import scipy.integrate
from matplotlib import animation as anim, pyplot as plt
import matplotlib as mpl
import numpy as np
import math, sys


mpl.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg-build\bin\ffmpeg.exe'
plt.style.use(r'C:\Users\lnick\Documents\Personal\Programming\Python\Resources\proplot_style.mplstyle')


INITIAL_VALUES = np.array([25, 75])     # initial values of dependent variables
INITIAL_T = 0                           # initial value of independent variable
STEP_T = 1e-2                           # maximum integration step size
ANIM_STEP_T = 1e-0                      # update frame every interval
DEP_VAR_NAMES = ('Tank A', 'Tank B')    # shown in legend
SAVE_OR_VIEW = 'view'


def system_rhs(t: float, y_vec: np.ndarray) -> np.ndarray:

    x, y = y_vec

    return np.array([
        7*1.5 + 5*y/100 - 12*x/50,      # = dx/dt
        2*x/50 - 5*y/100                # = dy/dt
    ])


def animate(frame: int, last_vals: np.ndarray, all_t, all_y_vec):

    # set graphical options
    plt.cla()
    plt.title('Evolution of system')
    plt.xlabel('Time / hrs')
    plt.ylabel('Mass of contaminant / g')

    # the values of t to be plotted in this frame
    t_range = np.array([INITIAL_T + STEP_T * frame * window, \
                        INITIAL_T + STEP_T * (frame + 1) * window])

    # set first values for this range
    last_vals = [y_val[-1] for y_val in all_y_vec] if frame != 0 else INITIAL_VALUES

    # solve system over these t bounds
    sol = scipy.integrate.solve_ivp(system_rhs, t_range,
        last_vals, method="BDF", max_step=STEP_T)  # solve the system over these t
    
    # record values up to this latest point
    all_t += list(sol.t)
    for i in range(NUM_DEPENDENT_VARS):
        all_y_vec[i] += list(sol.y[i])

    # print for record
    print(f't = {round(all_t[-1], 5)}, y_vec = {[y_val[-1] for y_val in sol.y]}')

    # plot full lines up to the latest point
    for varname, solution in zip(DEP_VAR_NAMES, all_y_vec):
        plt.plot(all_t, solution, label=varname)

    # show legend
    plt.legend(loc='lower left')


NUM_DEPENDENT_VARS = len(DEP_VAR_NAMES)
window = int(ANIM_STEP_T / STEP_T)
last_vals = INITIAL_VALUES
all_t = []
all_y_vec = [[] for _ in range(NUM_DEPENDENT_VARS)]

fig = plt.figure()
ani = anim.FuncAnimation(fig, animate, interval=10, save_count=sys.maxsize, \
                         fargs=(last_vals, all_t, all_y_vec))

if SAVE_OR_VIEW == 'view':
    plt.show()
elif SAVE_OR_VIEW == 'save':
    ani.save('MyVideo.mp4', writer=anim.FFMpegWriter(fps=30, codec='h264'))
