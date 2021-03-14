import pandas as pd
from invoiced_parts_treatment.DAO.Connect import conn_sqlserver_wings as wings
from invoiced_parts_treatment.Business.partnumber import Peca

wings_connection = wings.connect_sqlserver()

def get_disp_part(pedido, seq):

    seq = int(seq)
    if seq >= 100:
        seq /= 100
    sql = query_disp_part(pedido, int(seq))
    df = pd.read_sql(sql, con=wings_connection)
    disp_part = ''
    for index, row in df.iterrows():
        disp_part = Peca.troca_bps_para_pbs(row['supplied_popims_part'])
        break
    if df.empty:
        disp_part = ''
    return disp_part.ljust(21)



    disp_part = ''
    return disp_part.ljust(21)

def query_disp_part(pedido, seq):

    sql = '''
                select 
                   supplied_popims_part
            
                from (
                       SELECT c.WIN080_BK_CUSTOMER_C CUSTOMER ,
                       w.WIN350_ORDER_CONTROL_D WINGSO_ORDER_NBR,
                       w.WIN350_POPIMS_ORDER_R POPIMS_ORDER_NBR,
                       I.WIN351_BK_SEQ_ITEM_R SEQUENCE_ITEM,
                       I.WIN351_PRICE_ORIGINAL_A UNIT_PRICE_BY_PHYSICAL_UNITS,
                       id.WIN352_PART_Q SUPPLIED_QTY_IN_PHYSICAL_UNITS,
                       (
                             select st.WIN014_BK_STATUS_R
                       from
                             bzwingsprd.dbo.MWIN014_STATUS st
                       where
                             st.WIN014_STATUS_UID_K = id.WIN352_WIN014_STATUS_UID_D) STATUS_TYPE,
                       (
                             select st.WIN014_STATUS_N
                       from
                             bzwingsprd.dbo.MWIN014_STATUS st
                       where
                             st.WIN014_STATUS_UID_K = id.WIN352_WIN014_STATUS_UID_D) STATUS_TYPE_NAME,
                       CASE
                       WHEN id.WIN352_BILL_OF_LANDING_Y IS NOT NULL THEN id.WIN352_BILL_OF_LANDING_Y
                                                                    ELSE id.WIN352_INVOICE_Y
                       END dispatch_date,              
                       P1.WIN100_POPIMS_ARG_BRA_C supplied_popims_part,
                       ltrim(rtrim(p1.WIN100_BK_GSPN_BASE_C)) AS NEW_BASE,
                       ltrim(rtrim(p1.WIN100_BK_GSPN_PREFIX_C)) AS NEW_PREFIX,
                       ltrim(rtrim(p1.WIN100_BK_GSPN_SUFFIX_C)) AS NEW_SUFIX,
                       CONCAT(LTRIM(SUBSTRING(P1.WIN100_POPIMS_ARG_BRA_C, 11, 4)),
                              LTRIM(SUBSTRING(P1.WIN100_POPIMS_ARG_BRA_C, 1, 9)) ,
                              CONCAT(LTRIM(SUBSTRING(P1.WIN100_POPIMS_ARG_BRA_C, 16, 2)),LTRIM(SUBSTRING(P1.WIN100_POPIMS_ARG_BRA_C, 19, 4)))) AS NEW_OWS_PARTNUMBER
                    FROM
                           bzwingsprd.dbo.MWIN350_WORK_ORDERS w
                    left join bzwingsprd.dbo.MWIN080_CUSTOMERS c on
                           c.WIN080_CUSTOMER_UID_K = w.wIN350_WIN080_CUSTOMER_UID_D
                    left join bzwingsprd.dbo.MWIN300_OUTBOUND_ORDER_TYPE ORD on
                           ORD.WIN300_OUTBOUND_ORDER_TYPE_UID_K = W.WIN350_WIN300_OUTBOUND_ORDER_TYPE_UID_D
                    left join bzwingsprd.dbo.MWIN351_WORK_ORDERS_ITEMS I on
                           I.WIN351_WIN350_BK_WORK_ORDER_UID_D = W.WIN350_BK_WORK_ORDER_UID_K
                    left join bzwingsprd.dbo.MWIN352_WORK_ORDER_ITEMS_DETAILS id on
                           id.WIN352_WIN351_BK_WORK_ORDER_ITEM_UID_D = i.WIN351_WORK_ORDER_ITEM_UID_K
                    left join bzwingsprd.dbo.MWIN101_PARTS_X_SUB_DIVISION sub on sub.WIN101_PART_SUB_DIVISION_UID_K = i.WIN351_WIN101_PART_SUB_DIVISION_UID_D
                    left join bzwingsprd.dbo.MWIN101_PARTS_X_SUB_DIVISION sub1 on sub1.WIN101_PART_SUB_DIVISION_UID_K = id.WIN352_WIN101_PART_SUB_DIVISION_UID_D
                    left join bzwingsprd.dbo.MWIN100_PARTS p on p.WIN100_PART_UID_K = sub.WIN101_WIN100_BK_PART_UID_D
                    left join bzwingsprd.dbo.MWIN100_PARTS p1 on p1.WIN100_PART_UID_K = sub1.WIN101_WIN100_BK_PART_UID_D
                    where
                           w.WIN350_WIN005_SUB_DIVISION_UID_D IN (1)
                           AND W.WIN350_WORK_ORDER_S >= '2019-07-01 00:00:00'
                           and ORD.WIN300_BK_ORDER_TYPE_R in (07,  17)           
                           ) as my_view
                where 
                    STATUS_TYPE in (70, 60, 90, 95, 99) --or null e se null considerar como 70
                and popims_order_nbr in ( '{}')
                and SEQUENCE_ITEM = {}
        '''.format(pedido, seq)
    return sql


