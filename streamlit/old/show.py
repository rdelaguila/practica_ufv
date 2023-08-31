import io

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import streamlit as st

# interact with FastAPI endpoint
backend = "http://fastapi:8000/show"

def app():
    st.title('Mostramos')
    st.write('mostramos 1')
