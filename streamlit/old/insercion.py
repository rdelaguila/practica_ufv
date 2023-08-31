import io
import pandas as pd
import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import csv
import streamlit as st
import os
from os import remove

# interact with FastAPI endpoint
#backend = "http://0.0.0.0:8000/insercion"
backend = "http://fastapi:8000/insercion"
#backend = "http://fastapi:8000/datos"

def process(file,texto, server_url:str, st):
    #curl -X POST "http://0.0.0.0:8000/insercion?name=MYTEST" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@expresiones_regulares2.py;type=text/x-python"

    m = MultipartEncoder(fields={"file": ("filename", file, "text/plain"),"name":texto})
    #print(m.to_string())
    #st.write(m.to_string())
    r = requests.post(server_url, data = m, headers = {"Content-Type": m.content_type}, timeout=60)
    #st.write("requests " + r.to_string())
    return r


def process2(file,server_url:str, st):
    #curl -X POST "http://0.0.0.0:8000/insercion?name=MYTEST" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@expresiones_regulares2.py;type=text/x-python"
    #curl -X POST "http://0.0.0.0:8000/insercion?name=aA" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@expresiones_regulares2.py;type=text/x-python"
    #curl -X POST "http://0.0.0.0:8000/insercion?name=aa" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@explorador_autores.py;type=text/x-python"

    #file=@expresiones_regulares2.py;type=text/x-python"

    #fields={
    #"file": ("filename", file, "text/plain"
    #"name":texto
    #}

    #m = MultipartEncoder(fields={"name":name, "file": ("filename", file, "text/plain")})
    #m = MultipartEncoder(fields={"name":name, "file": ("filename", file, "text/x-python")})
    #m = MultipartEncoder([("name", name),("file", file)])
    m = MultipartEncoder({file.name: file})

    #print(m.to_string())
    #st.write(m.to_string())
    #st.write(m.content_type)
    st.write("server_url: " + str(server_url))
    st.write("m.content_type: " +  str(m.content_type))
    st.write("m.to_string(): " + str(m.to_string()))
    #r = requests.post(server_url, data = m, headers = {"Content-Type": m.content_type}, timeout=60, verify=False)
    #r = requests.post(server_url, data = m, headers = {'Content-Type': 'application/octet-stream', 'accept': 'application/json'})
    r = requests.post(server_url, data = m, headers = {'Content-Type': 'multipart/form-data', 'accept': 'application/json'})

    #r = requests.post(server_url, data = m, headers = {'Content-Type': m.content_type})
    st.write("requests " + r.text)
    return r

def app():
    st.title('Insercion nuevo Microrelato')
    #st.write('mostramos 1')
    #form = st.form(key = 'my-form')

    nombre = st.text_input(label = 'Nombre')
    apellidos = st.text_input(label = 'Apellidos')
    titulo = st.text_input(label = 'Titulo')
    pais = st.text_input(label = 'Pais')


    submit = st.button('Enviar datos')
    if submit:
        #if (nombre.find("") == -1)  & (apellidos.find("") == -1) & (titulo.find("") == -1)  & (pais.find("") == -1) :
        if (len(nombre) > 0)  and (len(apellidos) > 0) and (len(titulo) > 0)  and (len(pais) > 0) :
            st.success("Validacion todos los datos OK")
            ###data = {}
            ###results_df = pd.DataFrame()
            ###data = {'Nombre':nombre, 'Apellidos':apellidos, 'Titulo':titulo, 'Pais':pais}
            ###results_df = results_df.append(data, ignore_index=True)
            ###s_buf = io.StringIO()
            ###results_df.to_csv(s_buf)
            text = 'Nombre;Apellidos;Titulo;Pais'+ '\n' + nombre + ';' + apellidos + ';' + titulo + ';' + pais
            st.write(text)
            if(os.path.isfile('salida.csv')):
                remove('salida.csv')
            myFile = open('salida.csv', 'w')
            myFile.write(text)
            myFile.close()
            myFile2 = open('salida.csv', 'rb')
            st.success("Enviando Fichero al servidor")
            #process(s_buf, "out.csv", backend, st)
            process2(myFile2, "http://fastapi:8000/insercion", st)

            st.success("Fichero enviado al servidor OK")
        else:
            st.warning("Rellene todos los campos")
            #st.warning("Rellene todos los campos " + nombre + " " + str(len(nombre)) + " " + apellidos + " " + str(len(apellidos)) + " " + titulo + " " + str(len(titulo)) + " " + pais + str(len(pais)))
        #request.post('http://127.0.0.1/letters', json=new_candidates)


        #results_df.to_csv("Escritura.csv")
