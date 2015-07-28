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
import numpy
import platform
import fnmatch
import configparser


def reformat(path, _reformat, delimiter='\t'):
    data = numpy.loadtxt(path, dtype=bytes, ndmin=2).astype(str)
    pathBase = os.path.splitext(path)[0]
    for ext, _data in _reformat(data):
        _path = pathBase + ext
        numpy.savetxt(_path, _data, fmt='%s', delimiter=delimiter)


def main():
    config = configparser.ConfigParser()
    config.read(os.path.splitext(__file__)[0] + '.ini')
    name = os.path.splitext(os.path.basename(__file__))[0]
    pathRoot = os.path.expandvars(config.get(name, 'root.' + platform.system()))
    pattern = config.get(name, 'pattern')
    _reformat = eval(config.get(name, 'reformat'))
    paths = []
    for pathParent, _, fileNames in os.walk(pathRoot):
        for fileName in fileNames:
            if fnmatch.fnmatch(fileName, pattern):
                path = os.path.join(pathParent, fileName)
                paths.append(path)
    for path in paths:
        print(path)
        reformat(path, _reformat)


if __name__ == '__main__':
    main()
