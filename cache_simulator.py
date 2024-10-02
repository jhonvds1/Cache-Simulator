from math import log
import sys


def Abrir_arquivo(entrada,lista):
	"""
	Abre os Arquivos e guarda os endereços
	"""
	try:
		with open(entrada, 'rb') as arquivo:
			while True:
				conteudo = arquivo.read(4)  # Lê o conteúdo completo do arquivo
				if(not conteudo):
					break
				else:
					inteiro = int.from_bytes(conteudo, byteorder='big', signed=False)
					lista.append(inteiro)

	except FileNotFoundError:
		print('Arquivo não encontrado!')
	



# Políticas de substituição
def Random():
	pass


def LRU():
	pass


def FIFO():
	pass


def Com_flag():
	pass

def Sem_flag():
	pass





class Cache:
	def __init__(self, nsets, bsize, assoc, subs):
		self.nsets=nsets
		self.bsize=bsize
		self.assoc=assoc
		self.subs=subs
		self.tamanho = nsets*bsize*assoc
		self.bits_offset = int(log(bsize,2))
		self.bits_indice = int(log(nsets,2))
		self.bits_tag = 32 - self.bits_offset - self.bits_indice
		self.validade = self.Gerar_Validade()
		self.tag = self.Gerar_Tag()
	
	def Gerar_Validade(self) -> list[list[int]]:
		"""
		método que gera a estrutura que armazena os bits de validade
		"""
		validade = []
		for l in range(0, self.nsets):
			linha = []
			for c in range(0, self.assoc):
				linha.append(0)
			validade.append(linha)
		return validade

	def Gerar_Tag(self)->list[list[int]]:
		tag=[]
		for l in range(0, self.nsets):
			linha=[]
			for c in range(0, self.assoc):
				linha.append(-1)
			tag.append(linha)
		return tag
	
	def Printf(self, lst: list[list[int]])->None:
		for c in lst:
			print(c)
		print('\n\n\n')


	def Acessar_Endereco(self, endereco:int) -> None:
		tag = endereco >> (self.bits_indice + self.bits_offset)
		#print(endereco)
		indice = (endereco >> self.bits_offset) & (2**self.bits_indice -1)
		if(1 in self.validade[indice]):
			for c in range(0,self.validade[indice]):
				if(tag==self.tag[indice][c]):
					pass #hit++
			#
		else:
			pass #miss++
		


		print(self.bits_indice)
		print(self.bits_offset)
		print(tag)
		print(indice)







def main():
	if (len(sys.argv) != 7):
		print("Numero de argumentos incorreto. Utilize:")
		print("python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
		exit(1)

	# Guarda a flag de saída
	flag = int(sys.argv[5])

	# Lê o arquivo de entrada e guarda os endereços
	arquivoEntrada = sys.argv[6]
	enderecos=[]
	Abrir_arquivo('Enderecos/' + arquivoEntrada, enderecos)
	
	# Cria um objeto cache com os parâmetros da cache
	cache = Cache(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
															#<--------------
	#cache.Printf(cache.validade)                       	        
	#cache.Printf(cache.tag)

	#for end in enderecos:
	cache.Acessar_Endereco(enderecos[0])				
															 
															#<--------------




	#for end in enderecos:
	#	acesarCache(end)
	



	"""
	print("nsets =", nsets)
	print("bsize =", bsize)
	print("assoc =", assoc)
	print("subst =", subst)
	print("flagOut =", flagOut)
	print("arquivo =", arquivoEntrada)
	"""







if __name__ == '__main__':
	main()


# python cache_simulator.py 2 2 2 2 1 arquivo_de_entrada
# python cache_simulator.py 2 2 2 2 1 bin_100.bin