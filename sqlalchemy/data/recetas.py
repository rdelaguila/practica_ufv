from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

#sqlacodegen sqlite:///recetas.db

class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    IDINGREDIENTE = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String(100))


class Receta(Base):
    __tablename__ = 'receta'

    IDRECETA = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String(100))


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class RecetaIngrediente(Base):
    __tablename__ = 'receta_ingrediente'

    id = Column(Integer, primary_key=True)
    IDINGREDIENTE = Column(ForeignKey('ingrediente.IDINGREDIENTE'))
    IDRECETA = Column(ForeignKey('receta.IDRECETA'))
    CANTIDAD = Column(Integer, nullable=False)

    ingrediente = relationship('Ingrediente')
    receta = relationship('Receta')
