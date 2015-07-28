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
import numpy
import pyoptimization.utility


def objective(config, properties):
    path = pyoptimization.utility.get_pyoptimization_path(config)
    if re.match('^ZDT\d$', properties['problem']):
        return numpy.array([(0.0, 1.0)] * properties['objectives'])
    elif properties['problem'] == 'DTLZ1':
        return numpy.array([(0.0, 0.5)] * properties['objectives'])
    elif re.match('^(Convex)?DTLZ[23456]I?$', properties['problem']):
        return numpy.array([(0.0, 1.0)] * properties['objectives'])
    elif properties['problem'] == 'DTLZ7':
        return numpy.loadtxt(
            os.path.join(path, 'Data', 'Boundary', 'Objective', 'DTLZ7', str(properties['objectives']) + '.csv'),
            ndmin=2)
    elif re.match('^WFG\d$', properties['problem']):
        return numpy.array([(0.0, upper) for upper in range(2, (properties['objectives'] + 1) * 2, 2)])
