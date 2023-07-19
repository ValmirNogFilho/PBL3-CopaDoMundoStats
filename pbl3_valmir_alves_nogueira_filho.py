'''
Autor: Valmir Alves Nogueira Filho
Componente Curricular: Algoritmos I
Concluído em: --/1-/2022
Declaro que este código foi elaborado por mim de forma individual e não contém
nenhum trecho de código de colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação do autor e a fonte do
código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
-------------------------------------------------------------------------------------------------------------------------------------------'''
import json
LETRAS = list('ABCDEFGH')
#retornos de -1 indicam erros que encerram execução do programa

class Time:
    def __init__(self):
        self.nome = ''
        self.pontos = 0
        self.gols = 0
        self.sofridos = 0
    def saldo(self):
        return self.gols - self.sofridos


class Partida:
    def __init__(self):
        self.jogo = ''
        self.timea = ''
        self.timeb = ''
        self.golsa = 0
        self.golsb = 0
        self.horario = ''
        self.local = ''
        self.data = 0
        self.placar = ''


def valida_menu(MSG, n_opcoes): #impede digitação errada nos menus 
    opcoes = ''
    for i in range(1, n_opcoes+1):
        opcoes += str(i)

    print(MSG)
    resposta = input('\n\nOpção escolhida: ')
    while  resposta not in opcoes or len(resposta.strip()) !=1 :
        print('\n')
        print('Opção escolhida inválida.\n')
        print(MSG)
        resposta = input('\n\nOpção escolhida: ')

    print('\n')
    return resposta


def geraArquivoGrupos():
    print("Arquivo GRUPOS.json criado.")
    dict_grupos = {}
    for letra in LETRAS:
        chave = f'{letra}'
        dict_grupos[chave] = ['','','','']
    return dict_grupos


def cadastroGrupos(dict_grupos, data):

    print('CADASTRAMENTO DAS SELEÇÕES DE CADA GRUPO')
    print('Digite a letra "p" ou "P" a qualquer momento, caso queira pausar o cadastro.')
    for grupo in dict_grupos:
        for i in range(4):
            if dict_grupos[grupo][i] == '': #se não tiver sido preenchida com nenhum dado (visto que os
                                            #arquivos são criados com seus valores iniciais sendo '')
                selecao = input(f'{i+1}° seleção do grupo {grupo}: ').upper().strip()

                if selecao == 'P': #se pedir pra parar, cadastre os dados até então recebidos
                    json.dump(dict_grupos, data, ensure_ascii=False, indent=4)
                    return 0
                dict_grupos[grupo][i] = selecao.upper()
        print('-'*100)
    print('TODOS OS TIMES DA COPA DO MUNDO 2022 FORAM CADASTRADOS!')
    json.dump(dict_grupos, data, ensure_ascii=False, indent=4)
      
                
def alteraOuRemoveGrupos(dict_grupos, data, acao): #acao = remoção ou alteração
    letra = input('Digite a letra do grupo: ').upper()
    while letra not in LETRAS or len(letra) != 1:
        letra = input('Entrada inválida. Digite a letra do grupo: ').upper()

    for i in range(4):
        print(f'{i+1}°: {dict_grupos[letra][i]}')

    opcao = valida_menu('Digite a posição do elemento no grupo: ', 4)
    opcao = int(opcao)

    if acao == 'alteração':
        elemento = input(f'{opcao}° seleção do grupo {letra}: ').upper()
    else: #remoção: substitui o valor antigo por '' (valor default inicial do arquivo json)
        elemento = ''
    dict_grupos[letra][opcao - 1] = elemento
    
    with open('GRUPOS.json', 'w', encoding='utf-8') as data:
        json.dump(dict_grupos, data, ensure_ascii=False, indent=4)
    print('FEITO!')

    if valida_menu(f'[1] para fazer nova {acao}\n[2] para sair: ', 2) == '1':
        alteraOuRemoveGrupos(dict_grupos, data, acao)


