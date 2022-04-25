# diff-eq-animated-solver
Solves a system of ordinary differential equations (using `scipy.integrate.solve_ivp`) and animates the solutions,
in real time as it continues to solve. Has the option to save the video as an `.MP4`.

The example provided solves the system

<img src="https://render.githubusercontent.com/render/math?math=\color{Orange}\left\{\begin{matrix}x'=ax-bxy\\y'=cxy-dy\end{matrix}\right.">

and can be generalised to any nonlinear system of _n_ ODEs.

![Result](animation.gif)

^ compressed - actual output is in MP4, much higher resolution, can be as long as you want, 30 fps.
