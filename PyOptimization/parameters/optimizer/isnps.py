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

def enumerate_degree1(config, problem):
	resolution = 70
	amplification = config.getfloat('isnps', 'amplification')
	if amplification == 3:
		if re.match('^DTLZ[1-4]$', type(problem).__name__):
			return {
				3:	numpy.linspace(0, 5, resolution),
				6:	numpy.linspace(7, 15, resolution),
			}[problem.GetNumberOfObjectives()]
		elif re.match('^DTLZ[56]$', type(problem).__name__):
			return {
				3:	numpy.linspace(0, 1, resolution),
				6:	numpy.linspace(0, 5, resolution),
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'DTLZ7':
			return {
				3:	numpy.linspace(0.5, 2.5, resolution),
				6:	numpy.linspace(2.5, 7, resolution),
			}[problem.GetNumberOfObjectives()]

def degree1(config, problem):
	amplification = config.getfloat('isnps', 'amplification')
	if amplification == 3:
		if type(problem).__name__ == 'DTLZ1':
			return {
				2:	0.9,
				3:	2.1,
				4:	4.1,
				5:	6.5,
				6:	8.7,
				8:	13.2,
				10:	15.6,
			}[problem.GetNumberOfObjectives()]
		elif re.match('^DTLZ[24]$', type(problem).__name__):
			return {
				2:	0.9,
				3:	2.3,
				4:	5.3,
				5:	8.5,
				6:	10.4,
				8:	14.5,
				10:	17.7,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'DTLZ3':
			return {
				2:	0.9,
				3:	2,
				4:	4.1,
				5:	6.5,
				6:	8.7,
				8:	13.2,
				10:	15.6,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'DTLZ5':
			return {
				3:	0.2,
				4:	0.15,
				5:	0.5,
				6:	0.7,
				8:	0.8,
				10:	1.15,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'DTLZ6':
			return {
				3:	0.2,
				4:	0.15,
				5:	0.5,
				6:	0.75,
				8:	0.95,
				10:	1.2,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'DTLZ7':
			return {
				3:	1,
				4:	2,
				5:	3,
				6:	3.9,
				8:	7.5,
				10:	11.5,
			}[problem.GetNumberOfObjectives()]
		###
		if type(problem).__name__ == 'DTLZ1':
			return {
				2:	0.81,
				3:	7.5,
				4:	15.5,
				5:	22.5,
				6:	27.1,
				8:	32.6,
				10:	36,
			}[problem.GetNumberOfObjectives()]
		elif re.match('^DTLZ[24]$', type(problem).__name__):
			return {
				2:	0.71,
				3:	6.79,
				4:	14.7,
				5:	21.9,
				6:	27.9,
				8:	35.5,
				10:	39,
			}[problem.GetNumberOfObjectives()]
		elif re.match('^DTLZ[2-4]$', type(problem).__name__):
			return {
				2:	0.71,
				3:	6.53,
				4:	14.1,
				5:	19.7,
				6:	23.9,
				8:	26.5,
				10:	29,
			}[problem.GetNumberOfObjectives()]
		elif re.match('^DTLZ[56]$', type(problem).__name__):
			return {
				2:	0.71,
				3:	0.71,
				4:	0.77,
				5:	0.89,
				6:	1.67,
				8:	2.15,
				10:	2.55,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'DTLZ7':
			return {
				2:	0.75,
				3:	3.05,
				4:	5.76,
				5:	8.9,
				6:	11.6,
				8:	32,
				10:	37,
			}[problem.GetNumberOfObjectives()]
		elif re.match('^ConvexDTLZ[2-4]$', type(problem).__name__):
			return {
				2:	0.89,
				3:	6.9,
				4:	14.7,
				5:	21.9,
				6:	27.9,
				8:	37,
				10:	39,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'WFG1':
			return {
				2:	0.35,
				3:	3.3,
				4:	6.9,
				5:	10.1,
				6:	13.1,
				8:	16.7,
				10:	19.3,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'WFG2':
			return {
				2:	0.35,
				3:	3.9,
				4:	7.5,
				5:	12.5,
				6:	15.1,
				8:	23.5,
				10:	27.1,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'WFG3':
			return {
				2:	0.36,
				3:	0.55,
				4:	0.75,
				5:	0.95,
				6:	1.16,
				8:	1.56,
				10:	1.99,
			}[problem.GetNumberOfObjectives()]
		elif re.match('^WFG[4-9]$', type(problem).__name__):
			return {
				2:	0.31,
				3:	2.7,
				4:	6.9,
				5:	11.2,
				6:	15.1,
				8:	22.9,
				10:	29.7,
			}[problem.GetNumberOfObjectives()]
	elif amplification == 1:
		if type(problem).__name__ == 'DTLZ1':
			return {
				2:	0.81,
				3:	7.5,
				4:	15.5,
				5:	22.5,
				6:	27.6,
				8:	35.6,
				10:	38,
			}[problem.GetNumberOfObjectives()]
		elif re.match('^DTLZ[2-4]$', type(problem).__name__):
			return {
				2:	0.73,
				3:	6.9,
				4:	14.7,
				5:	21.9,
				6:	27.9,
				8:	37,
				10:	39,
			}[problem.GetNumberOfObjectives()]
		elif re.match('^DTLZ[56]$', type(problem).__name__):
			return {
				2:	0.73,
				3:	0.73,
				4:	0.75,
				5:	0.87,
				6:	1.03,
				8:	1.5,
				10:	1.7,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'DTLZ7':
			return {
				2:	0.86,
				3:	3.5,
				4:	6.6,
				5:	9.5,
				6:	13.6,
				8:	39,
				10:	42,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'WFG1':
			return {
				2:	0.35,
				3:	3.3,
				4:	6.9,
				5:	10.1,
				6:	13.1,
				8:	16.7,
				10:	19.3,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'WFG2':
			return {
				2:	0.35,
				3:	3.9,
				4:	7.5,
				5:	12.5,
				6:	15.1,
				8:	23.5,
				10:	27.1,
			}[problem.GetNumberOfObjectives()]
		elif type(problem).__name__ == 'WFG3':
			return {
				2:	0.36,
				3:	0.55,
				4:	0.75,
				5:	0.95,
				6:	1.16,
				8:	1.56,
				10:	1.99,
			}[problem.GetNumberOfObjectives()]
		elif re.match('^WFG[4-9]$', type(problem).__name__):
			return {
				2:	0.31,
				3:	2.7,
				4:	6.9,
				5:	11.2,
				6:	15.1,
				8:	22.9,
				10:	29.7,
			}[problem.GetNumberOfObjectives()]

def degree2(config, problem):
	if type(problem).__name__ == 'DTLZ7':
		return 15
	else:
		return 45