def validaGrupos(dict_grupos):
    contadora_erros = 0    
    for grupo in dict_grupos:
        for i in range(len(dict_grupos[grupo])):
            if dict_grupos[grupo][i] == '': #significa que o espaço está vazio e deve ser preenchido
                print(f'Preencha a {i+1}°  posição do grupo {grupo} com uma seleção')
                contadora_erros += 1    
    if contadora_erros > 0:
        return -1


def jogosCadaGrupo(grupo, lista): #função recursiva que retorna lista das partidas de um grupo
    if len(grupo) == 2:
        time = grupo.pop(0)
        for i in range(len(grupo)):
            lista.append(f'{time} x {grupo[i]}')
        return lista
    else:
        time = grupo.pop(0)
        for i in range(len(grupo)):
            lista.append(f'{time} x {grupo[i]}')
        return jogosCadaGrupo(grupo, lista)


def geraArquivoPartidas(dict_grupos, data):
    partidas = {}
    for grupo in dict_grupos:
            
        lista_partidas = [] #lista vazia a ser preenchida pela função jogosCadaGrupo()
        lista_partidas = jogosCadaGrupo(dict_grupos[grupo], lista_partidas)
        partidas[grupo] = []

        for i in range(6):
            jogo = lista_partidas[i]
            partidas[grupo].append({})
            partidas[grupo][i]['PARTIDA'] = jogo
            partidas[grupo][i]['DATA'] =  ''                
            partidas[grupo][i]['LOCAL'] = ''
            partidas[grupo][i]['HORÁRIO'] = ''
    json.dump(partidas, data, ensure_ascii=False, indent=4)
    return partidas


def cadastroPartidas(data, partidas):
    print('-'*100)
    print('Para pausar o cadastro, digite "p" ou "P", a qualquer momento.')
    print('Digite qualquer outra tecla para pular uma entrada de dados')
    print('(OBS: o programa receberá essa tecla como o dado a ser cadastrado.')
    print('Corrija os dados depois, para poder realizar as funções posteriores do programa.)')
    print('-'*100)
    for grupo in partidas:
        for i in range(6):
            print('PARTIDA: ', partidas[grupo][i]['PARTIDA'])
            if partidas[grupo][i]['DATA'] == '': #está preenchido?
                data_jogo = input('Data (escreva no formato "dd/mm"): ').strip().upper()
                if data_jogo == 'P': #pediram pra parar o cadastro?
                    json.dump(partidas, data, ensure_ascii=False, indent=4)
                    return 0
                      
            if partidas[grupo][i]['LOCAL'] == '':
                local = input('Local: ').strip().upper()
                if local == 'P':
                    json.dump(partidas, data, ensure_ascii=False, indent=4)
                    return 0
              
            if partidas[grupo][i]['HORÁRIO'] == '':
                horario = input('Horário da partida (escreva no formato "00:00"): ').strip().upper()            
                if horario == 'P':
                    json.dump(partidas, data, ensure_ascii=False, indent=4)
                    return 0
                
                partidas[grupo][i]['DATA'] =  data_jogo  
                partidas[grupo][i]['LOCAL'] = local 
                partidas[grupo][i]['HORÁRIO'] =  horario

            print('PARTIDA CADASTRADA!')

    print('TODAS PARTIDAS CADASTRADAS!')
    json.dump(partidas, data, ensure_ascii=False, indent=4)


