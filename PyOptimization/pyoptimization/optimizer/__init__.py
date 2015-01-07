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

def get_optimizer_module(config, problem, crossover):
	coding = pyoptimization.problem.coding.get_coding(problem)
	module = sys.modules['pyotl.crossover.' + coding]
	if issubclass(type(crossover), module.CoupleCrossover):
		return sys.modules['pyotl.optimizer.couple.' + coding]
	elif issubclass(type(crossover), module.CoupleCoupleCrossover):
		return sys.modules['pyotl.optimizer.couple_couple.' + coding]
	elif issubclass(type(crossover), module.TripleCrossover):
		return sys.modules['pyotl.optimizer.triple.' + coding]
	elif issubclass(type(crossover), module.TripleTripleCrossover):
		return sys.modules['pyotl.optimizer.triple_triple.' + coding]
	elif issubclass(type(crossover), module.XTripleCrossover):
		return sys.modules['pyotl.optimizer.xtriple.' + coding]
	else:
		return sys.modules['pyotl.optimizer.' + coding]

def make_sga(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.SGA(random, problem, initial, _crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.basic(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_rwsga(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.RWSGA(random, problem, initial, _crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.basic(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_nsga_ii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.NSGA_II(random, problem, initial, _crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.nsga_ii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_constrained_nsga_ii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.ConstrainedNSGA_II(random, problem, initial, _crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.nsga_ii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_spea2(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.SPEA2(random, problem, initial, _crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.spea2(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_spea2_sde(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.SPEA2_SDE(random, problem, initial, _crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.spea2(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_gde3(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	coding = pyoptimization.problem.coding.get_coding(problem)
	if coding == 'real':
		module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
		module = importlib.import_module(module)
		solutions = getattr(module, function)(config, problem)
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		probability = eval(config.get(coding + '_crossover', 'probability'))(problem)
		scaling_factor = config.getfloat('differential_evolution', 'scaling_factor')
		crossover = pyotl.crossover.real.DifferentialEvolution(random, probability, problem.GetBoundary(), scaling_factor)
		crossoverFetcher = lambda optimizer: pyoptimization.optimizer.fetcher.crossover.std(optimizer)
		optimizer = pyotl.optimizer.xtriple.real.GDE3(random, problem, initial, crossover)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.nsga_ii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_ibea_epsilon(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	scalingFactor = config.getfloat('ibea', 'scaling_factor')
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.IBEA_Epsilon(random, problem, initial, _crossover, mutation, scalingFactor)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ibea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_ibea_hd(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	scalingFactor = config.getfloat('ibea', 'scaling_factor')
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.IBEA_HD(random, problem, initial, _crossover, mutation, scalingFactor)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ibea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_ar(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.AR(random, problem, initial, _crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ar(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_ar_cd_(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.AR_CD_(random, problem, initial, _crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ar(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_grea(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module, function = config.get('grea', 'division').rsplit('.', 1)
	module = importlib.import_module(module)
	division = getattr(module, function)(config, problem)
	division = pyotl.utility.PyList2Vector_size_t(division)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.GrEA(random, problem, initial, _crossover, mutation, division)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.grea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_epsilon_moea(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, problem)
	lower, _ = zip(*boundary)
	lower = pyotl.utility.PyTuple2Vector_Real(lower)
	module, function = config.get('epsilon_moea', 'epsilon').rsplit('.', 1)
	module = importlib.import_module(module)
	epsilon = getattr(module, function)(config, problem)
	epsilon = pyotl.utility.PyList2Vector_Real(epsilon.tolist())
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.Epsilon_MOEA(random, problem, initial, crossover, mutation, lower, epsilon)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.epsilon_moea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_tdea(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, problem)
	boundary = pyotl.utility.PyList2Boundary_Real(boundary.tolist())
	module, function = config.get('tdea', 'territory').rsplit('.', 1)
	module = importlib.import_module(module)
	territorySize = getattr(module, function)(config, problem)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.TDEA(random, problem, initial, crossover, mutation, boundary, territorySize)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.tdea(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_isnps(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module, function = config.get('information_separation', 'convergence_direction').rsplit('.', 1)
	module = importlib.import_module(module)
	convergenceDirection = getattr(module, function)(config, problem)
	convergenceDirection = pyotl.utility.PyList2BlasVector_Real(convergenceDirection.tolist())
	module, function = config.get('isnps', 'degree1').rsplit('.', 1)
	module = importlib.import_module(module)
	degree1 = getattr(module, function)(config, problem)
	angle1 = degree1 * math.pi / 180
	module, function = config.get('isnps', 'degree2').rsplit('.', 1)
	module = importlib.import_module(module)
	degree2 = getattr(module, function)(config, problem)
	angle2 = degree2 * math.pi / 180
	amplification = config.getfloat('isnps', 'amplification')
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.ISNPS(random, problem, initial, _crossover, mutation, convergenceDirection, angle1, angle2, amplification)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.isnps(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def enumerate_isnps(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	_problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('information_separation', 'convergence_direction').rsplit('.', 1)
	module = importlib.import_module(module)
	convergenceDirection = getattr(module, function)(config, _problem)
	convergenceDirection = pyotl.utility.PyList2BlasVector_Real(convergenceDirection.tolist())
	module, function = config.get('isnps', 'enumerate_degree1').rsplit('.', 1)
	module = importlib.import_module(module)
	degree1List = getattr(module, function)(config, _problem)
	module, function = config.get('isnps', 'degree2').rsplit('.', 1)
	module = importlib.import_module(module)
	degree2 = getattr(module, function)(config, _problem)
	angle2 = degree2 * math.pi / 180
	amplification = config.getfloat('isnps', 'amplification')
	for degree1 in degree1List:
		angle1 = degree1 * math.pi / 180
		problem = problemFactory(random = random, progress = optimization)
		module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
		module = importlib.import_module(module)
		solutions = getattr(module, function)(config, problem)
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
		_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
		mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
		module = get_optimizer_module(config, problem, _crossover)
		optimizer = module.ISNPS(random, problem, initial, _crossover, mutation, convergenceDirection, angle1, angle2, amplification)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.isnps(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_nsga_iii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	module, function = config.get('nsga_iii', 'reference_set').rsplit('.', 1)
	module = importlib.import_module(module)
	referenceSet = getattr(module, function)(config, solutions, problem.GetNumberOfObjectives())
	if isinstance(referenceSet, numpy.ndarray):
		referenceSet = pyotl.utility.PyListList2VectorVector_Real(referenceSet.tolist())
	_solutions = len(referenceSet)
	_solutions += (4 - _solutions % 4) % 4
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, _solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.NSGA_III(random, problem, initial, _crossover, mutation, referenceSet)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.nsga_iii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_ar_dmo(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, problem)
	boundary = pyotl.utility.PyList2Boundary_Real(boundary.tolist())
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.AR_DMO(random, problem, initial, _crossover, mutation, boundary)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.ar(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_cdas(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module, function = config.get('cdas', 'angle').rsplit('.', 1)
	module = importlib.import_module(module)
	angle = getattr(module, function)(config, problem)
	angle = pyotl.utility.PyList2Vector_Real(angle)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.CDAS(random, problem, initial, _crossover, mutation, angle)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.cdas(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def enumerate_cdas(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	_problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('cdas', 'enumerate_angle').rsplit('.', 1)
	module = importlib.import_module(module)
	angleList = getattr(module, function)(config, _problem)
	for angle in angleList:
		problem = problemFactory(random = random, progress = optimization)
		module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
		module = importlib.import_module(module)
		solutions = getattr(module, function)(config, problem)
		initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
		crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
		_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
		mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
		_angle = pyotl.utility.PyList2Vector_Real([angle] * problem.GetNumberOfObjectives())
		module = get_optimizer_module(config, problem, _crossover)
		optimizer = module.CDAS(random, problem, initial, _crossover, mutation, _angle)
		fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.cdas(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
		executer(optimization, config, optimizer, fetcher)

def make_g_nsga_ii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module, function = config.get('g_nsga_ii', 'reference_point').rsplit('.', 1)
	module = importlib.import_module(module)
	referencePoint = getattr(module, function)(config, problem)
	referencePoint = pyotl.utility.PyList2Vector_Real(referencePoint.tolist())
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.G_NSGA_II(random, problem, initial, _crossover, mutation, referencePoint)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.g_nsga_ii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_r_nsga_ii(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module, function = config.get('r_nsga_ii', 'reference_point').rsplit('.', 1)
	module = importlib.import_module(module)
	referencePoint = getattr(module, function)(config, problem)
	referencePoint = pyotl.utility.PyList2Vector_Real(referencePoint.tolist())
	module, function = config.get('r_nsga_ii', 'threshold').rsplit('.', 1)
	module = importlib.import_module(module)
	threshold = getattr(module, function)(config, problem)
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.R_NSGA_II(random, problem, initial, _crossover, mutation, referencePoint, threshold)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.r_nsga_ii(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_msops(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module, function = config.get('msops', 'targets').rsplit('.', 1)
	module = importlib.import_module(module)
	count = eval(config.get('msops', 'count'))(solutions)
	targets = getattr(module, function)(config, count, problem.GetNumberOfObjectives())
	if isinstance(targets, numpy.ndarray):
		targets = pyotl.utility.PyListList2VectorVector_Real(targets.tolist())
	factor = config.getfloat('msops', 'factor')
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.MSOPS(random, problem, initial, _crossover, mutation, targets, factor)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.msops(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_moea_d_weighted_sum(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
	module = importlib.import_module(module)
	weightVectors = getattr(module, function)(config, solutions, problem.GetNumberOfObjectives())
	if isinstance(weightVectors, numpy.ndarray):
		weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, len(weightVectors))
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	neighborhoodRatio = config.getfloat('moea_d', 'neighborhood_ratio')
	neighbors = int(len(weightVectors) * neighborhoodRatio)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.MOEA_D_WeightedSum(random, problem, initial, crossover, mutation, weightVectors, neighbors)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.moea_d(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_moea_d_tchebycheff(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
	module = importlib.import_module(module)
	weightVectors = getattr(module, function)(config, solutions, problem.GetNumberOfObjectives())
	if isinstance(weightVectors, numpy.ndarray):
		weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
	try:
		adjust = config.getfloat('moea_d_tchebycheff', 'adjust')
		for weight in weightVectors:
			pyotl.optimizer.moea_d.AdjustWeight_Real(weight, adjust)
	except configparser.NoOptionError:
		raise
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, len(weightVectors))
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	neighborhoodRatio = config.getfloat('moea_d', 'neighborhood_ratio')
	neighbors = int(len(weightVectors) * neighborhoodRatio)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.MOEA_D_Tchebycheff(random, problem, initial, crossover, mutation, weightVectors, neighbors)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.moea_d(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_moea_d_norm_tchebycheff(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
	module = importlib.import_module(module)
	weightVectors = getattr(module, function)(config, solutions, problem.GetNumberOfObjectives())
	if isinstance(weightVectors, numpy.ndarray):
		weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
	try:
		adjust = config.getfloat('moea_d_norm_tchebycheff', 'adjust')
		for weight in weightVectors:
			pyotl.optimizer.moea_d.AdjustWeight_Real(weight, adjust)
	except configparser.NoOptionError:
		raise
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, len(weightVectors))
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	neighborhoodRatio = config.getfloat('moea_d', 'neighborhood_ratio')
	neighbors = int(len(weightVectors) * neighborhoodRatio)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.MOEA_D_NormTchebycheff(random, problem, initial, crossover, mutation, weightVectors, neighbors)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.moea_d(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_moea_d_pbi(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
	module = importlib.import_module(module)
	weightVectors = getattr(module, function)(config, solutions, problem.GetNumberOfObjectives())
	if isinstance(weightVectors, numpy.ndarray):
		weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
	if config.getboolean('moea_d_pbi', 'normalize'):
		for weight in weightVectors:
			pyotl.optimizer.moea_d.NormalizeWeight_Real(weight)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, len(weightVectors))
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	neighborhoodRatio = config.getfloat('moea_d', 'neighborhood_ratio')
	neighbors = int(len(weightVectors) * neighborhoodRatio)
	penalty = config.getfloat('moea_d_pbi', 'penalty')
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.MOEA_D_PBI(random, problem, initial, crossover, mutation, weightVectors, neighbors, penalty)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.moea_d_pbi(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_monte_carlo_hype(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	sample = config.getint('monte_carlo_hype', 'sample')
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.MonteCarloHypE(random, problem, initial, _crossover, mutation, sample)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.monte_carlo_hype(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_fast_monte_carlo_hype(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	_crossover = pyoptimization.optimizer.crossover.adapter(config, problem, crossover, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	sample = config.getint('monte_carlo_hype', 'sample')
	module = get_optimizer_module(config, problem, _crossover)
	optimizer = module.FastMonteCarloHypE(random, problem, initial, _crossover, mutation, sample)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.monte_carlo_hype(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_sms_emoa(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.SMS_EMOA(random, problem, initial, crossover, mutation)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.basic(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_monte_carlo_hv_sms_emoa(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	sample = config.getint('monte_carlo_hv_sms_emoa', 'sample')
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.MonteCarloHV_SMS_EMOA(random, problem, initial, crossover, mutation, sample)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.basic(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

def make_monte_carlo_sms_emoa(config, executer, problemFactory, problemFetcher):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = problemFactory(random = random, progress = optimization)
	module, function = config.get('optimizer', 'solutions').rsplit('.', 1)
	module = importlib.import_module(module)
	solutions = getattr(module, function)(config, problem)
	initial, initialFetcher = pyoptimization.optimizer.initial.get_initial(config, problem, random, solutions)
	crossover, crossoverFetcher = pyoptimization.optimizer.crossover.get_crossover(config, problem, random)
	mutation, mutationFetcher = pyoptimization.optimizer.mutation.get_mutation(config, problem, random)
	sample = config.getint('monte_carlo_sms_emoa', 'sample')
	module = get_optimizer_module(config, problem, crossover)
	optimizer = module.MonteCarloSMS_EMOA(random, problem, initial, crossover, mutation, sample)
	fetcher = lambda optimizer: pyoptimization.optimizer.fetcher.monte_carlo_sms_emoa(optimizer) + problemFetcher(optimizer) + initialFetcher(optimizer) + crossoverFetcher(optimizer) + mutationFetcher(optimizer)
	executer(optimization, config, optimizer, fetcher)

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
	if config.getboolean('optimizer_switch', 'enumerate_isnps'):
		enumerate_isnps(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'nsga_iii'):
		make_nsga_iii(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'ar_dmo'):
		make_ar_dmo(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'cdas'):
		make_cdas(config, executer, problemFactory, problemFetcher)
	if config.getboolean('optimizer_switch', 'enumerate_cdas'):
		enumerate_cdas(config, executer, problemFactory, problemFetcher)
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