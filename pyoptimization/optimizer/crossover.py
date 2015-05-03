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

def get_crossovers_real(config, problem, random, coding):
	crossovers = []
	if config.getboolean(coding + '_crossover_switch', 'simulated_binary_crossover'):
		fetcher = pyoptimization.optimizer.fetcher.crossover.sbx
		for probability in eval(config.get(coding + '_crossover', 'probability'))(problem):
			for distribution_index in map(float, config.get('simulated_binary_crossover', 'distribution_index').split()):
				crossover = pyotl.crossover.real.SimulatedBinaryCrossover(random, probability, problem.GetBoundary(), distribution_index)
				crossovers.append([crossover, fetcher])
	elif config.getboolean(coding + '_crossover_switch', 'differential_evolution'):
		fetcher = pyoptimization.optimizer.fetcher.crossover.std
		for probability in eval(config.get(coding + '_crossover', 'probability'))(problem):
			for scaling_factor in map(float, config.get('differential_evolution', 'scaling_factor').split()):
				crossover = pyotl.crossover.real.DifferentialEvolution(random, probability, problem.GetBoundary(), scaling_factor)
				crossovers.append([crossover, fetcher])
	return crossovers

def get_crossovers_integer(config, problem, random, coding):
	probability = eval(config.get(coding + '_crossover', 'probability'))(problem)
	crossovers = []
	if config.getboolean(coding + '_crossover_switch', 'single_point_crossover'):
		crossover = pyotl.crossover.integer.SinglePointCrossover(random, probability, problem.GetDecisionBits())
		fetcher = pyoptimization.optimizer.fetcher.crossover.std
		crossovers.append([crossover, fetcher])
	return crossovers

def get_crossovers_dynamic_bitset(config, problem, random, coding):
	crossovers = []
	if config.getboolean(coding + '_crossover_switch', 'single_point_crossover'):
		fetcher = pyoptimization.optimizer.fetcher.crossover.std
		for probability in eval(config.get(coding + '_crossover', 'probability'))(problem):
			crossover = pyotl.crossover.dynamic_bitset.BitsetSinglePointCrossover(random, probability)
			crossovers.append([crossover, fetcher])
	elif config.getboolean(coding + '_crossover_switch', 'uniform_crossover'):
		fetcher = pyoptimization.optimizer.fetcher.crossover.std
		for probability in eval(config.get(coding + '_crossover', 'probability'))(problem):
			crossover = pyotl.crossover.dynamic_bitset.DynamicBitsetUniformCrossover(random, probability)
			crossovers.append([crossover, fetcher])
	return crossovers

def get_crossovers_index(config, problem, random, coding):
	crossovers = []
	if config.getboolean(coding + '_crossover_switch', 'single_point_crossover'):
		fetcher = pyoptimization.optimizer.fetcher.crossover.std
		for probability in eval(config.get(coding + '_crossover', 'probability'))(problem):
			decisions = len(problem.GetBoundary())
			bits = math.ceil(math.log2(decisions))
			_bits = pyotl.utility.PyList2Vector_size_t([bits] * decisions)
			crossover = pyotl.crossover.index.SinglePointCrossover(random, probability, _bits)
			crossovers.append([crossover, fetcher])
	return crossovers

def get_crossovers_tsp(config, problem, random):
	probability = eval(config.get('tsp_crossover', 'probability'))(problem)
	crossovers = []
	if config.getboolean('tsp_crossover_switch', 'order_based_crossover'):
		fetcher = pyoptimization.optimizer.fetcher.crossover.std
		for probability in eval(config.get('tsp_crossover', 'probability'))(problem):
			crossover = pyotl.crossover.index.OrderBasedCrossover(random, probability)
			crossovers.append([crossover, fetcher])
	elif config.getboolean('tsp_crossover_switch', 'partially_mapped_crossover'):
		fetcher = pyoptimization.optimizer.fetcher.crossover.std
		for probability in eval(config.get('tsp_crossover', 'probability'))(problem):
			crossover = pyotl.crossover.index.PartiallyMappedCrossover(random, probability)
			crossovers.append([crossover, fetcher])
	elif config.getboolean('tsp_crossover_switch', 'position_based_crossover'):
		fetcher = pyoptimization.optimizer.fetcher.crossover.std
		for probability in eval(config.get('tsp_crossover', 'probability'))(problem):
			crossover = pyotl.crossover.index.PositionBasedCrossover(random, probability)
			crossovers.append([crossover, fetcher])
	return crossovers

def get_crossovers(config, problem, random):
	coding = pyoptimization.problem.coding.get_coding(problem)
	if coding == 'real':
		return get_crossovers_real(config, problem, random, coding)
	elif coding == 'integer':
		return get_crossovers_integer(config, problem, random, coding)
	elif coding == 'dynamic_bitset':
		return get_crossovers_dynamic_bitset(config, problem, random, coding)
	elif coding == 'index':
		if type(problem).__name__.endswith('TSP'):
			return get_crossovers_tsp(config, problem, random)
		else:
			return get_crossovers_index(config, problem, random, coding)
	else:
		raise Exception(type(problem).__name__, problem.GetNumberOfObjectives())

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