def alteraOuRemovePartidas(partidas, data, acao):
    letra = input(f'Digite a letra do grupo com a partida que deseja realizar a {acao}: ').strip().upper()
    while letra not in LETRAS or len(letra) != 1:
        letra = input('Entrada inválida. Digite a letra do grupo: ').strip.upper()
    for i in range(6):
        print('-'*100)
        print(f'{i+1}° partida: ', end='')
        print(partidas[letra][i]['PARTIDA'])
        print('DATA:', partidas[letra][i]['DATA'])
        print('HORÁRIO: ', partidas[letra][i]['HORÁRIO'])
        print('LOCAL: ', partidas[letra][i]['LOCAL'])
        print('-'*100)
    opcao = valida_menu(f'Digite o número da partida que deseja realizar a {acao}:', 6)
    opcao = int(opcao)
    print(partidas[letra][opcao-1]['PARTIDA'])

    if acao == 'alteração':
        data_jogo = input('DATA: ').upper()      
        horario = input('HORÁRIO: ').upper()        
        local = input('LOCAL: ').upper()
       
    else: #remoção
        data_jogo = ''
        horario = ''
        local = ''
    partidas[letra][opcao-1]['DATA'] = data_jogo
    partidas[letra][opcao-1]['HORÁRIO'] = horario
    partidas[letra][opcao-1]['LOCAL'] = local

    with open('PARTIDAS.json', 'w', encoding='utf-8') as data:
        json.dump(partidas, data, ensure_ascii=False, indent=4)
    print('FEITO!')

    if valida_menu(f'[1] para fazer nova {acao}\n[2] para sair: ', 2) == '1':
        alteraOuRemovePartidas(partidas, data, acao)


def validaPartidas(partidas):
    contadora_erros = 0
    for grupo in partidas:
        for i in range(6):
            dia = partidas[grupo][i]['DATA'][:2]
            mes = partidas[grupo][i]['DATA'][3:]
            hora = partidas[grupo][i]['HORÁRIO'][:2]
            minuto = partidas[grupo][i]['HORÁRIO'][3:]
            partida = partidas[grupo][i]['PARTIDA']

            if dia == '' or mes == '' or len(partidas[grupo][i]['DATA']) != 5:
                print(f'Preencha a partida {partida} com uma data escrita de forma válida (formato dd/mm).')
                contadora_erros += 1
            if mes == '11':
                if not 20 <= int(dia) <= 30:
                    print('Corrija a data da partida ', partida)
                    contadora_erros += 1
            if mes == '12':
                if not 1 <= int(dia) <= 18:
                    print('Corrija a data da partida ', partida) 
                    contadora_erros += 1

            if (hora == '' or minuto == '' or 
            len(partidas[grupo][i]['HORÁRIO']) != 5 or
            partidas[grupo][i]['HORÁRIO'][2] != ':'): #se não estiver no formato 00:00                
                print(f'Preencha a partida {partida} com um horário escrito de forma válida (formato 00:00).')
                contadora_erros += 1
                print('-'*100)
            elif not hora.isnumeric() or not minuto.isnumeric(): #se hora e minuto não forem escritos por números
                print(f'Preencha a partida {partida} com um horário escrito de forma válida (formato 00:00).')
                contadora_erros += 1        
                print('-'*100)
            elif not 0 <= int(hora) <= 23 or not 0 <= int(minuto) <= 23:
                print('Corrija o horário da partida ', partida)
                contadora_erros += 1
                print('-'*100)
        
    if contadora_erros > 0:
        return -1


def geraArquivoResultados(partidas, data):
    resultados = {}
    for grupo in partidas:
        resultados[grupo] = [] #futura lista de dicionários
        for i in range(6):
            chave = str(partidas[grupo][i]['PARTIDA'])
            resultado = {'PARTIDA' : chave, 'PLACAR' : 'NxN'}
            resultados[grupo].append(resultado)
    return resultados


def cadastroResultados(dict_resultados, data):
    print('-'*100)
    print('Para pausar o cadastro, digite "p" ou "P"')
    print('digite qualquer outra tecla para pular uma partida')
    print('Corrija o resultado depois, para poder realizar as funções posteriores do programa.)')
    print('-'*100)
    for grupo in dict_resultados:
        for i in range(6):
            partida = dict_resultados[grupo][i]['PARTIDA']
            if dict_resultados[grupo][i]['PLACAR'] == 'NxN':
                resultado = input(f'Resultado da partida {partida} (escreva no formato NxN):').strip().lower()
                if resultado == 'p':
                    json.dump(dict_resultados, data, ensure_ascii=False, indent=4)
                    return 0
                dict_resultados[grupo][i]['PLACAR'] = resultado
    print('CADASTRO DAS 32 EQUIPES ESTÁ REALIZADO!')            
    json.dump(dict_resultados, data, ensure_ascii=False, indent=4)


