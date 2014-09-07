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

import configparser
import importlib
import pyoptimization.utility
import pyoptimization.main

def main():
	config = configparser.ConfigParser()
	pyoptimization.utility.read_config(config, __file__)
	for module in ['pyoptimization.problem', 'pyoptimization.optimizer']:
		globals()[module] = importlib.import_module(module)
	codings = pyoptimization.utility.get_codings()
	optimization = [(eval('pyoptimization.problem.make_problem_' + coding), eval('pyoptimization.optimizer.make_optimizer_' + coding)) for coding in codings]
	pyoptimization.main.optimization(config, optimization)

if __name__ == '__main__':
	main()