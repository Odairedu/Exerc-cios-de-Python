from dataclasses import dataclass
from datetime import datetime, timedelta 
from typing import List, Tuple

#Definindo classes
@dataclass
class Cliente:
    nome: str
    telefone: str

@dataclass
class Equipamento:
    id: int
    cliente: Cliente
    descricao_problema: str
    tecnico: str
    data_entrada: datetime

    #Campos que vão mudar durante o processo
    status: str = "Em análise"
    orcamento_aprovado: bool = False
    preco_total: float = 0.0

    #Detalhes do orçamento
    servicos_orcados: List[Tuple[str, float]] = None
    pecas_orcadas: List[Tuple[str, float, str]] = None

#Banco de dados
ordens_de_servico: List[Equipamento] = []

servicos_fixos = {
    "Formatação": 80.0,
    "Limpeza geral": 50.0,
    "Remoção de virus": 60.0,
    "Instalação de programas": 40.0,
}

#Estoque
Estoque = {
    "Memória RAM": [150.0, 5],
    "SDD 480GB": [300.0, 4],
    "Fonte 500w": [200.0, 2],
}

proximo_id = 1

#Funções do sistema

def receber_equipamento():
    global proximo_id
    print("\n--- REGISTRO DE ENTRADA ---")
    nome = input("Nome do cliente: ")
    telefone = input("Telefone do cliente: ")
    descricao = input("Descrição do problema: ")
    tecnico = input("Nome do técnico responsável: ")
    novo_cliente = Cliente(nome=nome, telefone=telefone)

    nova_os = Equipamento(
        id=proximo_id,
        cliente=novo_cliente,
        descricao_problema=descricao,
        tecnico=tecnico,
        data_entrada=datetime.now(),
        servicos_orcados=[],
        pecas_orcadas=[]
    )
    ordens_de_servico.append(nova_os)
    proximo_id += 1
    print(f"\nEquipamento de {nome} recebido! OS ID: {nova_os.id}. Status: Em análise.")

def buscar_os():
    try:
        os_id = int(input("Digite o ID da Ordem de serviço para gerenciar: "))
        for os in ordens_de_servico:
            if os.id == os_id:
                return os
        print(f"OS ID {os_id} não encontrada.")
        return None
    except ValueError:
        print("ID inválido.")
        return None

def calcular_preco_peca(preco_custo: float) -> float:
    return preco_custo * 1.3

def fazer_orcamento(os: Equipamento):
    os.servicos_orcados = []
    os.pecas_orcadas = []
    os.preco_total = 0.0
    print(f"\n--- Fazendo orçamento (OS ID: {os.id}) ---")

    for nome, preco in servicos_fixos.items():
        escolha = input(f"Incluir {nome} (R${preco:.2f})? (s/n): ").lower()
        if escolha == 's':
            os.servicos_orcados.append((nome, preco))
            os.preco_total += preco
            print(f" -> {nome} adicionado.")

    print("\n--- Adicionando Peças (Custo + 30% Lucro) ---")
    for nome_peca, dados in Estoque.items():
        preco_custo = dados[0]
        quantidade = dados[1]

        if quantidade > 0:
            preco_venda = calcular_preco_peca(preco_custo)
            escolha = input(f"Incluir 1x {nome_peca} (R${preco_venda:.2f}, Estoque: {quantidade})? (s/n): ").lower()

            if escolha == 's':
                os.pecas_orcadas.append((nome_peca, preco_venda, nome_peca))
                os.preco_total += preco_venda
                print(f"  -> {nome_peca} adicionada.")
        else:
            print(f"-> {nome_peca} (Fora de estoque)")

    os.status = "Aguardando Orçamento"
    print("\nOrçamento pronto!")
    print(f"Preço Total Provisório: R${os.preco_total:.2f}") 

def aprovar_orcamento(os: Equipamento):
    print(f"\n--- APROVAÇÃO DE ORÇAMENTO (OS ID: {os.id}) ---")
    print(f"Orçamento a ser aprovado: R${os.preco_total:.2f}")

    aprovacao = input("O cliente aprovou o orçamento? (s/n): ").lower()

    if aprovacao == 's':
        os.orcamento_aprovado = True
        os.status = "Em Manutenção"

        for nome_peca, preco_venda, nome_estoque in os.pecas_orcadas:
            if nome_estoque in Estoque:
                Estoque[nome_estoque][1] -= 1

        print("\nOrçamento APROVADO. Peças baixadas do estoque. Status: Em Manutenção.")

    else:
        taxa_avaliacao = 30.00
        os.orcamento_aprovado = False
        os.preco_total = taxa_avaliacao
        os.status = "Pronto para Retirar (Taxa de Avaliação)"
        print(f"\nOrçamento REPROVADO. Cobrada Taxa de Avaliação: R${taxa_avaliacao:.2f}. Status: Pronto para Retirar.")

#Funções de tempo e relatorios

