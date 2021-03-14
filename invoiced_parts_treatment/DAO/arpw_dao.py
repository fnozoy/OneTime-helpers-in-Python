import pandas as pd
from invoiced_parts_treatment.DAO.Connect import conn_oracle_arpw as arpw

conn = arpw.connect_oracle()

def get_qtd_ord_from_ARPW(pedido, seq):
    sql = query(pedido, seq)
    df = pd.read_sql(sql, conn)
    qtd_ord = 0
    for index, row in df.iterrows():
        qtd_ord = row['CANT_PED']
        break
    if df.empty:
        qtd_ord = 0
    return '{0:07d}'.format(qtd_ord)

def query(pedido, seq):
    sql = ("""
            SELECT
                pw050_cant_ped as cant_ped
            FROM
                 dbaorapw.tpw040_pedidos_pw
                ,dbaorapw.tpw050_pedidos_det_pw
            where     
                pw050_nro_conc        = pw040_nro_conc
            and pw050_nro_pedido_pw   = pw040_nro_pedido_pw
            and pw040_nro_pedido_po = {}
            and pw050_nro_sec = {}
            and pw050_cant_ped > 0
		 """.format(pedido, seq))  # use triple quotes if you want to spread your query across multiple lines
    return sql

