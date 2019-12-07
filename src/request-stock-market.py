# -*- coding: utf-8 -*-
'''
Criado em quinta-feira, 5 de dezembro de 2019
@Autor: Paulo https://github.com/alpdias
'''

# Bibliotecas importadas
import bs4
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Mostra o horário atual para verificações
dataAtual = datetime.now()
horas = dataAtual.hour

# Função para verificar a conexão com o site
def verificarConexao():
    try:
        url = (f'https://finance.yahoo.com/lookup')
        req = requests.get(url)
        fonteOnline = (req.status_code)
        if fonteOnline == 200:
            print('\033[0;32mOnline\033[m')
        else:
            print('\033[0;31mOffline\033[m')
    except:
        print('\033[0;31m#ERRO#\033[m')


# Função para mostra se a negocição da BM&FBOVESPA está aberta ou fechada
def bovespaON():
    try:
        if horas >= 10 and horas <= 17: # Adicionar diferença de dia para final de semana!
            print('\033[0;32mBM&FBOVESPA ON\033[m') 
        else:
            print('\033[0;31mBM&FBOVESPA OFF\033[m') 
    except:
        print('\033[0;31m#ERRO#\033[m')


# Funções de 'raspagem' da informação do site para obter os dados solicitados
def empresaBRL():
    r = requests.get(f'https://finance.yahoo.com/quote/{codigo}.SA/')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    nomeEmpresa = soup.find_all('div',{'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text
    valorEmpresa = soup.find_all('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    print(f'Empresa: {nomeEmpresa}')
    print(f'Preço atual {codigo}: {valorEmpresa} - Currency in BRL') # Mudar a formatação de valores para padrão pt-BR!
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')


def empresaUSD():
    r = requests.get(f'https://finance.yahoo.com/quote/{codigo}/')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    nomeEmpresa = soup.find_all('div',{'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text
    valorEmpresa = soup.find_all('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    print(f'Empresa: {nomeEmpresa}')
    print(f'Preço atual {codigo}: {valorEmpresa} - Currency in USD')
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')


def indiceMercado():
    r = requests.get(f'https://finance.yahoo.com/quote/^{codigo}/')
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    nomeIndice = soup.find_all('div',{'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text
    valorIndice = soup.find_all('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    print(f'Índice: {nomeIndice}') # Arrumar formato do nome aprensentado
    print(f'Preço atual {codigo}: {valorIndice}')
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')


# Variável que recebe o código da empresa ou índice
print('')
codigo = str(input('Código da empresa ou índice: ')).upper() 

# Exibição das informações requisitadas
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
            print('\033[0;31mEmpresa/Índice não encontrada, tente novamente!\033[m')
            
print('')
