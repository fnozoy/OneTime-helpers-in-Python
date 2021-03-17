from datetime import datetime
import cx_Oracle
import pandas as pd
import numpy as np

def __init__():

	inicio = datetime.now()
	checkpoint = datetime.now()
	print('inicio ', inicio)
	conn = conecta_oracle()
	ora = conn.cursor()
	print('tempo conexão = ', datetime.now() - checkpoint)
	checkpoint = datetime.now()
	chunck = pd.read_csv('vk623.csv',chunksize=100000)
	#chunck = pd.read_csv('teste.csv',chunksize=100)	
	print('tempo chunckear = ', datetime.now() - checkpoint)
	checkpoint = datetime.now()
	#count_chunck = 0
	for df in chunck:
		#count_chunck += 1
		#if count_chunck <= 3:
		#	continue
		df = df.replace(np.nan, '', regex=True)
		print('tempo ler csv = ', datetime.now() - checkpoint)
		checkpoint = datetime.now()
		print('vou iterar o chunck')
		for index, row in df.iterrows():
			df.at[index, 'ATDT_623CREATDATE'] = arrange_date(row.ATDT_623CREATDATE)
			df.at[index, 'ATDT_623ALTERDATE'] = arrange_date(row.ATDT_623ALTERDATE)
		print('tempo iterar chunck = ', datetime.now() - checkpoint)
		checkpoint = datetime.now()
		columns = ', '.join(df.columns)
		values=','.join([':{:d}'.format(i+1) for i in range(len(df.columns))])
		sql = ('''INSERT INTO dbaorapw.pacd623v_peca_reca (
					pksf_623nrorecall,
					pksf_623vin,
					pknd_632reparo,
					pksf_623peca,
					atsf_623peca_desc,
					atsf_623creatuser,
					atdt_623creatdate,
					atsf_623alteruser,
					atdt_623alterdate
				) VALUES (
				:1, :2, :3, :4, :5, :6, :7, :8, :9
				)''')
		df = df.drop(df.columns[[0, 8, 11]], axis=1)	
		rows = [tuple(x) for x in df.values.tolist()]
		print('tempo montar tuple = ', datetime.now() - checkpoint)
		checkpoint = datetime.now()
		try:		
			ora.executemany(sql, rows)		
		except cx_Oracle.Error as error:
			print('Error occurred:')
			print(error)
		print('tempo insert = ', datetime.now() - checkpoint)
		checkpoint = datetime.now()
		conn.commit()
		print('tempo commit = ', datetime.now() - checkpoint)
	tempo = datetime.now() - inicio
	print('terminou em ', tempo)
	quit()
	
def arrange_date(data):	

	ano = data[2: 4: 1]
	mes = data[5: 7: 1]
	dia = data[8: 10: 1]
	if mes == '01':
		mes='jan'
	elif mes == '02':
		mes='feb'
	elif mes == '03':
		mes='mar'
	elif mes == '04':
		mes='apr'
	elif mes == '05':
		mes='may'
	elif mes == '06':
		mes='jun'
	elif mes == '07':
		mes='jul'
	elif mes == '08':
		mes='aug'
	elif mes == '09':
		mes='sep'
	elif mes == '10':
		mes='oct'
	elif mes == '11':
		mes='nov'
	elif mes == '12':
		mes='dec'
	if dia == '':
		data=''
	else:
		data = ('{}-{}-{}'.format(dia, mes, ano))

	return data
	
def conecta_oracle():
	#dsn_tns = cx_Oracle.makedsn('Host Name', 'Port Number', service_name='Service Name') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
	server='xxxx.cloud.ford.com'
	port='1521'
	db='xxxx'
	user_x=r'xxxx'
	password_x=decrypt('xxxx')
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
	
__init__()
