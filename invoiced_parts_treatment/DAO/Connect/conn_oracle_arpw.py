import cx_Oracle

def connect_oracle():
	#dsn_tns = cx_Oracle.makedsn('Host Name', 'Port Number', service_name='Service Name') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
	server='xxxx.ford.com'
	port='1521'
	db='arpwp1'
	user_x=r'user'
	password_x=decrypt('pass')
	dsn_tns = cx_Oracle.makedsn(server, port, service_name=db) 
	conn = cx_Oracle.connect(user=user_x, password=password_x, dsn=dsn_tns)
	return conn

def encrypt(message):
    newS=''
    for car in message:
        newS=newS+chr(ord(car)+2)
    return newS

def decrypt(message):
    newS=''
    for car in message:
        newS=newS+chr(ord(car)-2)
    return newS
