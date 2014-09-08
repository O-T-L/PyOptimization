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
import numpy

def angle(config, problem):
	dtlz2 = {
		3:	0.5,
		4:	0.5,
		5:	0.5,
		6:	0.5,
		8:	0.5,
		10:	0.5,
	}
	if re.match('^DTLZ[234]$', type(problem).__name__):
		return numpy.array([dtlz2[problem.GetNumberOfObjectives()]] * problem.GetNumberOfObjectives()) * numpy.pi