def calcular_taxa_armazenamento(os: Equipamento) -> float:
    """Calcula a taxa de R$ 10/dia se o PC estiver pronto há mais de 30 dias."""
    
    if "Pronto para Retirar" not in os.status:
        return 0.0

    data_hoje = datetime.now()
    dias_limite = 30
    taxa_diaria = 10.0
    diferenca = data_hoje - os.data_entrada

    if diferenca.days > dias_limite:
        dias_cobrar = diferenca.days - dias_limite
        taxa_total = dias_cobrar * taxa_diaria

        print(f"\nAVISO: OS ID {os.id} está pronta há {diferenca.days} dias.")
        print(f"Cobrar taxa de armazenamento de {dias_cobrar} dias: R${taxa_total:.2f}")
        return taxa_total

    return 0.0

def relatorio_tecnicos():
    """Mostra o número de OS gerenciadas por cada técnico."""
    produtividade = {}
    for os in ordens_de_servico:
        produtividade[os.tecnico] = produtividade.get(os.tecnico, 0) + 1

    print("\n--- RELATÓRIO DE PRODUTIVIDADE ---")
    if not produtividade:
        print("Nenhuma OS registrada para análise.")
        return

    for tecnico, count in sorted(produtividade.items(), key=lambda item: item[1], reverse=True):
        print(f"- {tecnico}: {count} Ordens de Serviço gerenciadas.")

def relatorio_defeitos():
    """Lista os problemas mais comuns registrados."""
    defeitos = {}
    for os in ordens_de_servico:
        problema = os.descricao_problema.strip().title()
        defeitos[problema] = defeitos.get(problema, 0) + 1

    print("\n--- RELATÓRIO DE DEFEITOS COMUNS ---")
    if not defeitos:
        print("Nenhum defeito registrado.")
        return

    top_defeitos = sorted(defeitos.items(), key=lambda item: item[1], reverse=True)
    for problema, count in top_defeitos:
        print(f"- {problema}: {count} ocorrências.")

#Funções do menu

def listar_oss():
    """Lista todos os equipamentos e seus status principais e checa taxa de armazenamento."""
    if not ordens_de_servico:
        print("\nNenhuma Ordem de Serviço registrada.")
        return

    print("\n--- LISTA DE EQUIPAMENTOS NA LOJA ---")
    print("-" * 75)
    print(f"{'ID':<4} | {'Cliente':<15} | {'Data Entrada':<12} | {'Status':<30} | {'Total':<8}")
    print("-" * 75)

    for os in ordens_de_servico:
        total = f"R${os.preco_total:.2f}"

        if os.orcamento_aprovado:
            aprovacao = "(APROVADO)"
        elif os.preco_total == 30.0 and "Taxa" in os.status:
            aprovacao = "(REPROVADO)"
        else:
            aprovacao = "(PENDENTE)"

        status_completo = f"{os.status} {aprovacao}"
        data_formatada = os.data_entrada.strftime("%d/%m/%Y")

        print(f"{os.id:<4} | {os.cliente.nome:<15} | {data_formatada:<12} | {status_completo:<30} | {total:<8}")
    print("-" * 75)

    # Verifica a taxa de armazenamento após listar
    for os in ordens_de_servico:
        calcular_taxa_armazenamento(os)

def menu_gerenciamento():
    """Menu para realizar ações em uma OS existente."""
    listar_oss()

    os = buscar_os()

    if os:
        while True:
            print(f"\n--- Gerenciando OS ID {os.id} de {os.cliente.nome} (Status: {os.status}) ---")
            print("1. Fazer/Refazer Orçamento")
            print("2. Aprovar/Reprovar Orçamento")
            print("3. Atualizar Status (Ex: Em Manutenção, Testando, Pronto para Retirar)")
            print("4. Voltar ao Menu Principal")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                fazer_orcamento(os)
            elif opcao == "2":
                if os.status == "Aguardando Orçamento":
                    aprovar_orcamento(os)
                else:
                    print("O orçamento precisa estar no status 'Aguardando Orçamento' para ser decidido.")
            elif opcao == "3":
                novo_status = input("Novo Status: ")
                os.status = novo_status
                print(f"Status da OS {os.id} atualizado para: {novo_status}")
            elif opcao == "4":
                break
            else:
                print("Opção inválida.")

def menu_relatorios():
    """Menu de navegação para os relatórios."""
    while True:
        print("\n=== MENU DE RELATÓRIOS ===")
        print("1. Produtividade dos Técnicos")
        print("2. Defeitos Mais Comuns")
        print("3. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            relatorio_tecnicos()
        elif opcao == "2":
            relatorio_defeitos()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")


def menu_principal():
    """Menu de navegação principal do sistema."""
    while True:
        print("\n=== SISTEMA TECHFIX - MENU PRINCIPAL ===")
        print("1. Registrar Novo Equipamento (Receber)")
        print("2. Listar Equipamentos (Visão Geral) e Checar Taxa de Armazenamento")
        print("3. Gerenciar uma Ordem de Serviço (Orçamento/Status/Aprovação)")
        print("4. Relatórios")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            receber_equipamento()
        elif opcao == "2":
            listar_oss()
        elif opcao == "3":
            menu_gerenciamento()
        elif opcao == "4":
            menu_relatorios()
        elif opcao == "5":
            print("Saindo do sistema... Obrigado!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
