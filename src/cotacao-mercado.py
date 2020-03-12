# -*- coding: utf-8 -*-
'''
Criado em 12/2019
@Autor: Paulo https://github.com/alpdias
'''

# Bibliotecas importadas
import bs4
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Mostra o horário e data atual para verificações
dataAtual = datetime.now()
minutos = dataAtual.minute
horasMinutos = ((dataAtual.hour * 60) + minutos) 

# Função para verificar a conexão com o site
def verificarConexao():
    try:
        url = (f'https://finance.yahoo.com/lookup')
        req = requests.get(url)
        fonteOnline = (req.status_code)
        if fonteOnline == 200:
            fonte = ('\033[0;32mONLINE\033[m')
            return fonte
        else:
            fonte = ('\033[0;31mOFFLINE\033[m')
            return fonte
    except:
        fonte = ('\033[0;31mERRO\033[m')
        return fonte


# Função para mostra se a negocição da BM&FBOVESPA está aberta ou fechada
def bovespaON():
    import datetime
    diaSemana = datetime.datetime.today().weekday()
    if diaSemana in [0, 1, 2, 3, 4]:
        try:
            if horasMinutos >= 600 and horasMinutos <= 1020:
                bovespa = ('\033[0;32mABERTO\033[m') 
                return bovespa
            elif horasMinutos >= 1020 and horasMinutos <= 1080:
                bovespa = ('\033[0;33mPRÉ-FECHAMENTO\033[m')
                return bovespa
            else:
                bovespa = ('\033[0;31mFECHADO\033[m') 
                return bovespa
        except:
            bovespa = ('\033[0;31mERRO\033[m')
            return bovespa
    else:
        bovespa = ('\033[0;31mFECHADO\033[m') 
        return bovespa


# Função para formatar os números de acordo com o padrão pt-BR
def tratamento(n=0):
    import locale
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    return (locale.format_string("%.2f", n, grouping=True))


'''

Para Windows utilize -->

locale.setlocale(locale.LC_ALL, "pt-BR")
locale.format_string("%.2f", n, grouping=True, monetary=True)

'''

# Funções de 'raspagem' da informação do site para obter os dados solicitados
def empresaBRL():
    r = requests.get(f'https://finance.yahoo.com/quote/{codigo}.SA/')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    nomeEmpresa = soup.find_all('div',{'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text
    valorEmpresa = float(soup.find_all('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text)
    print(f'Empresa: {nomeEmpresa}')
    print(f'Preço atual {codigo}: {tratamento(valorEmpresa)} - Valor em BRL')
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')


def empresaUSD():
    r = requests.get(f'https://finance.yahoo.com/quote/{codigo}/')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    nomeEmpresa = soup.find_all('div',{'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text
    valorEmpresa = float(soup.find_all('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text)
    print(f'Empresa: {nomeEmpresa}')
    print(f'Preço atual {codigo}: {tratamento(valorEmpresa)} - Valor em USD') 
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')


def indiceMercado():
    r = requests.get(f'https://finance.yahoo.com/quote/^{codigo}/')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    nomeIndice = soup.find_all('div',{'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text.split()
    valorIndice = soup.find_all('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    print(f'Índice: {nomeIndice[2]}') 
    print(f'Valor atual {codigo}: {valorIndice}')
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')


# Exibição das informações requisitadas
print('')
print(f'COTAÇÃO / MERCADO DE AÇÕES -- {verificarConexao()}')
print(f'BM&FBOVESPA: {bovespaON()}')
print('')

# Variável que recebe o código da empresa ou índice
codigo = str(input('Código da empresa ou índice: ')).upper() 

print('')
try:
    empresaBRL()
except IndexError:
    try:
        empresaUSD()
    except IndexError:
        try:
            indiceMercado()
        except IndexError:
            print('\033[0;31mERRO!\033[m Empresa/Índice não encontrada, tente novamente.')

print('')
