import io
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import streamlit as st

# interact with FastAPI endpoint
backend = "http://fastapi:8000/explorer"

sparql = SPARQLWrapper("https://mired.uspceu.es/sparql")

sparql.setQuery("""
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>
    select distinct ?uri where { graph ?uri { ?s a ?t } }
""")

sparql.setReturnFormat(JSON)
result = sparql.query().convert()

def app():
    st.title('Grafos disponibles:')
    for hit in result["results"]["bindings"]:

        #print(hit["Concept"]["value"])
        st.write(hit["uri"]["value"])
