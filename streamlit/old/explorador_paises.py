import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import re
#print('hola')
# Specify the DBPedia endpoint


def query_generica(my_query, st_tool):
    sparql1 = SPARQLWrapper("https://mired.uspceu.es/sparql")
    sparql1.setQuery(my_query)
    sparql1.setReturnFormat(JSON)
    result1 = sparql1.query().convert()
    for hit in result1["results"]["bindings"]:
        my_other_autor = hit["nombre_autor"]["value"]
        my_other_titulo = hit["titulo"]["value"]


        st_tool.write(my_other_autor + ", "+ my_other_titulo)

def query_sobre_titulo(my_query_autor, st_tool):
    sparql1 = SPARQLWrapper("https://mired.uspceu.es/sparql")
    sparql1.setQuery("""
        icrorrelato rdfs:label ?titulo
        FILTER regex(?nombre_autor, "(?i).*""" + my_query_autor + """" )
    }
    """)
    sparql1.setReturnFormat(JSON)
    result1 = sparql1.query().convert()
    for hit in result1["results"]["bindings"]:
        my_other_autor = hit["titulo"]["value"]
        st_tool.text(my_other_autor)

backend = "http://fastapi:8000/explorador_paises"

results_df = pd.DataFrame()
sparql = SPARQLWrapper("https://mired.uspceu.es/sparql")

sparql.setQuery("""
prefix mcr: <https://mired.uspceu.es/microrrelatos#>

    select distinct ?pais_string{
    ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
    ?uri_autor mcr:tienePais ?pais .
    ?pais rdfs:label ?pais_string
    ?pais mcr:codigoDePais ?codigo_pais
}

""")


# Convert results to JSON format
sparql.setReturnFormat(JSON)
result = sparql.query().convert()


results_cp = pd.DataFrame()
sparql = SPARQLWrapper("https://mired.uspceu.es/sparql")

sparql.setQuery("""
prefix mcr: <https://mired.uspceu.es/microrrelatos#>

    select distinct ?codigo_pais{
    ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
    ?uri_autor mcr:tienePais ?pais .
    ?pais rdfs:label ?pais_string
    ?pais mcr:codigoDePais ?codigo_pais
}

""")


# Convert results to JSON format
sparql.setReturnFormat(JSON)
resultcp = sparql.query().convert()


#df_autor_titulo = pd.Dataframe()
#df_autor_titulo = pd.DataFrame(df_autor_titulo, columns = ['autor' , 'titulo'])

# The return data contains "bindings" (a list of dictionaries)
data = {}
contador = 1
for hit in resultcp["results"]["bindings"]:
    my_pais = hit["pais_string"]["value"]

    if (contador == 1):
        data = {'pais':my_pais}
        results_cp = results_cp.append(data, ignore_index=True)
    else:
        data_row = {'pais':my_pais}
        results_cp = results_cp.append(data_row, ignore_index=True)
    contador  = contador + 1


ata = {}
contador = 1
for hit in result["results"]["bindings"]:
    my_pais = hit["pais_string"]["value"]

    if (contador == 1):
        data = {'pais':my_pais}
        results_df = results_df.append(data, ignore_index=True)
    else:
        data_row = {'pais':my_pais}
        results_df = results_df.append(data_row, ignore_index=True)
    contador  = contador + 1


def extraer_nombre(texto):
    debug = False
    expresion = '\d+'
    x = re.search(expresion, texto)

    if(x != None):
        if (debug):
            print("hay un numero")
        new_str = texto.replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').rstrip().lstrip()
        if (debug):
            print("new_str:" + new_str)

        expresion2 = '[\r\n]'
        x2 = re.search(expresion2, new_str)
        if(x2 != None):
        #str.split('\n')
            new_str2 = new_str.split('\n')[0]
            if (debug):
                print("new_str2:" + new_str2 + "#")
            return new_str2
    else:
        print("no hay un numero")
        return "no cumple formato"


def app():
    makes_pais = results_df['pais']
    make_choice_titulo = st.selectbox('Seleccion de pais:', makes_pais)
    #query_sobre_titulo(var_autor1, st)



    query = """
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>

    select distinct ?autor{
    ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
    ?uri_autor rdfs:label?autor .
    ?uri_autor mcr:tienePais ?pais .
    ?pais rdfs:label ?pais_string
    FILTER regex(?pais_string, """ + make_choice_titulo + """)
    }
    """

    query2 = """
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>

        select distinct ?nombre_autor ?titulo{
        ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
        ?uri_autor rdfs:label ?nombre_autor .
        ?uri_microrrelato rdfs:label ?titulo .
        ?uri_autor mcr:tienePais ?pais .
        ?pais rdfs:label ?mypais
        FILTER regex(?mypais, "(?i).*""" + make_choice_titulo + """" )
    }
    """
    query_generica(query2, st)
