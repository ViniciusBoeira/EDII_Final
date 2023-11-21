expressao = input()
operadores = ['+', '-', '/', '*']
class Node:
    def __init__(self, esquerda=None, direita=None, valor=None):
        self.esquerda = esquerda
        self.direita = direita
        self.valor = valor

    def definir_esquerda(self, valor):
        self.esquerda = valor

    def definir_direita(self, valor):
        self.direita = valor

    def definir_valor(self, valor):
        self.valor = valor

class Operadores:
    def __init__(self, valor=None, parenteses=None, posicao = None):
        self.valor = valor
        self.parenteses = parenteses
        self.posicao = posicao

    def definir_valor(self, valor):
        self.valor = valor
    def definir_parenteses(self, valor):
        self.parenteses = valor
    def definir_posicao(self, valor):
        self.posicao = valor        
# ENCOTRANDO A RAIZ DA ARVORE:
opPresentes = []
for i in range (len(expressao)):
    if expressao[i] in operadores:
        substring = expressao[0:i]
        operador = Operadores(valor = expressao[i], parenteses = substring.count('(') - substring.count(')'), posicao = i)
        opPresentes.append(operador)
raiz = None
for operador in opPresentes:
    if raiz == None:
        raiz = operador
    if (operador.valor == '*' or operador.valor == '/') and raiz.parenteses > operador.parenteses:
        raiz = operador
    if (operador.valor == '+' or operador.valor == '-') and (raiz.parenteses >= operador.parenteses):
        raiz = operador
print(raiz.valor)   
    