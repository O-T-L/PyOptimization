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

import sys
import pyoptimization.problem.coding


def get_crossover(optimizer):
    problem = optimizer.GetProblem()
    coding = pyoptimization.problem.coding.get_coding(problem)
    module = sys.modules['pyotl.crossover.' + coding]
    crossover = optimizer.GetCrossover()
    if issubclass(type(crossover), module.CoupleCrossoverAdapter):
        return crossover.GetCrossover()
    elif issubclass(type(crossover), module.CoupleCoupleCrossoverAdapter):
        return crossover.GetCrossover()
    elif issubclass(type(crossover), module.TripleCrossoverAdapter):
        return crossover.GetCrossover()
    elif issubclass(type(crossover), module.TripleTripleCrossoverAdapter):
        return crossover.GetCrossover()
    elif issubclass(type(crossover), module.XTripleCrossoverAdapter):
        return crossover.GetCrossover()
    else:
        return crossover


def basic(optimizer):
    crossover = get_crossover(optimizer)
    return [('crossover', type(crossover).__name__)]


def std(optimizer):
    crossover = get_crossover(optimizer)
    return basic(optimizer) + [('crossoverProbability', crossover.GetProbability())]


def sbx(optimizer):
    crossover = get_crossover(optimizer)
    return std(optimizer) + [('SBX Distribution Index', crossover.GetDistributionIndex())]
