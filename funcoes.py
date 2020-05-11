from menu import interfacemenu

def menu(op):


    if op == 'Listar':
        listar()
    if op == 'Inserir':
        inserir()
    if op == 'Atualizar':
        atualizar()
    if op == 'Deletar':
        deletar()
    if op == 'Venda':
        venda()


from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from bson import errors as beeros
import PySimpleGUI as sg

def conectar():
    conn=MongoClient('localhost',27017) #aqui se faz a conexão com o banco de dados em questão
    return conn

def desconectar(conn):
    if conn:
        conn.close()


def listar():
    from tabulate import tabulate
    import PySimpleGUI as sg
    conn=conectar()
    db=conn.dbProdutos #dbProdutos -> banco de dados
    table=[]
    sg.theme("Reddit")
    try:
        if db.produtos.count_documents({})>0: #ve se tem pelo menos de 1 documento no banco de dados
            produtos=db.produtos.find()
            for produto in produtos:
                id=(f"{produto['_id']}")
                nome=(f"{produto['nome']}")
                preco=(f"{produto['preco']} R$")
                estoque=(f"{produto['estoque']}")
                table.append([id, nome, preco, estoque])

            sg.Print(
                tabulate(headers=["ID", "Nome", "Preco", "Estoque"], tablefmt="presto", tabular_data=table),
                keep_on_top=True)
        else:
            sg.popup("Não há produtos cadastrados",keep_on_top=True)
    except errors.PyMongoError as e:
        sg.popup(f'Erro ao acessar o bando de dados: {e}',keep_on_top=True)
    desconectar(conn)

def inserir():

    sg.theme("Reddit")
    layout=[[sg.Text("Digite o nome do produto: "),sg.InputText()],
            [sg.Text("Digite o preco do produto: "),sg.InputText()],
            [sg.Text("Digite o estoque do produto: "),sg.InputText()],
            [sg.Ok(),sg.Cancel()]]
    window=sg.Window("Inserir produto",layout,use_ttk_buttons=True,keep_on_top=True)
    while True:
        event,values=window.read()
        if event in (None, 'Cancel'):
            break
        inserir2(values[0],values[1],values[2])
        if event in (None, 'Ok'):
            break
        break
    window.Close()


def inserir2(nome,preco,estoque):
    conn = conectar()
    db = conn.dbProdutos

    try:
        db.produtos.insert_one(
            {
                "nome": str(nome),
                "preco": float(preco),
                "estoque": int(estoque)
            }
        )
        sg.popup(f'O produto {nome} foi inserido com sucesso.',keep_on_top=True)
    except errors.PyMongoError as e:
        sg.popup(f'Erro ao inserir o produto {nome} : {e} ',keep_on_top=True)
    desconectar(conn)

def atualizar():
    conn = conectar()
    db = conn.dbProdutos
    sg.theme("Reddit")
    layout = [[sg.Text("Digite o Id do produto a ser atualizado: "), sg.InputText()],
        [sg.Text("Digite o novo nome do produto: "), sg.InputText()],
              [sg.Text("Digite o novo preco do produto: "), sg.InputText()],
              [sg.Text("Digite o novo estoque do produto: "), sg.InputText()],
              [sg.Ok(), sg.Cancel()]]
    window = sg.Window("Inserir produto", layout, use_ttk_buttons=True, keep_on_top=True)
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        atualizar2(values[0], values[1], values[2],values[3])
        if event in (None, 'Ok'):
            break
        break
    window.Close()

def atualizar2(*args):
    _id=args[0];nome=args[1];preco=args[2];estoque=args[3]
    conn = conectar()
    db = conn.dbProdutos

    sg.theme("reddit")

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "nome": nome,
                        "preco": preco,
                        "estoque": estoque
                    }
                }
            )
            if res.modified_count == 1:
                sg.popup(f'O produto {nome} foi atualizado com sucesso.',keep_on_top=True)
            else:
                sg.popup('Não foi possível atualizar o produto.',keep_on_top=True)
        else:
            sg.popup('Não existem documentos para serem atualizados.',keep_on_top=True)
    except errors.PyMongoError as e:
        sg.popup(f'Erro ao acessar o banco de dados: {e}',keep_on_top=True)
    except beeros.InvalidId as f:
        sg.popup(f'ObjectID inválido. {f}',keep_on_top=True)
    desconectar(conn)

def deletar():
    layout=[[sg.Text("Id do produto que será deletado: "),sg.InputText()],
            [sg.Ok(),sg.Cancel()]]
    window=sg.Window("Deletando produto",layout,keep_on_top=True)
    while True:
        event,values=window.read()
        if event=='Cancel':
            break
        deletar2(values[0])
        break
    window.close()

def deletar2(_id):
    conn = conectar()
    db = conn.dbProdutos
    sg.theme("reddit")


    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.delete_one(
                {
                    "_id": ObjectId(_id)
                }
            )
            if res.deleted_count > 0:
                sg.Popup('Produto deletado com sucesso.',keep_on_top=True)
            else:
                sg.Popup('Não foi possível deletar o produto.',keep_on_top=True)
        else:
            sg.Popup('Não existem produtos para serem deletados.',keep_on_top=True)
    except errors.PyMongoError as e:
        sg.Popup(f'Erro ao acessar o banco de dados: {e}',keep_on_top=True)
    except beeros.InvalidId as f:
        sg.Popup(f'ObjectID inválido. {f}',keep_on_top=True)
    desconectar(conn)

def venda():
    layout = [[sg.Text("Id do produto que foi vendido: "), sg.InputText()],
              [sg.Ok(), sg.Cancel()]]
    window = sg.Window("Venda do produto", layout, keep_on_top=True)
    while True:
        event, values = window.read()
        if event == 'Cancel':
            break
        venda2(values[0])
        break
    window.close()

def venda2(_id):
    conn = conectar()
    db = conn.dbProdutos


    sg.theme("reddit")

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.update_one({'_id' : ObjectId(_id) }, {'$inc': {'estoque': -1}})
            ps=(db.produtos.find({'_id' : ObjectId(_id)}))
            nome=f"{ps[0]['nome']}"
            if ps[0]['estoque']==0:
                sg.popup(f'O estoque do produto {nome} acabou, deletando...',keep_on_top=True)
                deletar2(_id)

            if res.modified_count == 1:
                sg.popup(f'O produto {nome} foi atualizado com sucesso.',keep_on_top=True)
            else:
                sg.popup('Não foi possível atualizar o produto.',keep_on_top=True)
        else:
            sg.popup('Não existem documentos para serem atualizados.',keep_on_top=True)
    except errors.PyMongoError as e:
        sg.popup(f'Erro ao acessar o banco de dados: {e}',keep_on_top=True)
    except beeros.InvalidId as f:
        sg.popup(f'ObjectID inválido. {f}',keep_on_top=True)
    desconectar(conn)
