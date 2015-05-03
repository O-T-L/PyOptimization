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
import numpy
import pyoptimization.utility

def random(config):
	path = os.path.join(pyoptimization.utility.get_pyoptimization_path(config), 'Data', 'MOTSP')
	results = []
	city = 'Random30'
	for objectives in map(int, config.get('motsp', 'objectives').split()):
		matrics = [numpy.loadtxt(os.path.join(path, city, str(objectives), str(objective) + '.csv'), ndmin = 2) for objective in range(objectives)]
		results.append([matrics, city])
	return results