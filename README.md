# SprintMaker
Python script that automates generation of contact matrices for [SPRINT coordinates](https://plumed.github.io/doc-v2.4/user-doc/html/_s_p_r_i_n_t.html) in [PLUMED](http://www.plumed.org/) input files. This script was written by members of the [Pfaendtner Research Group](http://prg.washington.edu/) in the Department of Chemical Engineering at the University of Washington.

**Requires python 3+ and PLUMED 2.3+**

# Python Dependencies
- MDTraj
- Pandas

# Usage
```
$ python sprintmaker.py h2o.pdb plumed.dat
Cutoff for O-O: 2.20
Cutoff for O-H: 2.00
Cutoff for H-H: 2.00
Generated file: plumed.dat
$ cat plumed.dat
DENSITY SPECIES=2 LABEL=H1
DENSITY SPECIES=3 LABEL=H2
DENSITY SPECIES=1 LABEL=O1

CONTACT_MATRIX ...
ATOMS=H1,H2,O1

SWITCH101={RATIONAL R_0=2.00}
SWITCH102={RATIONAL R_0=2.00}
SWITCH103={RATIONAL R_0=2.00}
SWITCH202={RATIONAL R_0=2.00}
SWITCH203={RATIONAL R_0=2.00}
SWITCH303={RATIONAL R_0=2.20}

LABEL=cmat
... CONTACT_MATRIX


SPRINT MATRIX=cmat LABEL=SP
```
