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
import configparser
import sqlite3
import pyoptimization.executer


def get_columns(path, table):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    result = cursor.execute('PRAGMA table_info(%s)' % table)
    return map(lambda row: row[1], result)


def optimization(config, problem_optimize, optimizer_optimize):
    executer = pyoptimization.executer.make_executer(config)
    repeat = config.getint('experiment', 'repeat')
    for _ in range(repeat):
        problem_optimize(config, executer, optimizer_optimize)
    if config.get('common', 'executer') == 'parallel':
        executer.join()
    print('Finished normally')


def evaluation(config, fnEvaluator):
    executer = pyoptimization.executer.make_executer(config)
    path = os.path.expandvars(config.get('database', 'file.' + platform.system()))
    conn = sqlite3.connect(path)
    conn.isolation_level = None  # Enable automatic commit
    table = config.get('database', 'table')
    cursor = conn.cursor()
    columns = tuple(get_columns(path, table))
    try:
        condition = config.get('database', 'condition')
        cursor.execute('SELECT rowid,* FROM %s WHERE %s' % (table, condition))
    except configparser.NoOptionError:
        cursor.execute('SELECT rowid,* FROM ' + table)
    results = cursor.fetchall()
    nRows = len(results)
    for index, result in enumerate(results):
        print('Evaluating %u of %u' % (index, nRows))
        fnEvaluator(config, result[0], columns, result[1:], executer)
    if config.get('common', 'executer') == 'parallel':
        executer.join()
    print('Finished normally')
