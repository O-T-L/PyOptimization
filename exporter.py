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
import platform
import sqlite3
import csv
import configparser
import pyoptimization.utility


def get_properties_settings(path, delimiter='\t'):
    f = open(path, 'r')
    reader = csv.reader(f, delimiter=delimiter)
    propertiesSettings = []
    for column, converter in reader:
        converter = eval(converter)
        propertiesSettings.append((column, converter))
    return propertiesSettings


def path_fill_properties(path, propertiesSettings, columns, rowData):
    for column, converter in propertiesSettings:
        properties = converter(rowData[columns.index(column)])
        path = os.path.join(path, properties)
    return path


def main():
    config = configparser.ConfigParser()
    pyoptimization.utility.read_config(config, __file__)
    # Database
    propertiesSettings = os.path.expandvars(config.get('exporter', 'properties_settings'))
    propertiesSettings = get_properties_settings(propertiesSettings)
    root = os.path.expandvars(config.get('exporter', 'root.' + platform.system()))
    conn = sqlite3.connect(os.path.expandvars(config.get('database', 'file.' + platform.system())))
    table = config.get('database', 'table')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM %s' % table)
    columns = list(map(lambda x: x[0], cursor.description))
    dataColumn = config.get('exporter', 'data_column')
    for rowData in cursor.fetchall():
        path = path_fill_properties(root, propertiesSettings, columns, rowData)
        data = rowData[columns.index(dataColumn)]
        print(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        f = open(path, 'wb')
        f.write(data)
        f.close()
    print('Finished normally')


if __name__ == '__main__':
    main()
