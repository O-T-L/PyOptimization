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
import os
import math
import copy
import configparser
import importlib
import sqlite3
import numpy
import pyotl.utility
import pyotl.crossover.real
import pyotl.optimizer.real
import pyotl.optimizer.integer
import pyotl.optimizer.dynamic_bitset
import pyotl.optimizer.index
import pyotl.optimizer.couple.real
import pyotl.optimizer.couple.integer
import pyotl.optimizer.couple.dynamic_bitset
import pyotl.optimizer.couple.index
import pyotl.optimizer.couple_couple.real
import pyotl.optimizer.couple_couple.integer
import pyotl.optimizer.couple_couple.dynamic_bitset
import pyotl.optimizer.couple_couple.index
import pyotl.optimizer.triple.real
import pyotl.optimizer.triple.integer
import pyotl.optimizer.triple.dynamic_bitset
import pyotl.optimizer.triple.index
import pyotl.optimizer.xtriple.real
import pyotl.optimizer.xtriple.integer
import pyotl.optimizer.xtriple.dynamic_bitset
import pyotl.optimizer.xtriple.index
import pyotl.optimizer.moea_d
import pyoptimization.database
import pyoptimization.indicator
import pyoptimization.problem.coding
import pyoptimization.optimizer.optimization
import pyoptimization.optimizer.initial
import pyoptimization.optimizer.crossover
import pyoptimization.optimizer.mutation
import pyoptimization.optimizer.fetcher
import pyoptimization.optimizer.fetcher.crossover
import pyoptimization.optimizer.fetcher.mutation

def get_optimizer_module(config, problem, crossover, optimizer = 'pyotl.optimizer'):
	coding = pyoptimization.problem.coding.get_coding(problem)
	module = sys.modules['pyotl.crossover.' + coding]
	if issubclass(type(crossover), module.CoupleCrossover):
		return sys.modules[optimizer + '.couple.' + coding]
	elif issubclass(type(crossover), module.CoupleCoupleCrossover):
		return sys.modules[optimizer + '.couple_couple.' + coding]
	elif issubclass(type(crossover), module.TripleCrossover):
		return sys.modules[optimizer + '.triple.' + coding]
	elif issubclass(type(crossover), module.TripleTripleCrossover):
		return sys.modules[optimizer + '.triple_triple.' + coding]
	elif issubclass(type(crossover), module.XTripleCrossover):
		return sys.modules[optimizer + '.xtriple.' + coding]
	else:
		return sys.modules[optimizer + '.' + coding]

