class Node:
    def __init__(self, esquerda=None, direita=None, valor=None, posicao=None):
        self.esquerda = esquerda
        self.direita = direita
        self.valor = valor
        self.posicao = posicao

    def definir_esquerda(self, valor):
        self.esquerda = valor

    def definir_direita(self, valor):
        self.direita = valor

    def definir_valor(self, valor):
        self.valor = valor

    def definir_posicao(self, valor):
        self.posicao = valor

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
def defineRoot(expressao):
    opPresentes = []
    for i in range (len(expressao)):
        if expressao[i] in operadores:
            substring = expressao[0:i]
            operador = Operadores(valor = expressao[i], parenteses = substring.count('(') - substring.count(')'), posicao = i)
            opPresentes.append(operador)

    raizOperador = None
    for operador in opPresentes:
        if raizOperador == None:
            raizOperador = operador
        if (operador.valor == '*' or operador.valor == '/') and raizOperador.parenteses > operador.parenteses:
            raizOperador = operador
        if (operador.valor == '+' or operador.valor == '-'):
            if (raizOperador.valor == '-' or raizOperador.valor == '+'):
                if(raizOperador.parenteses > operador.parenteses):
                    raizOperador = operador
            if (raizOperador.valor == '*' or raizOperador.valor == '/'):
                if(raizOperador.parenteses >= operador.parenteses):
                    raizOperador = operador

    raiz = Node(valor=raizOperador.valor, posicao=raizOperador.posicao)
    #print(raiz.valor)

    raiz.definir_esquerda(defineSubRoot(expressao[0:raiz.posicao]))
    raiz.definir_direita(defineSubRoot(expressao[raiz.posicao+1:]))
    return raiz

def defineSubRoot(expressao):
    opPresentes = []
    for i in range (len(expressao)):
        if expressao[i] in operadores:
            substring = expressao[0:i]
            substringDireita = expressao[i+1:]
            operador = Operadores(valor = expressao[i], parenteses = substring.count('(') - substring.count(')'), posicao = i)
            opPresentes.append(operador)
    raizOperador = None
    nodo = None
    if(len(opPresentes) == 0):
        if(expressao[0] == '(' or expressao[0] == ')'):
            expressao = expressao.replace('(', '').replace(')', '') 
            return expressao[0:]
        else:
            expressao = expressao.replace('(', '').replace(')', '')
            return expressao[0:]
    else:    
        for operador in opPresentes:
            if raizOperador == None:
                raizOperador = operador
            if (operador.valor == '*' or operador.valor == '/') and raizOperador.parenteses > operador.parenteses:
                raizOperador = operador
            if (operador.valor == '+' or operador.valor == '-'):
                if (raizOperador.valor == '-' or raizOperador.valor == '+'):
                    if(raizOperador.parenteses > operador.parenteses):
                        raizOperador = operador
                if (raizOperador.valor == '*' or raizOperador.valor == '/'):
                    if(raizOperador.parenteses >= operador.parenteses):
                        raizOperador = operador
    #print (raizOperador.valor)
    nodo = Node(valor=raizOperador.valor, posicao=raizOperador.posicao)
    nodo.definir_esquerda(defineSubRoot(substring))
    nodo.definir_direita(defineSubRoot(substringDireita))

    return nodo

def calcular(node):
    if isinstance(node, Node):
        if node.valor in ['+', '-', '*', '/']:
            esquerda = calcular(node.esquerda)
            direita = calcular(node.direita)
            if node.valor == '+':
                return esquerda + direita
            elif node.valor == '-':
                return esquerda - direita
            elif node.valor == '*':
                return esquerda * direita
            elif node.valor == '/':
                if direita != 0:
                    return esquerda / direita
                else:
                    print("Erro: divisão por zero!")
                    return 0
    else:
        return float(node)

expressao = input()
if(expressao.count('(') != expressao.count(')')):
    print("Erro: parênteses desbalanceados")
else:
    operadores = ['+', '-', '/', '*']
    calcularExpressao = defineRoot(expressao)
    print(calcular(calcularExpressao))