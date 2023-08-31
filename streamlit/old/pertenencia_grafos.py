import io
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import streamlit as st1

# interact with FastAPI endpoint
backend = "http://fastapi:8000/pertenencia_grafos"

sparql = SPARQLWrapper("https://mired.uspceu.es/sparql")

sparql.setQuery("""
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>
    select distinct ?g ?type where { graph ?g { ?x a ?type. } } limit 100
""")

sparql.setReturnFormat(JSON)
result = sparql.query().convert()
def app():
    data = {}
    results_df = pd.DataFrame()
    st1.title('Grafos disponibles:')
    for hit in result["results"]["bindings"]:

        #print(hit["Concept"]["value"])
        #st.write(hit["g"]["value"] + hit["type"]["value"])
        data = {'grafo':hit["g"]["value"], 'tipo':hit["type"]["value"]}
        results_df = results_df.append(data, ignore_index=True)
        #st.write(hit["type"]["value"])
    #chart = st1.write(results_df)
    #st1.dataframe(results_df)
    st1.table(results_df)
