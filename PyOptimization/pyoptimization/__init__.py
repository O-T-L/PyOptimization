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

class NewContex:
	def __init__(self):
		self._names = []
		self._generators = []
	
	def set(self, name, generator):
		try:
			n = self._names.index(name)
			self._generators[n] = generator
		except ValueError:
			self._names.append(name)
			self._generators.append(generator)
	
	def __call__(self):
		context = {}
		for name, generator in zip(self._names, self._generators):
			context[name] = generator(context)
		return context