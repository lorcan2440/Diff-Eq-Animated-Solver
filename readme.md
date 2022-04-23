# diff-eq-animated-solver
Solves a system of ordinary differential equations (using `scipy.integrate.solve_ivp`) and animates the solutions,
in real time as it continues to solve. Has the option to save the video as an `.MP4`.

The example provided solves the system

![Figure](https://latex.codecogs.com/svg.image?\dpi{110}&space;\bg_white&space;\color{Pink}\left\{\begin{matrix}x'=0.05y-0.24x+10.5\\y'=0.04x-0.05y\end{matrix}\right.)

<img src="https://render.githubusercontent.com/render/math?math=\color{Pink}\left\{\begin{matrix}x'=0.05y-0.24x+10.5\\y'=0.04x-0.05y\end{matrix}\right.">
