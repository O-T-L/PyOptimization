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
import parameters.optimizer

def iteration(config, optimizer):
	if re.match('^(Convex|Scaled|Negative)?DTLZ\dI?$', type(optimizer.GetProblem()).__name__) and len(optimizer.GetProblem().GetBoundary()) == optimizer.GetProblem().GetNumberOfObjectives() - 1:
		return 100
	elif re.match('^WFG\d$', type(optimizer.GetProblem()).__name__) and len(optimizer.GetProblem().GetBoundary()) == optimizer.GetProblem().GetPosDecisions():
		return 100
	if type(optimizer.GetProblem()).__name__ == 'XSinX':
		return 50
	elif type(optimizer.GetProblem()).__name__ == 'Camel':
		return 50
	elif type(optimizer.GetProblem()).__name__ == 'ShafferF6':
		return 50
	elif type(optimizer.GetProblem()).__name__ == 'Shubert':
		return 50
	elif type(optimizer.GetProblem()).__name__ == 'ParetoBox':
		return 300
	elif type(optimizer.GetProblem()).__name__ == 'Water':
		return 300
	elif re.match('^(Rotated)?Rectangle$', type(optimizer.GetProblem()).__name__):
		return 300
	elif re.match('^ZDT[12356]$', type(optimizer.GetProblem()).__name__):
		return 300
	elif re.match('^ZDT[4]$', type(optimizer.GetProblem()).__name__):
		return 600
	elif re.match('^UF\d+$', type(optimizer.GetProblem()).__name__):
		return 300
	elif re.match('^(Convex|Scaled|Negative)?DTLZ[136]I?$', type(optimizer.GetProblem()).__name__):
		return 1000
	elif re.match('^(Convex|Scaled|Negative)?DTLZ[2457]I?$', type(optimizer.GetProblem()).__name__):
		return 300
	elif re.match('^WFG\d$', type(optimizer.GetProblem()).__name__):
		return 300
	elif re.match('^WFG[1]$', type(optimizer.GetProblem()).__name__):
		return 1000
	elif re.match('^WFG[2-9]$', type(optimizer.GetProblem()).__name__):
		return 300
	elif re.match('^FDA\d$', type(optimizer.GetProblem()).__name__):
		return 300
	elif re.match('^[A-Za-z0-9]*Knapsack$', type(optimizer.GetProblem()).__name__):
		return 1000
	elif type(optimizer.GetProblem()).__name__ == 'TSP':
		return 300
	elif type(optimizer.GetProblem()).__name__ == 'MOTSP':
		return 1000
	elif type(optimizer.GetProblem()).__name__ == 'ONL':
		return 300

def evaluation(config, optimizer):
	return iteration(config, optimizer) * 100
	return iteration(config, optimizer) * parameters.optimizer.population(config, optimizer.GetProblem())