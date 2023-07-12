#cria um dicionario dos caracteres e um banco de dados das strings que vão ser adicionadas ao dicionario.
banco_dados_caracteres = {}
banco_dados_strings = []


# função que cria o histograma principal, usa do banco_dados_strings para conferir se a palavra ja foi adicionada ao dicionario para evitar repetições.
def construir_histograma(nome, bd_strings,bd_char):

    if( nome not in bd_strings):
        for char in nome:
            if char in bd_char:
                bd_char[char] += 1
            else:
                bd_char[char] = 1
    return bd_char

# função que cria o histograma para as palavras que estão sendo comparadas.
def construir_histograma_excluir(string):
    histograma = {}
    for char in string:
        if char in histograma:
            histograma[char] += 1
        else:
            histograma[char] = 1
    return histograma

#função para encontrar as exclusões necessárias
def encontrar_exclusoes_minimas(string1, string2, str_excluida):
    string_final = "" #string criada para ser adicionada nela os caracteres que são iguais as duas palavras
    histograma1 = construir_histograma_excluir(string1)
    histograma2 = construir_histograma_excluir(string2)
    
    exclusoes_minimas = 0
    
    # Percorre cada caractere no histograma1
    for char, count in histograma1.items():
        if char in histograma2:
            if (count != histograma2[char]):
                exclusoes_minimas += abs(count - histograma2[char])
                str_excluida.update({char:count- histograma2[char]})
                string_final += char * min(histograma1[char],histograma2[char])

            else:
                string_final += char * abs(count)


        else:
            
            str_excluida.update({char:count})
            exclusoes_minimas += count
    
    # Percorre cada caractere no histograma2 para verificar se há caracteres extras
    for char, count in histograma2.items():
        if char not in histograma1:
            exclusoes_minimas += count
            str_excluida.update({char:count})

    histograma_resultado = construir_histograma_excluir(string_final)        
    
    return exclusoes_minimas, str_excluida, histograma1, histograma2, histograma_resultado

def plotar_histograma(bd_caracteres):

    chave_max = max(bd_caracteres, key = bd_caracteres.get) #pega o número de chaves para saber quantas linhas a matriz vai ter
    linhas = (bd_caracteres[chave_max] + 1) #adicionei +1 para colocar na ultima linha as strings analisadas
    colunas = len(bd_caracteres)
    matriz = [[" " for _ in range(colunas)] for _ in range(linhas)]

    lista_key = list(bd_caracteres.keys()) #fiz duas listas para poder pegar os valores do dicionario 
    lista_valores = list(bd_caracteres.values())

    while (linhas >= 0): # aqui roda um loop para criar a matriz de baixo pra cima 
        for i in range(len(bd_caracteres)):

            if (linhas == (bd_caracteres[chave_max] + 1)): # aqui na ultima linha é adicionado os caracteres analisados
                matriz[linhas - 1][i] = f"{lista_key[i]}"
            
            else:
                if (lista_valores[i] > 0): # aqui é adicionado um "|" pela quantidade de frequência daquele caractere
                    matriz[linhas - 1][i] = "|"
                    lista_valores[i] -= int(1)
    
        linhas -= int(1)

    for linha in matriz: #aqui eu ploto o histograma
        for elementos in linha:
            print (elementos, end = ' ')

        print() 


#primeira entrada para começar a executar o programa
palavra = str(input("Qual palavra gostaria de adicionar?\n")).upper() #transformando tudo em letras maiúscula

#loop criado para continuar adicionando palavras ou comparando elas.
while (palavra != "N"):

    #adiciono ao banco_dados_caracteres o histograma gerado pela função e adiciono a palavra no banco_dados_strings
    banco_dados_caracteres = construir_histograma(palavra,banco_dados_strings,banco_dados_caracteres)
    banco_dados_strings.append(palavra)


    #confiro se tem mais de uma palavra no banco_dados_strings para fim de comparações
    if (len(banco_dados_strings) > 1):

        comando = str(input("\nDeseja comparar duas palavras para saber qual o mínimo de caracteres precisam ser removidos para o histograma ficar igual? S/N\n")).upper()
        
        if (comando == "S"):

            #crio um dicionario auxiliar para mostrar quais são os caracteres excluídos e um contador
            caracteres_excluidas = {}
            contador = int(0)

            #aqui eu mostro as palavras disponíveis para fazer a comparação
            print("\nAs palavras disponíveis são:\n")
            for i in banco_dados_strings:
                print (f"{contador} - {i} \n")
                contador += int(1)

            else:

                #aqui pergunto quais as palavras vão ser escolhidas para fazer a comparação
                print("\nEscolha pelo index\n")
                palavra_1 = int(input("Qual a primeira palavra? "))
                palavra_2 = int(input("Qual a segunda palavra? "))

                #chamo a função para fornecer quantos caracteres devem ser excluidos e armazeno quais são em um dicionario com o caractere e sua quantidade que foi excluida
                numero_minimo, caracteres_excluidas,histograma_1,histograma_2,histograma_final = encontrar_exclusoes_minimas(banco_dados_strings[palavra_1],banco_dados_strings[palavra_2], caracteres_excluidas)
                print(f"\nO número mínimo de exclusões é: {numero_minimo} e os caracteres são:\n")

                for i in caracteres_excluidas:
                    print (f"{i}: {caracteres_excluidas[i]}\n")
                
                print(f'\nO histograma da palavra "{banco_dados_strings[palavra_1]}" é esse: \n')
                plotar_histograma(histograma_1)
                print(f'\nO histograma da palavra "{banco_dados_strings[palavra_2]}" é esse: \n')
                plotar_histograma(histograma_2)
                print(f'\nE o histograma da resultante é esse: \n')
                plotar_histograma(histograma_final)
        
        else:
            comando = ""

    comando = str(input("\nDeseja visualizar o histograma atual? S/N \n")).upper()

    if (comando == "S"):
        print("O histograma atual esta assim: \n")
        plotar_histograma(banco_dados_caracteres) #chama a função para criar a matriz

    else:
        comando = ""

    palavra = str(input("\nDeseja adicionar outra palavra? S/N\n")).upper()

    if (palavra == "S"):
        palavra = str(input("\nQual palavra gostaria de adicionar?\n")).upper()
    