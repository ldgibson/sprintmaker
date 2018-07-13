# SprintMaker
Python script that automates generation of contact matrices for [SPRINT coordinates](https://plumed.github.io/doc-v2.4/user-doc/html/_s_p_r_i_n_t.html) in [PLUMED](http://www.plumed.org/) input files. This script was written by members of the [Pfaendtner Research Group](http://prg.washington.edu/) in the Department of Chemical Engineering at the University of Washington.

**Requires python 3+ and PLUMED 2.3+**

# Python Dependencies
- MDTraj
- Pandas

# Usage
```
$ python sprintmaker.py h2o.pdb plumed.dat
Cutoff for O-O: 0.220
Cutoff for O-H: 0.200
Cutoff for H-H: 0.200
Generated file: plumed.dat
$ cat plumed.dat
DENSITY SPECIES=2 LABEL=H1
DENSITY SPECIES=3 LABEL=H2
DENSITY SPECIES=1 LABEL=O1

CONTACT_MATRIX ...
ATOMS=H1,H2,O1

SWITCH101={RATIONAL R_0=0.200}
SWITCH102={RATIONAL R_0=0.200}
SWITCH103={RATIONAL R_0=0.200}
SWITCH202={RATIONAL R_0=0.200}
SWITCH203={RATIONAL R_0=0.200}
SWITCH303={RATIONAL R_0=0.220}

LABEL=cmat
... CONTACT_MATRIX


SPRINT MATRIX=cmat LABEL=SP
```
