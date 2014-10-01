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

def epsilon(config, problem):
	if re.match('^DTLZ[1-7]$', type(problem).__name__):
		return numpy.array([{
			'DTLZ1':	{
				3:	0.033,
				4:	0.052,
				5:	0.059,
				6:	0.0554,
				8:	0.0549,
				10:	0.0565,
			},
			'DTLZ2':	{
				3:	0.06,
				4:	0.1312,
				5:	0.1927,
				6:	0.234,
				8:	0.29,
				10:	0.308,
			},
			'DTLZ3':	{
				3:	0.06,
				4:	0.1385,
				5:	0.2,
				6:	0.227,
				8:	0.1567,
				10:	0.85,
			},
			'DTLZ4':	{
				3:	0.06,
				4:	0.1312,
				5:	0.1927,
				6:	0.234,
				8:	0.29,
				10:	0.308,
			},
			'DTLZ5':	{
				3:	0.0052,
				4:	0.042,
				5:	0.0785,
				6:	0.11,
				8:	0.1272,
				10:	0.1288,
			},
			'DTLZ6':	{
				3:	0.0227,
				4:	0.12,
				5:	0.3552,
				6:	0.75,
				8:	1.15,
				10:	1.45,
			},
			'DTLZ7':	{
				2:	0.005,
				3:	0.048,
				4:	0.105,
				5:	0.158,
				6:	0.15,
				8:	0.225,
				10:	0.46,
			},
		}[type(problem).__name__][problem.GetNumberOfObjectives()]] * problem.GetNumberOfObjectives())
	elif re.match('^DTLZ[56]I$', type(problem).__name__):
		return numpy.array([{
			'DTLZ5I':	{
				10:	{
					3:	0.06,
					4:	0.12,
					5:	0.16,
					6:	0.2,
					7:	0.24,
					8:	0.25,
					9:	0.26,
				},
			},
		}[type(problem).__name__][problem.GetNumberOfObjectives()][problem.GetManifold() + 1]] * problem.GetNumberOfObjectives())