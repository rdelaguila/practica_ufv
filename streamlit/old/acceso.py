
import Analisis_de_transacciones
import streamlit as st
from multiapp import MultiApp
import requests
import time 
#PAGES = {
#    "Formulario": form,
#    "Mostramos": show,
##    "Grafos": grafos,
#    "Pertenencia Grafos": pertenencia_grafos,
#    "Explorador de Conceptos": explorer,
#    "Explorador de Autores": myformulario,
#    "Explorador de titulos": explorador_autores,
#    "Explorador de paises": explorador_paises,
#    "Insercion": insercion,
#}

#st.sidebar.title('Navegar')
#selection = st.sidebar.radio("Go to", list(PAGES.keys()))
#page = PAGES[selection]
#page.app()



def run ():
    with st.spinner('MiRed engine: iniciando sistema'):
        time.sleep(2)
    st.success('Vamos!')
    #import streamlit.components.v1 as components  # Import Streamlit

    # Render the h1 block, contained in a frame of size 200x200.
    #components.html("<html><body><h1>Hello, World</h1></body></html>", width=200, height=200)



    app.run(True)




