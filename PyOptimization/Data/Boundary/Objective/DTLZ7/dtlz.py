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

import os
import importlib
import numpy
import pyotl.utility
import pyotl.initial.real
import pyotl.crossover.real
import pyotl.mutation.real
import pyotl.optimizer.real
import pyotl.optimizer.couple_couple.real

def optimization(random, problem, weight):
	weightVectors = [weight] * 100
	weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors)
	for weight in weightVectors:
		pyotl.optimizer.moea_d.NormalizeWeight(weight)
	initial = pyotl.initial.real.PopulationUniform(random, problem.GetBoundary(), len(weightVectors))
	crossover = pyotl.crossover.real.SimulatedBinaryCrossover(random, 1, problem.GetBoundary(), 20)
	mutation = pyotl.mutation.real.PolynomialMutation(random, 1 / float(len(problem.GetBoundary())), problem.GetBoundary(), 20)
	optimizer = pyotl.optimizer.couple_couple.real.MOEA_D_PBI(random, problem, initial, crossover, mutation, weightVectors, 10, 5)
	while optimizer.GetProblem().GetNumberOfEvaluations() < 100000:
		optimizer()
	return [list(individual.objective_) for individual in optimizer.GetSolutionSet()]

def main():
	module = 'pyotl.problem.real'
	globals()[module] = importlib.import_module(module)
	problemName = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
	problemType = eval(module + '.' +  problemName)
	random = pyotl.utility.Random()
	path = os.path.splitext(__file__)[0] + '.csv'
	for nObjectives in range(2, 21):
		path = '%u.csv' % nObjectives
		if not os.path.exists(path):
			print(path)
			problem = problemType(nObjectives, 0)
			extreme = []
			for obj in range(nObjectives):
				weight = numpy.eye(nObjectives)[obj]
				pf = optimization(random, problem, weight.tolist())
				objective = min(pf, key = lambda objective: objective[obj])
				extreme.append(objective)
			boundary = [[min(extreme, key = lambda objective: objective[obj])[obj], max(extreme, key = lambda objective: objective[obj])[obj]] for obj in range(nObjectives)]
			numpy.savetxt(path, boundary, delimiter = '\t')

if __name__ == '__main__':
	main()