def alteraOuRemoveResultados(dict_resultados, data, acao):
    letra = input(f'Digite a letra do grupo com a partida que deseja fazer a {acao}: ').strip().upper()

    while letra not in LETRAS or len(letra) != 1:
        letra = input('Entrada inválida. Digite a letra do grupo: ').strip().upper()

    for i in range(6):
        partida = dict_resultados[letra][i]['PARTIDA']
        placar = dict_resultados[letra][i]['PLACAR']
        print('-'*100)
        print(f'{i+1}° PARTIDA: {partida} -> {placar}')
        print('-'*100)

    opcao = valida_menu(f'Digite o número da partida que deseja fazer a {acao}',6)
    opcao = int(opcao) - 1
    partida_escolhida = dict_resultados[letra][opcao]['PARTIDA']
    if acao == 'remoção':
        dict_resultados[letra][opcao]['PLACAR'] = 'NxN'
    else:
        resultado = input(f'Resultado da partida {partida_escolhida} (escreva no formato NxN):').strip().lower()
        dict_resultados[letra][opcao]['PLACAR'] = resultado

    with open('RESULTADOS.json', 'w', encoding='utf-8') as data:
        json.dump(dict_resultados, data, ensure_ascii=False, indent=4)
    print('FEITO!')

    if valida_menu(f'[1] para fazer nova {acao}\n[2] para sair: ', 2) == '1':
        alteraOuRemoveResultados(dict_resultados, data, acao)


def validaResultados(dict_resultados):
    contadora_erros = 0
    for grupo in dict_resultados:
        for i in range(6):
            partida = dict_resultados[grupo][i]['PARTIDA'] 
            placar = dict_resultados[grupo][i]['PLACAR']
            indice_x = placar.find('x')
            if len(placar) < 3:
                contadora_erros += 1
                print('Corrija o formato do placar da partida', partida)
            if indice_x == -1:
                contadora_erros += 1
                print('Corrija o formato do placar da partida', partida)
            elif indice_x == 0 or indice_x == len(placar)-1:
                contadora_erros += 1
                print('Corrija o formato do placar da partida', partida)
            if not placar[:indice_x].isnumeric() or not placar[indice_x+1:].isnumeric():
                contadora_erros += 1
                print('Corrija o formato do placar da partida', partida)

    if contadora_erros > 0:
        return -1


def validacoes(nomearquivo):
    try:
        with open(nomearquivo + '.json', 'r', encoding='utf-8') as data:
            dicionario = json.load(data)
            if nomearquivo == 'GRUPOS':
                validacao = validaGrupos(dicionario)
            if nomearquivo == 'PARTIDAS':
                validacao = validaPartidas(dicionario)
            if nomearquivo == 'RESULTADOS':
                validacao = validaResultados(dicionario)
            if validacao == -1:
                print(f'Corrija os erros no cadastro de {nomearquivo.lower()} para poder dar prosseguimento ao programa.')
                return -1
            else: return dicionario            
    except FileNotFoundError:
        print(f'Faça o cadastro de {nomearquivo.lower()} primeiro.')
        return -1                


def alteraOuRemove(nome_arquivo, acao):
    print('VERIFICANDO PREEXISTÊNCIA DE DADOS:\n.\n.\n.\n')
    try:
        with open(nome_arquivo+'.json', 'r', encoding='utf-8') as data:
            print('DADOS ENCONTRADOS!')
            dict_do_arquivo = json.load(data)
        if nome_arquivo == 'GRUPOS':
            alteraOuRemoveGrupos(dict_do_arquivo, data, acao)
        elif nome_arquivo == 'PARTIDAS':
            alteraOuRemovePartidas(dict_do_arquivo, data, acao)
        elif nome_arquivo == 'RESULTADOS':
            alteraOuRemoveResultados(dict_do_arquivo, data, acao)
    except FileNotFoundError:
        print(f'PARA REALIZAR A {acao.upper()}, FAÇA O CADASTRO DE {nome_arquivo} PRIMEIRO.')
        return -1


