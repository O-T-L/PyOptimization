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
import csv
import sqlite3
import configparser
import pyoptimization.utility


def get_settings(path, delimiter='\t'):
    f = open(path, 'r')
    reader = csv.reader(f, delimiter=delimiter)
    settingsList = []
    for row in reader:
        assert (2 <= len(row) <= 3)
        if len(row) == 2:
            settingsList.append(row + [''])
        elif len(row) == 3:
            if bool(row[-1]):
                settingsList.append(row[:2] + ['NOT NULL'])
            else:
                settingsList.append(row[:2] + [''])
        assert (len(settingsList[-1]) == 3)
    return settingsList


def main():
    config = configparser.ConfigParser()
    pyoptimization.utility.read_config(config, __file__)
    pathSettingsCSV = os.path.expandvars(config.get('reset', 'settings'))
    settingsList = get_settings(pathSettingsCSV)
    # Database
    path = os.path.expandvars(config.get('database', 'file.' + platform.system()))
    print(path)
    if config.getboolean('reset', 'remove'):
        try:
            os.remove(path)
        except:
            pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    table = config.get('database', 'table')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS %s' % table)

    sql = 'CREATE TABLE %s (%s)' % (
    table, ','.join(['"%s" %s %s' % (column, dataType, notNull) for column, dataType, notNull in settingsList]))
    cursor.execute(sql)
    conn.commit()


if __name__ == '__main__':
    main()
