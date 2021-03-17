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
	chunck = pd.read_csv('vk622.csv',chunksize=100000,dtype={"ATSF_622OPTCDREC": "string"})
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
			df.at[index, 'ATDT_622DATAEXEC'] = arrange_date(row.ATDT_622DATAEXEC)
			df.at[index, 'ATDT_622OCREATEDT'] = arrange_date(row.ATDT_622OCREATEDT)
			df.at[index, 'ATDT_622OALTERDT'] = arrange_date(row.ATDT_622OALTERDT)
			df.at[index, 'ATDT_622IMPRESSAO'] = arrange_date(row.ATDT_622IMPRESSAO)
			df.at[index, 'ATDT_622REIMPRESS'] = arrange_date(row.ATDT_622REIMPRESS)+''
			data = row.ATTS_622CARGAVK[0: 10: 1]		
			data = arrange_date(data)
			df.at[index, 'ATTS_622CARGAVK'] = ('{}{}'.format(data,' 09.58.08.662317000 AM'))				
			#insere(row, ora)
		print('tempo iterar chunck = ', datetime.now() - checkpoint)
		checkpoint = datetime.now()
		df['PKSF_622FSA'] = df.PKSF_622NRORECALL
		#df.ATSF_622OPTCDREC.apply(str)
		#df['ATSF_622OPTCDREC'].astype(basestring)
		columns = ', '.join(df.columns)
		values=','.join([':{:d}'.format(i+1) for i in range(len(df.columns))])
		#values=', '.join(['?' for i in range(len(df.columns))])
		#sql = 'INSERT INTO DBAORAPW.PACD622V_REC_VIN ({columns:}) VALUES ({values:})'
		sql = ('''INSERT INTO DBAORAPW.PACD622V_REC_VIN (
				PKSF_622NRORECALL,
				PKSF_622VIN,
				ATND_622DEALEREXEC,
				ATDT_622DATAEXEC,
				ATSF_622STATUS,
				ATDT_622IMPRESSAO,
				ATDT_622REIMPRESS,
				ATDT_622OCREATEDT,
				ATSF_622OCREATEUS,
				ATDT_622OALTERDT,
				ATSF_622OALTERUS,
				ATSF_622RETSERPRO,
				ATTS_622CARGAVK,
				ATSF_622CARGAUS,
				ATSF_622CARGAACT,
				ATSF_622OPTCDREC,
				ATSF_622REPDESC,
				ATND_622VAL_MOBRA,
				PKSF_622FSA
				) VALUES (
				:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19
				)''')
		df = df.drop(df.columns[[0]], axis=1)	
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

def insere(row, ora):
	sql=("""INSERT INTO dbaorapw.pacd622v_rec_vin (
			pksf_622nrorecall,
			pksf_622fsa,
			pksf_622vin,
			atnd_622dealerexec,
			atdt_622dataexec,
			atsf_622status,
			atdt_622impressao,
			atdt_622reimpress,
			atdt_622ocreatedt,
			atsf_622ocreateus,
			atdt_622oalterdt,
			atsf_622oalterus,
			atsf_622retserpro,
			atts_622cargavk,
			atsf_622cargaus,
			atsf_622cargaact,
			atsf_622optcdrec,
			atsf_622repdesc,
			atnd_622val_mobra
			) VALUES (
			'{}',
			'{}',
			'{}',
			{},
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			'{}',
			{}
			)""".format(
			row.PKSF_622NRORECALL,
			row.PKSF_622NRORECALL,
			row.PKSF_622VIN,
			row.ATND_622DEALEREXEC,
			row.ATDT_622DATAEXEC,
			row.ATSF_622STATUS,
			row.ATDT_622IMPRESSAO,
			row.ATDT_622REIMPRESS,
			row.ATDT_622OCREATEDT,
			row.ATSF_622OCREATEUS,
			row.ATDT_622OALTERDT,
			row.ATSF_622OALTERUS,
			row.ATSF_622RETSERPRO,
			row.ATTS_622CARGAVK,
			row.ATSF_622CARGAUS,
			row.ATSF_622CARGAACT,
			row.ATSF_622OPTCDREC,
			row.ATSF_622REPDESC,
			row.ATND_622VAL_MOBRA	
			))	
	try:
		ora.execute(sql, '')
	except cx_Oracle.Error as error:
		print('Error occurred:')
		print(error)		

	
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
