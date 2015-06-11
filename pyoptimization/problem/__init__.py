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

def optimize_xsinx(config, executer, optimize):
	optimize(config, executer,
		lambda **kwargs: pyotl.problem.real.XSinX(),
		lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def optimize_camel(config, executer, optimize):
	optimize(config, executer,
		lambda **kwargs: pyotl.problem.real.Camel(),
		lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def optimize_shaffer_f6(config, executer, optimize):
	optimize(config, executer,
		lambda **kwargs: pyotl.problem.real.ShafferF6(),
		lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def optimize_shubert(config, executer, optimize):
	optimize(config, executer,
		lambda **kwargs: pyotl.problem.real.Shubert(),
		lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def optimize_binh(config, executer, optimize):
	optimize(config, executer,
		lambda **kwargs: pyotl.problem.real.Binh(),
		lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def optimize_pareto_box(config, executer, optimize):
	optimize(config, executer,
		lambda **kwargs: pyotl.problem.real.ParetoBox(),
		lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def optimize_water(config, executer, optimize):
	optimize(config, executer,
		lambda **kwargs: pyotl.problem.real.Water(),
		lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def optimize_rectangle(config, executer, optimize):
	module, function = config.get('rectangle', 'boundaries').rsplit('.', 1)
	module = importlib.import_module(module)
	for boundary, boundaryOptimal in getattr(module, function)(config):
		boundary = pyotl.utility.PyListList2VectorPair_Real(boundary)
		boundaryOptimal = pyotl.utility.PyListList2VectorPair_Real(boundaryOptimal)
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.Rectangle(boundary, boundaryOptimal),
			lambda optimizer: pyoptimization.problem.fetcher.rectangle(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def optimize_rotated_rectangle(config, executer, optimize):
	getDirection = eval(config.get('rotated_rectangle', 'direction'))
	module, function = config.get('rotated_rectangle', 'boundaries').rsplit('.', 1)
	module = importlib.import_module(module)
	for boundary, boundaryOptimal in getattr(module, function)(config):
		boundary = pyotl.utility.PyListList2VectorPair_Real(boundary)
		boundaryOptimal = pyotl.utility.PyListList2VectorPair_Real(boundaryOptimal)
		direction = getDirection(len(boundary))
		_direction = pyotl.utility.PyList2BlasVector_Real(direction)
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.RotatedRectangle(boundary, boundaryOptimal, _direction),
			lambda optimizer: pyoptimization.problem.fetcher.rotated_rectangle(optimizer.GetProblem(), direction) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def optimize_kursawe(config, executer, optimize):
	decisions = config.getint('kursawe', 'decisions')
	optimize(config, executer,
		lambda **kwargs: pyotl.problem.real.Kursawe(decisions) if decisions > 1 else pyotl.problem.real.Kursawe(),
		lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
	)

def optimize_sch(config, executer, optimize):
	if config.getboolean('problem_switch', 'sch1'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.SCH1(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'sch2'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.SCH2(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def optimize_viennet(config, executer, optimize):
	if config.getboolean('problem_switch', 'viennet1'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.Viennet1(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'viennet2'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.Viennet2(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'viennet3'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.Viennet3(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'viennet4'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.Viennet4(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def optimize_zdt_real(config, executer, optimize):
	distDecisions = config.getint('zdt', 'dist_decisions')
	if config.getboolean('problem_switch', 'zdt1'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT1(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT1(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'zdt2'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT2(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT2(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'zdt3'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT3(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT3(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'zdt4'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT4(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT4(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'zdt6'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.ZDT6(distDecisions) if distDecisions >= 0 else pyotl.problem.real.ZDT6(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def optimize_uf(config, executer, optimize):
	distDecisions2 = config.getint('uf', 'dist_decisions2')
	distDecisions3 = config.getint('uf', 'dist_decisions3')
	if config.getboolean('problem_switch', 'uf1'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF1(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF1(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf2'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF2(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF2(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf3'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF3(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF3(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf4'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF4(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF4(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf5'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF5(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF5(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf6'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF6(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF6(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf7'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF7(distDecisions2) if distDecisions2 >= 0 else pyotl.problem.real.UF7(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf8'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF8(distDecisions3) if distDecisions3 >= 0 else pyotl.problem.real.UF8(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf9'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF9(distDecisions3) if distDecisions3 >= 0 else pyotl.problem.real.UF9(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)
	if config.getboolean('problem_switch', 'uf10'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.real.UF10(distDecisions3) if distDecisions3 >= 0 else pyotl.problem.real.UF10(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def optimize_dtlz(config, executer, optimize):
	distDecisions = config.getint('dtlz', 'dist_decisions')
	for nObjectives in map(int, config.get('dtlz', 'objectives').split()):
		if config.getboolean('problem_switch', 'dtlz1'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ1(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ1(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz2'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ2(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ2(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz3'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ3(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ3(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz4'):
			fetcher = lambda optimizer: pyoptimization.problem.fetcher.dtlz4(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer)
			if distDecisions >= 0:
				try:
					for baisFactor in map(float, config.get('dtlz4', 'bias_factor').split()):
						optimize(config, executer,
							lambda **kwargs: pyotl.problem.real.DTLZ4(nObjectives, distDecisions, baisFactor),
							fetcher,
						)
				except configparser.NoOptionError:
					optimize(config, executer,
						lambda **kwargs: pyotl.problem.real.DTLZ4(nObjectives, distDecisions),
						fetcher,
					)
			else:
				optimize(config, executer,
					lambda **kwargs: pyotl.problem.real.DTLZ4(nObjectives),
					fetcher,
				)
		if config.getboolean('problem_switch', 'dtlz5'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ5(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ5(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz6'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ6(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ6(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz7'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.DTLZ7(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ7(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'dtlz5i'):
			for nManifold in eval(config.get('dtlz_i', 'manifold'))(nObjectives):
				optimize(config, executer,
					lambda **kwargs: pyotl.problem.real.DTLZ5I(nObjectives, nManifold, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ5I(nObjectives, nManifold),
					lambda optimizer: pyoptimization.problem.fetcher.dtlz_i(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		if config.getboolean('problem_switch', 'dtlz6i'):
			for nManifold in eval(config.get('dtlz_i', 'manifold'))(nObjectives):
				optimize(config, executer,
					lambda **kwargs: pyotl.problem.real.DTLZ6I(nObjectives, nManifold, distDecisions) if distDecisions >= 0 else pyotl.problem.real.DTLZ6I(nObjectives, nManifold),
					lambda optimizer: pyoptimization.problem.fetcher.dtlz_i(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		if config.getboolean('problem_switch', 'convex_dtlz2'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.ConvexDTLZ2(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ2(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'convex_dtlz3'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.ConvexDTLZ3(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ3(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'convex_dtlz4'):
			lambda optimizer: pyoptimization.problem.fetcher.dtlz4(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer)
			if distDecisions >= 0:
				try:
					for baisFactor in map(float, config.get('dtlz4', 'bias_factor').split()):
						optimize(config, executer,
							lambda **kwargs: pyotl.problem.real.ConvexDTLZ4(nObjectives, distDecisions, baisFactor),
							fetcher,
						)
				except configparser.NoOptionError:
					optimize(config, executer,
						lambda **kwargs: pyotl.problem.real.ConvexDTLZ4(nObjectives, distDecisions),
						fetcher,
					)
			else:
				optimize(config, executer,
					lambda **kwargs: pyotl.problem.real.ConvexDTLZ4(nObjectives),
					fetcher,
				)
		if config.getboolean('problem_switch', 'convex_dtlz5'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.ConvexDTLZ5(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ5(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'convex_dtlz6'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.ConvexDTLZ6(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ6(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'convex_dtlz5i'):
			for nManifold in range(2, nObjectives - 1):
				optimize(config, executer,
					lambda **kwargs: pyotl.problem.real.ConvexDTLZ5I(nObjectives, nManifold, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ5I(nObjectives, nManifold),
					lambda optimizer: pyoptimization.problem.fetcher.dtlz_i(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		if config.getboolean('problem_switch', 'convex_dtlz6i'):
			for nManifold in range(2, nObjectives - 1):
				optimize(config, executer,
					lambda **kwargs: pyotl.problem.real.ConvexDTLZ6I(nObjectives, nManifold, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ConvexDTLZ6I(nObjectives, nManifold),
					lambda optimizer: pyoptimization.problem.fetcher.dtlz_i(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		if config.getboolean('problem_switch', 'scaled_dtlz2'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.ScaledDTLZ2(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.ScaledDTLZ2(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'negative_dtlz2'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.NegativeDTLZ2(nObjectives, distDecisions) if distDecisions >= 0 else pyotl.problem.real.NegativeDTLZ2(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def optimize_wfg(config, executer, optimize):
	nPosGroups = config.getint('wfg', 'pos_groups')
	nDistDecisions = config.getint('wfg', 'dist_decisions')
	for nObjectives in map(int, config.get('wfg', 'objectives').split()):
		if config.getboolean('problem_switch', 'wfg1'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG1(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG1(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg2'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG2(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG2(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg3'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG3(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG3(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg4'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG4(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG4(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg5'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG5(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG5(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg6'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG6(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG6(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg7'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG7(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG7(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg8'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG8(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG8(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)
		if config.getboolean('problem_switch', 'wfg9'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.WFG9(nObjectives, nPosGroups, nDistDecisions) if nPosGroups > 0 and nDistDecisions >= 0 else pyotl.problem.real.WFG9(nObjectives),
				lambda optimizer: pyoptimization.problem.fetcher.wfg(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def optimize_fda(config, executer, optimize):
	fixedSteps = config.getint('fda', 'fixed_steps')
	distinctSteps = config.getint('fda', 'distinct_steps')
	distDecisions = config.getint('fda', 'dist_decisions')
	for nObjectives in map(int, config.get('fda', 'objectives').split()):
		if config.getboolean('problem_switch', 'fda5'):
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.real.FDA5(nObjectives, kwargs['progress'], fixedSteps, distinctSteps, distDecisions) if fixedSteps > 0 and distinctSteps > 0 and distDecisions >= 0 else pyotl.problem.real.FDA5(nObjectives, kwargs['progress']),
				lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def optimize_real(config, executer, optimize):
	if config.getboolean('problem_switch', 'xsinx'):
		optimize_xsinx(config, executer, optimize)
	if config.getboolean('problem_switch', 'camel'):
		optimize_camel(config, executer, optimize)
	if config.getboolean('problem_switch', 'shaffer_f6'):
		optimize_shaffer_f6(config, executer, optimize)
	if config.getboolean('problem_switch', 'shubert'):
		optimize_shubert(config, executer, optimize)
	if config.getboolean('problem_switch', 'binh'):
		optimize_binh(config, executer, optimize)
	if config.getboolean('problem_switch', 'pareto_box'):
		optimize_pareto_box(config, executer, optimize)
	if config.getboolean('problem_switch', 'water'):
		optimize_water(config, executer, optimize)
	if config.getboolean('problem_switch', 'rectangle'):
		optimize_rectangle(config, executer, optimize)
	if config.getboolean('problem_switch', 'rotated_rectangle'):
		optimize_rotated_rectangle(config, executer, optimize)
	if config.getboolean('problem_switch', 'kursawe'):
		optimize_kursawe(config, executer, optimize)
	if config.getboolean('problem_switch', 'sch'):
		optimize_sch(config, executer, optimize)
	if config.getboolean('problem_switch', 'viennet'):
		optimize_viennet(config, executer, optimize)
	if config.getboolean('problem_switch', 'zdt'):
		optimize_zdt_real(config, executer, optimize)
	if config.getboolean('problem_switch', 'uf'):
		optimize_uf(config, executer, optimize)
	if config.getboolean('problem_switch', 'dtlz'):
		optimize_dtlz(config, executer, optimize)
	if config.getboolean('problem_switch', 'wfg'):
		optimize_wfg(config, executer, optimize)
	if config.getboolean('problem_switch', 'fda'):
		optimize_fda(config, executer, optimize)

def optimize_zdt_integer(config, executer, optimize):
	if config.getboolean('problem_switch', 'zdt5'):
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.integer.ZDT5(),
			lambda optimizer: pyoptimization.problem.fetcher.std(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def optimize_integer(config, executer, optimize):
	if config.getboolean('problem_switch', 'zdt'):
		optimize_zdt_integer(config, executer, optimize)

def optimize_knapsack(config, executer, optimize):
	module, function = config.get('knapsack', 'parameters').rsplit('.', 1)
	module = importlib.import_module(module)
	for price, weight, capacity in getattr(module, function)(config):
		price = pyotl.utility.PyListList2BlasMatrix_Real(price.tolist())
		weight = pyotl.utility.PyListList2BlasMatrix_Real(weight.tolist())
		capacity = pyotl.utility.PyList2Vector_Real(capacity)
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.dynamic_bitset.Knapsack(price, weight, capacity),
			lambda optimizer: pyoptimization.problem.fetcher.basic(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.dynamic_bitset(config, optimizer),
		)

def optimize_greedy_repair_knapsack(config, executer, optimize):
	module, function = config.get('knapsack', 'parameters').rsplit('.', 1)
	module = importlib.import_module(module)
	for price, weight, capacity in getattr(module, function)(config):
		price = pyotl.utility.PyListList2BlasMatrix_Real(price.tolist())
		weight = pyotl.utility.PyListList2BlasMatrix_Real(weight.tolist())
		capacity = pyotl.utility.PyList2Vector_Real(capacity)
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.dynamic_bitset.GreedyRepairKnapsack(price, weight, capacity),
			lambda optimizer: pyoptimization.problem.fetcher.basic(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.dynamic_bitset(config, optimizer),
		)

def optimize_dynamic_bitset(config, executer, optimize):
	if config.getboolean('problem_switch', 'knapsack'):
		optimize_knapsack(config, executer, optimize)
	if config.getboolean('problem_switch', 'greedy_repair_knapsack'):
		optimize_greedy_repair_knapsack(config, executer, optimize)

def optimize_tsp(config, executer, optimize):
	module, function = config.get('tsp', 'matrix').rsplit('.', 1)
	module = importlib.import_module(module)
	for matrix, city in getattr(module, function)(config):
		matrix = pyotl.utility.PyListList2BlasSymmetricMatrix_Real(matrix.tolist())
		optimize(config, executer,
			lambda **kwargs: pyotl.problem.index.TSP(matrix),
			lambda optimizer: pyoptimization.problem.fetcher.tsp(optimizer.GetProblem(), city) + pyoptimization.problem.fetcher.result.std(config, optimizer),
		)

def optimize_motsp(config, executer, optimize):
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
				optimize(config, executer,
					lambda **kwargs: pyotl.problem.index.MOTSP(_matrics),
					lambda optimizer: pyoptimization.problem.fetcher.correlation_motsp(optimizer.GetProblem(), city, correlation) + pyoptimization.problem.fetcher.result.std(config, optimizer),
				)
		except configparser.NoOptionError:
			_matrics = pyotl.utility.PyListListList2VectorBlasSymmetricMatrix_Real(matrics)
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.index.MOTSP(_matrics),
				lambda optimizer: pyoptimization.problem.fetcher.correlation_motsp(optimizer.GetProblem(), city, correlation) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def optimize_onl(config, executer, optimize):
	module, function = config.get('onl', 'metrics').rsplit('.', 1)
	module = importlib.import_module(module)
	metrics = getattr(module, function)(config)
	module, function = config.get('community_discovery', 'graphs').rsplit('.', 1)
	module = importlib.import_module(module)
	for graph in getattr(module, function)(config):
		_graph = pyotl.utility.PyListList2BlasSymmetricMatrix_Real(graph.tolist())
		for _metrics in metrics:
			_metrics = pyotl.problem.community_discovery.PyList2Vector_Metric(_metrics)
			optimize(config, executer,
				lambda **kwargs: pyotl.problem.index.ONL(_graph, _metrics, kwargs['random']),
				lambda optimizer: pyoptimization.problem.fetcher.basic(optimizer.GetProblem()) + pyoptimization.problem.fetcher.result.std(config, optimizer),
			)

def optimize_index(config, executer, optimize):
	if config.getboolean('problem_switch', 'tsp'):
		optimize_tsp(config, executer, optimize)
	if config.getboolean('problem_switch', 'motsp'):
		optimize_motsp(config, executer, optimize)
	if config.getboolean('problem_switch', 'onl'):
		optimize_onl(config, executer, optimize)

def optimize(config, executer, optimize):
	optimize_real(config, executer, optimize)
	optimize_integer(config, executer, optimize)
	optimize_dynamic_bitset(config, executer, optimize)
	optimize_index(config, executer, optimize)