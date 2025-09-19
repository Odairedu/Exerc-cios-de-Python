#Importando módulos para criar classes e datas
from dataclasses import dataclass
from datetime import datetime

#Criando a classe para armazenar usuarios
@dataclass
class Usuario:
    nome: str
    email: str
    senha: str

#Criando a classe de comentarios
@dataclass
class Comentario:
    usuario: str
    texto: str
    data_hora: datetime

#Criando lista para armazenar usuarios
lista = []
    
#Criando a classe para armazenar informações da Publicação
@dataclass
class Publicacao:
    conteudo: str
    descricao: str
    usuario: Usuario
    data_hora: datetime
    curtidas: int = 0
    comentarios: list = None


    def __post_init__(self):
        if self.comentarios is None:
            self.comentarios = []

def comentar_publicacao():
    print("\n=== COMENTAR PUBLICAÇÃO ===")
    if not lista_publicacoes:
        print("Nenhuma publicação disponível.")
        return

    visualizar_feed() #Mostra ao usuário o feed e a opção de comentar

    try:
        indice = int(input("Digite o número da publicação para comentar: ")) - 1
        if 0 <= indice < len(lista_publicacoes):
            nome_usuario = input("Digite seu nome de usuário: ")
            comentario_texto = input("Digite seu comentário: ")
            data = datetime.now()

            #Criando um novo comentário e adicionando na lista de publicação
            novo_comentario = Comentario(nome_usuario, comentario_texto, data)
            lista_publicacoes[indice].comentarios.append(novo_comentario)

            print("Comentário adicionado com sucesso!")
        else:
            print("Publicação não encontrada.")
    except ValueError:
        print("Número inválido.")

#Criando a classe para criar usuário, email e senha  

#Função de criar usuarios e suas informações    
def criar_usuario():
    nome = input("Qual o seu nome: ")
    email = input("Qual o seu email: ")
    senha = input("Qual a sua senha: ")
    usuario_digitado = Usuario(nome,email,senha)
    lista.append(usuario_digitado)
    print("Cadastro realizado com sucesso!")

#Função de fazer login
def fazer_login():
    login_email = input("Qual o seu email: ")
    login_senha = input("Qual a sua senha: ")
    
    for usuario in lista:
        if usuario.email == login_email:
            if usuario.senha == login_senha:
                print("Acesso autorizado")
            else:
                print("Email ou senha incorreto")
        else:
            print("Email ou senha incorreto")

#Variavel lista para guardar publicações
lista_publicacoes = []

#Função de criar uma publicação e informações da publicação
def criar_publicacao():
    print("\n=== CRIAR PUBLICAÇÃO ===")
    conteudo = input("Digite o conteúdo da publicação: ")
    descricao = input("Digite a descrição: ")
    usuario = input("Digite o nome do usuario: ")
    data_hora = datetime.now()

#Append para adicionar publicações ao final da lista
    nova_publicacao = Publicacao(conteudo, descricao, usuario, data_hora)
    lista_publicacoes.append(nova_publicacao)
    print("Publicação criada com sucesso!")

#Função para curtir uma publicação
def curtir_publicacao():
    print("\n=== CURTIR PUBLICAÇÃO ===")
    if not lista_publicacoes:
        print("Nenhuma publicação disponível.")
        return
#Visualizar feed e curtir publicações
    visualizar_feed()
    try:
        indice = int(input("Digite o número da publicação para curtir: ")) - 1
        if 0 <= indice < len(lista_publicacoes):
            lista_publicacoes[indice].curtidas += 1
            print("Publicação curtida!")
        else:
            print("Publicação não encontrada.")
    except ValueError:
        print("Número inválido.")

#Visualizar feed e ver informações das publicações
def visualizar_feed():
    print("\n=== FEED ===")
    if not lista_publicacoes:
        print("Nenhuma publicação disponível.")
        return
    
    for i, pub in enumerate(lista_publicacoes, 1):
        print(f"{i}. {pub.usuario} - {pub.curtidas} curtidas")
        print(f"   {pub.conteudo[:50]}...")
        print(f"   {pub.data_hora.strftime('%d/%m/%Y %H:%M')}")
        print("-" * 40)
 
 #Visualizar e buscar por publicações individuais   
def visualizar_publicacao_individual():
    print("\n=== VISUALIZAR PUBLICAÇÃO ===")
    if not lista_publicacoes:
        print("Nenhuma publicação disponível.")
        return
    
    visualizar_feed()
    try:
        indice = int(input("digite o número da publicação: ")) - 1
        if 0 <= indice < len(lista_publicacoes):
            pub = lista_publicacoes[indice]
            print(f"\nUsuario: {pub.usuario}")
            print(f"Data: {pub.data_hora.strftime('%d/%m/%Y %H:%M')}")
            print(f"Conteúdo: {pub.conteudo}")
            print(f"Descrição: {pub.descricao}")
            print(f"Curtidas: {pub.curtidas}")
        else:
            print("Publicação não encontrada.")
    except ValueError:
        print("Número inválido.")

#Visualizar e buscar por publicações pelo Autor do post
def visualizar_publicacoes_por_usuario():
    print("\n=== PUBLICAÇÕES POR USUARIO ===")
    if not lista_publicacoes:
        print("Nenhuma publicação disponível.")
        return

    usuario = input("Digite o nome do usuario: ")
    publicacoes_usuario = [pub for pub in lista_publicacoes if pub.usuario.lower() == usuario.lower()]

    if not publicacoes_usuario:
        print(f"Nenhuma publição encontrada para {usuario}.")
        return

    print(f"\nPublicações de {usuario}:")
    for pub in publicacoes_usuario:
        print(f"- {pub.conteudo[:50]}... ({pub.curtidas} curtidas)")
        print(f"  {pub.data_hora.strftime('%d/%m/%Y %H:%M')}")
        print("-" * 30)

#Criando o Menu de interação da rede social
def menu():
    while True:
        print("\n=== REDE SOCIAL ===")
        print("1. Criar conta")
        print("2. Fazer login")
        print("3. Criar Publicação")
        print("4. Curtir Publicação")
        print("5. Visualizar Feed")
        print("6. Visualizar Publicação Individual")
        print("7. Visualizar Publicações por Usuario")
        print("8. Comentar Publicação")
        print("0. Sair")
    
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            fazer_login()
        elif opcao == "3":
            criar_publicacao()
        elif opcao == "4":
            curtir_publicacao()
        elif opcao == "5":
            visualizar_feed()
        elif opcao == "6":
            visualizar_publicacao_individual()
        elif opcao == "7":
            visualizar_publicacoes_por_usuario()
        elif opcao == "8":
            comentar_publicacao()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

menu()
    
    