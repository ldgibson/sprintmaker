#!/bin/env python

# Usage: python sprintmaker.py <topology_file> [<plumed_file>]

from itertools import product
import sys

import mdtraj as md
import pandas as pd


def unique_pairs(iterable):
    """Returns unique combinations of 2.

    Parameters
    ----------
    iterable

    Yields
    ------
    tuple
        Combination of two elements in `iterable`."""

    pool = tuple(iterable)
    idx = range(len(pool))

    for i, j in product(idx, repeat=2):
        if i > j:
            pass
        else:
            yield (pool[i], pool[j])


def atoms_from_topology(topology):
    """Retrieves atom list from topology file."""
    top = md.load(topology).topology
    table, bonds = top.to_dataframe()
    atom_list = table['element'].tolist()
    return atom_list


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("Not enough input parameters. " +
                        "Please specify topology file.")
    else:
        pass

    top = sys.argv[1]

    if len(sys.argv) - 1 < 2:
        outputf = 'plumed.dat'
    else:
        outputf = sys.argv[2]

    # Get atom list from topology in correct order.
    atom_list = atoms_from_topology(top)

    # Get unique atoms from `atom_list`.
    unique_atoms = set(atom_list)

    # Get unique atom pairs.
    atom_pairs = [frozenset(pair) for pair in unique_pairs(unique_atoms)]

    # Build cutoffs for all pairs.
    cutoff = {}

    for pair in atom_pairs:
        tpair = tuple(pair)
        if len(pair) == 1:
            atoms = (tpair[0], tpair[0])
        else:
            atoms = (tpair[0], tpair[1])

        cutoff[pair] = input("Cutoff for {}-{}: ".format(*atoms))

    # Build DataFrame for data management.
    df = pd.DataFrame(data=atom_list, index=range(1, len(atom_list) + 1),
                      columns=['atom'])

    # Get total number of counts of each atom.
    total_counts = df.groupby('atom')['atom'].count()

    counters = {}

    for atom in unique_atoms:
        counters[atom] = 0

    # Counter keeps track of number of occurences of each atom
    # and assigns the next number in the sequence on an atom
    # by atom basis.
    for atom_id in df.index:
        current_atom = df.loc[atom_id, 'atom']
        if counters[current_atom] < total_counts[current_atom]:
            counters[current_atom] += 1
            df.loc[atom_id, 'label'] = "".join([df.loc[atom_id, 'atom'],
                                                str(counters[current_atom])])
        else:
            raise Exception("Error while atom labels.")

    df = df.sort_values(by='label')
    # label_id is used for ordering in the `ATOMS` section of the file.
    df['label_id'] = range(1, len(atom_list) + 1)

    # Print to PLUMED file.
    with open(outputf, 'w') as f:
        for label in df['label']:
            # Print DENSITY section.
            f.write("DENSITY SPECIES={} LABEL={}\n".format(df[df['label'] ==
                                                              label].index[0],
                                                           label))
        f.write("\n")

        # CONTACT_MATRIX section.
        f.write("CONTACT_MATRIX ...\n")
        f.write("")
        # Print atoms present in CONTACT_MATRIX.
        f.write("ATOMS=" + ",".join(df['label']) + "\n")
        f.write("\n")

        for pair in unique_pairs(df['label_id']):
            i, j = pair

            atom_i = df[df['label_id'] == i]['atom'].values[0]
            atom_j = df[df['label_id'] == j]['atom'].values[0]
            ij_cutoff = cutoff[frozenset([atom_i, atom_j])]

            i = str(i)
            if j < 10:
                j = "0" + str(j)
            else:
                j = str(j)

            f.write("SWITCH{}{}={{RATIONAL R_0={}}}\n".format(i, j, ij_cutoff))

        f.write("\n")
        f.write("LABEL=cmat\n")
        f.write("... CONTACT_MATRIX\n")
        f.write("\n")
        f.write("\n")
        f.write("SPRINT MATRIX=cmat LABEL=SP\n")

    print("Generated file: {}".format(outputf))
