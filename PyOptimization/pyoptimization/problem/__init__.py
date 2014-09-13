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
import copy
import io
import configparser
import importlib
import sqlite3
import numpy
import pyotl.problem.real
import pyotl.problem.integer
import pyotl.problem.dynamic_bitset
import pyotl.problem.index
import pyotl.problem.community_discovery
import pyoptimization.database
import pyoptimization.optimizer
import pyoptimization.problem.fetcher
import pyoptimization.problem.fetcher.result

def make_xsinx(config, executer, optimization):
	optimization(config, executer,
		lambda **kwargs: pyotl.problem.real.XSinX(),
		fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def make_camel(config, executer, optimization):
	optimization(config, executer,
		lambda **kwargs: pyotl.problem.real.Camel(),
		fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def make_shaffer_f6(config, executer, optimization):
	optimization(config, executer,
		lambda **kwargs: pyotl.problem.real.ShafferF6(),
		fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def make_shubert(config, executer, optimization):
	optimization(config, executer,
		lambda **kwargs: pyotl.problem.real.Shubert(),
		fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def make_pareto_box(config, executer, optimization):
	optimization(config, executer,
		lambda **kwargs: pyotl.problem.real.ParetoBox(),
		fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def make_water(config, executer, optimization):
	optimization(config, executer,
		lambda **kwargs: pyotl.problem.real.Water(),
		fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def make_rectangle(config, executer, optimization):
	module, function = config.get('rectangle', 'boundaries').rsplit('.', 1)
	module = importlib.import_module(module)
	for boundary, boundaryOptimal in getattr(module, function)(config):
		boundary = pyotl.utility.PyList2Boundary_Real(boundary)
		boundaryOptimal = pyotl.utility.PyList2Boundary_Real(boundaryOptimal)
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.Rectangle(boundary, boundaryOptimal),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.rectangle(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def make_rotated_rectangle(config, executer, optimization):
	getDirection = eval(config.get('rotated_rectangle', 'direction'))
	module, function = config.get('rotated_rectangle', 'boundaries').rsplit('.', 1)
	module = importlib.import_module(module)
	for boundary, boundaryOptimal in getattr(module, function)(config):
		boundary = pyotl.utility.PyList2Boundary_Real(boundary)
		boundaryOptimal = pyotl.utility.PyList2Boundary_Real(boundaryOptimal)
		direction = getDirection(len(boundary))
		_direction = pyotl.utility.PyList2BlasVector_Real(direction)
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.RotatedRectangle(boundary, boundaryOptimal, _direction),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.rotated_rectangle(optimizer.GetProblem(), direction) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def make_onl(config, executer, optimization):
	module, function = config.get('onl', 'metrics').rsplit('.', 1)
	module = importlib.import_module(module)
	metrics = getattr(module, function)(config)
	module, function = config.get('community_discovery', 'graphs').rsplit('.', 1)
	module = importlib.import_module(module)
	for graph in getattr(module, function)(config):
		_graph = pyotl.utility.PyListList2BlasSymmetricMatrix_Real(graph.tolist())
		for _metrics in metrics:
			_metrics = pyotl.problem.community_discovery.PyList2Vector_Metric(_metrics)
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.index.ONL(_graph, _metrics, kwargs['random']),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.basic(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def make_zdt_real(config, executer, optimization):
	distDecisions = config.getint('zdt', 'dist_decisions')
	if config.getboolean('problem_switch', 'zdt1'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT1(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT1(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'zdt2'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT2(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT2(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'zdt3'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT3(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT3(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'zdt4'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT4(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT4(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'zdt6'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT6(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT6(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def make_uf(config, executer, optimization):
	distDecisions2 = config.getint('uf', 'dist_decisions2')
	distDecisions3 = config.getint('uf', 'dist_decisions3')
	if config.getboolean('problem_switch', 'uf1'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF1(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF1(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf2'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF2(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF2(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf3'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF3(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF3(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf4'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF4(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF4(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf5'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF5(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF5(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf6'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF6(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF6(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf7'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF7(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF7(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf8'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF8(distDecisions3) if distDecisions3 >= 0 else pyotl.problem.real.UF8(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf9'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF9(distDecisions3) if distDecisions3 >= 0 else pyotl.problem.real.UF9(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf10'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.real.UF10(distDecisions3) if distDecisions3 >= 0 else pyotl.problem.real.UF10(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def make_dtlz(config, executer, optimization):
	distDecisions = config.getint('dtlz', 'dist_decisions')
	for nObjectives in map(int, config.get('dtlz', 'objectives').split()):
		if config.getboolean('problem_switch', 'dtlz1'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ1(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ1(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz2'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ2(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ2(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz3'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ3(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ3(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz4'):
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.dtlz4(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer)
			if distDecisions >= 0:
				try:
					for baisFactor in map(float, config.get('dtlz4', 'bias_factor').split()):
						optimization(config, executer,
							lambda **kwargs: pyotl.problem.real.DTLZ4(nObjectives, distDecisions, baisFactor),
							fetcher = fetcher,
						)
				except configparser.NoOptionError:
					optimization(config, executer,
						lambda **kwargs: pyotl.problem.real.DTLZ4(nObjectives, distDecisions),
						fetcher = fetcher,
					)
			else:
				optimization(config, executer,
					lambda **kwargs: pyotl.problem.real.DTLZ4(nObjectives),
					fetcher = fetcher,
				)
		if config.getboolean('problem_switch', 'dtlz5'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ5(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ5(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz6'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ6(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ6(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz7'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ7(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ7(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz5i'):
			for nManifold in range(2, nObjectives - 1):
				optimization(config, executer,
					lambda **kwargs: pyotl.problem.real.DTLZ5I(nObjectives, nManifold, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ5I(nObjectives, nManifold),
					fetcher = lambda optimizer: pyoptimization.problem.fetcher.dtlz_i(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		if config.getboolean('problem_switch', 'dtlz6i'):
			for nManifold in range(2, nObjectives - 1):
				optimization(config, executer,
					lambda **kwargs: pyotl.problem.real.DTLZ6I(nObjectives, nManifold, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ6I(nObjectives, nManifold),
					fetcher = lambda optimizer: pyoptimization.problem.fetcher.dtlz_i(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		if config.getboolean('problem_switch', 'convex_dtlz2'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.ConvexDTLZ2(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ2(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'convex_dtlz3'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.ConvexDTLZ3(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ3(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'convex_dtlz4'):
			try:
				for baisFactor in map(float, config.get('dtlz4', 'bias_factor').split()):
					optimization(config, executer,
						lambda **kwargs: pyotl.problem.real.ConvexDTLZ4(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ4(nObjectives, baisFactor),
						fetcher = lambda optimizer: pyoptimization.problem.fetcher.dtlz4(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
					)
			except configparser.NoOptionError:
				optimization(config, executer,
					lambda **kwargs: pyotl.problem.real.ConvexDTLZ4(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ4(nObjectives),
					fetcher = lambda optimizer: pyoptimization.problem.fetcher.dtlz4(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		if config.getboolean('problem_switch', 'convex_dtlz5'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.ConvexDTLZ5(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ5(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'convex_dtlz6'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.ConvexDTLZ6(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ6(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'convex_dtlz5i'):
			for nManifold in range(2, nObjectives - 1):
				optimization(config, executer,
					lambda **kwargs: pyotl.problem.real.ConvexDTLZ5I(nObjectives, nManifold, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ5I(nObjectives, nManifold),
					fetcher = lambda optimizer: pyoptimization.problem.fetcher.dtlz_i(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		if config.getboolean('problem_switch', 'convex_dtlz6i'):
			for nManifold in range(2, nObjectives - 1):
				optimization(config, executer,
					lambda **kwargs: pyotl.problem.real.ConvexDTLZ6I(nObjectives, nManifold, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ6I(nObjectives, nManifold),
					fetcher = lambda optimizer: pyoptimization.problem.fetcher.dtlz_i(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		if config.getboolean('problem_switch', 'scaled_dtlz2'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.ScaledDTLZ2(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ScaledDTLZ2(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def make_wfg(config, executer, optimization):
	nPosGroups = config.getint('wfg', 'pos_groups')
	nDistDecisions = config.getint('wfg', 'dist_decisions')
	for nObjectives in map(int, config.get('wfg', 'objectives').split()):
		if config.getboolean('problem_switch', 'wfg1'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG1(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG1(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg2'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG2(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG2(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg3'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG3(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG3(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg4'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG4(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG4(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg5'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG5(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG5(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg6'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG6(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG6(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg7'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG7(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG7(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg8'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG8(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG8(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg9'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG9(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG9(nObjectives),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def make_fda(config, executer, optimization):
	fixedSteps = config.getint('fda', 'fixed_steps')
	distinctSteps = config.getint('fda', 'distinct_steps')
	distDecisions = config.getint('fda', 'dist_decisions')
	for nObjectives in map(int, config.get('fda', 'objectives').split()):
		if config.getboolean('problem_switch', 'fda5'):
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.real.FDA5(nObjectives, kwargs['progress'], fixedSteps, distinctSteps, distDecisions) if fixedSteps > 0 and distinctSteps > 0 and distDecisions >= 0 else pyotl.problem.real.FDA5(nObjectives, kwargs['progress']),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def make_problem_real(config, executer, optimization):
	if config.getboolean('problem_switch', 'xsinx'):
		make_xsinx(config, executer, optimization)
	if config.getboolean('problem_switch', 'camel'):
		make_camel(config, executer, optimization)
	if config.getboolean('problem_switch', 'shaffer_f6'):
		make_shaffer_f6(config, executer, optimization)
	if config.getboolean('problem_switch', 'shubert'):
		make_shubert(config, executer, optimization)
	if config.getboolean('problem_switch', 'pareto_box'):
		make_pareto_box(config, executer, optimization)
	if config.getboolean('problem_switch', 'water'):
		make_water(config, executer, optimization)
	if config.getboolean('problem_switch', 'rectangle'):
		make_rectangle(config, executer, optimization)
	if config.getboolean('problem_switch', 'rotated_rectangle'):
		make_rotated_rectangle(config, executer, optimization)
	if config.getboolean('problem_switch', 'zdt'):
		make_zdt_real(config, executer, optimization)
	if config.getboolean('problem_switch', 'uf'):
		make_uf(config, executer, optimization)
	if config.getboolean('problem_switch', 'dtlz'):
		make_dtlz(config, executer, optimization)
	if config.getboolean('problem_switch', 'wfg'):
		make_wfg(config, executer, optimization)
	if config.getboolean('problem_switch', 'fda'):
		make_fda(config, executer, optimization)

def make_zdt_integer(config, executer, optimization):
	if config.getboolean('problem_switch', 'zdt5'):
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.integer.ZDT5(),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def make_problem_integer(config, executer, optimization):
	if config.getboolean('problem_switch', 'zdt'):
		make_zdt_integer(config, executer, optimization)

def make_knapsack(config, executer, optimization):
	module, function = config.get('knapsack', 'parameters').rsplit('.', 1)
	module = importlib.import_module(module)
	for price, weight, capacity in getattr(module, function)(config):
		price = pyotl.utility.PyListList2BlasMatrix_Real(price.tolist())
		weight = pyotl.utility.PyListList2BlasMatrix_Real(weight.tolist())
		capacity = pyotl.utility.PyList2Vector_Real(capacity.tolist())
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.dynamic_bitset.Knapsack(price, weight, capacity),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.basic(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.dynamic_bitset(config, optimizer),
		)

def make_greedy_repair_knapsack(config, executer, optimization):
	module, function = config.get('knapsack', 'parameters').rsplit('.', 1)
	module = importlib.import_module(module)
	for price, weight, capacity in getattr(module, function)(config):
		price = pyotl.utility.PyListList2BlasMatrix_Real(price.tolist())
		weight = pyotl.utility.PyListList2BlasMatrix_Real(weight.tolist())
		capacity = pyotl.utility.PyList2Vector_Real(capacity.tolist())
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.dynamic_bitset.GreedyRepairKnapsack(price, weight, capacity),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.basic(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.dynamic_bitset(config, optimizer),
		)

def make_problem_dynamic_bitset(config, executer, optimization):
	if config.getboolean('problem_switch', 'knapsack'):
		make_knapsack(config, executer, optimization)
	if config.getboolean('problem_switch', 'greedy_repair_knapsack'):
		make_greedy_repair_knapsack(config, executer, optimization)

def make_tsp(config, executer, optimization):
	module, function = config.get('tsp', 'matrix').rsplit('.', 1)
	module = importlib.import_module(module)
	for matrix, city in getattr(module, function)(config):
		matrix = pyotl.utility.PyListList2BlasSymmetricMatrix_Real(matrix.tolist())
		optimization(config, executer,
			lambda **kwargs: pyotl.problem.index.TSP(matrix),
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.tsp(optimizer.GetProblem(), city) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def make_motsp(config, executer, optimization):
	module, function = config.get('motsp', 'matrics').rsplit('.', 1)
	module = importlib.import_module(module)
	for matrics, city in getattr(module, function)(config):
		matrics = [matrix.tolist() for matrix in matrics]
		try:
			for correlation in map(float, config.get('motsp', 'correlation').split()):
				_correlation = [correlation] * (len(matrics) - 1)
				_correlation = pyotl.utility.PyList2Vector_Real(_correlation)
				_matrics = pyotl.utility.PyListListList2VectorBlasSymmetricMatrix_Real(matrics)
				pyotl.problem.index.CorrelateAdjacencyMatrics_Real(_correlation, _matrics)
				optimization(config, executer,
					lambda **kwargs: pyotl.problem.index.MOTSP(_matrics),
					fetcher = lambda optimizer: pyoptimization.problem.fetcher.correlation_motsp(optimizer.GetProblem(), city, correlation) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		except configparser.NoOptionError:
			_matrics = pyotl.utility.PyListListList2VectorBlasSymmetricMatrix_Real(matrics)
			optimization(config, executer,
				lambda **kwargs: pyotl.problem.index.MOTSP(_matrics),
				fetcher = lambda optimizer: pyoptimization.problem.fetcher.correlation_motsp(optimizer.GetProblem(), city, correlation) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def make_problem_index(config, executer, optimization):
	if config.getboolean('problem_switch', 'tsp'):
		make_tsp(config, executer, optimization)
	if config.getboolean('problem_switch', 'motsp'):
		make_motsp(config, executer, optimization)
	if config.getboolean('problem_switch', 'onl'):
		make_onl(config, executer, optimization)

def generate_make_problem(coding):
	return eval('make_problem_' + coding)