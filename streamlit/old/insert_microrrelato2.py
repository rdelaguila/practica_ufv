import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import streamlit as st


def app(state):
    st.title('Formulario')
    st.write('Welcome to formulario')

    backend = "http://fastapi:8000/insercion" #Esta URL meterla en un parámetro de configuración

    def process( id, apellidos_gs,nombre_gs,genero_gn,clase_medio_digital_de_publicacion_gs,nombre_del_medio_digital_de_publicacion_gs,direccion_txt,inicio_fin_dr,presencia_de_minificcion_gs,pueblo_gs,ciudad_de_origen_gs,pais_1_gs,codigo_pais_1_gs,pais_2_gs,codigo_pais_2_gs,funcion_de_la_imagen_txt,audio_video_b,titulo_del_microrrelato_gs,tipologia_gs,titulo_de_publicacion_impresa_gs,datos_editorial_gs, archivo, server_url: str):

        multipart_data = MultipartEncoder(
            fields={
                # a file upload field
                # plain text fields
                ##'titulo': titulo,
                ##'autor': autor,
                ##'pais':pais,
                ##'genero':genero,
                'id': id,
                'apellidos_gs': apellidos_gs,
                'nombre_gs': nombre_gs,
                'genero_gn': genero_gn,
                'clase_medio_digital_de_publicacion_gs': clase_medio_digital_de_publicacion_gs,
                'nombre_del_medio_digital_de_publicacion_gs': nombre_del_medio_digital_de_publicacion_gs,
                'direccion_txt': direccion_txt,
                'inicio_fin_dr': inicio_fin_dr,
                'presencia_de_minificcion_gs': presencia_de_minificcion_gs,
                'pueblo_gs': pueblo_gs,
                'ciudad_de_origen_gs': ciudad_de_origen_gs,
                'pais_1_gs': pais_1_gs,
                'codigo_pais_1_gs': codigo_pais_1_gs,
                'pais_2_gs': pais_2_gs,
                'codigo_pais_2_gs': codigo_pais_2_gs,
                'funcion_de_la_imagen_txt': funcion_de_la_imagen_txt,
                'audio_video_b': audio_video_b,
                'titulo_del_microrrelato_gs': titulo_del_microrrelato_gs,
                'tipologia_gs': tipologia_gs,
                'titulo_de_publicacion_impresa_gs': titulo_de_publicacion_impresa_gs,
                'datos_editorial_gs': datos_editorial_gs,

            #'archivo': (titulo + '.txt', archivo, 'text/plain'),
            'archivo': (id + '.txt', archivo, 'text/plain'),
            }
        )

        r = requests.post(
            server_url, data=multipart_data, headers={"Content-Type": multipart_data.content_type}, timeout=8000
        )

        return r

    with streamlit.old.form(key='Formulario de entrada de microrrelato'):
        ##text_input = st.text_input(label='Titulo')
        ##text_input2 = st.text_input(label='Autor')
        ##text_input3 = st.text_input(label='Pais')
        ##text_input4 = st.text_input(label='Genero')
        text_input1 = "0"
        #text_input1 = st.text_input(label='id')
        text_input2 = st.text_input(label='Apellidos')
        text_input3 = st.text_input(label='Nombre')
        ##text_input4 = st.text_input(label='Género')
        text_input4 = st.selectbox('Género',('mujer','hombre'))
        ##text_input5 = st.text_input(label='Medio Digital de Publicación')
        text_input5 = st.selectbox('Medio Digital de Publicación', ('Blog','Facebook','Twitter','Instragram','Libro','YouTube','Revista impresa','Cortometraje','Remediación audivisual','Revista digital','Espacio televisivo en Youtube','Espacio radiofónico en Facebook',
'Espacio radiofónico','Taller digital'))
        text_input6 = st.text_input(label='Nombre Medio Digital de Publicación')
        text_input7 = st.text_input(label='Dirección')
        text_input8 = st.text_input(label='Inicio-Fin')
        text_input9 = st.text_input(label='Presencia de minificción')
        text_input10 = st.text_input(label='Pueblo')
        text_input11 = st.text_input(label='Ciudad de Origen')
        text_input12 = st.text_input(label='País')
        text_input13 = st.text_input(label='Código País')
        text_input14 = st.text_input(label='País 2')
        text_input15 = st.text_input(label='Código País 2')
        text_input16 = st.text_input(label='Funcion de la imagen')
        text_input17 = st.text_input(label='Audio o Video')
        text_input18 = st.text_input(label='Título del microrrelato')
        ##text_input19 = st.text_input(label='Tipología')
        text_input19 = st.selectbox('Tipología',('Texto + Fotografía','Texto + Video','Audiomicrorrelato','Texto + Dibujo infantil','Texto + Ilustración','Texto + Fotografía de pintura','Ilustración con microrrelato insertado','Creeypasta','Texto + Meme','Recreación audiovisual','Lámina ilustrada','Cuentometraje','Texto + hiperenlace','Texto + Dibujo','Texto + Dibujo Lápiz','Texto + Tinta china sobre papel algodón e hilo rojo','Videominificción','Texto + Fotografía de la portada de libro','Texto + Pintura','Texto + Fotografía de portada de revista','Texto + Fotografía de cuadro','Texto + Ilustración','Texto + Vídeo','Texto + Audio ReC','Texto + Fotografía + Audio','Microrrelato visual animado'))
        text_input20 = st.text_input(label='Título de publicacion impresa')
        text_input21 = st.text_input(label='Datos Editorial')
        uploaded_file = st.file_uploader("insert file")

        submit_button = st.form_submit_button(label='Submit')

        #if submit_button and uploaded_file and text_input  and text_input2 and text_input3 and text_input4:
        if submit_button and uploaded_file and text_input1:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type,
                            "FileSize": uploaded_file.size}
            st.write(uploaded_file)
            st.write(text_input1)
            st.write(text_input2)
            st.write(text_input3)
            st.write(text_input4)
            st.write(text_input5)
            st.write(text_input6)
            st.write(text_input7)
            st.write(text_input8)
            st.write(text_input9)
            st.write(text_input10)
            st.write(text_input11)
            st.write(text_input12)
            st.write(text_input13)
            st.write(text_input14)
            st.write(text_input15)
            st.write(text_input16)
            st.write(text_input17)
            st.write(text_input18)
            st.write(text_input19)
            st.write(text_input20)
            st.write(text_input21)
            #segments = process(text_input, text_input2,text_input3,text_input4, uploaded_file,  backend)
            segments = process(text_input1, text_input2,text_input3,text_input4,text_input5,text_input6,text_input7,text_input8,text_input9,text_input10,text_input11,text_input12,text_input13,text_input14,text_input15,text_input16,text_input17,text_input18,text_input19,text_input20,text_input21, uploaded_file,  backend)
            json_data = json.loads(segments.text)
            st.write(json_data)

        else:
            # handle case with no image
            st.write("Insert an input!")