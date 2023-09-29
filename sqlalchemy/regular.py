from data.recetas import  *
from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import logging


if __name__ == '__main__':
    try:
        dbname = 'recetas.db'
        engine = create_engine('sqlite:///' + dbname,echo=True)
        with Session(engine) as session:

            receta = Receta( nombre='pollo al chilindron')
            ingrediente1 = Ingrediente( nombre='chilindron')
            rel1 = RecetaIngrediente(IDINGREDIENTE=4, IDRECETA=2, CANTIDAD=1)
            rel2 = RecetaIngrediente(IDINGREDIENTE=6, IDRECETA=2, CANTIDAD=2)

            session.add_all([receta,  ingrediente1, rel1, rel2])
            session.commit()

            logging.info("success calling db func: " + func.__name__)
    except Exception as e:
        logging.error(e.args)
        session.rollback()
    finally:
        session.close()

