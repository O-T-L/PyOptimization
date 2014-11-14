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

def basic(optimizer, population):
	return [('optimizer', type(optimizer).__name__), ('population', population)]

def nsga_ii(optimizer, population):
	crowdingDistance = list(map(lambda solution: solution.crowdingDistance_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, crowdingDistance)
	crowdingDistance = f.getvalue()
	return basic(optimizer, population) + [
		('crowdingDistance', crowdingDistance),
	]

def spea2(optimizer, population):
	fitness = list(map(lambda solution: solution.fitness_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, population) + [
		('fitness', fitness),
	]

def moea_d(optimizer, population, config):
	return basic(optimizer, population) + [
		('weightVectors', config.get('moea_d', 'weight_vectors')),
	]

def ibea(optimizer, population):
	fitness = list(map(lambda solution: solution.fitness_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, population) + [
		('fitness', fitness),
	]

def hype(optimizer, population):
	fitness = list(map(lambda solution: solution.fitness_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, population) + [
		('fitness', fitness),
	]

def sms_emoa(optimizer, population):
	fitness = list(map(lambda solution: solution.hvContribution_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, population) + [
		('fitness', fitness),
	]

def monte_carlo_sms_emoa(optimizer, population):
	return sms_emoa(optimizer, population) + [
		('sample', optimizer.GetSampleSize()),
	]

def ar(optimizer, population):
	fitness = list(map(lambda solution: solution.averageRank_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, population) + [
		('fitness', fitness),
	]

def epsilon_moea(optimizer, population):
	epsilon = optimizer.GetEpsilon()
	if len(numpy.unique(epsilon)) == 1:
		epsilon = str(epsilon[0])
	else:
		epsilon = ' '.join(map(str, epsilon))
	return basic(optimizer, population) + [
		('epsilon', epsilon),
	]

def tdea(optimizer, population):
	return basic(optimizer, population) + [
		('territory', optimizer.GetTerritorySize()),
	]

def isnps(optimizer, population):
	fitness = list(map(lambda solution: solution.convergence_, optimizer.GetSolutionSet()))
	f = io.BytesIO()
	numpy.savetxt(f, fitness)
	fitness = f.getvalue()
	return basic(optimizer, population) + [
		('fitness', fitness),
		('degree', optimizer.GetAngle1() * 180 / math.pi),
		('rounds', optimizer.GetRounds()),
	]

def grea(optimizer, population):
	division = optimizer.GetDivision()
	if len(numpy.unique(division)) == 1:
		division = str(division[0])
	else:
		division = ' '.join(map(str, division))
	return basic(optimizer, population) + [
		('division', division),
	]

def cdas(optimizer, population):
	return nsga_ii(optimizer, population) + [
		('degreeVector', ' '.join(map(str, optimizer.GetAngle() * 180 / math.pi))),
	]

def g_nsga_ii(optimizer, population):
	return nsga_ii(optimizer, population) + [
		('referencePoint', ' '.join(map(str, optimizer.GetReferencePoint()))),
	]

def r_nsga_ii(optimizer, population):
	return nsga_ii(optimizer, population) + [
		('referencePoint', ' '.join(map(str, optimizer.GetReferencePoint()))),
		('R-NSGA-II Threshold', optimizer.GetThreshold()),
	]
