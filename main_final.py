import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import textblob
from textblob import TextBlob
import nltk
# nltk.download('brown')
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.corpus import stopwords
import numpy as np

# FORMAT

class Noticia:
    def __init__(self, titulo=None, medio=None, link=None, copete=None, texto=None, fecha=None,
                 valorar=None, terminos=None, sentimiento=None):
        self.titulo = titulo
        self.medio = medio
        self.terminos = terminos
        self.link = link
        self.copete = copete
        self.texto = texto
        self.fecha = fecha
        self.valorar = valorar
        self.sentimiento = sentimiento

    def get_titulo(self):
        return self.titulo

    def get_medio(self):
        return self.medio

    def get_link(self):
        return self.link

    def get_copete(self):
        return self.copete

    def get_texto(self):
        return self.texto

    def get_fecha(self):
        return self.fecha

    def get_valoracion(self):
        return self.valorar

    def get_terminos(self):
        return self.terminos

    def get_sentimiento(self):
        return self.sentimiento
    # def agg_sent(self, sent):
    #     self.sentimiento = sent

# TextBlob
# Esta funcion analiza el sentimiento del texto pasado y devuelve si es negativo, neutro o positivo.
def sentimiento(texto):
    blob = textblob.TextBlob(texto)
    blob = blob.translate('es')
    r = blob.sentiment.polarity
    if r < 0:
        sentiment = 'negativo'
    elif r > 0:
        sentiment = 'positivo'
    else:
        sentiment = 'neutro'
    return sentiment


df = pd.read_csv('noticias_santa_fe.csv')
# Con este codigo se pasan los datos de un dataframe de pandas a un a lista de objetos Noticia.
lista = []  # Lista de objetos Noticia.
for index, row in df.iterrows():
    noticia = Noticia(titulo=row['titulo'], medio=row['medio'], link=row['link'], texto=row['texto'],
                      fecha=row['fecha'], terminos=row['terminos'], sentimiento=sentimiento(row['titulo']))
    lista.append(noticia)

# print(len(lista))

# Este script devuelve la estructura de una tabla en html con las noticias analizadas.
def tabla (lista):
    trr = ''
    index = 0
    for i in lista:
        index += 1
        tr = f'<tr><th>{index}</th><td>{i.get_fecha()}</td><td>{i.get_medio()}</td><td>{i.get_titulo()}</td><td>{i.get_terminos()}</td></tr>'
        trr += tr
    return trr

# Funcion que genera un grafico con el sentimiento de noticias por termino.
def sent_terminos(lista):
    # Genero un diccionario con la cant de pos, neu y neg de cada termino
    terminos = {}
    for i in lista:
        termino = [i.get_terminos()]
        sent = i.get_sentimiento()
        for x in termino:
            if x not in terminos:
                terminos[x] = [0, 0, 0]
                continue
            if x in terminos:
                if sent == 'positivo':
                    terminos[x][0] += 1
                if sent == 'neutro':
                    terminos[x][1] += 1
                if sent == 'neutro':
                    terminos[x][2] += 1
    categorias = []
    positiva = []
    neutra = []
    negativa = []
    for nombre, valor in terminos.items():
        categorias.append(nombre)
        positiva.append(valor[0])
        neutra.append(valor[1])
        negativa.append(valor[2])
    # Formateo de ceros.
    for i in range(0, len(positiva)):
        if positiva[i] == 0:
            positiva[i] = 0.05
    for i in range(0, len(neutra)):
        if neutra[i] == 0:
            neutra[i] = 0.05
    for i in range(0, len(negativa)):
        if negativa[i] == 0:
            negativa[i] = 0.05
    # Configuración del gráfico
    ancho_barra = 0.25
    indice = np.arange(len(categorias))
    # Crear el gráfico de barras
    plt.figure()
    plt.bar(indice, positiva, width=ancho_barra, label='Positivas', color='green')
    plt.bar(indice + ancho_barra, neutra, width=ancho_barra, label='Neutras')
    plt.bar(indice + 2*ancho_barra, negativa, width=ancho_barra, label='Negativas', color='orange')
    plt.xlabel('Candidatos')
    plt.ylabel('Cantidad de noticias')
    plt.title('Sentimiento de noticias')
    plt.xticks(indice + ancho_barra, categorias)
    plt.legend()
    plt.savefig('./assets/grafico_triple.png', bbox_inches='tight', dpi=300)
    return """
        <div class="grafico_simple">
            <img src="./assets/grafico_triple.png" alt="">
        </div>"""

