from dataclasses import dataclass

# Classe cliente para armazenar informações do cliente
@dataclass
class Cliente:
    nome: str
    telefone: str

# Classe serviço para armazenar informações sobre o serviço (Nome e preço)
@dataclass
class Servico:
    nome: str
    preco: float

# Classe agendamento para armazenar o agendamento de um cliente
@dataclass
class Agendamento:
    cliente: Cliente
    servico: Servico
    data: str
    hora: str
    status: str #Status de progresso do serviço.

# Lista de clientes cadastrados
clientes = []

# Lista de serviços agendados
agendamentos = []

# Lista de serviços disponíveis
servicos = [
    Servico("formatação", 80),
    Servico("limpeza geral", 50),
    Servico("troca de peças", 0),
    Servico("remoção de vírus", 60),
    Servico("instalação de programas", 40)
]

# Dicionário de técnicos (nome do técnico e serviços prestados)
tecnicos = {
    "Carlos": ["formatação", "limpeza", "remoção de vírus"],
    "Ana": ["troca de peças", "formatação"],
    "João": ["instalação de programas", "limpeza", "troca de peças"]
}

# Função para cadastrar um novo cliente
def cadastrar_cliente():
    nome = input("Digite seu nome: ")
    telefone = input("Digite seu telefone: ")

    for c in clientes:
        if c.telefone == telefone:
            print("Você já está cadastrado.")
            return c

    # Caso o cliente não esteja cadastrado, crie um cadastro
    novo_cliente = Cliente(nome, telefone)
    clientes.append(novo_cliente)
    print(f"Cliente {nome} cadastro realizado com sucesso!")
    return novo_cliente

# Função de buscar cliente
def buscar_cliente():
    telefone = input("Digite o telefone do cliente: ")
    for c in clientes:
        if c.telefone == telefone:
            print(f"Cliente encontrado: {c.nome}")
            return c
    print("Cliente não encontrado. Por favor, faça o cadastro.")
    return None

#Função de agendar um serviço
def agendar_servico():
    print("Vamos começar o agendamento do serviço.")
    cliente = buscar_cliente()
    if cliente is None:
        print("Cliente não encontrado, vamos realizar o cadastro.")
        cliente = cadastrar_cliente()

    print("Serviços disponíveis:")
    for s in servicos:
        print(f"- {s.nome} (R${s.preco})")

    servico_nome = input("Digite o nome do serviço que deseja agendar: ")


    servico_escolhido = None
    for s in servicos:
        if s.nome.lower() == servico_nome.lower():
            servico_escolhido = s
            break
    
    if servico_escolhido is None:
        print("Serviço não encontrado. Verifique o nome digitado.")
        return

    # Escolher data e hora
    data = input("Digite a data do agendamento (DD/MM/AAAA): ")
    hora = input("Digite a hora do agendamento (HH:MM): ")

    # Verificar se o horario está ocupado
    for ag in agendamentos:
        if ag.data == data and ag.hora == hora:
            print("Já existe um serviço agendado nesse horário. Tente outro horário.")
            return

    # Criar o agendamento
    novo_agendamento = Agendamento(
        cliente=cliente,
        servico=servico_escolhido,
        data=data,
        hora=hora,
        status="Pendente"
    )

    agendamentos.append(novo_agendamento)

    # Adicionar na lista de agendamentos

    print(f"\n Agendamento realizado com sucesso para {cliente.nome}!")
    print(f" Serviço: {servico_escolhido.nome} - R${servico_escolhido.preco}")
    print(f" Data: {data} às {hora}")
