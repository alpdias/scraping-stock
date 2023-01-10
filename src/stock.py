# -*- coding: utf-8 -*-

'''
Criado em 12/2019
@Autor: Paulo https://github.com/alpdias
'''

# bibliotecas importadas
import bs4
import requests
import datetime
import locale
from bs4 import BeautifulSoup
from datetime import datetime

# mostra o horario e data atual para verificaçoes
dataAtual = datetime.now()
minutos = dataAtual.minute
horasMinutos = ((dataAtual.hour * 60) + minutos) 


def verificarConexao():
    
    """
    -> Funçao para verificar a conexao com o site
    """
    
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


def bovespaON():
    
    """
    -> Funçao para mostra se a negocição da BM&FBOVESPA esta aberta ou fechada
    """
    
    diaSemana = datetime.today().weekday()
    
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


def tratamento(n=0, formato=''):
    
    """
    -> Funçao para formatar os numeros de acordo com o padrao local selecionado
    """

    locale.setlocale(locale.LC_MONETARY, formato)
    
    return locale.currency(n, grouping=True)


def empresaBRL():
    
    """
    -> Funçao para 'raspagem' da informação do site para obter os dados solicitados
    """

    cabecalho = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # adição de cabecalho na requisicao, sem isso o site não aceita mais a o download de dados
    r = requests.get(f'https://finance.yahoo.com/quote/{codigo}.SA/', headers=cabecalho)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    nomeEmpresa = soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text
    valorEmpresa = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    valorEmpresa = float(valorEmpresa.replace(',','')) # remover a virgula para poder converter em numerico
    
    print(f'Empresa: {nomeEmpresa}')
    print(f'Preço atual {codigo}: {tratamento(valorEmpresa, "pt_BR.UTF-8")} - Valor em BRL')
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')


def empresaUSD():
          
    """
    -> Funçao para 'raspagem' da informação do site para obter os dados solicitados
    """

    cabecalho = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # adição de cabecalho na requisicao, sem isso o site não aceita mais a o download de dados
    r = requests.get(f'https://finance.yahoo.com/quote/{codigo}/', headers=cabecalho)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    nomeEmpresa = soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text
    valorEmpresa = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    valorEmpresa = float(valorEmpresa.replace(',','')) # remover a virgula para poder converter em numerico
    
    print(f'Empresa: {nomeEmpresa}')
    print(f'Preço atual {codigo}: {tratamento(valorEmpresa, "en_US.UTF-8")} - Valor em USD') 
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')


def indiceMercado():
          
    """
    -> Funçao para 'raspagem' da informação do site para obter os dados solicitados
    """

    cabecalho = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # adição de cabecalho na requisicao, sem isso o site não aceita mais a o download de dados   
    r = requests.get(f'https://finance.yahoo.com/quote/^{codigo}/', headers=cabecalho)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    nomeIndice = soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text
    valorIndice = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    valorIndice = float(valorIndice.replace(',','')) # remover a virgula para poder converter em numerico
    valorIndice = tratamento(valorIndice).replace('€','') # remover o simbolo de '€' valor em pontos

    print(f'Índice: {nomeIndice}') 
    print(f'Valor atual {codigo}: {valorIndice}')
    print(f'Fonte: Yahoo Finance')
    print(f'{dataAtual}')

print('')
          
print(f'COTAÇÃO / MERCADO DE AÇÕES -- {verificarConexao()}')
print(f'BM&FBOVESPA: {bovespaON()}')
          
print('')

codigo = str(input('Código da empresa ou índice: ')).upper() 

print('')

try:
    empresaBRL()
    
except (IndexError, AttributeError):
    try:
        empresaUSD()
        
    except (IndexError, AttributeError):
        try:
            indiceMercado()
            
        except (IndexError, AttributeError):
            print('\033[0;31mERRO!\033[m Empresa/Índice não encontrada, tente novamente!')

print('')
