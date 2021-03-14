import pyodbc

def connect_sqlserver():
	server = 'xxx.FORD.COM'
	database = 'bzwingsprd'
	username = 'xx'
	password = decrypt('xxx')
	conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
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