def encontraXNaString(string):
    for i in range(len(string)):
        if string[i] == 'x':
            return i


def dadosResultado(resultado):
    
    indice_x_partida = encontraXNaString(resultado['PARTIDA'])
    time_a = resultado['PARTIDA'][:indice_x_partida].strip()
    time_b = resultado['PARTIDA'][indice_x_partida+1:].strip()
    indice_x_placar = encontraXNaString(resultado['PLACAR'])
    gols_a = int(resultado['PLACAR'][:indice_x_placar].strip())
    gols_b = int(resultado['PLACAR'][indice_x_placar+1:].strip())
    return (time_a,time_b,gols_a,gols_b)


def objetosPartidas(partida, resultado):
    objeto = Partida()
    objeto.jogo = partida['PARTIDA'] 
    objeto.data = partida['DATA']
    objeto.horario = partida['HORÁRIO']
    objeto.local = partida['LOCAL']
    objeto.placar = resultado['PLACAR']
    dados = dadosResultado(resultado)
    objeto.timea = dados[0]
    objeto.timeb = dados[1]
    objeto.golsa = dados[2]
    objeto.golsb = dados[3]
    return objeto


def mediaGols(colecao_objetos):
    soma = 0
  
    for i in range(len(colecao_objetos)):
        soma += colecao_objetos[i].golsa
        soma += colecao_objetos[i].golsb
    return soma

def maisGolsUmaPartida(colecao_objetos):
    
    maior = colecao_objetos[0][0].golsa
    objeto = colecao_objetos[0][0]
    time_mais_gols = colecao_objetos[0][0].timea
    for i in range(len(colecao_objetos)):
        for j in range(6):
            if colecao_objetos[i][j].golsa > maior:
                maior = colecao_objetos[i][j].golsa
                objeto = colecao_objetos[i][j] 
                time_mais_gols = colecao_objetos[i][j].timea
                adversario = colecao_objetos[i][j].timeb
            if colecao_objetos[i][j].golsb > maior:
                maior = colecao_objetos[i][j].golsb
                objeto = colecao_objetos[i][j]
                time_mais_gols = colecao_objetos[i][j].timeb
                adversario = colecao_objetos[i][j].timea
    print('SELEÇÃO COM MAIS GOLS EM UMA PARTIDA: ', time_mais_gols)
    print('TIME ADVERSÁRIO: ', adversario)
    print('DATA DA PARTIDA: ', objeto.data)
    print('HORÁRIO DA PARTIDA: ', objeto.horario)
    print('LOCAL DA PARTIDA: ', objeto.local)
    

def objetosTimes(grupo, resultados):
    lista_grupo = []
    for time in grupo:
        objeto = Time() 
        objeto.nome = time
        lista_grupo.append(objeto)
    for resultado in resultados:
        dados = dadosResultado(resultado)
        saldo = dados[2] - dados[3]        
        for time in lista_grupo:
            if dados[0] == time.nome:
                time.gols += dados[2]
                time.sofridos += dados[3]
                if saldo > 0:
                    time.pontos += 3
                elif saldo == 0:
                    time.pontos += 1    
            elif dados[1] == time.nome:
                time.gols += dados[3]
                time.sofridos += dados[2]    
                if saldo < 0:
                    time.pontos += 3
                elif saldo == 0:
                    time.pontos += 1

    return lista_grupo                  


def bubble_sort(lista):
    tamanho = len(lista)
    for i in range(1, tamanho):
        for j in range(tamanho-1, i-1, -1):

            if lista[j-1].pontos < lista[j].pontos:
                lista[j],lista[j-1] = lista[j-1],lista[j]  

            elif lista[j-1].pontos == lista[j].pontos:

                if lista[j-1].saldo() < lista[j].saldo():
                    lista[j],lista[j-1] = lista[j-1],lista[j]

                elif lista[j-1].saldo() == lista[j].saldo():

                    if lista[j-1].gols < lista[j].gols:
                        lista[j],lista[j-1] = lista[j-1],lista[j]


