import ibm_db as db2
import ibm_db_dbi
import pandas as pd
conn = db2.connect("DATABASE=LOCDB2FA;HOSTNAME=xxx.ford.com;PORT=446;PROTOCOL=TCPIP;UID=xxx;PWD=xxx;", "", "")

sql = 'select * FROM AXG0203.PACD622V_REC_VIN'
conn = ibm_db_dbi.Connection(conn)
df = pd.read_sql(sql, conn)
df.to_csv('vk622.csv')
sql = 'select * FROM AXG0203.PACD623V_PECA_RECA'
#conn = ibm_db_dbi.Connection(conn)
df = pd.read_sql(sql, conn)
df.to_csv('vk623.csv')
