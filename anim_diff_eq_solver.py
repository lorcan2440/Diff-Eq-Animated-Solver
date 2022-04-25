import scipy.integrate
from matplotlib import animation as anim, pyplot as plt
import matplotlib as mpl
import numpy as np
import math, sys, time


FFMPEG_PATH = r'C:\ffmpeg-build\bin\ffmpeg.exe'
MPL_STYLESHEET = r'C:\Users\lnick\Documents\Personal\Programming\Python\Resources\proplot_style.mplstyle'

INITIAL_VALUES = np.array([10, 6])      # initial values of dependent variables
INITIAL_T = 0                           # initial value of independent variable
MAX_STEP_T = 0.01                           # maximum integration step size
ANIM_STEP_T = 2                       # update frame every interval
SLIDING_WINDOW_T = 60                   # start moving along with the graph after this time
DEP_VAR_NAMES = np.array(['Rabbits (prey)', 'Foxes (predators)'])    # shown in legend
SAVE_OR_VIEW = 'view'                   # save: terminate program to end video recording, or
                                        # view: watch graphing in progress

def system_rhs(t: float, y_vec: np.ndarray) -> np.ndarray:

    a, b, c, d = 1.1, 0.4, 0.1, 0.4
    x, y = y_vec

    return np.array([
        a * x - b * x * y,      # = dx/dt
        c * x * y - d * y       # = dy/dt
    ])


def init_graph():

    plt.style.use(MPL_STYLESHEET)
    mpl.rcParams['animation.ffmpeg_path'] = FFMPEG_PATH


def animate(frame: int, history: dict[str, np.ndarray]) -> None:

    # clear and set graphical options
    plt.cla()
    plt.title('Evolution of populations')
    plt.xlabel('Time / weeks')
    plt.ylabel('Population, in hundreds')

    # the new values of t to be plotted in this frame
    t_range = np.array([INITIAL_T + MAX_STEP_T * frame * window, \
                        INITIAL_T + MAX_STEP_T * (frame + 1) * window])

    # set first values for this range
    last_vals, all_t, all_y_vec = history['last_vals'], history['all_t'], history['all_y_vec']
    last_vals = all_y_vec[:, -1] if frame != 0 else INITIAL_VALUES

    # solve system over these t bounds
    sol = scipy.integrate.solve_ivp(system_rhs, t_range,
        last_vals, method="BDF", max_step=MAX_STEP_T)  # solve the system over these t
    
    # record values up to this latest point
    all_t = np.concatenate((all_t, sol.t))
    all_y_vec = np.concatenate((all_y_vec, sol.y), axis=1)
    print(f't = {np.round_(all_t[-1], 5)}, y_vec = {all_y_vec[:, -1]}')

    # chop down lists if needed
    if SLIDING_WINDOW_T is not None:
        new_cutoff = all_t[-1] - SLIDING_WINDOW_T
        all_t = all_t[all_t >= new_cutoff]
        all_y_vec = all_y_vec[:, -1 * len(all_t):]
        if all_t[-1] < INITIAL_T + SLIDING_WINDOW_T:
            plt.xlim(INITIAL_T, INITIAL_T + SLIDING_WINDOW_T)

    # update the record of the previous values, passed into the next animation frame
    history.update({'last_vals': last_vals, 'all_t': all_t, 'all_y_vec': all_y_vec})

    # plot lines up to the latest point
    for i, y_vec in enumerate(all_y_vec):
        plt.plot(all_t, y_vec, label=DEP_VAR_NAMES[i])

    # show legend
    plt.legend(loc='upper left')


if __name__ == '__main__':

    NUM_DEPENDENT_VARS = len(DEP_VAR_NAMES)
    window = int(ANIM_STEP_T / MAX_STEP_T)
    history = {
        'last_vals': INITIAL_VALUES,
        'all_t': np.array([INITIAL_T]),
        'all_y_vec': np.array([[y_val] for y_val in INITIAL_VALUES])
        }

    fig = plt.figure()
    ani = anim.FuncAnimation(fig, animate, fargs=(history,), init_func=init_graph, \
                             interval=10, save_count=sys.maxsize)

    if SAVE_OR_VIEW == 'view':
        plt.show()
    elif SAVE_OR_VIEW == 'save':
        ani.save('MyVideo.mp4', writer=anim.FFMpegWriter(fps=30, codec='libx264', bitrate=-1))
