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

import math
import pyotl.mutation.real
import pyotl.mutation.integer
import pyotl.mutation.dynamic_bitset
import pyotl.mutation.index
import pyoptimization.problem.coding
import pyoptimization.optimizer.fetcher.mutation

def get_mutation_real(config, problem, random, coding):
	mutation = config.get(coding, 'mutation')
	probability = eval(config.get(coding + '_mutation', 'probability'))(problem)
	if mutation == 'PolynomialMutation':
		distribution_index = config.getfloat('polynomial_mutation', 'distribution_index')
		return pyotl.mutation.real.PolynomialMutation(random, probability, problem.GetBoundary(), distribution_index), pyoptimization.optimizer.fetcher.mutation.pm

def get_mutation_integer(config, problem, random, coding):
	mutation = config.get(coding, 'mutation')
	probability = eval(config.get(coding + '_mutation', 'probability'))(problem)
	if mutation == 'BitwiseMutation':
		return lambda random, problem: pyotl.mutation.integer.BitwiseMutation(random, probability, problem.GetDecisionBits()), pyoptimization.optimizer.fetcher.mutation.std

def get_mutation_dynamic_bitset(config, problem, random, coding):
	mutation = config.get(coding, 'mutation')
	probability = eval(config.get(coding + '_mutation', 'probability'))(problem)
	if mutation == 'BitsetBitwiseMutation':
		return pyotl.mutation.dynamic_bitset.BitsetBitwiseMutation(random, probability), pyoptimization.optimizer.fetcher.mutation.std

def get_mutation_index(config, problem, random, coding):
	mutation = config.get(coding, 'mutation')
	probability = eval(config.get(coding + '_mutation', 'probability'))(problem)
	if mutation == 'BitwiseMutation':
		decisions = len(problem.GetBoundary())
		bits = math.ceil(math.log2(decisions))
		_bits = pyotl.utility.PyList2Vector_size_t([bits] * decisions)
		return pyotl.mutation.index.BitwiseMutation(random, probability, _bits), pyoptimization.optimizer.fetcher.mutation.std

def get_mutation_tsp(config, problem, random):
	mutation = config.get('tsp', 'mutation')
	probability = eval(config.get('tsp_mutation', 'probability'))(problem)
	if mutation == 'DisplacementMutation':
		return pyotl.mutation.index.DisplacementMutation(random, probability), pyoptimization.optimizer.fetcher.mutation.std
	elif mutation == 'ExchangeMutation':
		return pyotl.mutation.index.ExchangeMutation(random, probability), pyoptimization.optimizer.fetcher.mutation.std
	elif mutation == 'InsertionMutation':
		return pyotl.mutation.index.InsertionMutation(random, probability), pyoptimization.optimizer.fetcher.mutation.std
	elif mutation == 'InversionMutation':
		return pyotl.mutation.index.InversionMutation(random, probability), pyoptimization.optimizer.fetcher.mutation.std
	elif mutation == 'SpreadMutation':
		return pyotl.mutation.index.SpreadMutation(random, probability), pyoptimization.optimizer.fetcher.mutation.std

def get_mutation(config, problem, random):
	coding = pyoptimization.problem.coding.get_coding(problem)
	if coding == 'real':
		mutation, fetcher = get_mutation_real(config, problem, random, coding)
	elif coding == 'integer':
		mutation, fetcher = get_mutation_integer(config, problem, random, coding)
	elif coding == 'dynamic_bitset':
		mutation, fetcher = get_mutation_dynamic_bitset(config, problem, random, coding)
	elif coding == 'index':
		if type(problem).__name__.endswith('TSP'):
			mutation, fetcher = get_mutation_tsp(config, problem, random)
		else:
			mutation, fetcher = get_mutation_index(config, problem, random, coding)
	else:
		raise
	return mutation, lambda optimzier: fetcher(mutation)