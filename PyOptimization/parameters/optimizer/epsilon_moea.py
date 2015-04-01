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

def epsilon(config, problem):
	if type(problem).__name__ == 'DTLZ1':
		table = {
			3:	0.033,
			4:	0.052,
			5:	0.059,
			6:	0.0554,
			8:	0.0549,
			10:	0.0565,
		}
		_epsilon = table[problem.GetNumberOfObjectives()]
		epsilon = [_epsilon] * problem.GetNumberOfObjectives()
		return [epsilon]
	elif type(problem).__name__ == 'DTLZ2':
		table = {
			2:	0.006,
			3:	0.06,
			4:	0.1312,
			5:	0.1927,
			6:	0.234,
			8:	0.29,
			10:	0.308,
		}
		_epsilon = table[problem.GetNumberOfObjectives()]
		epsilon = [_epsilon] * problem.GetNumberOfObjectives()
		return [epsilon]
	elif type(problem).__name__ == 'DTLZ3':
		table = {
			3:	0.06,
			4:	0.1385,
			5:	0.2,
			6:	0.227,
			8:	0.1567,
			10:	0.85,
		}
		_epsilon = table[problem.GetNumberOfObjectives()]
		epsilon = [_epsilon] * problem.GetNumberOfObjectives()
		return [epsilon]
	elif type(problem).__name__ == 'DTLZ4':
		table = {
			3:	0.06,
			4:	0.1312,
			5:	0.1927,
			6:	0.234,
			8:	0.29,
			10:	0.308,
		}
		_epsilon = table[problem.GetNumberOfObjectives()]
		epsilon = [_epsilon] * problem.GetNumberOfObjectives()
		return [epsilon]
	elif type(problem).__name__ == 'DTLZ5':
		table = {
			3:	0.0052,
			4:	0.042,
			5:	0.0785,
			6:	0.11,
			8:	0.1272,
			10:	0.1288,
		}
		_epsilon = table[problem.GetNumberOfObjectives()]
		epsilon = [_epsilon] * problem.GetNumberOfObjectives()
		return [epsilon]
	elif type(problem).__name__ == 'DTLZ6':
		table = {
			3:	0.0227,
			4:	0.12,
			5:	0.3552,
			6:	0.75,
			8:	1.15,
			10:	1.45,
		}
		_epsilon = table[problem.GetNumberOfObjectives()]
		epsilon = [_epsilon] * problem.GetNumberOfObjectives()
		return [epsilon]
	elif type(problem).__name__ == 'DTLZ7':
		table = {
			2:	0.005,
			3:	0.048,
			4:	0.105,
			5:	0.158,
			6:	0.15,
			8:	0.225,
			10:	0.46,
		}
		_epsilon = table[problem.GetNumberOfObjectives()]
		epsilon = [_epsilon] * problem.GetNumberOfObjectives()
		return [epsilon]
	elif type(problem).__name__ == 'ConvexDTLZ2':
		table = {
			2:	0.0075,
			3:	0.035,
		}
		_epsilon = table[problem.GetNumberOfObjectives()]
		epsilon = [_epsilon] * problem.GetNumberOfObjectives()
		return [epsilon]
	elif type(problem).__name__ == 'DTLZ5I':
		if problem.GetNumberOfObjectives() == 10:
			table = {
				3:	0.06,
				4:	0.12,
				5:	0.16,
				6:	0.2,
				7:	0.24,
				8:	0.25,
				9:	0.26,
			}
			_epsilon = table[problem.GetManifold() + 1]
			epsilon = [_epsilon] * problem.GetNumberOfObjectives()
			return [epsilon]
	raise Exception(type(problem).__name__, problem.GetNumberOfObjectives())