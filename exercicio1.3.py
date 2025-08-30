def menu():
    print("\n1 - Cadastro Paciente")
    print("2 - Lista de Pacientes")
    print("3 - Atendimento ao Paciente")
    print("4 - Encerrar Atendimento")
    return input("Como posso ajudar? ")
    
pacientes = []

while True:
    opcao = menu()
    
    if opcao == "1":
        nome = input("Nome do Paciente: ")
        idade = input("Idade do paciente: ")
        sintomas = input("Sintomas: ")
        paciente = {
            "nome": nome,
            "idade": idade,
            "sintomas": sintomas
        }
        pacientes.append(paciente)
        print("Paciente cadastrado com sucesso!")
        
    elif opcao == "2":
        if pacientes:
            print("\nLista de pacientes:")
            for i, p, in enumerate(pacientes, 1): 
                print(f"{i}, {p['nome']} - {p['idade']} anos - Sintomas: {p['sintomas']}")
        else:
            print("Nenhum paciente cadastrado!")
            
    elif opcao == "3":
        if pacientes:
            paciente_atendido = pacientes.pop(0)
            print(f"Atendendo {paciente_atendido['nome']}, {paciente_atendido['idade']} anos.")
            print(f"Sintomas: {paciente_atendido['sintomas']}")
        else:
            print("Não há pacientes em espera...")
            
    elif opcao == "4":
        print("Encerrando atendimento. Até logo!")
        break
    
    else:
        print("Opção inválida. Tente novamente.")