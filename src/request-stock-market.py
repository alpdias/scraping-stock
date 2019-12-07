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

# Verificação de conexão com o site
print('')
try:
    url = (f'https://finance.yahoo.com/lookup')
    req = requests.get(url)
    fonteOnline = (req.status_code)
    if fonteOnline == 200:
        print('Sistema online')
    else:
        print('Sistema offline')
except:
    print('Erro de conexão!')

# Mostra o horário atual
dataAtual = datetime.now()
horas = dataAtual.hour

# Mostra o horário de negocição da BM&FBOVESPA 
print('')
if horas >= 10 and horas <= 17:
    print('O pregão negociação da BM&FBOVESPA está aberto')
else:
    print('O pregão negociação da BM&FBOVESPA está fechado') 
    print('Os valores exibidos depois desse período se referem ao fechamento') # Adicionar diferença de dia para final de semana!

# Variável que recebe o código da empresa
print('')
codigoEmpresa = str(input('Código da empresa: ')).upper() 

# Função de 'raspagem' da informação do site para obter o nome da empresa solicitada
def nomeEmpresa():
    try:
        r = requests.get(f'https://finance.yahoo.com/quote/{codigoEmpresa}.SA/')
        soup = bs4.BeautifulSoup(r.content, 'html.parser')
        nomeEmpresa = soup.find_all('div',{'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text
        return nomeEmpresa
    except IndexError:
        print('Empresa não encontrada, tente novamente!')


# Função de 'raspagem' da informação do site para obter preço atual da ação
def valorAtual():
    try:
        r = requests.get(f'https://finance.yahoo.com/quote/{codigoEmpresa}.SA/')
        soup = bs4.BeautifulSoup(r.content, 'html.parser')
        valor = soup.find_all('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        return valor
    except IndexError:
        print('Empresa não encontrada, tente novamente!')


# Exibição das informações requisitadas
print('')
if valorAtual() == None or nomeEmpresa() == None:
    pass
else:
    print(f'Empresa: {nomeEmpresa()}')
    print(f'Preço atual {codigoEmpresa}: {valorAtual()}') # Mudar a formatação de valores para padrão pt-BR!
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')

print('')
