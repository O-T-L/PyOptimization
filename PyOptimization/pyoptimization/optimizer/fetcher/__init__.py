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

def basic(optimizer, solutions):
	return [('optimizer', type(optimizer).__name__), ('solutions', solutions)]

def nsga_ii(optimizer, solutions):
	crowdingDistance = list(map(lambda solution: solution.crowdingDistance_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, crowdingDistance)
	crowdingDistance = f.getvalue()
	return basic(optimizer, solutions) + [
		('crowdingDistance', crowdingDistance),
	]

def spea2(optimizer, solutions):
	fitness = list(map(lambda solution: solution.fitness_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, solutions) + [
		('fitness', fitness),
	]

def moea_d(optimizer, solutions, config):
	return basic(optimizer, solutions) + [
		('weightVectors', config.get('moea_d', 'weight_vectors')),
	]

def ibea(optimizer, solutions):
	fitness = list(map(lambda solution: solution.fitness_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, solutions) + [
		('fitness', fitness),
	]

def monte_carlo_hype(optimizer, solutions):
	return basic(optimizer, solutions) + [
		('sample', optimizer.GetSampleSize()),
	]

def monte_carlo_sms_emoa(optimizer, solutions):
	return basic(optimizer, solutions) + [
		('sample', optimizer.GetSampleSize()),
	]

def ar(optimizer, solutions):
	fitness = list(map(lambda solution: solution.averageRank_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, solutions) + [
		('fitness', fitness),
	]

def epsilon_moea(optimizer, solutions):
	epsilon = optimizer.GetEpsilon()
	if len(numpy.unique(epsilon)) == 1:
		epsilon = str(epsilon[0])
	else:
		epsilon = ' '.join(map(str, epsilon))
	return basic(optimizer, solutions) + [
		('epsilon', epsilon),
	]

def tdea(optimizer, solutions):
	return basic(optimizer, solutions) + [
		('territory', optimizer.GetTerritorySize()),
	]

def isnps(optimizer, solutions):
	fitness = list(map(lambda solution: solution.convergence_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, solutions) + [
		('fitness', fitness),
		('degree', optimizer.GetAngle1() * 180 / math.pi),
		('rounds', optimizer.GetRounds()),
	]

def nsga_iii(optimizer, solutions):
	fitness = list(map(lambda solution: solution.minDistance_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, solutions) + [
		('fitness', fitness),
		('epsilon', optimizer.GetEpsilon()),
	]

def grea(optimizer, solutions):
	division = optimizer.GetDivision()
	if len(numpy.unique(division)) == 1:
		division = str(division[0])
	else:
		division = ' '.join(map(str, division))
	return basic(optimizer, solutions) + [
		('division', division),
	]

def cdas(optimizer, solutions):
	angle = optimizer.GetAngle()
	if len(numpy.unique(angle)) == 1:
		degree = str(angle[0] * 180 / math.pi)
	else:
		degree = ' '.join(map(lambda _angle: str(_angle * 180 / math.pi), angle))
	return nsga_ii(optimizer, solutions) + [
		('degreeVector', degree),
	]

def g_nsga_ii(optimizer, solutions):
	return nsga_ii(optimizer, solutions) + [
		('referencePoint', ' '.join(map(str, optimizer.GetReferencePoint()))),
	]

def r_nsga_ii(optimizer, solutions):
	return nsga_ii(optimizer, solutions) + [
		('referencePoint', ' '.join(map(str, optimizer.GetReferencePoint()))),
		('R-NSGA-II Threshold', optimizer.GetThreshold()),
	]
