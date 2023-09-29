# Práctica final programación II


    Este ejemplo lo he adaptado de la documentación oficial de [streamlit.io](https://streamlit.io), 
    de su [documentación](https://docs.streamlit.io) y de un proyecto de investigación. Se usa para visualizar datos
    en forma de dashboard, aunque también tiene capacidad para hacer apps web de tipo CRUD con un `backend` como [fastapi](https://fastapi.tiangolo.com).
    
    Ojo, este ejemplo es un punto de partida para vosotros, pero ni es visual, ni cuenta una historia. Lo siento, pero os pido mucho más.
    
    Lo he montado como un dashboard con multiapp. Las páginas están bajo el directorio `pages`. Si quieres añadir más páginas, añade más páginas. Pero 
    también podrías montar un dashboard sin necesidad de que sea multipágina. 
    
    En la página principal voy a volcar todo el contenido de un dataframe. Esto no debería hacerse así, sobretodo si el conjunto de datos es muy grande. 
    Es más, puedes gestionar datos desde `streamlit` (app monolítica), pero
    ya hemos visto que una arquitectura basada en microservicios tiene ciertas ventajas sobre  una app monolítica.
    
    Además, os he subido un par de presentaciones dentro de la carpeta 'doc' y código para que veais cómo se usa sqlalchemy dentro de la carpeta sqlalchemy.
    De esta documentación, nosotros veremos en clase la presentación de introducción a los contenedores.

    La fecha límite de entrega de la práctica es el viernes 15 de diciembre 23:59 horas.
    Tendréis que hacer un fork del repositorio y crear una carpeta con vuestro nombre donde esté el código e instrucciones de ejecución de vuestra práctica, así
    como una memoria exponiendo lo que se ha realizado, la fuente de datos y qué se pretende analizar. La entrega se hará mediante pull request.  

    La práctica os la voy a evaluar del siguiente modo:
    
    1. Para tener un apto (5) deberéis buscar un conjunto de datos, documentarlo, y hacer un dashboard. La nota puede llegar a 6 en función de 
       que lo que me quieras contar se entienda bien con el dashboard que me muestras. 
    2. Para llegar al 7, deberá tener gráficos de tipo interactivos.
    3. Para llegar al 8, en el backend deberá tener un método post, que tenga sentido.
    4. Para llegar al 9, deberás utilizar una jerarquía de clases con BaseModel y, además, hacer una adecuada gestión de errores: excepciones y logs.
    5. Para llegar al 10, deberías utilizar una base de datos en un servicio adicional. 
    6. Me haría muy feliz si utilizaseis un ORM como SQLAlchemy.
   
    A por ello! 💪💪💪
