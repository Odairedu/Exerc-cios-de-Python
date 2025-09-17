from dataclasses import dataclass

# ========== MENU PRINCIPAL ==========

def menu_cliente():
    while True:
        print("\n--- Menu Cliente ---")
        print("1 - Cadastrar e agendar corte")
        print("2 - Consultar último corte")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_e_agendar_corte()
        elif opcao == "2":
            consultar_ultimo_corte()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_funcionario():
    while True:
        print("\n--- Menu Funcionário ---")
        print("1 - Ver histórico de cortes")
        print("2 - Iniciar atendimento")
        print("3 - Encerrar atendimento")
        print("0 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            ver_historico_barbeiro()
        elif opcao == "2":
            iniciar_atendimento()
        elif opcao == "3":
            encerrar_atendimento()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def sistema():
    while True:
        print("\n=== Bem-vindo à Barbearia ===")
        print("Você é:")
        print("1 - Cliente")
        print("2 - Funcionário")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            menu_cliente()
        elif escolha == "2":
            menu_funcionario()
        elif escolha == "0":
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# ========== CLASSES ==========

@dataclass
class Cliente:
    nome: str
    telefone: str
    historico: list

@dataclass
class Agendamento:
    cliente_telefone: str
    cliente_nome: str
    barbeiro: str
    dia_semana: str
    servico: str
    preco: float
    status: str

# ========== DADOS DO SISTEMA ==========

clientes = []
agendamentos = []

barbeiros = {
    "Barbeiro 1": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
    "Barbeiro 2": ["Terça", "Quarta", "Quinta", "Sexta"],
    "Barbeiro 3": ["Sábado", "Domingo"]
}

servicos = {
    "Corte Simples": 25.0,
    "Corte + Barba": 35.0,
    "Barba Completa": 20.0,
    "Corte Social": 30.0
}

# ========== FUNÇÕES CLIENTE ==========

def cadastrar_e_agendar_corte():
    print("\n--- Agendamento de Corte ---")
    nome = input("Digite seu nome: ")
    telefone = input("Digite seu telefone: ")

    # Verificar cliente existente
    cliente = None
    for c in clientes:
        if c.telefone == telefone:
            cliente = c
            break

    if not cliente:
        cliente = Cliente(nome, telefone, [])
        clientes.append(cliente)
        print("Cliente cadastrado com sucesso!")
    else:
        print("Cliente já cadastrado. Continuando com agendamento...")

    # Escolher barbeiro
    print("\nBarbeiros disponíveis:")
    for idx, barbeiro in enumerate(barbeiros.keys(), 1):
        print(f"{idx} - {barbeiro}")
    escolha_barbeiro = int(input("Escolha o número do barbeiro: "))
    barbeiro_escolhido = list(barbeiros.keys())[escolha_barbeiro - 1]

    # Escolher dia da semana
    dias_disponiveis = barbeiros[barbeiro_escolhido]
    print(f"\nDias disponíveis para {barbeiro_escolhido}:")
    for idx, dia in enumerate(dias_disponiveis, 1):
        print(f"{idx} - {dia}")
    escolha_dia = int(input("Escolha o número do dia: "))
    dia_escolhido = dias_disponiveis[escolha_dia - 1]

    # Escolher serviço
    print("\nServiços disponíveis:")
    for idx, (nome_servico, preco) in enumerate(servicos.items(), 1):
        print(f"{idx} - {nome_servico} (R${preco:.2f})")
    escolha_servico = int(input("Escolha o número do serviço: "))
    nome_servico = list(servicos.keys())[escolha_servico - 1]
    preco_servico = servicos[nome_servico]

    # Calcular posição na fila
    fila = [
        a for a in agendamentos
        if a.barbeiro == barbeiro_escolhido and a.dia_semana == dia_escolhido and a.status == "Agendado"
    ]
    posicao_fila = len(fila) + 1

    # Criar agendamento
    agendamento = Agendamento(
        cliente_telefone=cliente.telefone,
        cliente_nome=cliente.nome,
        barbeiro=barbeiro_escolhido,
        dia_semana=dia_escolhido,
        servico=nome_servico,
        preco=preco_servico,
        status="Agendado"
    )
    agendamentos.append(agendamento)
    cliente.historico.append(agendamento)

    print(f"\nCorte agendado com {barbeiro_escolhido} na {dia_escolhido}.")
    print(f"Você está na posição {posicao_fila} da fila.")

def consultar_ultimo_corte():
    print("\n--- Consultar Último Corte ---")
    telefone = input("Digite seu telefone: ")

    cliente = None
    for c in clientes:
        if c.telefone == telefone:
            cliente = c
            break

    if not cliente or not cliente.historico:
        print("Nenhum corte encontrado para esse número.")
        return

    ultimo = cliente.historico[-1]
    print(f"\nÚltimo corte feito por {ultimo.barbeiro} na {ultimo.dia_semana}")
    print(f"Serviço: {ultimo.servico} - R${ultimo.preco:.2f}")
    print(f"Status: {ultimo.status}")

# ========== FUNÇÕES FUNCIONÁRIO ==========

def iniciar_atendimento():
    print("\n--- Iniciar Atendimento ---")
    barbeiro = input("Digite seu nome (Barbeiro 1, Barbeiro 2 ou Barbeiro 3): ")

    fila = [
        a for a in agendamentos
        if a.barbeiro == barbeiro and a.status == "Agendado"
    ]

    if not fila:
        print("Nenhum cliente aguardando para esse barbeiro.")
        return

    print(f"\nClientes na fila para {barbeiro}:")
    for idx, ag in enumerate(fila, 1):
        print(f"{idx} - {ag.cliente_nome} ({ag.servico}) - Dia: {ag.dia_semana}")

    escolha = int(input("Escolha o número do cliente para iniciar atendimento: "))
    atendimento = fila[escolha - 1]
    atendimento.status = "Em Atendimento"

    print(f"\nAtendimento iniciado com {atendimento.cliente_nome}.")

def encerrar_atendimento():
    print("\n--- Encerrar Atendimento ---")
    barbeiro = input("Digite seu nome (Barbeiro 1, Barbeiro 2 ou Barbeiro 3): ")

    em_atendimento = [
        a for a in agendamentos
        if a.barbeiro == barbeiro and a.status == "Em Atendimento"
    ]

    if not em_atendimento:
        print("Nenhum atendimento em andamento para esse barbeiro.")
        return

    print(f"\nClientes em atendimento com {barbeiro}:")
    for idx, ag in enumerate(em_atendimento, 1):
        print(f"{idx} - {ag.cliente_nome} ({ag.servico}) - Dia: {ag.dia_semana}")

    escolha = int(input("Escolha o número do atendimento para encerrar: "))
    atendimento = em_atendimento[escolha - 1]
    atendimento.status = "Concluído"

    print(f"\nAtendimento encerrado para {atendimento.cliente_nome}.")

def ver_historico_barbeiro():
    print("\n--- Histórico de Cortes ---")
    barbeiro = input("Digite seu nome (Barbeiro 1, Barbeiro 2 ou Barbeiro 3): ")

    historico = [
        a for a in agendamentos
        if a.barbeiro == barbeiro and a.status == "Concluído"
    ]

    if not historico:
        print("Nenhum corte concluído registrado para este barbeiro.")
        return

    print(f"\nHistórico de cortes de {barbeiro}:")
    for ag in historico:
        print(f"- Cliente: {ag.cliente_nome}, Serviço: {ag.servico}, Dia: {ag.dia_semana}")

# ========== INICIAR SISTEMA ==========

sistema()
