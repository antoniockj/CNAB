from database import menu, adicionar_boleto, gerar_remessa

while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_boleto()
    elif opcao == "2":
        gerar_remessa()
    elif opcao == "3":
        print("Saindo...")
        break
    else:
        print("Opção inválida.")