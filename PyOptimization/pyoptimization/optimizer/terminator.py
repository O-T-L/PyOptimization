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
import importlib

class IterationTerminator:
	def __init__(self, iteration):
		self.iteration = iteration
	
	def __call__(self, optimizer, optimization):
		return optimization.iteration < self.iteration

class EvaluationTerminator:
	def __init__(self, evaluation):
		self.evaluation = evaluation
	
	def __call__(self, optimizer, optimization):
		return optimizer.GetProblem().GetNumberOfEvaluations() < self.evaluation

def get_terminator(config, optimizer):
	termination = config.get('optimization', 'termination')
	if termination == 'iteration':
		module, function = config.get('optimization', termination).rsplit('.', 1)
		module = importlib.import_module(module)
		iteration = getattr(module, function)(config, optimizer)
		terminator = IterationTerminator(iteration)
	elif termination == 'evaluation':
		module, function = config.get('optimization', termination).rsplit('.', 1)
		module = importlib.import_module(module)
		evaluation = getattr(module, function)(config, optimizer)
		terminator = EvaluationTerminator(evaluation)
	return terminator