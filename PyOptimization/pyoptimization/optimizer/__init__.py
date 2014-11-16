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
import pyotl.initial.real
import pyotl.initial.integer
import pyotl.initial.dynamic_bitset
import pyotl.initial.index
import pyotl.crossover.real
import pyotl.crossover.integer
import pyotl.crossover.dynamic_bitset
import pyotl.crossover.index
import pyotl.mutation.real
import pyotl.mutation.integer
import pyotl.mutation.dynamic_bitset
import pyotl.mutation.index
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
import pyoptimization.optimizer.optimization
import pyoptimization.optimizer.crossover
import pyoptimization.optimizer.fetcher
import pyoptimization.optimizer.fetcher.crossover
import pyoptimization.optimizer.fetcher.mutation

def get_optimizer_module(coding, crossover):
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

def make_sga(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.SGA(random, problem, initial, _crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.basic(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_rwsga(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.RWSGA(random, problem, initial, _crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.basic(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_nsga_ii(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.NSGA_II(random, problem, initial, _crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.nsga_ii(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_constrained_nsga_ii(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.ConstrainedNSGA_II(random, problem, initial, _crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.basic(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_spea2(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.SPEA2(random, problem, initial, _crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.spea2(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_spea2_sde(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.SPEA2_SDE(random, problem, initial, _crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.spea2(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_gde3(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	module = sys.modules['pyotl.optimizer.xtriple.' + coding]
	optimizer = module.GDE3(random, problem, initial, crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.nsga_ii(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_ibea_epsilon(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	scalingFactor = config.getfloat('ibea', 'scaling_factor')
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.IBEA_Epsilon(random, problem, initial, _crossover, mutation, scalingFactor)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.ibea(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_ibea_hd(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	scalingFactor = config.getfloat('ibea', 'scaling_factor')
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.IBEA_HD(random, problem, initial, _crossover, mutation, scalingFactor)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.ibea(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_ar(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.AR(random, problem, initial, _crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.ar(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_ar_cd_(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.AR_CD_(random, problem, initial, _crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.ar(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_grea(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module, function = config.get('grea', 'division').rsplit('.', 1)
	module = importlib.import_module(module)
	division = getattr(module, function)(config, problem)
	division = pyotl.utility.PyList2Vector_size_t(division)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.GrEA(random, problem, initial, _crossover, mutation, division)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.grea(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_epsilon_moea(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, problem)
	lower, _ = zip(*boundary)
	lower = pyotl.utility.PyTuple2Vector_Real(lower)
	module, function = config.get('epsilon_moea', 'epsilon').rsplit('.', 1)
	module = importlib.import_module(module)
	epsilon = getattr(module, function)(config, problem)
	epsilon = pyotl.utility.PyList2Vector_Real(epsilon.tolist())
	module = get_optimizer_module(coding, crossover)
	optimizer = module.Epsilon_MOEA(random, problem, initial, crossover, mutation, lower, epsilon)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.epsilon_moea(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_tdea(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, problem)
	boundary = pyotl.utility.PyList2Boundary_Real(boundary.tolist())
	module, function = config.get('tdea', 'territory').rsplit('.', 1)
	module = importlib.import_module(module)
	territorySize = getattr(module, function)(config, problem)
	print(territorySize)
	module = get_optimizer_module(coding, crossover)
	optimizer = module.TDEA(random, problem, initial, crossover, mutation, boundary, territorySize)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.tdea(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_isnps(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, problem)
	lower, _ = zip(*boundary)
	lower = pyotl.utility.PyTuple2Vector_Real(lower)
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
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.ISNPS(random, problem, initial, _crossover, mutation, lower, convergenceDirection, angle1, angle2, amplification)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.isnps(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def enumerate_isnps(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	_problem = newProblem(random = random, progress = optimization)
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
		problem = newProblem(random = random, progress = optimization)
		module, function = config.get('optimizer', 'population').rsplit('.', 1)
		module = importlib.import_module(module)
		population = getattr(module, function)(config, problem)
		initial = kwargs['initialGen'](random, problem, population)
		crossover = kwargs['crossoverGen'](random, problem)
		_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
		mutation = kwargs['mutationGen'](random, problem)
		module, function = config.get('boundary', 'objective').rsplit('.', 1)
		module = importlib.import_module(module)
		boundary = getattr(module, function)(config, problem)
		lower, _ = zip(*boundary)
		lower = pyotl.utility.PyTuple2Vector_Real(lower)
		module = eval('pyotl.optimizer.' + coding)
		optimizer = module.ISNPS(random, problem, initial, _crossover, mutation, lower, convergenceDirection, angle1, angle2, amplification)
		_kwargs = copy.copy(kwargs)
		_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.isnps(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
		executer(optimization, config, optimizer, **_kwargs)

def make_nsga_iii(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	module, function = config.get('nsga_iii', 'reference_set').rsplit('.', 1)
	module = importlib.import_module(module)
	referenceSet = getattr(module, function)(config, population, problem.GetNumberOfObjectives())
	if isinstance(referenceSet, numpy.ndarray):
		referenceSet = pyotl.utility.PyListList2VectorVector_Real(referenceSet.tolist())
	_population = len(referenceSet)
	while _population % 4:
		_population += 1
	initial = kwargs['initialGen'](random, problem, _population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.NSGA_III(random, problem, initial, _crossover, mutation, referenceSet)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.nsga_iii(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_ar_dmo(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, problem)
	boundary = pyotl.utility.PyList2Boundary_Real(boundary.tolist())
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.AR_DMO(random, problem, initial, _crossover, mutation, boundary)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.ar(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_cdas(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module, function = config.get('cdas', 'angle').rsplit('.', 1)
	module = importlib.import_module(module)
	angle = getattr(module, function)(config, problem)
	angle = pyotl.utility.PyList2Vector_Real(angle.tolist())
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.CDAS(random, problem, initial, _crossover, mutation, angle)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.cdas(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_g_nsga_ii(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module, function = config.get('g_nsga_ii', 'reference_point').rsplit('.', 1)
	module = importlib.import_module(module)
	referencePoint = getattr(module, function)(config, problem)
	referencePoint = pyotl.utility.PyList2Vector_Real(referencePoint.tolist())
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.G_NSGA_II(random, problem, initial, _crossover, mutation, referencePoint)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.g_nsga_ii(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_r_nsga_ii(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module, function = config.get('r_nsga_ii', 'reference_point').rsplit('.', 1)
	module = importlib.import_module(module)
	referencePoint = getattr(module, function)(config, problem)
	referencePoint = pyotl.utility.PyList2Vector_Real(referencePoint.tolist())
	module, function = config.get('r_nsga_ii', 'threshold').rsplit('.', 1)
	module = importlib.import_module(module)
	threshold = getattr(module, function)(config, problem)
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.R_NSGA_II(random, problem, initial, _crossover, mutation, referencePoint, threshold)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.r_nsga_ii(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_msops(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	module, function = config.get('msops', 'targets').rsplit('.', 1)
	module = importlib.import_module(module)
	count = eval(config.get('msops', 'count'))(population)
	targets = getattr(module, function)(config, count, problem.GetNumberOfObjectives())
	if isinstance(targets, numpy.ndarray):
		targets = pyotl.utility.PyListList2VectorVector_Real(targets.tolist())
	factor = config.getfloat('msops', 'factor')
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.MSOPS(random, problem, initial, _crossover, mutation, targets, factor)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.basic(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_moea_d_weighted_sum(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
	module = importlib.import_module(module)
	weightVectors = getattr(module, function)(config, population, problem.GetNumberOfObjectives())
	if isinstance(weightVectors, numpy.ndarray):
		weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
	initial = kwargs['initialGen'](random, problem, len(weightVectors))
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	neighborhoodRatio = config.getfloat('moea_d', 'neighborhood_ratio')
	module = get_optimizer_module(coding, crossover)
	optimizer = module.MOEA_D_WeightedSum(random, problem, initial, crossover, mutation, weightVectors, int(len(weightVectors) * neighborhoodRatio))
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.moea_d(optimizer, population, config) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_moea_d_tchebycheff(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
	module = importlib.import_module(module)
	weightVectors = getattr(module, function)(config, population, problem.GetNumberOfObjectives())
	if isinstance(weightVectors, numpy.ndarray):
		weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
	try:
		adjust = config.getfloat('moea_d_tchebycheff', 'adjust')
		for weight in weightVectors:
			pyotl.optimizer.moea_d.AdjustWeight(weight, adjust)
	except configparser.NoOptionError:
		pass
	initial = kwargs['initialGen'](random, problem, len(weightVectors))
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	neighborhoodRatio = config.getfloat('moea_d', 'neighborhood_ratio')
	module = get_optimizer_module(coding, crossover)
	optimizer = module.MOEA_D_Tchebycheff(random, problem, initial, crossover, mutation, weightVectors, int(len(weightVectors) * neighborhoodRatio))
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.moea_d(optimizer, population, config) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_moea_d_norm_tchebycheff(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
	module = importlib.import_module(module)
	weightVectors = getattr(module, function)(config, population, problem.GetNumberOfObjectives())
	if isinstance(weightVectors, numpy.ndarray):
		weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
	try:
		adjust = config.getfloat('moea_d_norm_tchebycheff', 'adjust')
		for weight in weightVectors:
			pyotl.optimizer.moea_d.AdjustWeight(weight, adjust)
	except configparser.NoOptionError:
		pass
	initial = kwargs['initialGen'](random, problem, len(weightVectors))
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	neighborhoodRatio = config.getfloat('moea_d', 'neighborhood_ratio')
	module = get_optimizer_module(coding, crossover)
	optimizer = module.MOEA_D_NormTchebycheff(random, problem, initial, crossover, mutation, weightVectors, int(len(weightVectors) * neighborhoodRatio))
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.moea_d(optimizer, population, config) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_moea_d_pbi(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	module, function = config.get('moea_d', 'weight_vectors').rsplit('.', 1)
	module = importlib.import_module(module)
	weightVectors = getattr(module, function)(config, population, problem.GetNumberOfObjectives())
	if isinstance(weightVectors, numpy.ndarray):
		weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
	if config.getboolean('moea_d_pbi', 'normalize'):
		for weight in weightVectors:
			pyotl.optimizer.moea_d.NormalizeWeight(weight)
	initial = kwargs['initialGen'](random, problem, len(weightVectors))
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	neighborhoodRatio = config.getfloat('moea_d', 'neighborhood_ratio')
	penalty = config.getfloat('moea_d_pbi', 'penalty')
	module = get_optimizer_module(coding, crossover)
	optimizer = module.MOEA_D_PBI(random, problem, initial, crossover, mutation, weightVectors, int(len(weightVectors) * neighborhoodRatio), penalty)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.moea_d(optimizer, population, config) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_hype(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	_crossover = pyoptimization.optimizer.crossover.adapter(coding, crossover, random)
	mutation = kwargs['mutationGen'](random, problem)
	sample = config.getint('hype', 'sample')
	module = eval('pyotl.optimizer.' + coding)
	optimizer = module.HypE(random, problem, initial, _crossover, mutation, sample)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.hype(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_sms_emoa(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	module = get_optimizer_module(coding, crossover)
	optimizer = module.SMS_EMOA(random, problem, initial, crossover, mutation)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.sms_emoa(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_monte_carlo_sms_emoa(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	sample = config.getint('monte_carlo_sms_emoa', 'sample')
	module = get_optimizer_module(coding, crossover)
	optimizer = module.MonteCarloSMS_EMOA(random, problem, initial, crossover, mutation, sample)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.monte_carlo_sms_emoa(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_monte_carlo_hv_sms_emoa(config, executer, newProblem, coding, **kwargs):
	optimization = pyoptimization.optimizer.optimization.Optimization()
	random = pyotl.utility.Random(pyotl.utility.Time())
	problem = newProblem(random = random, progress = optimization)
	module, function = config.get('optimizer', 'population').rsplit('.', 1)
	module = importlib.import_module(module)
	population = getattr(module, function)(config, problem)
	initial = kwargs['initialGen'](random, problem, population)
	crossover = kwargs['crossoverGen'](random, problem)
	mutation = kwargs['mutationGen'](random, problem)
	sample = config.getint('monte_carlo_hv_sms_emoa', 'sample')
	module = get_optimizer_module(coding, crossover)
	optimizer = module.MonteCarloHV_SMS_EMOA(random, problem, initial, crossover, mutation, sample)
	_kwargs = copy.copy(kwargs)
	_kwargs['fetcher'] = lambda optimizer: kwargs['fetcher'](optimizer) + pyoptimization.optimizer.fetcher.sms_emoa(optimizer, population) + kwargs['crossoverFetcher'](crossover) + kwargs['mutationFetcher'](mutation)
	executer(optimization, config, optimizer, **_kwargs)

def make_optimizer(config, executer, newProblem, coding, **kwargs):
	if config.getboolean('optimizer_switch', 'sga'):
		make_sga(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'rwsga'):
		make_rwsga(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'nsga_ii'):
		make_nsga_ii(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'constrained_nsga_ii'):
		make_constrained_nsga_ii(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'spea2'):
		make_spea2(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'spea2_sde'):
		make_spea2_sde(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'gde3'):
		make_gde3(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'ibea_epsilon'):
		make_ibea_epsilon(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'ibea_hd'):
		make_ibea_hd(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'ar'):
		make_ar(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'ar_cd_'):
		make_ar_cd_(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'grea'):
		make_grea(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'epsilon_moea'):
		make_epsilon_moea(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'tdea'):
		make_tdea(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'isnps'):
		make_isnps(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'enumerate_isnps'):
		enumerate_isnps(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'nsga_iii'):
		make_nsga_iii(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'ar_dmo'):
		make_ar_dmo(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'cdas'):
		make_cdas(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'g_nsga_ii'):
		make_g_nsga_ii(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'r_nsga_ii'):
		make_r_nsga_ii(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'msops'):
		make_msops(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'moea_d_weighted_sum'):
		make_moea_d_weighted_sum(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'moea_d_tchebycheff'):
		make_moea_d_tchebycheff(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'moea_d_norm_tchebycheff'):
		make_moea_d_norm_tchebycheff(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'moea_d_pbi'):
		make_moea_d_pbi(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'hype'):
		make_hype(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'sms_emoa'):
		make_sms_emoa(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'monte_carlo_sms_emoa'):
		make_monte_carlo_sms_emoa(config, executer, newProblem, coding, **kwargs)
	if config.getboolean('optimizer_switch', 'monte_carlo_hv_sms_emoa'):
		make_monte_carlo_hv_sms_emoa(config, executer, newProblem, coding, **kwargs)

def make_optimizer_real(config, executer, newProblem, **kwargs):
	coding = 'real'
	kwargs['initialGen'] = lambda random, problem, populationSize: pyotl.initial.real.PopulationUniform(random, problem.GetBoundary(), populationSize)
	kwargs['crossoverGen'], kwargs['crossoverFetcher'] = {
		'SimulatedBinaryCrossover': (lambda random, problem: pyotl.crossover.real.SimulatedBinaryCrossover(random, eval(config.get(coding + '_crossover', 'probability'))(problem), problem.GetBoundary(), config.getfloat('simulated_binary_crossover', 'distribution_index')), pyoptimization.optimizer.fetcher.crossover.sbx),
		'DifferentialEvolution': (lambda random, problem: pyotl.crossover.real.DifferentialEvolution(random, eval(config.get(coding + '_crossover', 'probability'))(problem), problem.GetBoundary(), config.getfloat('differential_evolution', 'scaling_factor')), pyoptimization.optimizer.fetcher.crossover.std),
	}[config.get(coding, 'crossover')]
	kwargs['mutationGen'], kwargs['mutationFetcher'] = {
		'PolynomialMutation': (lambda random, problem: pyotl.mutation.real.PolynomialMutation(random, eval(config.get(coding + '_mutation', 'probability'))(problem), problem.GetBoundary(), config.getfloat('polynomial_mutation', 'distribution_index')), pyoptimization.optimizer.fetcher.mutation.pm),
	}[config.get(coding, 'mutation')]
	make_optimizer(config, executer, newProblem, coding, **kwargs)

def make_optimizer_integer(config, executer, newProblem, **kwargs):
	coding = 'integer'
	kwargs['initialGen'] = lambda random, problem, populationSize: pyotl.initial.integer.PopulationUniform(random, problem.GetBoundary(), populationSize)
	kwargs['crossoverGen'], kwargs['crossoverFetcher'] = {
		'SinglePointCrossover': (lambda random, problem: pyotl.crossover.integer.SinglePointCrossover(random, eval(config.get(coding + '_crossover', 'probability'))(problem), problem.GetDecisionBits()), pyoptimization.optimizer.fetcher.crossover.std),
	}[config.get(coding, 'crossover')]
	kwargs['mutationGen'], kwargs['mutationFetcher'] = {
		'BitwiseMutation': (lambda random, problem: pyotl.mutation.integer.BitwiseMutation(random, eval(config.get(coding + '_mutation', 'probability'))(problem), problem.GetDecisionBits()), pyoptimization.optimizer.fetcher.mutation.std),
	}[config.get(coding, 'mutation')]
	make_optimizer(config, executer, newProblem, coding, **kwargs)

def make_optimizer_dynamic_bitset(config, executer, newProblem, **kwargs):
	coding = 'dynamic_bitset'
	kwargs['initialGen'] = lambda random, problem, populationSize: pyotl.initial.dynamic_bitset.PopulationUniform(random, problem.GetNumberOfBits(), populationSize)
	kwargs['crossoverGen'], kwargs['crossoverFetcher'] = {
		'BitsetSinglePointCrossover': (lambda random, problem: pyotl.crossover.dynamic_bitset.BitsetSinglePointCrossover(random, eval(config.get(coding + '_crossover', 'probability'))(problem)), pyoptimization.optimizer.fetcher.crossover.std),
		'DynamicBitsetUniformCrossover': (lambda random, problem: pyotl.crossover.dynamic_bitset.DynamicBitsetUniformCrossover(random, eval(config.get(coding + '_crossover', 'probability'))(problem)), pyoptimization.optimizer.fetcher.crossover.std),
	}[config.get(coding, 'crossover')]
	kwargs['mutationGen'], kwargs['mutationFetcher'] = {
		'BitsetBitwiseMutation': (lambda random, problem: pyotl.mutation.dynamic_bitset.BitsetBitwiseMutation(random, eval(config.get(coding + '_mutation', 'probability'))(problem)), pyoptimization.optimizer.fetcher.mutation.std),
	}[config.get(coding, 'mutation')]
	make_optimizer(config, executer, newProblem, coding, **kwargs)

def make_optimizer_index(config, executer, newProblem, **kwargs):
	coding = 'index'
	if kwargs['type'] == 'tsp':
		kwargs['initialGen'] = lambda random, problem, populationSize: pyotl.initial.index.PopulationShuffle(random, problem.GetNumberOfCities(), populationSize)
		kwargs['crossoverGen'], kwargs['crossoverFetcher'] = {
			'OrderBasedCrossover': (lambda random, problem: pyotl.crossover.index.OrderBasedCrossover(random, eval(config.get(coding + '_crossover', 'probability'))(problem)), pyoptimization.optimizer.fetcher.crossover.std),
			'PartiallyMappedCrossover': (lambda random, problem: pyotl.crossover.index.PartiallyMappedCrossover(random, eval(config.get(coding + '_crossover', 'probability'))(problem)), pyoptimization.optimizer.fetcher.crossover.std),
			'PositionBasedCrossover': (lambda random, problem: pyotl.crossover.index.PositionBasedCrossover(random, eval(config.get(coding + '_crossover', 'probability'))(problem)), pyoptimization.optimizer.fetcher.crossover.std),
		}[config.get(coding, 'crossover')]
		kwargs['mutationGen'], kwargs['mutationFetcher'] = {
			'DisplacementMutation': (lambda random, problem: pyotl.mutation.index.DisplacementMutation(random, eval(config.get(coding + '_mutation', 'probability'))(problem)), pyoptimization.optimizer.fetcher.mutation.std),
			'ExchangeMutation': (lambda random, problem: pyotl.mutation.index.ExchangeMutation(random, eval(config.get(coding + '_mutation', 'probability'))(problem)), pyoptimization.optimizer.fetcher.mutation.std),
			'InsertionMutation': (lambda random, problem: pyotl.mutation.index.InsertionMutation(random, eval(config.get(coding + '_mutation', 'probability'))(problem)), pyoptimization.optimizer.fetcher.mutation.std),
			'InversionMutation': (lambda random, problem: pyotl.mutation.index.InversionMutation(random, eval(config.get(coding + '_mutation', 'probability'))(problem)), pyoptimization.optimizer.fetcher.mutation.std),
			'SpreadMutation': (lambda random, problem: pyotl.mutation.index.SpreadMutation(random, eval(config.get(coding + '_mutation', 'probability'))(problem)), pyoptimization.optimizer.fetcher.mutation.std),
		}[config.get(coding, 'mutation')]
		make_optimizer(config, executer, newProblem, coding, **kwargs)
	elif kwargs['type'] == 'community_discovery':
		_coding = coding
		coding = 'integer'
		kwargs['initialGen'] = lambda random, problem, populationSize: pyotl.initial.index.PopulationUniform(random, problem.GetBoundary(), populationSize)
		kwargs['crossoverGen'], kwargs['crossoverFetcher'] = {
			'SinglePointCrossover': (lambda random, problem: pyotl.crossover.index.SinglePointCrossover(random, eval(config.get(coding + '_crossover', 'probability'))(problem), pyotl.utility.PyList2Vector_size_t([math.ceil(math.log2(len(problem.GetBoundary())))] * len(problem.GetBoundary()))), pyoptimization.optimizer.fetcher.crossover.std),
		}[config.get(coding, 'crossover')]
		kwargs['mutationGen'], kwargs['mutationFetcher'] = {
			'BitwiseMutation': (lambda random, problem: pyotl.mutation.index.BitwiseMutation(random, 1 / len(problem.GetBoundary()), pyotl.utility.PyList2Vector_size_t([math.ceil(math.log2(len(problem.GetBoundary())))] * len(problem.GetBoundary()))), pyoptimization.optimizer.fetcher.mutation.std),
		}[config.get(coding, 'mutation')]
		coding = _coding
		make_optimizer(config, executer, newProblem, coding, **kwargs)