def chaveamento(matriz_grupos):
    print('CONFRONTOS DAS OITAVAS DE FINAL DA COPA DO MUNDO FIFA 2022: ')
    print('-'*100)    

    for i in range(0, 8, 2):
        print(f'{matriz_grupos[i][0].nome} x {matriz_grupos[i+1][1].nome}')
        print('-'*100) 
        print(f'{matriz_grupos[i][1].nome} x {matriz_grupos[i+1][0].nome}')
        print('-'*100) 


def arquivoPartidasCriado():
    try:
        with open('PARTIDAS.json', 'r', encoding='utf-8') as data:
            arquivo_partidas_criado = True
    except FileNotFoundError:
            arquivo_partidas_criado = False    
    return arquivo_partidas_criado


def arquivoResultadosCriado():
    try:
        with open('RESULTADOS.json', 'r', encoding='utf-8') as data:
            arquivo_resultados_criado = True      
    except FileNotFoundError:
        arquivo_resultados_criado = False
    return arquivo_resultados_criado


##########################################################################################################################################################################################################################
##########################################################################################################################################################################################################################
##########################################################################################################################################################################################################################

def main():
    print('-'*100)
    print('{:^100}'.format('COPA DO MUNDO 2022'))
    print('-'*100)

    resposta = valida_menu('[1] CADASTRO\n[2] ALTERAÇÃO\n[3] REMOÇÃO\n[4] EXIBIR RELATÓRIO\n[5] CHAVEAMENTO DAS OITAVAS\n[6] SAIR', 6)
    while resposta != '6':

        if resposta == '1': #CADASTRO

            opcao = valida_menu('[1] GRUPOS\n[2] PARTIDAS\n[3] RESULTADOS\n[4] SAIR', 4)
            
            if opcao == '1': #CADASTRO DE GRUPOS
                if arquivoPartidasCriado():
                    print('Você já iniciou o cadastro de partidas, logo, a manipulação de grupos não é permitida.')
                    return -1

                print('VERIFICANDO PREEXISTÊNCIA DE DADOS:\n.\n.\n.\n')

                try:
                    with open('GRUPOS.json', 'r', encoding='utf-8') as data:
                        dict_grupos = json.load(data)
                        print('DADOS PREEXISTENTES ENCONTRADOS!')
                    cadastro = valida_menu('[1] FAZER NOVO CADASTRO, APAGANDO O ANTERIOR\n[2] CONTINUAR CADASTRO INCOMPLETO\n[3] MANTER O CADASTRO DO JEITO QUE ESTÁ', 3)
                    if cadastro == '1':
                        with open('GRUPOS.json', 'w', encoding='utf-8') as data:
                            dict_grupos = geraArquivoGrupos()
                            cadastroGrupos(dict_grupos, data)
                            
                    elif cadastro == '2':
                        with open('GRUPOS.json', 'w', encoding='utf-8') as data:
                            cadastroGrupos(dict_grupos, data)                                
                                                            
                except FileNotFoundError:
                    with open('GRUPOS.json', 'w', encoding='utf-8') as data:
                        dict_grupos = geraArquivoGrupos()
                        cadastroGrupos(dict_grupos, data)


            elif opcao == '2': #CADASTRO DE PARTIDAS

                if arquivoResultadosCriado():
                    print('Você já iniciou o cadastro de resultados, logo, a manipulação de partidas não é permitida.')
                    return -1
                    
                print('VERIFICANDO PREEXISTÊNCIA DE DADOS:\n.\n.\n.\n')
                
                dict_grupos = validacoes('GRUPOS') #pode retornar o dicionario json ou -1
                if dict_grupos == -1:
                    return -1

                try:
                    with open('PARTIDAS.json', 'r', encoding='utf-8') as data:
                        dict_partidas = json.load(data)
                        print('DADOS PREEXISTENTES ENCONTRADOS!')

                    cadastro = valida_menu('[1] FAZER NOVO CADASTRO, APAGANDO O ANTERIOR\n[2] CONTINUAR CADASTRO INCOMPLETO\n[3] MANTER O CADASTRO DO JEITO QUE ESTÁ', 3)
                    if cadastro == '1':
                        with open('PARTIDAS.json', 'w', encoding='utf-8') as data:
                            geraArquivoPartidas(dict_grupos, data)
                        with open('PARTIDAS.json', 'w', encoding='utf-8') as data:
                            cadastroPartidas(data, dict_partidas)
                    elif cadastro == '2':
                        with open('PARTIDAS.json', 'w', encoding='utf-8') as data:
                            cadastroPartidas(data, dict_partidas)

                except FileNotFoundError:
                    print('A partir do começo desse cadastro, você não poderá efetuar mudanças no cadastro de grupos. Deseja continuar?')
                    
                    if valida_menu('[1] SIM \n[2] NÃO', 2) == '1':
                        
                        with open('PARTIDAS.json', 'w', encoding='utf-8') as data:
                            geraArquivoPartidas(dict_grupos, data)
                        with open('PARTIDAS.json', 'r', encoding='utf-8') as data:
                            dict_partidas = json.load(data)
                        with open('PARTIDAS.json', 'w', encoding='utf-8') as data:
                            cadastroPartidas(data, dict_partidas)

            elif opcao == '3': #CADASTRO DE RESULTADOS
               
                print('VERIFICANDO PREEXISTÊNCIA DE DADOS:\n.\n.\n.\n')
                
                dict_partidas = validacoes('PARTIDAS') #pode retornar o dicionario json ou -1
                if dict_partidas == -1:
                    return -1

                try:
                    with open('RESULTADOS.json', 'r', encoding='utf-8') as data:
                        dict_resultados = json.load(data)
                        print('DADOS ENCONTRADOS!')
                        cadastro = valida_menu('[1] FAZER NOVO CADASTRO, APAGANDO O ANTERIOR\n[2] CONTINUAR CADASTRO INCOMPLETO\n[3] MANTER O CADASTRO DO JEITO QUE ESTÁ', 3)
                    if cadastro == '1':
                        with open('RESULTADOS.json', 'w', encoding='utf-8') as data:
                            dict_resultados = geraArquivoResultados(dict_partidas, data)
                        with open('RESULTADOS.json', 'w', encoding='utf-8') as data:
                            cadastroResultados(dict_resultados, data)
                    elif cadastro == '2':
                        with open('RESULTADOS.json', 'w', encoding='utf-8') as data:
                            cadastroResultados(dict_resultados, data)

                except FileNotFoundError:             
                    print('A partir do começo desse cadastro, você não poderá efetuar mudanças no cadastro de grupos. Deseja continuar?')
                   
                    if valida_menu('[1] SIM \n[2] NÃO', 2) == '1':
                        with open('RESULTADOS.json', 'w', encoding='utf-8') as data:
                            dict_resultados = geraArquivoResultados(dict_partidas, data)
                        with open('RESULTADOS.json', 'w', encoding='utf-8') as data:
                            cadastroResultados(dict_resultados, data) 

        if resposta == '2': #ALTERAÇÃO
            opcao = valida_menu('[1] GRUPOS\n[2] PARTIDAS\n[3] RESULTADOS\n[4] SAIR', 4)

            if opcao == '1': #ALTERAÇÃO DE GRUPOS
                if arquivoPartidasCriado():
                    print('Você já iniciou o cadastro de partidas, logo, a manipulação de grupos não é permitida.')
                    return -1
                alteraOuRemove('GRUPOS', 'alteração')    
            elif opcao == '2': #ALTERAÇÃO DE PARTIDAS
                if arquivoResultadosCriado():
                    print('Você já iniciou o cadastro de resultados, logo, a manipulação de partidas não é permitida.')
                    return -1
                alteraOuRemove('PARTIDAS', 'alteração')            
            elif opcao == '3': #ALTERAÇÃO DE RESULTADOS
                alteraOuRemove('RESULTADOS', 'alteração')

        if resposta == '3': #REMOÇÃO
            opcao = valida_menu('[1] GRUPOS\n[2] PARTIDAS\n[3] RESULTADOS\n[4] SAIR', 4)
            
            if opcao == '1': #REMOÇÃO DE GRUPOS
                if arquivoPartidasCriado():
                    print('Você já iniciou o cadastro de partidas, logo, a manipulação de grupos não é permitida.')
                    return -1
                alteraOuRemove('GRUPOS', 'remoção')
            elif opcao == '2': #REMOÇÃO DE PARTIDAS
                if arquivoResultadosCriado():
                    print('Você já iniciou o cadastro de resultados, logo, a manipulação de partidas não é permitida.')
                    return -1
                alteraOuRemove('PARTIDAS', 'remoção')            
            elif opcao == '3': #REMOÇÃO DE RESULTADOS
                alteraOuRemove('RESULTADOS', 'remoção')

        if resposta == '4':
           
            print('-'*100)
            print('{:^100}'.format('RELATÓRIO:'))
            print('-'*100)
            print('VERIFICANDO PREEXISTÊNCIA DE DADOS:\n.\n.\n.\n')

            dict_resultados = validacoes('RESULTADOS') #pode retornar o dicionario json ou -1
            if dict_resultados == -1:
                return -1
 
            dict_partidas = validacoes('PARTIDAS') #pode retornar o dicionario json ou -1
            if dict_partidas == -1:
                return -1
 
 
            #produção de coleção de objetos usada para o relatório
            objetos_partidas_por_grupo = []
            for letra in LETRAS:
                grupo = []                 
                for i in range(6):
                        
                    objeto = objetosPartidas(dict_partidas[letra][i], dict_resultados[letra][i])
                    grupo.append(objeto)
                    
                objetos_partidas_por_grupo.append(grupo)

            #médias do relatório
            soma_total = 0   
            tamanho = len(objetos_partidas_por_grupo)
            for i in range(tamanho):
                soma = mediaGols(objetos_partidas_por_grupo[i]) 
                print('Média de gols por partida do grupo {}: {:.2f}'.format(LETRAS[i], soma/6))
                soma_total += soma
            print('-'*100)
            print('média geral de gols da primeira fase: {:.2f}'.format(soma_total/48))

            #dados da partida com mais gols
            maisGolsUmaPartida(objetos_partidas_por_grupo)
            print('-'*100)            
        if resposta == '5':
            
            dict_grupos = validacoes('GRUPOS') #pode retornar o dicionario json ou -1
            if dict_grupos == -1:
                return -1

            dict_resultados = validacoes('RESULTADOS') #pode retornar o dicionario json ou -1
            if dict_resultados == -1:
                return -1

            objetos_times_por_grupo = []

            print('TIMES CLASSIFICADOS SÃO IMPRESSOS COM A COR \033[0;30;42mVERDE\033[m')
            for letra in LETRAS:            
                grupo = objetosTimes(dict_grupos[letra], dict_resultados[letra])          
                bubble_sort(grupo)    
                print(f'GRUPO {letra}:')
                for i in range(4):
                    if i <= 1:
                        print(f'\033[0;30;42m{i+1}° {grupo[i].nome:15} || PONTOS: {grupo[i].pontos}    SALDO DE GOLS: {grupo[i].saldo():2}   \033[m')
                    else:
                        print(f'{i+1}° {grupo[i].nome:15} || PONTOS: {grupo[i].pontos}    SALDO DE GOLS: {grupo[i].saldo()}')
                print('-'*100)    
                objetos_times_por_grupo.append(grupo)

            chaveamento(objetos_times_por_grupo)

        resposta = valida_menu('[1] CADASTRO\n[2] ALTERAÇÃO\n[3] REMOÇÃO\n[4] EXIBIR RELATÓRIO\n[5] CHAVEAMENTO DAS OITAVAS\n[6] SAIR', 6)

    return 0
    

if __name__ == '__main__' :
    main()
    print('Programa encerrado.')