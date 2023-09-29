# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    Base = automap_base()

    dbname = 'recetas.db'
    engine = create_engine('sqlite:///' + dbname)
    session = Session(engine)

    Base.prepare(autoload_with=engine)

    Receta = Base.classes.receta
    Ingrediente = Base.classes.ingrediente
    Relacion = Base.classes.receta_ingrediente

    session.add(Ingrediente(nombre="tomate", IDINGREDIENTE=1))
    session.add(Ingrediente(nombre="pasta", IDINGREDIENTE=2))
    session.add(Receta(nombre="Macarron con tomate", IDRECETA=1))
    session.add(Relacion(id=1,IDRECETA=1, IDINGREDIENTE=1, CANTIDAD=10))
    session.add(Relacion(id=2,IDRECETA=1, IDINGREDIENTE=2, CANTIDAD=42))

    session.commit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
