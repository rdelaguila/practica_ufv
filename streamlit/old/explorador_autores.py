import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import re
#print('hola')
# Specify the DBPedia endpoint


def query_sobre_titulo(my_query_autor, st_tool):
    sparql1 = SPARQLWrapper("https://mired.uspceu.es/sparql")
    sparql1.setQuery("""
        prefix mcr: <https://mired.uspceu.es/microrrelatos#>

        select distinct ?titulo{
        ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
        ?uri_autor rdfs:label ?nombre_autor .
        ?uri_microrrelato rdfs:label ?titulo
        FILTER regex(?nombre_autor, "(?i).*""" + my_query_autor + """" )
    }
    """)
    sparql1.setReturnFormat(JSON)
    result1 = sparql1.query().convert()
    for hit in result1["results"]["bindings"]:
        my_other_autor = hit["titulo"]["value"]
        st_tool.text(my_other_autor)

backend = "http://fastapi:8000/explorador_autores"

results_df = pd.DataFrame()
sparql = SPARQLWrapper("https://mired.uspceu.es/sparql")

sparql.setQuery("""
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>

    select distinct ?nombre_autor ?titulo{
    ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
    ?uri_autor rdfs:label ?nombre_autor .
    ?uri_microrrelato rdfs:label ?titulo
}

""")


# Convert results to JSON format
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

#df_autor_titulo = pd.Dataframe()
#df_autor_titulo = pd.DataFrame(df_autor_titulo, columns = ['autor' , 'titulo'])

# The return data contains "bindings" (a list of dictionaries)
data = {}
contador = 1
for hit in result["results"]["bindings"]:
    # We want the "value" attribute of the "comment" field
    #print(hit["nombre_autor"]["value"])
    #print(hit["titulo"]["value"])
    my_autor = hit["nombre_autor"]["value"]
    #df_nombre_autor.insert(my_nombre)
    my_titulo = hit["titulo"]["value"]
    #print(my_nombre + "|" + my_autor)
    #df.loc[1]=[ my_nombre, my_autor ]
    #df_autor_titulo = df.append(my_nombre, my_autor,ignore_index=True)
    #d_parcial = {contador, my_autor, my_titulo}
    #d_parcial = {"id":[],"autor":[],"titulo":[]};

    ##@d_parcial = {"id":[],"autor":[],"titulo":[]}
    ##d_parcial["id"].append(contador)
    ##d_parcial["autor"].append(my_autor)
    ##d_parcial["titulo"].append(my_titulo)
    ##data.update(d_parcial)

    if (contador == 1):
        #data = {['autor', my_autor], ['titulo', my_titulo]}
        data = {'autor':my_autor, 'titulo':my_titulo}
###        results_df = pd.DataFrame()
        results_df = results_df.append(data, ignore_index=True)
    else:
        data_row = {'autor':my_autor, 'titulo':my_titulo}
        #print(data_row)
        results_df = results_df.append(data_row, ignore_index=True)
    #print(d_parcial)
    #print('d_parcial')
    #print(d_parcial)

    contador  = contador + 1
    #print(contador)
    #data = [ ['autor', my_nombre], ['titulo', my_autor]]

#print(results_df)
#makes = results_df['autor'].drop_duplicates()
#make_choice = st.sidebar.selectbox('Seleccion de autores:', makes)


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
    makes_titulo = results_df['titulo']
    #make_choice_titulo = st.sidebar.selectbox('Seleccion de titulo:', makes_titulo)
    make_choice_titulo = st.selectbox('Seleccion de titulo:', makes_titulo)
#print('make_choice: ' + make_choice)
    print('make_choice_titulo: ' + make_choice_titulo)
#print(results_df.loc[results_df['titulo'].isin(make_choice_titulo)])
#print(results_df.loc[results_df['titulo'] == make_choice_titulo]['autor'])

#st.line_chart(results_df.loc[results_df['titulo'] == make_choice_titulo]['autor'])
    var_autor = results_df.loc[results_df['titulo'] == make_choice_titulo]['autor']
    #print(var_autor)
    var_autor1 = extraer_nombre(str(var_autor))
    st.text("Autor: " + var_autor1)
    st.text("Obras del mismo autor:")


    #st.text(var_autor1)
    query_sobre_titulo(var_autor1, st)

#results_df = pd.io.json.json_normalize(results['results']['bindings'])
#results_df[['item.value', 'itemLabel.value']]
#df = pd.DataFrame(data ,columns = ['id', 'autor' , 'titulo'])
#print(df)
