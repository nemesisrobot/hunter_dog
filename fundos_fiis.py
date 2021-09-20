from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from lib.constantes_sistema import *


#pegando todos os fiis
lista_fiis=[]
fiis_html = BeautifulSoup(urlopen(Request('{}'.format(URL_FUNDS_EXPLORER),headers = HEADER)), 'html.parser')
html_puro_fiis = fiis_html.findAll("span",{"class":"symbol"})
for fiis in html_puro_fiis:
    lista_fiis.append(fiis.getText())

#definindo colunas dos fis
colunas_csv = '{}|{}|{}|{}|{}|{}|{}|{}|{}'.format("FII","Cotação","Empresa","Data Atualização","Segmento",\
                                                  "Div. Yield","Dividendo/cota","Cap Rate","Vacância Média")

#metodo para gerar arquivo csv
def gera_csv():
    return open('base_fiis.csv','w')

#metodo para escrever no csv
def escreve(arquivo,dados):
    arquivo.write(dados+'\n')

#metodo para fechar csv
def fechar_arquivo(arquivo):
    arquivo.close()
    

#gerando CSV
arquivo = gera_csv()

#escrevendo colunas
escreve(arquivo,colunas_csv)

#contador
CONTADOR=1

print("----------------------------------------------------------")
print("|                Iniciando Hunter Dog!!!!!!              |")
print("----------------------------------------------------------")

for fii in lista_fiis:
    #pegando pagina do fiis
    print("Coleta de dados em : {}%".format(round((CONTADOR/len(lista_fiis))*100),1))
    

    try:
        dados = Request('{}{}'.format(URL_FUNDAMENTUS,fii),headers = HEADER)
        resposta= urlopen(dados)
        lista_dados = []

        #fazendo parser de dados
        html = BeautifulSoup(resposta, 'html.parser')
        grid_dados = html.findAll('span')

        for dado in grid_dados:
            if '?' not in dado.getText():
                #print(dado.getText())
                lista_dados.append(dado.getText())

        #escrevendo conteudo
        conteudo_arquivo = '{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(lista_dados[2]\
                             ,lista_dados[4]\
                             ,(lista_dados[6]).replace(',','.')\
                             ,lista_dados[8]\
                             ,lista_dados[14]\
                             ,((lista_dados[40]).replace(',','.')).replace('%','')\
                             ,(lista_dados[42]).replace(',','.')\
                             ,(((lista_dados[94]).replace(',','.')).replace('%','')).replace('-','0')\
                             ,((lista_dados[100]).replace(',','.')).replace('%','')).replace('-','0')

        escreve(arquivo,conteudo_arquivo)
    except HTTPError:
        print("Erro"+HTTPError.reason)
    except IndexError:
        print("Erro na extração deda do FIIs {}".format(fii))

    CONTADOR=CONTADOR+1




#fechando escrita no arquivo
fechar_arquivo(arquivo)



