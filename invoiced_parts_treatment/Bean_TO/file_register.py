class File_register:
	def __init__(self, row):
		self.row_p1 = row[0: 9: 1]
		self.pedido = row[9: 16: 1]
		self.row_p2 = row[16: 22: 1]
		self.peca_ord = row[22: 43: 1]
		self.peca_desp = row[43: 64: 1]
		self.qtd_ord = row[64: 71: 1]
		self.qtd_desp = row[71: 78: 1]
		self.seq = row[78: 83: 1]
		self.dom = row[83: 85: 1]
		self.row_p5 = row[85: 90: 1]

