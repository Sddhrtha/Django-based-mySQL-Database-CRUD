import pymysql

def Connection(DBdetails):

	try:
		connection = pymysql.connect(
			host = str(DBdetails['Host']),
			user = str(DBdetails['Username']),
			password = str(DBdetails['Password']),
			db = str(DBdetails['Name']),
		)
	except:
		return False

	return connection