def _make_sga(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.SGA(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.basic(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_sga(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_sga(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_rwsga(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.RWSGA(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.basic(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_rwsga(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_rwsga(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_nsga_ii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.NSGA_II(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.nsga_ii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_nsga_ii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_nsga_ii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_constrained_nsga_ii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.ConstrainedNSGA_II(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.nsga_ii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_constrained_nsga_ii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_constrained_nsga_ii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_spea2(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.SPEA2(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.spea2(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_spea2(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_spea2(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_spea2_sde(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.SPEA2_SDE(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.spea2(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_spea2_sde(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_spea2_sde(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def make_gde3(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	coding = pyoptimization.problem.coding.get_coding(problem)
	if coding == 'real':
		module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
		module = importlib.import_module(module)
		for solutions in getattr(module, function)(config, problem):
			initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
			probability = eval(config.get(coding + '_crossover', 'probability'))(problem)
			scaling_factor = config.getfloat('differential_evolution', 'scaling_factor')
			crossover = pyotl.crossover.real.DifferentialEvolution(random, probability, problem.GetBoundary(), scaling_factor)
			crossoverFetcher = lambda optimizer: pyoptimization.optimizer.fetcher.crossover.std(optimizer)
			optimizer = pyotl.optimizer.xtriple.real.GDE3(random, problem, initial, crossover)
			fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.basic(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer)
			executer(optimization, config, optimizer, fetcher)

def _make_ibea_epsilon(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for scalingFactor in map(float, config.get('ibea', 'scaling_factor').split()):
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.IBEA_Epsilon(random, problem, initial, crossover, mutation, scalingFactor)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ibea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_ibea_epsilon(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_ibea_epsilon(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_ibea_hd(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for scalingFactor in map(float, config.get('ibea', 'scaling_factor').split()):
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.IBEA_HD(random, problem, initial, crossover, mutation, scalingFactor)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ibea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_ibea_hd(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_ibea_hd(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_ar(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.AR(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ar(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_ar(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_ar(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_ar_cd_(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.AR_CD_(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ar(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_ar_cd_(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_ar_cd_(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_grea(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('grea', 'division').rsplit('.', 1)
	module = importlib.import_module(module)
	for division in getattr(module, function)(config, problem):
		_division = pyotl.utility.PyList2Vector_size_t(division)
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.GrEA(random, problem, initial, crossover, mutation, _division)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.grea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_grea(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_grea(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_epsilon_moea(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('epsilon_moea', 'epsilon').rsplit('.', 1)
	module = importlib.import_module(module)
	for epsilon in getattr(module, function)(config, problem):
		_epsilon = pyotl.utility.PyList2Vector_Real(epsilon)
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.Epsilon_MOEA(random, problem, initial, crossover, mutation, _epsilon)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.epsilon_moea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_epsilon_moea(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_epsilon_moea(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_tdea(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, problem)
	_boundary = pyotl.utility.PyListList2VectorPair_Real(boundary.tolist())
	module, function = config.get('tdea', 'territory').rsplit('.', 1)
	module = importlib.import_module(module)
	for territory in getattr(module, function)(config, problem):
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.TDEA(random, problem, initial, crossover, mutation, _boundary, territory)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.tdea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_tdea(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_tdea(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_isnps(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('information_separation', 'convergence_direction').rsplit('.', 1)
	module = importlib.import_module(module)
	convergenceDirection = getattr(module, function)(config, problem)
	_convergenceDirection = pyotl.utility.PyList2BlasVector_Real(convergenceDirection)
	amplification = config.getfloat('isnps', 'amplification')
	module, function = config.get('isnps', 'degree1').rsplit('.', 1)
	module = importlib.import_module(module)
	for degree1 in getattr(module, function)(config, problem, amplification):
		angle1 = degree1 * math.pi / 180
		module, function = config.get('isnps', 'degree2').rsplit('.', 1)
		module = importlib.import_module(module)
		for degree2 in getattr(module, function)(config, problem, amplification):
			angle2 = degree2 * math.pi / 180
			problem = problemFactory(random = random, progress = optimization)
			module = get_optimizer_module(config, problem, crossover)
			optimizer = module.ISNPS(random, problem, initial, crossover, mutation, _convergenceDirection, angle1, angle2, amplification)
			fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.isnps(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
			executer(optimization, config, optimizer, fetcher)

def make_isnps(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_isnps(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_nsga_iii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, referenceSet):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.NSGA_III(random, problem, initial, crossover, mutation, referenceSet)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.nsga_iii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_nsga_iii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		module, function = config.get('nsga_iii', 'reference_set').rsplit('.', 1)
		module = importlib.import_module(module)
		for referenceSet in getattr(module, function)(config, solutions, problem.GetNumberOfObjectives()):
			if isinstance(referenceSet, numpy.ndarray):
				referenceSet = pyotl.utility.PyListList2VectorVector_Real(referenceSet.tolist())
			_solutions = len(referenceSet)
			_solutions += (4 - _solutions % 4) % 4
			initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, _solutions)
			for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
				crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
				for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
					_make_nsga_iii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, referenceSet)

def _make_ar_dmo(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, problem)
	_boundary = pyotl.utility.PyListList2VectorPair_Real(boundary.tolist())
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.AR_DMO(random, problem, initial, crossover, mutation, _boundary)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ar(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_ar_dmo(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_ar_dmo(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_cdas(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('cdas', 'angle').rsplit('.', 1)
	module = importlib.import_module(module)
	for angle in getattr(module, function)(config, problem):
		_angle = pyotl.utility.PyList2Vector_Real(angle)
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.CDAS(random, problem, initial, crossover, mutation, _angle)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.cdas(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_cdas(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_cdas(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_g_nsga_ii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('g_nsga_ii', 'reference_point').rsplit('.', 1)
	module = importlib.import_module(module)
	for referencePoint in getattr(module, function)(config, problem):
		_referencePoint = pyotl.utility.PyList2Vector_Real(referencePoint)
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.G_NSGA_II(random, problem, initial, crossover, mutation, _referencePoint)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.g_nsga_ii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_g_nsga_ii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_g_nsga_ii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_r_nsga_ii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('r_nsga_ii', 'reference_point').rsplit('.', 1)
	module = importlib.import_module(module)
	for referencePoint in getattr(module, function)(config, problem):
		_referencePoint = pyotl.utility.PyList2Vector_Real(referencePoint)
		module, function = config.get('r_nsga_ii', 'threshold').rsplit('.', 1)
		module = importlib.import_module(module)
		for threshold in getattr(module, function)(config, problem):
			problem = problemFactory(random = random, progress = optimization)
			module = get_optimizer_module(config, problem, crossover)
			optimizer = module.R_NSGA_II(random, problem, initial, crossover, mutation, _referencePoint, threshold)
			fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.r_nsga_ii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
			executer(optimization, config, optimizer, fetcher)

def make_r_nsga_ii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_r_nsga_ii(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_msops(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	solutions = len(initial)
	module, function = config.get('msops', 'count').rsplit('.', 1)
	module = importlib.import_module(module)
	for count in getattr(module, function)(config, problem, solutions):
		module, function = config.get('msops', 'targets').rsplit('.', 1)
		module = importlib.import_module(module)
		for targets in getattr(module, function)(config, count, problem.GetNumberOfObjectives()):
			if isinstance(targets, numpy.ndarray):
				targets = pyotl.utility.PyListList2VectorVector_Real(targets.tolist())
			for factor in map(float, config.get('msops', 'factor').split()):
				problem = problemFactory(random = random, progress = optimization)
				module = get_optimizer_module(config, problem, crossover)
				optimizer = module.MSOPS(random, problem, initial, crossover, mutation, targets, factor)
				fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.msops(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
				executer(optimization, config, optimizer, fetcher)

def make_msops(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_msops(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_moea_d_weighted_sum(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, weightVectors):
	assert(len(initial) == len(weightVectors))
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for neighborhoodRatio in map(float, config.get('moea_d', 'neighborhood_ratio').split()):
		neighbors = int(len(initial) * neighborhoodRatio)
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.MOEA_D_WeightedSum(random, problem, initial, crossover, mutation, weightVectors, neighbors)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.moea_d(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_moea_d_weighted_sum(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
		module = importlib.import_module(module)
		for weightVectors in getattr(module, function)(config, solutions, problem.GetNumberOfObjectives()):
			if isinstance(weightVectors, numpy.ndarray):
				weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
			initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, len(weightVectors))
			for crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
				for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
					_make_moea_d_weighted_sum(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, weightVectors)

def _make_moea_d_tchebycheff(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, weightVectors):
	assert(len(initial) == len(weightVectors))
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for neighborhoodRatio in map(float, config.get('moea_d', 'neighborhood_ratio').split()):
		neighbors = int(len(initial) * neighborhoodRatio)
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.MOEA_D_Tchebycheff(random, problem, initial, crossover, mutation, weightVectors, neighbors)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.moea_d(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_moea_d_tchebycheff(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
		module = importlib.import_module(module)
		for weightVectors in getattr(module, function)(config, solutions, problem.GetNumberOfObjectives()):
			if isinstance(weightVectors, numpy.ndarray):
				weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
			adjust = config.getfloat('moea_d_tchebycheff', 'adjust')
			for weight in weightVectors:
				pyotl.optimizer.moea_d.AdjustWeight_Real(weight, adjust)
			initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, len(weightVectors))
			for crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
				for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
					_make_moea_d_tchebycheff(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, weightVectors)

def _make_moea_d_norm_tchebycheff(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, weightVectors):
	assert(len(initial) == len(weightVectors))
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for neighborhoodRatio in map(float, config.get('moea_d', 'neighborhood_ratio').split()):
		neighbors = int(len(initial) * neighborhoodRatio)
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.MOEA_D_NormTchebycheff(random, problem, initial, crossover, mutation, weightVectors, neighbors)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.moea_d(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_moea_d_norm_tchebycheff(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
		module = importlib.import_module(module)
		for weightVectors in getattr(module, function)(config, solutions, problem.GetNumberOfObjectives()):
			if isinstance(weightVectors, numpy.ndarray):
				weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
			adjust = config.getfloat('moea_d_norm_tchebycheff', 'adjust')
			for weight in weightVectors:
				pyotl.optimizer.moea_d.AdjustWeight_Real(weight, adjust)
			initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, len(weightVectors))
			for crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
				for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
					_make_moea_d_norm_tchebycheff(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, weightVectors)

def _make_moea_d_pbi(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, weightVectors):
	assert(len(initial) == len(weightVectors))
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for neighborhoodRatio in map(float, config.get('moea_d', 'neighborhood_ratio').split()):
		neighbors = int(len(initial) * neighborhoodRatio)
		for penalty in map(float, config.get('moea_d_pbi', 'penalty').split()):
			problem = problemFactory(random = random, progress = optimization)
			module = get_optimizer_module(config, problem, crossover)
			optimizer = module.MOEA_D_PBI(random, problem, initial, crossover, mutation, weightVectors, neighbors, penalty)
			fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.moea_d_pbi(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
			executer(optimization, config, optimizer, fetcher)

def make_moea_d_pbi(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
		module = importlib.import_module(module)
		for weightVectors in getattr(module, function)(config, solutions, problem.GetNumberOfObjectives()):
			if isinstance(weightVectors, numpy.ndarray):
				weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
			if config.getboolean('moea_d_pbi', 'normalize'):
				for weight in weightVectors:
					pyotl.optimizer.moea_d.NormalizeWeight_Real(weight)
			initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, len(weightVectors))
			for crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
				for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
					_make_moea_d_pbi(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher, weightVectors)

def _make_monte_carlo_hype(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for sample in map(int, config.get('monte_carlo_hype', 'sample').split()):
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.MonteCarloHypE(random, problem, initial, crossover, mutation, sample)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.monte_carlo_hype(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_monte_carlo_hype(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_monte_carlo_hype(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_fast_monte_carlo_hype(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for sample in map(int, config.get('monte_carlo_hype', 'sample').split()):
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.FastMonteCarloHypE(random, problem, initial, crossover, mutation, sample)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.monte_carlo_hype(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_fast_monte_carlo_hype(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for _crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			crossover = pyoptimization.optimizer.crossover.adapter(config, problem, _crossover, random)
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_fast_monte_carlo_hype(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_sms_emoa(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.SMS_EMOA(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.basic(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_sms_emoa(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_sms_emoa(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_monte_carlo_hv_sms_emoa(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for sample in map(int, config.get('monte_carlo_hv_sms_emoa', 'sample').split()):
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.MonteCarloHV_SMS_EMOA(random, problem, initial, crossover, mutation, sample)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.basic(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_monte_carlo_hv_sms_emoa(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_monte_carlo_hv_sms_emoa(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def _make_monte_carlo_sms_emoa(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	for sample in map(int, config.get('monte_carlo_sms_emoa', 'sample').split()):
		problem = problemFactory(random = random, progress = optimization)
		module = get_optimizer_module(config, problem, crossover)
		optimizer = module.MonteCarloSMS_EMOA(random, problem, initial, crossover, mutation, sample)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.monte_carlo_sms_emoa(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_monte_carlo_sms_emoa(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	for solutions in getattr(module, function)(config, problem):
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		for crossover, crossoverFetcher in pyoptimization.optimizer.crossover.get_crossovers(config, problem, random):
			for mutation, mutationFetcher in pyoptimization.optimizer.mutation.get_mutations(config, problem, random):
				_make_monte_carlo_sms_emoa(config, executer, problemFactory, problemFetcher, initial, initialFetcher, crossover, crossoverFetcher, mutation, mutationFetcher)

def optimize(config, executer, problemFactory, problemFetcher):
	if config.getboolean('optimizer_switch', 'sga'):
		make_sga(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'rwsga'):
		make_rwsga(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'nsga_ii'):
		make_nsga_ii(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'constrained_nsga_ii'):
		make_constrained_nsga_ii(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'spea2'):
		make_spea2(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'spea2_sde'):
		make_spea2_sde(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'gde3'):
		make_gde3(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'ibea_epsilon'):
		make_ibea_epsilon(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'ibea_hd'):
		make_ibea_hd(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'ar'):
		make_ar(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'ar_cd_'):
		make_ar_cd_(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'grea'):
		make_grea(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'epsilon_moea'):
		make_epsilon_moea(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'tdea'):
		make_tdea(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'isnps'):
		make_isnps(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'nsga_iii'):
		make_nsga_iii(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'ar_dmo'):
		make_ar_dmo(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'cdas'):
		make_cdas(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'g_nsga_ii'):
		make_g_nsga_ii(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'r_nsga_ii'):
		make_r_nsga_ii(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'msops'):
		make_msops(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'moea_d_weighted_sum'):
		make_moea_d_weighted_sum(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'moea_d_tchebycheff'):
		make_moea_d_tchebycheff(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'moea_d_norm_tchebycheff'):
		make_moea_d_norm_tchebycheff(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'moea_d_pbi'):
		make_moea_d_pbi(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'monte_carlo_hype'):
		make_monte_carlo_hype(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'fast_monte_carlo_hype'):
		make_fast_monte_carlo_hype(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'sms_emoa'):
		make_sms_emoa(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'monte_carlo_hv_sms_emoa'):
		make_monte_carlo_hv_sms_emoa(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'monte_carlo_sms_emoa'):
		make_monte_carlo_sms_emoa(config, executer, problemFactory, problemFetcher)