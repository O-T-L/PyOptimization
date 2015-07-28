"""
Copyright (C) 2014, 申瑞珉 (Ruimin Shen)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import io
import math
import numpy
import pyotl.utility


def basic(optimizer):
    return [('optimizer', type(optimizer).__name__)]


def nsga_ii(optimizer):
    crowdingDistance = list(map(lambda solution: solution.crowdingDistance_, optimizer.GetSolutionSet()))
    f = io.BytesIO()
    numpy.savetxt(f, crowdingDistance)
    crowdingDistance = f.getvalue()
    return basic(optimizer) + [
        ('crowdingDistance', crowdingDistance),
    ]


def spea2(optimizer):
    fitness = list(map(lambda solution: solution.fitness_, optimizer.GetSolutionSet()))
    f = io.BytesIO()
    numpy.savetxt(f, fitness)
    fitness = f.getvalue()
    return basic(optimizer) + [
        ('fitness', fitness),
    ]


def moea_d(optimizer):
    return basic(optimizer) + [
        ('weightVectors', len(optimizer.GetWeightVectors())),
        ('moea_d_neighbors', len(optimizer.GetNeighbors()[0])),
    ]


def moea_d_pbi(optimizer):
    return moea_d(optimizer) + [
        ('pbi_penalty', optimizer.GetPenalty()),
    ]


def ibea(optimizer):
    fitness = list(map(lambda solution: solution.fitness_, optimizer.GetSolutionSet()))
    f = io.BytesIO()
    numpy.savetxt(f, fitness)
    fitness = f.getvalue()
    return basic(optimizer) + [
        ('fitness', fitness),
    ]


def monte_carlo_hype(optimizer):
    return basic(optimizer) + [
        ('sample', optimizer.GetSampleSize()),
    ]


def monte_carlo_sms_emoa(optimizer):
    return basic(optimizer) + [
        ('sample', optimizer.GetSampleSize()),
    ]


def ar(optimizer):
    fitness = list(map(lambda solution: solution.averageRank_, optimizer.GetSolutionSet()))
    f = io.BytesIO()
    numpy.savetxt(f, fitness)
    fitness = f.getvalue()
    return basic(optimizer) + [
        ('fitness', fitness),
    ]


def epsilon_moea(optimizer):
    epsilon = optimizer.GetEpsilon()
    if len(numpy.unique(epsilon)) == 1:
        epsilon = str(epsilon[0])
    else:
        epsilon = ' '.join(map(str, epsilon))
    return basic(optimizer) + [
        ('epsilon', epsilon),
    ]


def tdea(optimizer):
    return basic(optimizer) + [
        ('territory', optimizer.GetTerritorySize()),
    ]


def isnps(optimizer):
    fitness = list(map(lambda solution: solution.convergence_, optimizer.GetSolutionSet()))
    f = io.BytesIO()
    numpy.savetxt(f, fitness)
    fitness = f.getvalue()
    return basic(optimizer) + [
        ('fitness', fitness),
        ('degree', optimizer.GetAngle1() * 180 / math.pi),
        ('rounds', optimizer.GetRounds()),
    ]


def nsga_iii(optimizer):
    fitness = list(map(lambda solution: solution.minDistance_, optimizer.GetSolutionSet()))
    f = io.BytesIO()
    numpy.savetxt(f, fitness)
    fitness = f.getvalue()
    return basic(optimizer) + [
        ('fitness', fitness),
        ('epsilon', optimizer.GetEpsilon()),
    ]


def msops(optimizer):
    return basic(optimizer) + [
        ('weightVectors', len(optimizer.GetTargets())),
    ]


def grea(optimizer):
    division = optimizer.GetDivision()
    if len(numpy.unique(division)) == 1:
        division = str(division[0])
    else:
        division = ' '.join(map(str, division))
    return basic(optimizer) + [
        ('division', division),
    ]


def cdas(optimizer):
    angle = optimizer.GetAngle()
    if len(numpy.unique(angle)) == 1:
        degree = str(angle[0] * 180 / math.pi)
    else:
        degree = ' '.join(map(lambda _angle: str(_angle * 180 / math.pi), angle))
    return nsga_ii(optimizer) + [
        ('degreeVector', degree),
    ]


def g_nsga_ii(optimizer):
    return nsga_ii(optimizer) + [
        ('referencePoint', ' '.join(map(str, optimizer.GetReferencePoint()))),
    ]


def r_nsga_ii(optimizer):
    return nsga_ii(optimizer) + [
        ('referencePoint', ' '.join(map(str, optimizer.GetReferencePoint()))),
        ('R-NSGA-II Threshold', optimizer.GetThreshold()),
    ]
