from unittest import TestCase
from invoiced_parts_treatment.Business.partnumber import Peca


class Test_partnumber(TestCase):

    def test_troca_pbs_para_bps(self):
        pn = ' CN15/    5484/AA/   '
        expected_partnumber = '     5484/CN15/AA/   '
        self.assertEqual(expected_partnumber, Peca.troca_pbs_para_bps(pn))

    def test_troca_bps_para_pbs(self):
        pn = '     5484/CN15/AA/   '
        expected_partnumber = ' CN15/    5484/AA/   '
        self.assertEqual(expected_partnumber, Peca.troca_bps_para_pbs(pn))

    def test_troca_pbs_para_ows(self):
        pn = ' CN15/    5484/AA/   '
        expected_partnumber = 'CN155484AA'
        self.assertEqual(expected_partnumber, Peca.troca_pbs_para_ows(pn))



