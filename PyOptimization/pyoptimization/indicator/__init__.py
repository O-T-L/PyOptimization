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
import re
import io
import importlib
import sqlite3
import numpy
import pyotl.utility
import pyotl.indicator.real
import pyoptimization.database
import pyoptimization.utility
import pyoptimization.indicator.utility

def evaluate_gd(config, rowID, columns, rowData):
	properties = dict(zip(columns, rowData))
	problem = rowData[columns.index('problem')]
	if re.match('DTLZ[2-6]', problem):
		indicator = pyotl.indicator.real.DTLZ2GD()
	elif re.match('WFG[4-9]', problem):
		indicator = pyotl.indicator.real.WFG4GD()
	else:
		module, function = config.get('data', 'pf').rsplit('.', 1)
		module = importlib.import_module(module)
		pfTrue = getattr(module, function)(config, properties)
		assert(pfTrue.shape[1] == properties['objectives'])
		pfTrue = pyotl.utility.PyListList2VectorVector_Real(pfTrue.tolist())
		indicator = pyotl.indicator.real.FrontGD(pfTrue)
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['GD', 'GD Type'], [metric, type(indicator).__name__])

def evaluate_igd(config, rowID, columns, rowData):
	properties = dict(zip(columns, rowData))
	module, function = config.get('data', 'pf').rsplit('.', 1)
	module = importlib.import_module(module)
	pfTrue = getattr(module, function)(config, properties)
	assert(pfTrue.shape[1] == properties['objectives'])
	pfTrue = pyotl.utility.PyListList2VectorVector_Real(pfTrue.tolist())
	indicator = pyotl.indicator.real.InvertedGenerationalDistance(pfTrue)
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['IGD'], [metric])

def evaluate_eps(config, rowID, columns, rowData):
	properties = dict(zip(columns, rowData))
	module, function = config.get('data', 'pf').rsplit('.', 1)
	module = importlib.import_module(module)
	pfTrue = getattr(module, function)(config, properties)
	assert(pfTrue.shape[1] == properties['objectives'])
	pfTrue = pyotl.utility.PyListList2VectorVector_Real(pfTrue.tolist())
	method = config.get('eps', 'method')
	if method == 'additive':
		indicator = pyotl.indicator.real.AdditiveEpsilon(pfTrue)
	elif method == 'additive':
		indicator = pyotl.indicator.real.MultiplicativeEpsilon(pfTrue)
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['IGD'], [metric])

def evaluate_sp(config, rowID, columns, rowData):
	indicator = pyotl.indicator.real.Spacing()
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	pyoptimization.indicator.utility.update_row(config, rowID, ['SP'], [metric])

def evaluate_ms(config, rowID, columns, rowData):
	indicator = pyotl.indicator.real.MaximumSpread()
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['MS'], [metric])

def evaluate_ms1(config, rowID, columns, rowData):
	properties = dict(zip(columns, rowData))
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, properties)
	boundary = pyotl.utility.PyList2Boundary_Real(boundary.tolist())
	indicator = pyotl.indicator.real.MaximumSpread1(boundary)
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['MS1'], [metric])

def evaluate_ms2(config, rowID, columns, rowData):
	properties = dict(zip(columns, rowData))
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, properties)
	boundary = pyotl.utility.PyList2Boundary_Real(boundary.tolist())
	indicator = pyotl.indicator.real.MaximumSpread2(boundary)
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['MS2'], [metric])

def evaluate_dm(config, rowID, columns, rowData):
	properties = dict(zip(columns, rowData))
	module, function = config.get('boundary', 'objective').rsplit('.', 1)
	module = importlib.import_module(module)
	boundary = getattr(module, function)(config, properties)
	boundary = pyotl.utility.PyList2Boundary_Real(boundary.tolist())
	module, function = config.get('dm', 'division').rsplit('.', 1)
	module = importlib.import_module(module)
	division = getattr(module, function)(config, properties)
	division = pyotl.utility.PyList2Vector_size_t(division)
	module, function = config.get('dm', 'pf').rsplit('.', 1)
	module = importlib.import_module(module)
	pfTrue = getattr(module, function)(config, properties)
	assert(pfTrue.shape[1] == properties['objectives'])
	pfTrue = pyotl.utility.PyListList2VectorVector_Real(pfTrue.tolist())
	indicator = pyotl.indicator.real.DiversityMetric(boundary, division, pfTrue)
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['DM', 'DM Division'], [metric, ' '.join(map(str, division))])

