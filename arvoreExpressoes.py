import psycopg2

conexao = psycopg2.connect(
    database="",
    host="",
    user="",
    password="",
    port=""
)

cursor = conexao.cursor()

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
def defineRoot(expressao, id):
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
    raizVar = raiz.valor
    comando = f"INSERT INTO expressoes (id, expressao, raiz) VALUES ({id},'{expressao}', '{raizVar}')"
    cursor.execute(comando)
    conexao.commit()

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
while (True):
    print("Você deseja realizar uma operação, fazer uma consulta ou sair? \n1 - Operação \n2 - Consulta \n3- Sair")
    decisao = int(input())
    if (decisao == 1):
        print("Digite uma expressão: ")
        expressao = input()
        if(expressao.count('(') != expressao.count(')')):
            print("Erro: parênteses desbalanceados")
        else:
            comando_max_id = "SELECT MAX(id) FROM expressoes"
            cursor.execute(comando_max_id)
            maior_id = cursor.fetchone()[0]
            if (maior_id is None): 
                id = 1
            else:
                id = maior_id + 1
            operadores = ['+', '-', '/', '*']
            calcularExpressao = defineRoot(expressao, id)

            resultado = calcular(calcularExpressao)
            print(calcular(calcularExpressao))
            comando = f"update expressoes set resultado = {resultado} where id = {id}"
            cursor.execute(comando)
            conexao.commit()


    elif (decisao == 2):
        print("Você deseja listar todas as operações ou buscar pelo ID? \n1 - Listar todas \n2 - ID")
        decisaoConsulta = int(input())
        if (decisaoConsulta == 1):
            comando = f"select * from expressoes"
            cursor.execute(comando)
            resultados = cursor.fetchall()
            for resultado in resultados:
                id, expressao, resultado_valor, raiz = resultado
                resultado_float = float(resultado_valor)
                print(f"ID: {id}, Expressao: {expressao}, Resultado: {resultado_float}, Raiz: {raiz}")
        else:
            print("Digite o ID da operação que você deseja buscar: ")
            id = int(input())
            comando = f"select * from expressoes where id = {id}"
            cursor.execute(comando)
            resultados = cursor.fetchall()
            for resultado in resultados:
                id, expressao, resultado_valor, raiz = resultado
                resultado_float = float(resultado_valor)
                print(f"ID: {id}, Expressao: {expressao}, Resultado: {resultado_float}, Raiz: {raiz}")
    else:
        break

cursor.close()
conexao.close()