# SprintMaker
Python script that automates generation of contact matrices for [SPRINT coordinates](https://plumed.github.io/doc-v2.4/user-doc/html/_s_p_r_i_n_t.html) in [PLUMED](http://www.plumed.org/) input files. This script was written by members of the [Pfaendtner Research Group](http://prg.washington.edu/) in the Department of Chemical Engineering at the University of Washington.

**Requires python 3+ and PLUMED 2.3+**

# Python Dependencies
- MDTraj
- Pandas

# Usage
```
$ python sprintmaker.py topology.pdb plumed.dat
Cutoff for O-O: 2.20
Cutoff for O-H: 2.00
Cutoff for H-H: 2.00
Generated file: plumed.dat
```
