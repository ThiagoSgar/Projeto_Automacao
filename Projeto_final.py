# SUPER TRABLAHO DE AUTOMAÇÃO
# ALUNOS:
#       Aline Esther Moretto Carbinatto RA: 770103
#       Thiago Corrêa                   RA: 770016

import mysql.connector
import requests
import pip
# pip.main(['install','mysql-connector-python'])
import mysql.connector
from prettytable import from_db_cursor

db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='projeto_final')
cursor = db_connection.cursor()

def addProdutos():

    # inicia a balanca que ira gerar um peso aleatorio
    url = requests.get("http://10.0.0.125:5000/")
    x = url.json()
    count = {}
    peso = x.get('peso')


    #ENCONTRAR O PRODUTO

    produto = input("qual o nome do produto que deseja inserir?")
    print("Quandidade de " + str(produto) + " pesada: " + str(peso))
    encontraProduto = "SELECT id, quantidade_produto FROM silos WHERE produto_armazenado = '{}'".format(produto)
    cursor.execute(encontraProduto)
    imprimeProduto = cursor.fetchall()
    tamanho = len(imprimeProduto)

    #---------------------CASO SEJA ENCONTRADO NENHUM SILO COM O PRODUTO INSERIDO---------------------
    if(tamanho > 0):
        #
        id = imprimeProduto[0][0]
        quantidade = imprimeProduto[0][1] + peso

        #
        resposta = input("Produto já armazenado no silo "+str(id)+", deseja acrescentar a quantidade pesada de: "+str(peso)+" ? (S/N)")
        if resposta == "S":
            atualizaProduto = "UPDATE silos SET quantidade_produto = {} WHERE id= {} ".format(quantidade, id)
            cursor.execute(atualizaProduto)
            db_connection.commit()


        else:
            print("nenhuma alteração foi feita")


    #---------------------CASO NÃO SEJA ENCONTRADO NENHUM SILO COM O PRODUTO INSERIDO---------------------
    elif (tamanho == 0):

        encontraSilosVazios = "SELECT id FROM silos WHERE produto_armazenado = '' "
        cursor.execute(encontraSilosVazios)
        arraySilosVazios = cursor.fetchall()
        tamanhoArray =  len(arraySilosVazios)


        # CASO NÃO SEJA ENCONTRADO NENHUM SILO VAZIO
        if tamanhoArray == 0:
            print("Erro de inserção, nenhum silo esta disponível")

        # CASO ENCONTRE APENAS UM SILO VAZIO
        elif tamanhoArray == 1:
            idSilo = arraySilosVazios[0][0]
            updateProdutoSilo(produto, peso, idSilo)
        # CASO ENCONTRE MAIS DE UM SILO VAZIO
        else:
            print("Os silos disponiveis são: ")
            for i in range(tamanhoArray):
                print ("Silo Nº: "+str(arraySilosVazios[i][0]))

            idSiloEscolhido = input("Insira o numero do silo que deseja adicionar o produto"+ produto+": ")
            updateProdutoSilo(produto, peso, idSiloEscolhido)


    # ---------------------CASO NÃO SEJA ENCONTRADO NENHUM SILO (CASO TODOS ESTEJAM OCUPADOS)---------------------


        # atualizaProduto = "UPDATE silos SET quantidade= {} WHERE id= {} ".format(quantidade)

def updateProdutoSilo(produto, peso, idSilo):
    cadastraProduto = "UPDATE silos SET produto_armazenado = '{}',quantidade_produto = {} WHERE id= {} ".format(produto, peso, idSilo)
    cursor.execute(cadastraProduto)
    db_connection.commit()






def retirarProduto():
    cont = 0
    while (cont == 0):
        codigo_barras = input("insira o codigo de barrras do silo desejado: ")
        select_produto = "SELECT id, produto_armazenado, quantidade_produto FROM silos where codigo_barras = '{}'".format(codigo_barras)
        cursor.execute(select_produto)
        array_produto = cursor.fetchall()
        tamanho = len(array_produto)
    
            #dosador
        if (len(array_produto) > 0):
            quantidade_produto = array_produto[0][2]
            id_silo = array_produto[0][0]
            if(quantidade_produto == 0):
                print("O silo escolhido esta vazio")
                cont == 1
                break
            else:
                quantidade_produto = array_produto[0][2]
                id_silo = array_produto[0][0]
                dosador(quantidade_produto,id_silo)
                cont == 1
                break

        else:
            print("Codigo de Barras não encontrado, favor digitar direito!")
            cont == 0
def dosador(quantidade_produto,id_produto):



    if (quantidade_produto > 5):


        quantidade_retirada = quantidade_produto - 5

        update_produto = "UPDATE silos SET quantidade_produto = {}  WHERE id = {}".format(quantidade_retirada,id_produto)
        cursor.execute(update_produto)
        db_connection.commit()

        print("Foram retirados 5kg do produto, restando " + str(quantidade_retirada) + "kg de produto no silo")

    elif (quantidade_produto == 5):


        produto_armazenado = ''
        update_produto = "UPDATE silos SET produto_armazenado = '{}', quantidade_produto = 0  WHERE id = {}".format(produto_armazenado, id_produto)
        cursor.execute(update_produto)

        db_connection.commit()

        print("Foram retirados 5kg do produto, acabando o estoque do produto no silo")


    if (quantidade_produto < 5):


        quantidade_retirada = quantidade_produto

        produto_armazenado = ''
        update_produto = "UPDATE silos SET produto_armazenado = '{}', quantidade_produto = 0  WHERE id = {}".format(produto_armazenado, id_produto)
        cursor.execute(update_produto)
        db_connection.commit()

        print("Foram retirados " + str(quantidade_retirada) + "kg de produto, acabando o estoque do produto no silo")





def printAll():
    cursor.execute("SELECT * FROM silos")
    mytable = from_db_cursor(cursor)
    print(mytable)





switchCase = 0
while switchCase == 0:
    print("************* Menu *************")
    print("1 -> Adicionar Produto")
    print("2 -> Retirar produto")
    print("3 -> Listagem de Estoque")
    print("4 -> Encerrar\n")

    resposta = (input("Insira o numero correspondente à ação desejada: "))


    if resposta == '1':
        addProdutos()
        switchCase == 0

    if resposta == '2':
        retirarProduto()
        switchCase == 0

    if resposta == '3':
        printAll()
        switchCase == 0

    if resposta == '4':
        print("Tenha um bom dia!!")
        break

    if( resposta != '1' and resposta != '2' and resposta != '3'  and resposta != '4' ):
        print("Comando inválido, favor digitar atentamente")
        switchCase == 0


cursor.close()
db_connection.close()
