import shutil

import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile,Form
import pandas as pd
from typing import  List

from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Salaries(BaseModel):
    QB:int
    RB:int
    WR:int
    TE:int
    OL:int
    Offense:int
    IDL:int
    EDGE:int
    LB:int
    S:int
    CB:int
    Defense:int
    Team:str
    Year:int


class SalaryList(BaseModel):
    salaries = List[Salaries]

app = FastAPI(
    title="NFL",
    description="""Análisis de la relación entre el gasto en salarios y el éxito en la NFL""",
    version="0.1.0",
)


@app.get("/retrieve_data/")
#def insercion_endpoint (titulo:str = Form(...), autor:str=Form(...), pais:str=Form(...),genero:str=File(...),  archivo: UploadFile=File(...)):
def retrieve_data ():
    todosmisdatos = pd.read_csv('nfl.csv', sep=',')
    todosmisdatos = todosmisdatos.fillna(0)
    todosmisdatosdict = todosmisdatos.to_dict(orient='records')
    listado = SalaryList()
    listado.salaries = todosmisdatosdict
    return listado
