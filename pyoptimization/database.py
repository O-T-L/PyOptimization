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

def get_columns(cursor, table):
	result = cursor.execute('PRAGMA table_info(%s)' % table)
	return map(lambda row: row[1], result)

def remove_null_data(columns, rowData):
	items = zip(*[columns, rowData])
	items = list(filter(lambda column_Data: column_Data[1], items))
	columns, rowData = zip(*items)
	return columns, rowData