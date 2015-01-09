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

import numpy

def enumerate_angle(config, problem):
	resolution = 60
	return [[s * numpy.pi] * problem.GetNumberOfObjectives() for s in numpy.linspace(0.2, 0.8, resolution)]

def angle(config, problem):
	if type(problem).__name__ == 'DTLZ1':
		table = {
			3:	70.77967,
			5:	63.4576,
			10:	67.1186,
			15:	70.77966,
			20:	59.7966,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'DTLZ2':
		table = {
			3:	89.0847,
			5:	81.7627,
			10:	63.4576,
			15:	63.4576,
			20:	54.30508,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'DTLZ3':
		table = {
			3:	87.25424,
			5:	81.7627,
			10:	65.2881,
			15:	59.7966,
			20:	56.13559,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'DTLZ4':
		table = {
			3:	87.25424,
			5:	85.4237,
			10:	70.77966,
			15:	61.627,
			20:	59.7966,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'DTLZ5':
		table = {
			3:	89.0847,
			5:	83.59322,
			10:	78.101695,
			15:	78.101695,
			20:	76.2712,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'DTLZ6':
		table = {
			3:	85.42373,
			5:	76.2712,
			10:	56.13559,
			15:	54.3051,
			20:	50.6441,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'DTLZ7':
		table = {
			3:	89.0847,
			5:	83.5932,
			10:	85.42373,
			15:	87.25424,
			20:	87.2542,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'WFG1':
		table = {
			3:	67.1186,
			5:	48.8135,
			10:	37.8305,
			15:	39.6610,
			20:	45.1525,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'WFG2':
		table = {
			3:	83.5932,
			5:	83.5932,
			10:	72.6102,
			15:	89.0847,
			20:	57.9661,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'WFG3':
		table = {
			3:	72.6102,
			5:	85.4237,
			10:	92.7457,
			15:	125.6949,
			20:	85.4237,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'WFG4':
		table = {
			3:	85.4237,
			5:	79.9322,
			10:	74.4407,
			15:	72.6101,
			20:	67.1186,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'WFG5':
		table = {
			3:	85.4237,
			5:	79.9322,
			10:	78.1017,
			15:	72.6102,
			20:	74.4407,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'WFG6':
		table = {
			3:	87.2542,
			5:	79.9322,
			10:	78.1017,
			15:	76.2712,
			20:	70.7796,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'WFG7':
		table = {
			3:	87.2542,
			5:	79.9322,
			10:	74.4407,
			15:	67.1186,
			20:	67.1186,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'WFG8':
		table = {
			3:	81.7627,
			5:	76.2712,
			10:	76.2712,
			15:	81.7627,
			20:	67.1186,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'WFG9':
		table = {
			3:	83.5932,
			5:	76.2712,
			10:	76.2712,
			15:	78.10169,
			20:	74.4410,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	elif type(problem).__name__ == 'MOTSP':
		table = {
			4:	72.6102,
			5:	63.4576,
			10:	41.4915,
			15:	36.0,
		}
		degree = table[problem.GetNumberOfObjectives()]
		angle = [degree * numpy.pi / 180] * problem.GetNumberOfObjectives()
		return [angle]
	raise