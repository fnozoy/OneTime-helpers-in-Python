import pyodbc 
import pandas as pd
def process():
	arq_eb1 = open('../IO/reemviar_prev.txt', 'r')
	arq_ab1 = open('../IO/reemviar_after.txt', 'w')
	wings_connection = connect_wings()
	for reg_eb1 in arq_eb1:
		print(reg_eb1)
		antes                   = reg_eb1[0: 9: 1]
		pedido                  = reg_eb1[9: 16: 1]
		meio                    = reg_eb1[16: 23: 1]
		peca_despachada_prefixo = reg_eb1[23: 28: 1]
		peca_despachada_base    = reg_eb1[28: 37: 1]
		peca_despachada_sufixo  = reg_eb1[37: 43: 1]
		depois                  = reg_eb1[43: 90: 1]
		peca_despachada = ' '+peca_despachada_base+peca_despachada_prefixo+peca_despachada_sufixo				
		#monta query
		query = select(pedido, peca_despachada.rstrip())

		#roda a query
		df_ora = pd.read_sql(query, con=wings_connection)
		#pega EB1 troca peça despachada pela ordenada		
		
		for index, row in df_ora.iterrows():
			peca_ordenada         = row['ordered_popims_part']
			peca_ordenada_base    = peca_ordenada[1: 10: 1]
			peca_ordenada_prefixo = peca_ordenada[10: 15: 1]
			peca_ordenada_sufixo  = peca_ordenada[15: 21: 1]
			reg_ab1 = antes + pedido + meio + peca_ordenada_prefixo + peca_ordenada_base + peca_ordenada_sufixo.ljust(6) + depois + "\n"			
			arq_ab1.write(reg_ab1.ljust(90))
			break
		
		if df_ora.empty:
			arq_ab1.write(reg_eb1)
			print('esse eb1 deu erro=', reg_eb1)
		
		
		debug=False
		if debug:
			print('eb1 = ', reg_eb1)
			print('antes = ',antes)
			print('pedido = ',pedido)
			print('meio = ',meio)
			print('peca_despachada_prefixo  = ',peca_despachada_prefixo )
			print('peca_despachada_base = ',peca_despachada_base)
			print('peca_despachada_sufixo = ',peca_despachada_sufixo)
			print('depois = ',depois)
			print('peca ordenada = ',peca_ordenada)
			print('peca ordenada_bas = ',peca_ordenada_base)
			print('peca ordenada_pre = ',peca_ordenada_prefixo)
			print('peca ordenada_suf = ',peca_ordenada_sufixo)
			print('ab1 = ', reg_ab1)

	arq_eb1.close()
	arq_ab1.close()


def select(pedido, peca):
	sql = list()
	sql.append(  ' SELECT P.WIN100_POPIMS_ARG_BRA_C ordered_popims_part,')
	sql.append(  '        P1.WIN100_POPIMS_ARG_BRA_C dispatched_popims_part')
	sql.append(  ' from MWIN352_WORK_ORDER_ITEMS_DETAILS ordidetails')
	sql.append(  ' inner join MWIN351_WORK_ORDERS_ITEMS orditems  on ordidetails.WIN352_WIN351_BK_WORK_ORDER_ITEM_UID_D = orditems.WIN351_WORK_ORDER_ITEM_UID_K')
	sql.append(  ' inner join MWIN350_WORK_ORDERS ord on ord.WIN350_BK_WORK_ORDER_UID_K = orditems.WIN351_WIN350_BK_WORK_ORDER_UID_D')
	sql.append(  ' inner join MWIN014_STATUS stat on stat.WIN014_STATUS_UID_K = ordidetails.WIN352_WIN014_STATUS_UID_D')
	sql.append(  ' inner join MWIN101_PARTS_X_SUB_DIVISION pxsd on orditems.WIN351_WIN101_PART_SUB_DIVISION_UID_D = pxsd.WIN101_PART_SUB_DIVISION_UID_K')
	sql.append(  ' inner join MWIN100_PARTS P on pxsd.WIN101_WIN100_BK_PART_UID_D = P.WIN100_PART_UID_K')
	sql.append(  ' inner join MWIN101_PARTS_X_SUB_DIVISION pxsd1 on ordidetails.WIN352_WIN101_PART_SUB_DIVISION_UID_D = pxsd1.WIN101_PART_SUB_DIVISION_UID_K')
	sql.append(  ' inner join MWIN100_PARTS P1 on pxsd1.WIN101_WIN100_BK_PART_UID_D = P1.WIN100_PART_UID_K')
	sql.append(  ' where  ord.WIN350_POPIMS_ORDER_R in (\'{}\') '.format(pedido))
	sql.append(  ' and    P1.WIN100_POPIMS_ARG_BRA_C = (\'{}\');'.format(peca))
	sql = "".join(sql)
	return sql

def connect_wings():
	server = 'sql000693l.APP.FORD.COM' 
	database = 'bzwingsprd' 
	username = 'aplicpw' 	
	password = decrypt('GwUqw?Nkpfq229')
	#print ('senha=', encrypt('minha_senha'))
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
	
process()