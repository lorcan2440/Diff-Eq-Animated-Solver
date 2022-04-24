# diff-eq-animated-solver
Solves a system of ordinary differential equations (using `scipy.integrate.solve_ivp`) and animates the solutions,
in real time as it continues to solve. Has the option to save the video as an `.MP4`.

The example provided solves the system

<img src="https://render.githubusercontent.com/render/math?math=\color{Orange}\left\{\begin{matrix}x'=0.05y-0.24x%2B10.5\\y'=0.04x-0.05y\end{matrix}\right.">

and can be generalised to any nonlinear system of _n_ ODEs.

![Demo Doccou alpha](http://share.gifyoutube.com/KzB6Gb.gif)

<video src="https://github.com/lorcan2440/diff-eq-animated-solver/blob/main/MyVideo.mp4"></video>
