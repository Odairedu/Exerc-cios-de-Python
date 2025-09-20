from dataclasses import dataclass

#Classes
@dataclass
class Cliente:
    nome: str
    telefone: str

@dataclass
class Agendamento:
    cliente: Cliente
    barbeiro: str
    corte: str
    preco: float
    dia: str
    hora: str

#Dados iniciais
clientes = []
agendamentos = []

barbeiros = {
    "João": ["segunda", "terça", "quarta", "quinta", "sexta", "sábado"],
    "Carlos": ["terça", "quarta", "quinta", "sexta"],
    "Miguel": ["sábado", "domingo"]
}

horarios = [f"{h}:{m:02d}" for h in range(9, 20) for m in (0, 30)]

cortes = {
    "Corte simples": 30,
    "Corte degrade": 40,
    "Corte navalhado": 50,
    "Barba": 25
}

#Menu
def menu(titulo, opcoes):
    print(f"\n--- {titulo} ---")
    for i, opcao in enumerate(opcoes, start=1):
        print(f"{i} - {opcao}")
    print("0 - Voltar")
    return input("Escolha: ")

#Cadastrar cliente
def cadastrar_cliente():
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    for c in clientes:
        if c.telefone == telefone:
            print("Você já está cadastrado!")
            return c
    novo = Cliente(nome, telefone)
    clientes.append(novo)
    print(f"Bem-vindo, {nome}!")
    return novo

#Buscar cliente
def buscar_cliente():
    telefone = input("Digite seu telefone: ")
    for c in clientes:
        if c.telefone == telefone:
            print(f"Bem-vindo de volta, {c.nome}!")
            return c
    print("Você ainda não se cadastrou.")
    return None

#Buscar pelo corte
def agendar_corte(cliente):
    if not cliente:
        print("Cadastre-se primeiro!")
        return
    
    barbeiro = input(f"Escolha o barbeiro {list(barbeiros.keys())}: ")
    if barbeiro not in barbeiros:
        print("Barbeiro inválido!")
        return

    dia = input("Dia da semana: ")
    if dia not in barbeiros[barbeiro]:
        print(f"{barbeiro} não trabalha nesse dia.")
        return

    # horários livres
    ocupados = [a.hora for a in agendamentos if a.barbeiro == barbeiro and a.dia == dia]
    livres = [h for h in horarios if h not in ocupados]
    if not livres:
        print("Sem horários livres neste dia!")
        return
    
    hora = input(f"Escolha um horário {livres}: ")
    if hora not in livres:
        print("Horário inválido!")
        return
    
    corte = input(f"Escolha o corte {list(cortes.keys())}: ")
    if corte not in cortes:
        print("Corte inválido!")
        return

    agendamento = Agendamento(cliente, barbeiro, corte, cortes[corte], dia, hora)
    agendamentos.append(agendamento)
    print(f"Agendamento confirmado para {cliente.nome} com {barbeiro}, {corte}, dia {dia} às {hora}.")

def listar_agendamentos():
    if not agendamentos:
        print("Nenhum agendamento registrado.")
        return
    for a in agendamentos:
        print(f"{a.dia} {a.hora} - {a.cliente.nome} ({a.corte} - R${a.preco}) com {a.barbeiro}")

def calcular_lucro():
    lucro = {b: 0 for b in barbeiros}
    for a in agendamentos:
        lucro[a.barbeiro] += a.preco
    print("\n--- Lucros dos barbeiros ---")
    for b, total in lucro.items():
        print(f"{b}: R${total}")

while True:
    escolha = menu("Barbearia", ["Cliente", "Funcionário"])
    
    if escolha == "1":  # Cliente
        cliente_logado = None
        while True:
            opcao = menu("Área do Cliente", ["Cadastrar", "Agendar Corte"])
            if opcao == "1":
                cliente_logado = cadastrar_cliente()
            elif opcao == "2":
                if not cliente_logado:
                    cliente_logado = buscar_cliente()
                agendar_corte(cliente_logado)
            elif opcao == "0":
                break
    
    elif escolha == "2":  # Funcionário
        while True:
            opcao = menu("Área do Funcionário", ["Ver Agendamentos", "Calcular Lucros"])
            if opcao == "1":
                listar_agendamentos()
            elif opcao == "2":
                calcular_lucro()
            elif opcao == "0":
                break
    
    elif escolha == "0":
        print("Saindo...")
        break

