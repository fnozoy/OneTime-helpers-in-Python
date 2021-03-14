
class Peca:
    def __init__(self):
        pass

    def troca_pbs_para_bps(peca):
        prefixo = peca[1: 6: 1]
        base = peca[6: 15: 1]
        sufixo = peca[15: 24: 1]
        return ' ' + base + prefixo + sufixo

    def troca_bps_para_pbs(peca):
        base = peca[1: 10: 1]
        prefixo = peca[10: 15: 1]
        sufixo = peca[15: 24: 1]
        return ' ' + prefixo + base + sufixo

    def troca_pbs_para_ows(peca):
        prefixo = peca[1: 6: 1].strip().replace("/", "")
        base = peca[6: 15: 1].strip().replace("/", "")
        sufixo = peca[15: 24: 1].strip().replace("/", "")
        return prefixo + base + sufixo
