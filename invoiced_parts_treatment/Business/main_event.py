from invoiced_parts_treatment.DAO import arpw_dao
from datetime import datetime
from invoiced_parts_treatment.DAO import wings_dao
from invoiced_parts_treatment.Bean_TO.file_register import File_register


def processa():
    start_checkpoint = datetime.now()
    print('start main_event.py at', start_checkpoint)
    checkpoint = start_checkpoint

    arq_eb1 = open('../reemviar_prev.txt', 'r')
    arq_ab1 = open('reemviar_after.txt', 'w')

#    arpw_connection = arpw.connect_oracle()

    new_checkpoint = datetime.now()
    print('time to initialize', new_checkpoint - checkpoint)
    checkpoint = new_checkpoint

    for reg in arq_eb1:
        row = File_register(reg)
        if row.row_p1 == '*DETAIL *':
            try:
                qtd_ord = get_qtd_ord_from_ARPW(row.pedido, row.seq)
                if row.qtd_ord != qtd_ord:
                    print('qtd is different, order={}, partnumber={}, qtdFOC={}, qtdPW{}'.format(row.pedido, row.peca_ord,
                                                                                                 row.qtd_ord, qtd_ord))
                    if qtd_ord != '0000000':
                        row.qtd_ord = qtd_ord
            except:
                print('error on get_qtd_ord_from_ARPW, order={}, partnumber={}'.format(row.pedido, row.peca_ord))

            try:
                peca_desp = get_disp_part_from_WINGS(row.pedido, row.seq)
                if row.peca_desp != peca_desp:
                    print('dispatched part is different, order={}, seq={}, FOCpartnumber={}, WINGSpartnumber={}'.format(
                        row.pedido, row.seq, row.peca_desp, peca_desp))
                    if peca_desp.strip() != '':
                        row.peca_desp = peca_desp
            except:
                print('error on get_disp_part_from_WINGS, order={}, partnumber={}, seq={}'.format(row.pedido, row.peca_desp,
                                                                                                  row.seq))

            try:
                peca_ord = get_ord_part_from_WINGS(row.pedido, row.peca_desp)

                if row.peca_ord != peca_ord:
                    print('ordered part is different, order={}, seq={}, FOCpartnumber={}, WINGSpartnumber={}'.format(
                        row.pedido, row.seq, row.peca_ord, peca_ord))
                    row.peca_ord = peca_ord
            except:
                print('error on get_ord_part_from_WINGS, order={}, partnumber={}, seq={}'.format(row.pedido, row.peca_desp,
                                                                                                 row.seq))

        write_file(arq_ab1, row)

    new_checkpoint = datetime.now()
    print('time to iterate', new_checkpoint - checkpoint)

    arq_eb1.close()
    arq_ab1.close()

    new_checkpoint = datetime.now()
    print('finished main_event.py at {}, duration{}'.format(new_checkpoint, new_checkpoint - start_checkpoint))


def write_file(arq_ab1, row):

    ab1 = (row.row_p1 +
           row.pedido +
           row.row_p2 +
           row.peca_ord +
           row.peca_desp +
           row.qtd_ord +
           row.qtd_desp +
           row.seq +
           row.dom +
           row.row_p5
           )
    arq_ab1.write(ab1)


def get_qtd_ord_from_ARPW(pedido, seq):
    qtd_ord = arpw_dao.get_qtd_ord_from_ARPW(pedido, int(seq))
    return qtd_ord


def get_disp_part_from_WINGS(pedido, seq):
    disp_part = wings_dao.get_disp_part(pedido, seq)
    return disp_part


def get_ord_part_from_WINGS(pedido, peca_desp):
    ord_part = wings_dao.get_ord_part(pedido, peca_desp)
    return ord_part

if __name__ == '__main__':
    processa()