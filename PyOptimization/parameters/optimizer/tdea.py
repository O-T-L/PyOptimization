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

def territory(config, problem):
	if type(problem).__name__ == 'DTLZ1':
		table = {
			3:	0.06,
			4:	0.13,
			5:	0.3,
			6:	0.465,
			8:	0.89,
			10:	0.992,
		}
		territory = table[problem.GetNumberOfObjectives()]
		return [territory]
	elif type(problem).__name__ == 'DTLZ2':
		table = {
			3:	0.1,
			4:	0.22,
			5:	0.34,
			6:	0.44,
			8:	0.68,
			10:	0.89,
		}
		territory = table[problem.GetNumberOfObjectives()]
		return [territory]
	elif type(problem).__name__ == 'DTLZ3':
		table = {
			3,	0.1,
			4,	0.2112,
			5,	0.35,
			6,	0.48,
			8,	0.85,
			10,	0.94,
		}
		territory = table[problem.GetNumberOfObjectives()]
		return [territory]
	elif type(problem).__name__ == 'DTLZ4':
		table = {
			3:	0.1,
			4:	0.22,
			5:	0.34,
			6:	0.46,
			8:	0.78,
			10:	0.999,
		}
		territory = table[problem.GetNumberOfObjectives()]
		return [territory]
	elif type(problem).__name__ == 'DTLZ5':
		table = {
			3:	0.0098,
			4:	0.08,
			5:	0.159,
			6:	0.232,
			8:	0.296,
			10:	0.34,
		}
		territory = table[problem.GetNumberOfObjectives()]
		return [territory]
	elif type(problem).__name__ == 'DTLZ6':
		table = {
			3:	0.0236,
			4:	0.164,
			5:	0.335,
			6:	0.5,
			8:	0.75,
			10:	0.895,
		}
		territory = table[problem.GetNumberOfObjectives()]
		return [territory]
	elif type(problem).__name__ == 'DTLZ7':
		table = {
			3:	0.044,
			4:	0.145,
			5:	0.265,
			6:	0.436,
			8:	0.78,
			10:	0.909,
		}
		territory = table[problem.GetNumberOfObjectives()]
		return [territory]
	elif type(problem).__name__ == 'DTLZ5I':
		if problem.GetNumberOfObjectives() == 10:
			table = {
				3:	0.145,
				4:	0.3,
				5:	0.4,
				6:	0.5,
				7:	0.7,
				8:	0.9,
				9:	0.94,
			}
			territory = table[problem.GetManifold() + 1]
			return [territory]
	raise