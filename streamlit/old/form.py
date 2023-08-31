import io

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import streamlit as st


def app():
    st.title('Formulario')
    st.write('Welcome to formulario')

    backend = "http://fastapi:8000/datos"

    def process(file,texto, server_url: str):

        m = MultipartEncoder(fields={"file": ("filename", file, "text/plain"),
                                     "name":texto})
        print(m.to_string())
        r = requests.post(
            server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
        )

        return r

    # construct UI layout
    st.title("Introduccion de nombre de usuario y mando un archivo")

    st.write(
        """Vamos a poner un ejemplo a ver si va bien"""
    )  # description and instructions


    uploaded_file = st.file_uploader("insert file")  # image upload widget
    name = st.text_input("What's your name?")

    if st.button("Get segmentation map"):

        # col1, col2 = st.beta_columns(2)

        if uploaded_file and name:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type,
                            "FileSize": uploaded_file.size}
            st.write(uploaded_file)
            st.write(name)
            segments = process(uploaded_file,name, backend)
            json_data = json.loads(segments.text)
            st.write(json_data)



        else:
            # handle case with no image
            st.write("Insert an image!")