def get_ord_part(pedido, peca_desp):
    peca_desp_bpf = Peca.troca_pbs_para_bps(peca_desp)
    sql = query_ord_part(pedido, peca_desp_bpf.rstrip())
    df = pd.read_sql(sql, con=wings_connection)
    ord_part = ''
    for index, row in df.iterrows():
        ord_part = Peca.troca_bps_para_pbs(row['ordered_popims_part'])
        break
    if df.empty:
        ord_part = peca_desp
    return ord_part.ljust(21)

def query_ord_part(pedido, peca_desp):
    sql = list()
    sql.append(' SELECT P.WIN100_POPIMS_ARG_BRA_C ordered_popims_part,')
    sql.append('        P1.WIN100_POPIMS_ARG_BRA_C dispatched_popims_part')
    sql.append(' from MWIN352_WORK_ORDER_ITEMS_DETAILS ordidetails')
    sql.append(
        ' inner join MWIN351_WORK_ORDERS_ITEMS orditems  on ordidetails.WIN352_WIN351_BK_WORK_ORDER_ITEM_UID_D = orditems.WIN351_WORK_ORDER_ITEM_UID_K')
    sql.append(
        ' inner join MWIN350_WORK_ORDERS ord on ord.WIN350_BK_WORK_ORDER_UID_K = orditems.WIN351_WIN350_BK_WORK_ORDER_UID_D')
    sql.append(' inner join MWIN014_STATUS stat on stat.WIN014_STATUS_UID_K = ordidetails.WIN352_WIN014_STATUS_UID_D')
    sql.append(
        ' inner join MWIN101_PARTS_X_SUB_DIVISION pxsd on orditems.WIN351_WIN101_PART_SUB_DIVISION_UID_D = pxsd.WIN101_PART_SUB_DIVISION_UID_K')
    sql.append(' inner join MWIN100_PARTS P on pxsd.WIN101_WIN100_BK_PART_UID_D = P.WIN100_PART_UID_K')
    sql.append(
        ' inner join MWIN101_PARTS_X_SUB_DIVISION pxsd1 on ordidetails.WIN352_WIN101_PART_SUB_DIVISION_UID_D = pxsd1.WIN101_PART_SUB_DIVISION_UID_K')
    sql.append(' inner join MWIN100_PARTS P1 on pxsd1.WIN101_WIN100_BK_PART_UID_D = P1.WIN100_PART_UID_K')
    sql.append(' where  ord.WIN350_POPIMS_ORDER_R in (\'{}\') '.format(pedido))
    sql.append(' and    P1.WIN100_POPIMS_ARG_BRA_C = (\'{}\');'.format(peca_desp))
    sql = "".join(sql)
    return sql
