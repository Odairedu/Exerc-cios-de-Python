def menu():
    print("\n--- Bilheteria de Evento ---")
    print("1 - Cadastrar nome do Evento")
    print("2 - Vender ingressos")
    print("3 - Repor ingressos")
    print("4 - Ver ingressos disponiveis")
    print("0 - Sair")
    return input("Escolha uma opção: ")
    
nome = None
ingresso = 0
quantidade = 0

    
while True:
    opcao = menu()
    
    if opcao == "1":
        nome = input("Digite o nome do Evento: ")
        print(f"Nome '{nome}' cadastrado com sucesso!")
    
    elif opcao == "2":
        if ingresso is None:
            print("Nenhum ingresso cadastrado ainda!")
        else:
            comprar = int(input("Quantos você deseja comprar?: "))
        if comprar <= 0:
            print("Você precisa repor ingressos!")
        elif comprar > quantidade:
            print("Quantidade insuficiente de ingressos!")
        else:
            quantidade -= comprar
            print(f"Comprado {comprar} unidade(s). Ingressos disponíveis: {quantidade}")
    
    elif opcao == "3":
        if ingresso is None:
            print("Nenhum ingresso no Estoque")
        else:
            adicionar = int(input("Digite a quantidade de ingressos a adicionar: "))
        if adicionar <= 0:
            print("A quantidade deve ser maior que zero!")
        else:
            quantidade += adicionar
            print(f"Adicionado {adicionar} ingressos. Ingressos atuais {quantidade}")
            
    elif opcao == "4":
        if ingresso is None:
            print("Nenhum ingresso cadastrado ainda!")
        else:
            print(f"Ingressos: {comprar} | Quantidade em estoque: {quantidade}")
            
    elif opcao == "0":
        print("Saindo do sistema . . . Até logo!")
        break
    
    else:
        print("Opção inválida! Tente Novamente.")
