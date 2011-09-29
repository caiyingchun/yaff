# YAFF is yet another force-field code
# Copyright (C) 2008 - 2011 Toon Verstraelen <Toon.Verstraelen@UGent.be>, Center
# for Molecular Modeling (CMM), Ghent University, Ghent, Belgium; all rights
# reserved unless otherwise stated.
#
# This file is part of YAFF.
#
# YAFF is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# YAFF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --

import numpy as np

from molmod.units import *

from yaff.system import System


__all__ = ['get_val_table']


units = {
    'kjmol':        kjmol,
    'kjmol/A^2':    kjmol/(angstrom**2),
    'kjmol/rad^2':  kjmol/(rad**2),
    'A':            angstrom,
    'deg':          deg,
}


def get_val_table(fn_val):
    """
        Construct dictionairy containing the valence parameters from FFit2 output.
        The constructed dictionairy is actually a dictionairy of dictionairies:

            val_table = {"bond": bond_dict, "bend": bend_dict, "dihedral": dihedral_table, "ub": ub_table}

        Everey dictionairy (bond_dict, ...) has keys consisting of atom types and values of format (term, ic, parameters)
        parameters is a list of elements of format (kind, value)

        eg.:
            harmonic bond between C and H  with force constant of 1.1 and rest value of 1.8 will be stored in bond_dict as:
                ('C','H'): ('harm', 'dist', [ ('K', 1.8)  ,  ('q0', 1.8) ])

            harmonic bend between O and Al and O  with force constant of 2.2 and rest value of 0.56 will be stored in bend_dict as:
                ('O', 'Al', 'O'): ('harm', 'angle', [ ('K', 2.2)  ,  ('q0', 0.56) ])

            Dihedral of type 3.0*cos(2*psi) of quadruplet 'H','C','C','H' will be stored in dihedral_dict as:
                ('H', 'C', 'C', 'H'): ('cos-m2-0', 'dihed', [ ('K', 3.0) ])
    """
    val_table = {
        "bond":  {},
        "bend":  {},
        "dihed": {},
        "ub":    {},
    }
    f = file(fn_val)
    for line in f:
        line = line[:line.find('#')].strip()
        if len(line) > 0:
            words = line.split()
            ic   = words[0]
            term = words[1]
            if ic=="dist": kind="bond"
            elif ic in ["angle", "cangle"]: kind="bend"
            elif ic=="ub": kind="ub"
            elif ic=="dihed": kind="dihed"
            else:   raise ValueError("Unable to determine ff kind of ic %s" %ic)
            key  = tuple(words[3].split('.'))
            par  = words[4]
            unit = units[words[5]]
            value = float(words[6])
            if key in val_table[kind].keys():
                terminfo = val_table[kind][key]
                assert terminfo[0]==term
                assert terminfo[1]==ic
                terminfo[2].append((par, value*unit))
                if not key==key[::-1]:
                    val_table[kind][key[::-1]][2].append((par, value*unit))
            else:
                val_table[kind][key]       = (term, ic, [(par, value*unit)])
                if not key==key[::-1]:
                    val_table[kind][key[::-1]] = (term, ic, [(par, value*unit)])
    f.close()
    return val_table