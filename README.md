# octaveODE
Script for parsing readable ODEs from Octave simulation source.

The script translates Octave m-files to readable ODEs.

Usage:

    python getODEs.py <input file>
    
Result is written to standard output, has to be [redirected](http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-3.html) to a file (if needed).

> Note the script works only for Python 2.7.x !
> Simulation sources might be find on http://e-cyanobacterium.org/models/ when [simulating models](https://i.imgur.com/IZftFAB.png).
