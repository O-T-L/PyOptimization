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
import math
import pyotl.crossover.real
import pyotl.crossover.integer
import pyotl.crossover.dynamic_bitset
import pyotl.crossover.index
import pyoptimization.problem.coding
import pyoptimization.optimizer.fetcher.crossover

def get_crossover_real(config, problem, random, coding):
	crossover = config.get(coding, 'crossover')
	probability = eval(config.get(coding + '_crossover', 'probability'))(problem)
	if crossover == 'SimulatedBinaryCrossover':
		distribution_index = config.getfloat('simulated_binary_crossover', 'distribution_index')
		return pyotl.crossover.real.SimulatedBinaryCrossover(random, probability, problem.GetBoundary(), distribution_index), pyoptimization.optimizer.fetcher.crossover.sbx
	elif crossover == 'DifferentialEvolution':
		scaling_factor = config.getfloat('differential_evolution', 'scaling_factor')
		return pyotl.crossover.real.DifferentialEvolution(random, probability, problem.GetBoundary(), scaling_factor), pyoptimization.optimizer.fetcher.crossover.std

def get_crossover_integer(config, problem, random, coding):
	crossover = config.get(coding, 'crossover')
	probability = eval(config.get(coding + '_crossover', 'probability'))(problem)
	if crossover == 'SinglePointCrossover':
		return pyotl.crossover.integer.SinglePointCrossover(random, probability, problem.GetDecisionBits()), pyoptimization.optimizer.fetcher.crossover.std

def get_crossover_dynamic_bitset(config, problem, random, coding):
	crossover = config.get(coding, 'crossover')
	probability = eval(config.get(coding + '_crossover', 'probability'))(problem)
	if crossover == 'BitsetSinglePointCrossover':
		return pyotl.crossover.dynamic_bitset.BitsetSinglePointCrossover(random, probability), pyoptimization.optimizer.fetcher.crossover.std
	elif crossover == 'DynamicBitsetUniformCrossover':
		return pyotl.crossover.dynamic_bitset.DynamicBitsetUniformCrossover(random, probability), pyoptimization.optimizer.fetcher.crossover.std

def get_crossover_index(config, problem, random, coding):
	crossover = config.get(coding, 'crossover')
	probability = eval(config.get(coding + '_crossover', 'probability'))(problem)
	if crossover == 'SinglePointCrossover':
		decisions = len(problem.GetBoundary())
		bits = math.ceil(math.log2(decisions))
		_bits = pyotl.utility.PyList2Vector_size_t([bits] * decisions)
		return pyotl.crossover.index.SinglePointCrossover(random, probability, _bits), pyoptimization.optimizer.fetcher.crossover.std

def get_crossover_tsp(config, problem, random):
	crossover = config.get('tsp', 'crossover')
	probability = eval(config.get('tsp_crossover', 'probability'))(problem)
	if crossover == 'OrderBasedCrossover':
		return pyotl.crossover.index.OrderBasedCrossover(random, probability), pyoptimization.optimizer.fetcher.crossover.std
	elif crossover == 'PartiallyMappedCrossover':
		return pyotl.crossover.index.PartiallyMappedCrossover(random, probability), pyoptimization.optimizer.fetcher.crossover.std
	elif crossover == 'PositionBasedCrossover':
		return pyotl.crossover.index.PositionBasedCrossover(random, probability), pyoptimization.optimizer.fetcher.crossover.std

def get_crossover(config, problem, random):
	coding = pyoptimization.problem.coding.get_coding(problem)
	if coding == 'real':
		return get_crossover_real(config, problem, random, coding)
	elif coding == 'integer':
		return get_crossover_integer(config, problem, random, coding)
	elif coding == 'dynamic_bitset':
		return get_crossover_dynamic_bitset(config, problem, random, coding)
	elif coding == 'index':
		if type(problem).__name__.endswith('TSP'):
			return get_crossover_tsp(config, problem, random)
		else:
			return get_crossover_index(config, problem, random, coding)
	else:
		raise

def adapter(config, problem, crossover, random):
	coding = pyoptimization.problem.coding.get_coding(problem)
	module = sys.modules['pyotl.crossover.' + coding]
	if issubclass(type(crossover), module.Crossover):
		return crossover
	elif issubclass(type(crossover), module.CoupleCrossover):
		return module.CoupleCrossoverAdapter(crossover, random)
	elif issubclass(type(crossover), module.CoupleCoupleCrossover):
		return module.CoupleCoupleCrossoverAdapter(crossover, random)
	elif issubclass(type(crossover), module.TripleCrossover):
		return module.TripleCrossoverAdapter(crossover, random)
	elif issubclass(type(crossover), module.TripleTripleCrossover):
		return module.TripleTripleCrossoverAdapter(crossover, random)
	elif issubclass(type(crossover), module.XTripleCrossover):
		return module.XTripleCrossoverAdapter(crossover, random)