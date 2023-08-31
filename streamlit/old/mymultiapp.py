import streamlit as st
from multiapp import MultiApp

class MyMultiApp (MultiApp):
    def __init__(self) -> None:
        super().__init__()
    def run (self,state):
        app = st.sidebar.radio(
            'Go To',
            self.apps,
            format_func=lambda app: app['title'])

        app['function'](state)
