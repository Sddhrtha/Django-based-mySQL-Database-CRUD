from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse

from .mysqlConnector import *
from userCRUD.models import dbNames
# Create your views here.


def getdbDetails(pk):
	db = get_object_or_404(dbNames, pk = pk)
	Details = {
		'Name' : db.dbName,
		'Username' : db.dbUsername,
		'Password' : db.dbPassword,
		'Host' : db.dbHost,
		'Port' : db.dbPort,
	}
	return Details

"""***************************************************************************************************"""

@login_required
def Select(request, pk):
	Details = getdbDetails(pk)

	connection = Connection(Details)
	if connection is False:
		return HttpResponse("Connection failed.")
	else:
			with connection.cursor() as cursor:
				sql = f"SELECT * FROM information_schema.tables WHERE table_schema = '{Details['Name']}'"
				cursor.execute(sql)
				result = cursor.fetchall()
				tables = []
				for row in result:
					tables.append(row[2])
				return render(request, 'DBTables.html', { 'tables' : tables, 'pk' : pk })


"""***************************************************************************************************"""

@login_required
def Read(request, pk, table):
	Details = getdbDetails(pk)
	TableName = str(table)

	connection = Connection(Details)
	if connection is False:
		return HttpResponse("Connection failed. Check Database details.")
	else:
			with connection.cursor() as cursor:

				sql = f"SHOW columns FROM {TableName}"
				cursor.execute(sql)
				columns = cursor.fetchall()
				columnsList = []
				for tup in columns:
					columnsList.append(tup[0])
					
				sql = f"SELECT * FROM {TableName}"	
				cursor.execute(sql)
				rows = cursor.fetchall()


				Context = {
					'cList' : columnsList,
					'rows'  : rows,
					'Table' : TableName,
					'pk' : pk,
				}

			connection.commit()	
	return render(request, 'main.html', Context)


"""***************************************************************************************************"""

@login_required
def Delete(request, pk,row, table):
	Details = getdbDetails(pk)

	connection = Connection(Details)
	if connection is False:
		return HttpResponse("Connection failed. Check Database details.")
	else:
			with connection.cursor() as cursor:

				sql = f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'"
				cursor.execute(sql)
				pKey = cursor.fetchall()
				PKey = pKey[0][4]

				sql = f"SELECT {PKey} FROM {table}"
				cursor.execute(sql)
				rows = cursor.fetchall()
				Row = rows[row]
				Row  = Row[0]

				sql = f"DELETE FROM {table} WHERE {PKey} = '{Row}'"
				cursor.execute(sql)
			connection.commit()	
			return HttpResponseRedirect(reverse('connection:Read', args =(pk, table)))


"""***************************************************************************************************"""


@login_required
def Create(request, pk, table):
	Details = getdbDetails(pk)

	connection = Connection(Details)
	if connection is False:
		return HttpResponse("Connection failed. Check Database details.")
	else:
		with connection.cursor() as cursor:

			sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"
			cursor.execute(sql)
			result = cursor.fetchall()
			colList = []
			for column in result:
				colList.append(column[0])

			sql = f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}'"
			cursor.execute(sql)
			result = cursor.fetchall()
			colType = []
			for c in result:
				colType.append(c[0])


	if request.method == 'POST':

		Values = []
		for i, val in enumerate(colList):
			Values.append(request.POST.get(val))

			sql = f"INSERT INTO {table} ("

			for i, col in enumerate(colList):
				if i == len(colList) - 1 :
					sql = sql + str(col) + ") "
				else :
					sql = sql + str(col) + ","


			sql = sql + "VALUES ("

			for i ,val in  enumerate(Values):
				if i == len(Values) - 1 :
					sql = sql + "'" + str(val) + "'" + ")"
				else :
					sql = sql + "'" + str(val) + "'" + ","

		with connection.cursor() as cursor:
			cursor.execute(sql)
		connection.commit()
		return HttpResponseRedirect(reverse('connection:Read', args =(pk, table)))



	else:
		
			Context = {
				'cList'	: colList,
				'cType' : colType,
				'pk' : pk, 
				'Table' : table,
			}

			return render(request, 'Create.html', Context)


"""***************************************************************************************************"""

@login_required
def Update(request, pk,row,table):
	Details = getdbDetails(pk)
	connection = Connection(Details)
	if connection is False:
		return HttpResponse("Connection failed. Check Database details.")
	else:
		with connection.cursor() as cursor:

			sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"
			cursor.execute(sql)
			Columns = cursor.fetchall()
			colList = []
			for c in Columns:
				colList.append(c[0])

			sql = f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}'"
			cursor.execute(sql)
			ColTypes = cursor.fetchall()
			cType = []
			for c in ColTypes:
				cType.append(c[0])


	if request.method == 'POST':

		Values = []
		for i, val in enumerate(colList):
			Values.append(request.POST.get(val))

		with connection.cursor() as cursor:

			sql = f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'"
			cursor.execute(sql)
			pKey = cursor.fetchall()

			PKey = pKey[0][4]

			sql = f"SELECT {PKey} FROM {table}"
			cursor.execute(sql)
			allRows = cursor.fetchall()

			aRows = []
			for r in allRows:
				aRows.append(r[0])


			nRow = aRows[row]

			sql = f"UPDATE {table} SET "
			for c in range(len(colList)):

				if c == len(colList) - 1:
					sql = sql + str(colList[c]) +" = '"+ str(Values[c]) + f"' WHERE {PKey} = '{nRow}'"
				else:
					sql = sql + str(colList[c]) +" = '"+ str(Values[c]) + "', "
				cursor.execute(sql)

		connection.commit()

		return HttpResponseRedirect(reverse('connection:Read', args =(pk, table)))



	else:
		with connection.cursor() as cursor:

			sql = f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'"
			cursor.execute(sql)
			pKey = cursor.fetchall()

			PKey = pKey[0][4]

			sql = f"SELECT {PKey} FROM {table}"
			cursor.execute(sql)
			allRows = cursor.fetchall()

			aRows = []
			for r in allRows:
				aRows.append(r[0])


			nRow = aRows[row]
			sql = f"SELECT * FROM {table} WHERE {PKey} = '{nRow}'"
			cursor.execute(sql)
			tempList = cursor.fetchall()

			valList = []
			for r in tempList:
				for v in r:
					valList.append(v)


			MetaData = zip(colList, valList)

			Context = { 
				'Meta' : MetaData,
				'cType' : cType,
				'pk' : pk,
				'Table' : table,
				'counter' : row,
			}

			return render(request, 'Update.html',Context)


