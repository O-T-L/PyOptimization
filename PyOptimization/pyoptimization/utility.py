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

import sys
import os
import inspect

def read_config(config, path):
	config.read(os.path.join(os.path.dirname(path), 'config.ini'))
	config.read(os.path.splitext(path)[0] + '.ini')

def get_codings(prefix = 'pyotl.problem.'):
	codings = []
	for module in list(sys.modules.keys()):
		if module.startswith(prefix):
			try:
				_module = sys.modules[module]
				names, _ = zip(*inspect.getmembers(_module, inspect.isclass))
				if 'Problem'in names:
					codings.append(module[len(prefix):])
			except:
				pass
	return codings

def get_pyoptimization_path(config):
	try:
		return config.get('common', 'pyoptimization_path')
	except:
		return os.path.curdir