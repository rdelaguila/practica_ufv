import io
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import streamlit as st
#nombre y apellidos
# interact with FastAPI endpoint
backend = "http://fastapi:8000/myformulario"

sparql = SPARQLWrapper("https://mired.uspceu.es/sparql")

sparql.setQuery("""
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>
    select distinct ?nombre{
    ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?autor .
    ?autor rdfs:label ?nombre .
    }
""")

sparql.setQuery("""
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>
    select distinct ?nombre_autor{
    ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
    ?uri_autor rdfs:label ?nombre_autor .
    ?uri_microrrelato rdfs:label ?titulo
    }
""")


sparql.setQuery("""
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>
    select distinct ?nombre_autor ?titulo{
    ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
    ?uri_autor rdfs:label ?nombre_autor .
    ?uri_microrrelato rdfs:label ?titulo
    }
""")
sparql.setQuery("""
    prefix mcr: <https://mired.uspceu.es/microrrelatos#>
    select distinct ?nombre_autor{
    ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
    ?uri_autor rdfs:label ?nombre_autor .
    }
""")


sparql.setReturnFormat(JSON)
result = sparql.query().convert()

def app():
    st.title('Autor')
    for hit in result["results"]["bindings"]:

        #print(hit["Concept"]["value"])
        st.write(hit["nombre_autor"]["value"])
        #print(str(hit["nombre_autor"]["value"]) + ";" + str(hit["titulo"]["value"]))
