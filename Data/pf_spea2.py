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
import csv
import numpy
import pyotl.utility
import pyotl.problem.real
import pyotl.initial.real
import pyotl.crossover.real
import pyotl.mutation.real
import pyotl.optimizer.real


def optimization(problem, nPopulation, nGeneration):
    random = pyotl.utility.Random(pyotl.utility.Time())
    initial = pyotl.initial.real.PopulationUniform(random, problem.GetBoundary(), nPopulation)
    _crossover = pyotl.crossover.real.SimulatedBinaryCrossover(random, 1, problem.GetBoundary(), 20)
    crossover = pyotl.crossover.real.CoupleCoupleCrossoverAdapter(_crossover, random)
    mutation = pyotl.mutation.real.PolynomialMutation(random, 1 / float(len(problem.GetBoundary())),
                                                      problem.GetBoundary(), 20)
    optimizer = pyotl.optimizer.real.SPEA2(random, problem, initial, crossover, mutation)
    for generation in range(nGeneration):
        optimizer()
        print('Generation=%u' % generation)
    pf = [list(solution.objective_) for solution in optimizer.GetSolutionSet()]
    return pf


def main():
    for newProblem, getPath in [map(eval, row) for row in
                                csv.reader(open(os.path.splitext(__file__)[0] + '.problems', 'r'), delimiter='\t')]:
        for nObjectives, nPopulation, nGeneration in [map(int, row) for row in
                                                      csv.reader(open(os.path.splitext(__file__)[0] + '.csv', 'r'),
                                                                 delimiter='\t')]:
            problem = newProblem(nObjectives)
            assert (eval(problem.__module__) is pyotl.problem.real)
            root = 'PF_%u' % nPopulation
            path = os.path.join(root, getPath(problem))
            if os.path.exists(path):
                print('"%s" exists' % path)
            else:
                print('Producing %u solutions on %u-objective %s' % (nPopulation, nObjectives, type(problem).__name__))
                pf = optimization(problem, nPopulation, nGeneration)
                print('Saving points into "%s"' % path)
                try:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                except:
                    pass
                numpy.savetxt(path, pf, delimiter='\t')


if __name__ == '__main__':
    main()
