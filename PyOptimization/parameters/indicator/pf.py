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
import pyoptimization.utility

def pf(config, properties, folder = 'PF'):
	path = os.path.join(pyoptimization.utility.get_pyoptimization_path(config), 'Data', folder)
	if re.match('^ZDT[14]$', properties['problem']):
		return numpy.loadtxt(os.path.join(path, 'ZDT1.csv'), ndmin = 2)
	elif re.match('^ZDT[26]$', properties['problem']):
		return numpy.loadtxt(os.path.join(path, 'ZDT2.csv'), ndmin = 2)
	elif re.match('^ZDT3$', properties['problem']):
		return numpy.loadtxt(os.path.join(path, 'ZDT3.csv'), ndmin = 2)
	elif re.match('^ZDT5$', properties['problem']):
		return numpy.loadtxt(os.path.join(path, 'ZDT5.csv'), ndmin = 2)
	elif properties['problem'] == 'DTLZ1':
		return numpy.loadtxt(os.path.join(path, 'DTLZ1', str(properties['objectives']) + '.csv'), ndmin = 2)
	elif re.match('^DTLZ[234]$', properties['problem']):
		if properties['objectives'] == 2:
			return numpy.loadtxt(os.path.join(path, 'DTLZ5', str(properties['objectives']) + '.csv'), ndmin = 2)
		else:
			return numpy.loadtxt(os.path.join(path, 'DTLZ2', str(properties['objectives']) + '.csv'), ndmin = 2)
	elif re.match('^DTLZ[56]$', properties['problem']):
		return numpy.loadtxt(os.path.join(path, 'DTLZ5', str(properties['objectives']) + '.csv'), ndmin = 2)
	elif properties['problem'] == 'DTLZ7':
		return numpy.loadtxt(os.path.join(path, 'DTLZ7', str(properties['objectives']) + '.csv'), ndmin = 2)
	elif re.match('^DTLZ[56]I$', properties['problem']):
		return numpy.loadtxt(os.path.join(path, 'DTLZ5I', '%u_%u.csv' % (properties['objectives'], properties['DTLZ_I'])), ndmin = 2)
	elif re.match('^ScaledDTLZ[234]$', properties['problem']):
		pf = numpy.loadtxt(os.path.join(path, 'DTLZ2', str(properties['objectives']) + '.csv'), ndmin = 2)
		for i, col in enumerate(pf.T):
			col *= math.pow(10, i)
		return pf
	elif re.match('^WFG[1-3]$', properties['problem']):
		return numpy.loadtxt(os.path.join(path, properties['problem'], str(properties['objectives']) + '.csv'), ndmin = 2)
	elif re.match('^WFG[4-9]$', properties['problem']):
		return numpy.loadtxt(os.path.join(path, 'WFG4', str(properties['objectives']) + '.csv'), ndmin = 2)