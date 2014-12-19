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

def division(config, problem):
	if type(problem).__name__ == 'DTLZ1':
		if problem.GetNumberOfObjectives() == 3:
			return [10] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 4:
			return [10] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 5:
			return [10] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 6:
			return [10] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 8:
			return [10] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 10:
			return [11] * problem.GetNumberOfObjectives()
	elif re.match('DTLZ[24]', type(problem).__name__):
		if problem.GetNumberOfObjectives() == 3:
			return [10] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 4:
			return [10] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 5:
			return [9] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 6:
			return [8] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 8:
			return [7] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 10:
			return [8] * problem.GetNumberOfObjectives()
	elif type(problem).__name__ == 'DTLZ3':
		if problem.GetNumberOfObjectives() == 3:
			return [11] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 4:
			return [11] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 5:
			return [11] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 6:
			return [11] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 8:
			return [10] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 10:
			return [11] * problem.GetNumberOfObjectives()
	elif type(problem).__name__ == 'DTLZ5':
		if problem.GetNumberOfObjectives() == 3:
			return [35] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 4:
			return [35] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 5:
			return [29] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 6:
			return [14] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 8:
			return [11] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 10:
			return [11] * problem.GetNumberOfObjectives()
	elif type(problem).__name__ == 'DTLZ6':
		if problem.GetNumberOfObjectives() == 3:
			return [36] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 4:
			return [36] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 5:
			return [24] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 6:
			return [50] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 8:
			return [50] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 10:
			return [50] * problem.GetNumberOfObjectives()
	elif type(problem).__name__ == 'DTLZ7':
		if problem.GetNumberOfObjectives() == 3:
			return [9] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 4:
			return [9] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 5:
			return [8] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 6:
			return [6] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 8:
			return [5] * problem.GetNumberOfObjectives()
		elif problem.GetNumberOfObjectives() == 10:
			return [4] * problem.GetNumberOfObjectives()
	raise