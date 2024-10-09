from math import log
import sys
from random import randint

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
def Random(assoc:int):
	substituir=randint(0,assoc-1)
	return substituir


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
		self.subs=subs.upper()
		print(self.subs)
		self.tamanho= nsets*bsize*assoc
		self.blocos=nsets*assoc
		self.blocos_ocupados=0
		self.bits_offset = int(log(bsize,2))
		print(self.bits_offset)
		self.bits_indice = int(log(nsets,2))
		print(self.bits_indice)
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
		miss_atual = 1
		tag = endereco >> (self.bits_indice + self.bits_offset)
		
		#print(endereco)
		indice = (endereco >> self.bits_offset) & (2**self.bits_indice -1)
		print('indice: {}'.format(indice))
		if(1 in self.validade[indice]):
			print("aaa")
			for c in range(0,len(self.validade[indice])):
				if(tag==self.tag[indice][c]):
					miss_atual = 0
					global hits
					hits += 1
					print('hit')

			if miss_atual == 1:
				# cache cheia => miss capacidade
				if self.blocos_ocupados == self.blocos:
					global misses_capacidade
					misses_capacidade+=1
					if(self.assoc==1):
						self.validade[indice][0] = 1
						self.tag[indice][0] = tag
					elif self.subs=="R":
						entrada = Random(self.assoc)
						self.validade[indice][entrada] = 1
						self.tag[indice][entrada] = tag
					elif self.subs=="L":
						LRU(self.assoc)
					elif self.subs=="F":
						FIFO(self.assoc)
					

				else:
					global misses_conflito
					misses_conflito+1
					if(self.assoc==1):
						self.validade[indice][0] = 1
						self.tag[indice][0] = tag
					elif self.subs=="R":
						entrada = Random(self.assoc)
						self.validade[indice][entrada] = 1
						self.tag[indice][entrada] = tag
					elif self.subs=="L":
						LRU(self.assoc)
					elif self.subs=="F":
						FIFO(self.assoc)
			
			
		else:
			global misses_compulsorio
			misses_compulsorio+=1
			if(self.assoc==1):
				self.validade[indice][0] = 1
				self.tag[indice][0] = tag
				print("mc")
			elif self.subs=="R":
				entrada = Random(self.assoc)
				self.validade[indice][entrada] = 1
				self.tag[indice][entrada] = tag
			elif self.subs=="L":
				LRU(self.assoc)
			elif self.subs=="F":
				FIFO(self.assoc)




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
	for i in range(0,len(enderecos)):
		global acessos
		acessos += 1
		print(enderecos[i])
		cache.Acessar_Endereco(enderecos[i])
		print('-'*5)
	
	print(acessos, end=" ")
	print('{:.4f}'.format(hits/acessos), end=" ")
	misses = misses_compulsorio+misses_capacidade+misses_capacidade
	print('{:.4f}'.format(misses/acessos), end=" ")
	print(f"{misses_compulsorio/misses:.2f}", end=" ")			
	print(f"{misses_conflito/misses:.2}", end=" ")	
	print('{:.2f}'.format(misses_capacidade/misses), end=" ")						
															 
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




acessos=0
hits=0
misses_compulsorio = 0
misses_conflito=0
misses_capacidade=0

if __name__ == '__main__':
	main()



# python cache_simulator.py 2 2 2 2 1 arquivo_de_entrada
# python cache_simulator.py 32 1 1 R 1 bin_100.bin