# Funcion que genera un grafico con la cantidad de apariciones por termino.
def cant_term(lista):
    # Genero un diccionario con la cant de pos, neu y neg de cada termino
    terminos = {}
    for i in lista:
        termino = [i.get_terminos()]
        for x in termino:
            if x in terminos:
                terminos[x] += 1
            if x not in terminos:
                terminos[x] = 1
    # Configuración del gráfico
    ancho_barra = 0.25  # Ancho de cada barra
    indice = np.arange(len(terminos))
    # grafico
    claves = list(terminos.keys())
    valores = list(terminos.values())
    plt.figure()
    plt.bar(claves, valores, width=0.75, color='orange')
    plt.ylabel('Altura')
    plt.title('Gráfico 2: Barras simples')
    plt.xticks(claves)
    plt.legend()
    claves = list(terminos.keys())
    valores = list(terminos.values())
    plt.bar(claves, valores)
    plt.ylabel('Cantidad de apariciones')
    plt.title(f'Apariciones de cada candidato')
    plt.savefig('./assets/grafico.png', bbox_inches='tight', dpi=300)
    return """
        <div class="grafico_simple">
            <img src="./assets/grafico.png" alt="">
        </div>"""



#Creacion de html
html_1 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analizador</title>
    <!-- <link rel="stylesheet" href="./style.css"> -->
    <style>
                /* TABLA */
                body {
                    font-family: Arial, Helvetica, sans-serif;
                }
                .tabla {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }
                .titulo_tabla {
                    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                    font-size: 20px;
                    color: #039
                }
                table {
                    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                    font-size: 11px;
                    width: 80%;
                    text-align: left;
                    border-collapse: collapse;
                }
                th {
                    font-size: 11px;
                    font-weight: normal;
                    padding: 5px;
                    background: #b9c9fe;
                    color: #039;
                }
                td {
                    padding: 5px;
                    background: #e8edff;
                    border-bottom: 1px solid #fff;
                    color: #669;
                }
                /* GRAFICOS */
                body {
                    background-color: #ededed;
                    background-color: white;
                }
                .graficos{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    grid-template-rows: repeat(2, 1fr);
                }
                .grafico_simple .grafico_triple{
                    border: 1px solid #ccc; /* Opcional: agregar un borde para visualizar el contenedor */
                    display: flex; /* Utilizamos flex para centrar la imagen horizontal y verticalmente */
                    justify-content: center;
                    align-items: center;
                    overflow: hidden; /* Ocultar cualquier parte de la imagen que se salga del contenedor */
                }
                .grafico_simple img{
                    width: 100%;
                    height: 100%;
                    object-fit: contain;
                }
                .grafico_triple img{
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }
    </style>
</head>

<body>
    <section class="tabla">
        <h2 class="titulo_tabla">Noticias analizadas:</h2>
        <table border-collapse=collapse; class="dataframe">
            <thead>
                <tr style="text-align: center;">
                    <th></th>
                    <th>Fecha</th>
                    <th>Medio</th>
                    <th>Titulo</th>
                    <th>Terminos</th>
                </tr>
            </thead>"""
html_2 = tabla(lista)
html_3 = """
            </tbody>
        </table>
    </section>    

    <section class="graficos">"""
triple = sent_terminos(lista)
simple = cant_term(lista)
html_4 = """
    </section>
</body>
</html>"""

html = html_1 + html_2 + html_3 + triple + simple + html_4

archivo_html = open("analizador_html.html", "w")
archivo_html.write(html)
archivo_html.close()
