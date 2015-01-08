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

import re
import os
import math
import numpy
import pyotl.utility
import pyoptimization.utility

_pfs = {}

def get_pf(path):
	if path in _pfs:
		return _pfs[path]
	else:
		pf = numpy.loadtxt(path, ndmin = 2)
		_pf = pyotl.utility.PyListList2VectorVector_Real(pf.tolist())
		_pfs[path] = _pf
		return _pf

def pf(config, properties, folder = 'PF'):
	path = os.path.join(pyoptimization.utility.get_pyoptimization_path(config), 'Data', folder)
	if re.match('^ZDT[14]$', properties['problem']):
		return get_pf(os.path.join(path, 'ZDT1.csv'))
	elif re.match('^ZDT[26]$', properties['problem']):
		return get_pf(os.path.join(path, 'ZDT2.csv'))
	elif re.match('^ZDT3$', properties['problem']):
		return get_pf(os.path.join(path, 'ZDT3.csv'))
	elif re.match('^ZDT5$', properties['problem']):
		return get_pf(os.path.join(path, 'ZDT5.csv'))
	elif properties['problem'] == 'DTLZ1':
		return get_pf(os.path.join(path, 'DTLZ1', str(properties['objectives']) + '.csv'))
	elif re.match('^DTLZ[234]$', properties['problem']):
		if properties['objectives'] == 2:
			return get_pf(os.path.join(path, 'DTLZ5', str(properties['objectives']) + '.csv'))
		else:
			return get_pf(os.path.join(path, 'DTLZ2', str(properties['objectives']) + '.csv'))
	elif re.match('^DTLZ[56]$', properties['problem']):
		return get_pf(os.path.join(path, 'DTLZ5', str(properties['objectives']) + '.csv'))
	elif properties['problem'] == 'DTLZ7':
		return get_pf(os.path.join(path, 'DTLZ7', str(properties['objectives']) + '.csv'))
	elif re.match('^DTLZ[56]I$', properties['problem']):
		return get_pf(os.path.join(path, 'DTLZ5I', '%u_%u.csv' % (properties['objectives'], properties['DTLZ_I'])))
	elif re.match('^ScaledDTLZ[234]$', properties['problem']):
		pf = numpy.loadtxt(os.path.join(path, 'DTLZ2', str(properties['objectives']) + '.csv'))
		for i, col in enumerate(pf.T):
			col *= math.pow(10, i)
		return pf
	elif re.match('^WFG[1-3]$', properties['problem']):
		return get_pf(os.path.join(path, properties['problem'], str(properties['objectives']) + '.csv'))
	elif re.match('^WFG[4-9]$', properties['problem']):
		return get_pf(os.path.join(path, 'WFG4', str(properties['objectives']) + '.csv'))
	print(properties)
	raise