def evaluate_hv(config, rowID, columns, rowData):
	properties = dict(zip(columns, rowData))
	module, function = config.get('hv', 'reference_point').rsplit('.', 1)
	module = importlib.import_module(module)
	referencePoint = getattr(module, function)(config, properties)
	referencePoint = pyotl.utility.PyList2Vector_Real(referencePoint)
	indicator = pyotl.indicator.real.KMP_HV(referencePoint)
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['HV', 'referencePoint'], [metric, ' '.join(map(str, referencePoint))])

def evaluate_monte_carlo_hv(config, rowID, columns, rowData):
	properties = dict(zip(columns, rowData))
	module, function = config.get('hv', 'reference_point').rsplit('.', 1)
	module = importlib.import_module(module)
	referencePoint = getattr(module, function)(config, properties)
	referencePoint = pyotl.utility.PyList2Vector_Real(referencePoint)
	random = pyotl.utility.Random(pyotl.utility.Time())
	sample = config.getint('monte_carlo_hv', 'sample')
	indicator = pyotl.indicator.real.MonteCarloHV(referencePoint, random, sample)
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['HV', 'referencePoint'], [metric, ' '.join(map(str, referencePoint))])

def evaluate_r2(config, rowID, columns, rowData):
	properties = dict(zip(columns, rowData))
	module, function = config.get('r2', 'reference_point').rsplit('.', 1)
	module = importlib.import_module(module)
	referencePoint = getattr(module, function)(config, properties)
	referencePoint = pyotl.utility.PyList2Vector_Real(referencePoint)
	module, function = config.get('r2', 'weight_vectors').rsplit('.', 1)
	module = importlib.import_module(module)
	weightVectors = getattr(module, function)(config, properties['solutions'], properties['objectives'])
	assert(weightVectors.shape[1] == properties['objectives'])
	weightVectors = pyotl.utility.PyListList2VectorVector_Real(weightVectors.tolist())
	indicator = pyotl.indicator.real.R2(referencePoint, weightVectors)
	pf = rowData[columns.index('pf')]
	pf = pyotl.utility.PyListList2VectorVector_Real(numpy.loadtxt(io.BytesIO(pf), ndmin = 2).tolist())
	uuidIndicator = rowData[columns.index('uuid')] + '.' + type(indicator).__name__
	print(uuidIndicator)
	metric = indicator(pf)
	print('%s=%f' % (uuidIndicator, metric))
	pyoptimization.indicator.utility.update_row(config, rowID, ['HV', 'referencePoint'], [metric, ' '.join(map(str, referencePoint))])

def evaluate(config, rowID, columns, rowData, executer):
	columns, rowData = pyoptimization.database.remove_null_data(columns, rowData)
	if config.getboolean('switch', 'gd'):
		executer(evaluate_gd, config, rowID, columns, rowData)
	if config.getboolean('switch', 'igd'):
		executer(evaluate_igd, config, rowID, columns, rowData)
	if config.getboolean('switch', 'eps'):
		executer(evaluate_eps, config, rowID, columns, rowData)
	if config.getboolean('switch', 'sp'):
		executer(evaluate_sp, config, rowID, columns, rowData)
	if config.getboolean('switch', 'ms'):
		executer(evaluate_ms, config, rowID, columns, rowData)
	if config.getboolean('switch', 'ms1'):
		executer(evaluate_ms1, config, rowID, columns, rowData)
	if config.getboolean('switch', 'ms2'):
		executer(evaluate_ms2, config, rowID, columns, rowData)
	if config.getboolean('switch', 'dm'):
		executer(evaluate_dm, config, rowID, columns, rowData)
	if config.getboolean('switch', 'auto_hv'):
		objectives = rowData[columns.index('objectives')]
		if objectives <= config.getint('auto_hv', 'objectives'):
			executer(evaluate_hv, config, rowID, columns, rowData)
		else:
			executer(evaluate_monte_carlo_hv, config, rowID, columns, rowData)
	else:
		if config.getboolean('switch', 'hv'):
			executer(evaluate_hv, config, rowID, columns, rowData)
		if config.getboolean('switch', 'monte_carlo_hv'):
			executer(evaluate_monte_carlo_hv, config, rowID, columns, rowData)
	if config.getboolean('switch', 'r2'):
		executer(evaluate_r2, config, rowID, columns, rowData)