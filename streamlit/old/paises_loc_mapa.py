from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
import altair as alt
import datetime
from matplotlib.figure import Figure
from bokeh.plotting import figure
#print('hola')

from pandas import json_normalize

def llenar_un_array(myarray2, texto_nuevo):
    myarray2.append(texto_nuevo)
    return myarray2

def download_data ():
    sparql = SPARQLWrapper("https://mired.uspceu.es/sparql")

    # Query for the description of "Capsaicin", filtered by language
    sparql.setQuery("""
            prefix mcr: <https://mired.uspceu.es/microrrelatos#>
    select ?titulo , ?nombre_autor, ?anno, ?list_pais {
            ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
            ?uri_microrrelato rdfs:label ?titulo .
    ?uri_autor rdfs:label ?nombre_autor .
            ?uri_microrrelato mcr:tieneMedioDigitalDePublicacion ?medio .

    ?medio mcr:annoDeInicio ?anno.

            ?uri_autor rdfs:label ?nombre_autor .
            ?uri_microrrelato rdfs:label ?titulo .
            ?uri_autor mcr:tienePais ?mypersona .
            ?mypersona rdfs:label ?list_pais
        }

        """)

    sparql.setQuery("""

prefix mcr: <https://mired.uspceu.es/microrrelatos#>

    select distinct ?titulo , ?nombre_autor, ?list_pais {
            ?uri_microrrelato mcr:esObraArtisticaCreadaPor ?uri_autor .
            ?uri_microrrelato rdfs:label ?titulo .
            ?uri_autor rdfs:label ?nombre_autor .
            ?uri_autor rdfs:label ?nombre_autor .
            ?uri_microrrelato rdfs:label ?titulo .
            ?uri_autor mcr:tienePais ?mypersona .
            ?mypersona rdfs:label ?list_pais
        }

        """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    resultado = json_normalize(result["results"]["bindings"])

    # The return data contains "bindings" (a list of dictionaries)
    ###simple_table = resultado[["titulo.value", "nombre_autor.value", "anno.value", "list_pais.value"]]
    ###simple_table.columns = ["titulo", "nombre_autor", "anno", "nombre"]
    simple_table = resultado[["titulo.value", "nombre_autor.value", "list_pais.value"]]
    simple_table.columns = ["titulo", "nombre_autor", "nombre"]
    info_paises = pd.read_csv('catalogo_paises.csv')
    resultado = simple_table.merge(info_paises, how='left', on='nombre')
    return resultado

#def df_filter(message = 'Selecciona los campos para filtrar el dataframe',df):


#    return filtered_df

def app():

    myarray = []
    myarray_valores = []
    myarray_rep = []
    str_tmp = ""
    # Specify the DBPedia endpoint


    res = download_data()
    res.to_csv('mierdecilla2')
    df_merged = res
    df_merged.to_csv('mierdecilla3')
    data = {}
    data2 = {}
    data3 = {}
    data4 = {}

    contador = 1
    metrics = ['nombre','nombre_autor']


    with st.beta_container():
        col1,col2 = st.beta_columns(2)
        cols = col1.selectbox('Seleccionar dimension para ver', metrics)

        # let's ask the user which column should be used as Index
        if cols in metrics:
            metric_to_show_in_covid_Layer = cols

        # bar chart
        # if metric_to_show_in_covid_Layer == 'nombre_autor':
        conteo_paises = df_merged.groupby(metric_to_show_in_covid_Layer).count()
        # else:
        #     conteo_paises = df_merged.groupby(metric_to_show_in_covid_Layer ).count()
        conteo_paises.to_csv('mierdecilla')
        conteo_paises = conteo_paises[['iso']]
        conteo_paises.columns = ['count']
        conteo_paises.reset_index()
        filter_data = conteo_paises

        col1.markdown("Numero de microrrelatos x pais")
        col2.bar_chart(filter_data[['count']])
        
        # simple_table[(simple_table['anno'] >= '2000')].set_index("anno")


        ########################################################################################
        #   WIDGETS
    with st.beta_container():

        subset_data = df_merged

            ### MULTISELECT
        country_name_input = st.multiselect(
            'Country name',
            df_merged.groupby('nombre').count().reset_index()['nombre'].tolist())

        # by country name
        if len(country_name_input) > 0:
            subset_data = df_merged[df_merged['nombre'].isin(country_name_input)]

        ########################################################################################
        ## linechart

        view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2, )

        # Create the scatter plot layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=subset_data,
            pickable=False,
            opacity=0.3,
            stroked=True,
            filled=True,
            radius_scale=10,
            radius_min_pixels=5,
            radius_max_pixels=60,
            line_width_min_pixels=1,
            get_position=["longitude", "latitude"],

            get_radius=metric_to_show_in_covid_Layer,
            get_fill_color=[252, 136, 3],
            get_line_color=[255, 0, 0],
            tooltip="test test",
        )

        # Create the deck.gl map
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view,
            map_style="mapbox://styles/mapbox/light-v10",
        )

        # Create a subheading to display current date
        subheading = st.subheader("")

        # Render the deck.gl map in the Streamlit app as a Pydeck chart
        map = st.pydeck_chart(r)

