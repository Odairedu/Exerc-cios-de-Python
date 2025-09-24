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

def listar_agendamentos():
    if not agendamentos:
        print("Nenhum agendamento cadastrado.")
        return
    
    print("\n--- Lista de Agendamentos ---")
    for ag in agendamentos:
        print(f"Cliente: {ag.cliente.nome} - Telefone: {ag.cliente.telefone}")
        print(f"Serviço: {ag.servico.nome} - R${ag.servico.preco}")
        print(f"Data: {ag.data} às {ag.hora}")
        print(f"Status: {ag.status}")
        print("-" * 30)

# Criando o menu
def menu():
    print("\n=== Sistema de agendamento ===")
    print("1 - Cadastrar cliente")
    print("2 - Agendar serviço")
    print("3 - Listar agendamentos")
    print("4 - Ver meus agendamentos")
    print("5 - Atualizar status do agendamento")
    print("6 - Sair")
    escolha = input("Escolha uma opção: ")
    return escolha

def listar_agendamentos_cliente():
    telefone = input("Digite seu telefone para consultar seus agendamentos: ")

    # Buscar cliente pelo telefone
    cliente = None
    for c in clientes:
        if c.telefone == telefone:
            cliente = c
            break

    if cliente is None:
        print("Cliente não encontrado.")
        return

    # Buscar agendamentos do cliente
    agendamentos_cliente = [ag for ag in agendamentos if ag.cliente == cliente]


    if not agendamentos_cliente:
        print("Nenhum agendamento encontrado para este cliente.")
        return

    print(f"\n--- Agendamentos de {cliente.nome} ---")
    for ag in agendamentos_cliente:
        print(f"- Serviço: {ag.servico.nome}")
        print(f"  Data: {ag.data} às {ag.hora}")
        print(f"  Status: {ag.status}")
        print("-" * 20)

# Função para atualizar o status do agendamento
def atualizar_status_agendamento():
    print("\n--- Atualizar status do agendamento ---")
    telefone = input("Digite o telefone do cliente: ")

    cliente = None
    for c in clientes:
        if c.telefone == telefone:
            cliente = c
            break

    if clientes is None:
        print("Cliente não encontrado.")
        return

# Listar agendamentos do cliente
    agendamentos_cliente = [ag for ag in agendamentos if ag.cliente == cliente]

    if not agendamentos_cliente:
        print("Nenhum agendamento encontrado para este cliente.")
        return

    print(f"\nAgendamentos de {cliente.nome}:")
    for i, ag in enumerate(agendamentos_cliente):
        print(f"{i + 1 }. {ag.servico.nome} em {ag.data} às {ag.hora} - status: {ag.status}")

    escolha = int(input("Digite o número do agendamento que deseja atualizar: ")) - 1

    if not escolha.isdigit() or int(escolha) <1 or int(escolha) > len(agendamentos_cliente):
        print("Escolha inválida.")
        return

    agendamento_escolhido = agendamentos_cliente[int(escolha) - 1]

    print("\nEscolha o novo status:")
    status_opcoes = [
        "Em análise",
        "Aguardando orçamento",
        "Aguardando peça",
        "Em manutenção",
        "Testando",
        "Pronto para retirar",
    ]

    for i, status in enumerate(status_opcoes, 1):
        print(f"{i} - {status}")

    novo_status = input("Digite o número correspondente ao novo status:")

    if not novo_status.isdigit() or int(novo_status) < 1 or int(novo_status) > len(status_opcoes):
        print("Opção inválida de status.")
        return

    agendamento_escolhido.status = status_opcoes[int(novo_status) - 1]
    print("Status atualizado com sucesso!")        

def main():
    while True:
        escolha = menu()

        if escolha == "1":
            cadastrar_cliente()
        elif escolha == "2":
            agendar_servico()
        elif escolha == "3":
            listar_agendamentos()
        elif escolha == "4":
            listar_agendamentos_cliente()
        elif escolha == "5":
            atualizar_status_agendamento()
        elif escolha == "6":
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
        
