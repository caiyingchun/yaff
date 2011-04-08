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

from common import get_system_water32, get_system_graphene8, \
    get_system_polyethylene4, get_system_quartz, get_system_glycine, \
    get_system_cyclopropene, get_system_caffeine, get_system_butanol

from yaff import *


def test_topology_water32():
    system = get_system_water32()
    t = system.topology
    assert t.bonds[0,0] == 0
    assert t.bonds[0,1] == 1
    assert t.bonds[1,0] == 0
    assert t.bonds[1,1] == 2
    assert t.bonds[2,0] == 3
    assert t.bonds[2,1] == 4
    assert t.bonds[3,0] == 3
    assert t.bonds[3,1] == 5
    for i in xrange(system.size):
        if system.numbers[i] == 8:
            assert len(t.neighs1[i]) == 2
            assert system.numbers[t.neighs1[i][0]] == 1
            assert system.numbers[t.neighs1[i][1]] == 1
            assert len(t.neighs2[i]) == 0
            assert len(t.neighs3[i]) == 0
        elif system.numbers[i] == 1:
            assert len(t.neighs1[i]) == 1
            assert system.numbers[t.neighs1[i][0]] == 8
            print t.neighs2[i]
            assert len(t.neighs2[i]) == 1
            assert system.numbers[t.neighs2[i][0]] == 1
            assert len(t.neighs3[i]) == 0



def floyd_warshall(bonds, natom):
    '''A slow implementation of the Floyd-Warshall algorithm.

       Use it for small test systems only.
    '''
    dmat = np.zeros((natom, natom), int)+natom**2
    np.diag(dmat)[:] = 0
    for i0, i1 in bonds:
        dmat[i0,i1] = 1
        dmat[i1,i0] = 1
    for i0 in xrange(natom):
        for i1 in xrange(natom):
            for i2 in xrange(natom):
                if i2 == i1:
                    continue
                dmat[i1,i2] = min(dmat[i1,i2], dmat[i1,i0]+dmat[i0,i2])
    assert (dmat == dmat.transpose()).all()
    return dmat


def check_topology_slow(system):
    t = system.topology
    dmat = floyd_warshall(t.bonds, system.size)
    # check dmat with neigs*
    for i0, n0 in t.neighs1.iteritems():
        for i1 in n0:
            assert dmat[i0, i1] == 1
            assert dmat[i1, i0] == 1
    for i0, n0 in t.neighs2.iteritems():
        for i2 in n0:
            assert dmat[i0, i2] == 2
            assert dmat[i2, i0] == 2
    for i0, n0 in t.neighs3.iteritems():
        for i3 in n0:
            assert dmat[i0, i3] == 3
            assert dmat[i3, i0] == 3
    # check neigs* with dmat
    for i0 in xrange(system.size):
        for i1 in xrange(system.size):
            if dmat[i0, i1] == 1:
                assert i1 in t.neighs1[i0]
            if dmat[i0, i1] == 2:
                print i0, i1
                assert i1 in t.neighs2[i0]
            if dmat[i0, i1] == 3:
                assert i1 in t.neighs3[i0]


def test_topology_graphene8():
    system = get_system_graphene8()
    check_topology_slow(system)


def test_topology_polyethylene4():
    system = get_system_polyethylene4()
    check_topology_slow(system)


def test_topology_quartz():
    system = get_system_quartz()
    check_topology_slow(system)


def test_topology_glycine():
    system = get_system_glycine()
    check_topology_slow(system)


def test_topology_cyclopropene():
    system = get_system_cyclopropene()
    check_topology_slow(system)


def test_topology_caffeine():
    system = get_system_caffeine()
    check_topology_slow(system)


def test_topology_butanol():
    system = get_system_butanol()
    check_topology_slow(system)