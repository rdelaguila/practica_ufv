import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Establecer un fondo de página atractivo
st.set_page_config(
    page_title="Dashboard NFL",
    layout="wide")

# Importar los datos desde el archivo CSV
@st.cache_data
def load_data(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    mijson = r.json()
    listado = mijson['salaries']
    df = pd.DataFrame.from_records(listado)
    return df

df_merged = load_data('http://fastapi:8000/retrieve_data')

# Título principal
st.markdown("<h1 style='text-align: center; color: #4EBAE1;'>Salarios NFL</h1>", unsafe_allow_html=True)

# Subtítulo
st.subheader("Análisis visual del gasto total en salarios por posición de la liga nacional de futbol americano de los "
             "Estados Unidos (NFL) en la última década y la posible relación con el éxito.")

# Espaciado para mejorar la presentación
st.markdown("<br>", unsafe_allow_html=True)

# Texto explicativo
st.write("Datos interesantes:")

# Melt para transformar el formato de los datos
df_nfl = pd.melt(df_merged, id_vars=['Team', 'Year'], var_name='Position', value_name='Dollars')

# Convertir 'Position' a tipo de datos ordinal
df_nfl['Position'] = pd.Categorical(df_nfl['Position'], categories=df_nfl['Position'].unique(), ordered=True)
# Crear un dataframe sin las posiciones 'offense'y 'defense' ya que son el agregado del resto de posiciones
df_nfl_no_off_def = df_nfl[~df_nfl['Position'].isin(['Offense', 'Defense'])]


# Dividir la pantalla en dos columnas
col1, col2 = st.columns(2)

# Columna 2
with col1:
    # Encontrar el top 3 de equipos que han invertido más dinero
    st.markdown(
        "<p style='font-size: 18px; color: #4EBAE1;'><strong>Top 3 de Equipos que mas dinero han invertido:</strong></p>",
        unsafe_allow_html=True)
    top_teams = df_nfl.groupby('Team')['Dollars'].sum().nlargest(3)
    for team, spending in top_teams.items():
        st.write(f"  - {team}: ${spending:,.2f}")

    # Encontrar el top 3 de equipos que han invertido más dinero
    st.markdown(
        "<p style='font-size: 18px; color: #4EBAE1;'><strong>Top 3 de Equipos que menos dinero han invertido:"
        "</strong></p>",unsafe_allow_html=True)
    top_teams = df_nfl.groupby('Team')['Dollars'].sum().nsmallest(3)
    for team, spending in top_teams.items():
        st.write(f"  - {team}: ${spending:,.2f}")
# Columna 2
with col2:
    # Encontrar el top 3 de posiciones que han tenido el salario más alto
    top_positions = df_nfl_no_off_def.groupby('Position')['Dollars'].sum().nlargest(3)
    st.markdown(
        "<p style='font-size: 18px; color: #4EBAE1;'><strong>Top 3 de Posiciones con Salario más Alto:</strong></p>",
        unsafe_allow_html=True)
    for position, spending in top_positions.items():
        st.write(f"  - {position}: ${spending:,.2f}")

    # Encontrar el top 3 de posiciones que han tenido el salario más bajo
    top_positions = df_nfl.groupby('Position')['Dollars'].sum().nsmallest(3)
    st.markdown(
        "<p style='font-size: 18px; color: #4EBAE1;'><strong>Top 3 de Posiciones con Salario más Bajo:</strong></p>",
        unsafe_allow_html=True)
    for position, spending in top_positions.items():
        st.write(f"  - {position}: ${spending:,.2f}")


# Espaciado para mejorar la presentación
st.markdown("<br>", unsafe_allow_html=True)

# Gráfico 1 interactivo con Plotly Express con todos los gastos
st.markdown(
        "<p style='font-size: 18px; color: #4EBAE1;'><strong>Gasto Total por Año y Equipo</strong></p>",
        unsafe_allow_html=True)
fig = px.bar(df_nfl, x='Year', y='Dollars', color='Team')
st.plotly_chart(fig, use_container_width=True)

# Texto explicativo
st.write("""
En esta grafica interactiva se puede apreciar el incremento del dinero invertido en los jugadores por todos los 
equipos de la liga, llegando a practicamente duplicar la cantidad en tan solo una década. Tambien cabe resaltar 
el bajón del dinero invertido después del COVID (2021) y su sorprendete aumento el posterior año.
""")

# Espaciado para mejorar la presentación
st.markdown("<br>", unsafe_allow_html=True)

# Grafico 2
st.markdown(
        "<p style='font-size: 18px; color: #4EBAE1;'><strong>Variación de los Salarios de jugadores ofensivos y "
        "defensivos:</strong></p>",unsafe_allow_html=True)
st.write("""
El fútbol americano es diferente a todos los deportes ya que los equipos utilizan a diferentes jugadores y alineaciones 
para atacar y para defender, por lo tanto la defensa de un equipo no tiene nada que ver con el ataque y viceversa, ya 
que nunca estarán en el campo a la vez. 
""")
# Filtrar solo las posiciones 'Offense' y 'Defense'
offense_data = df_nfl[df_nfl['Position'] == 'Offense']
defense_data = df_nfl[df_nfl['Position'] == 'Defense']
# Agrupar por año y calcular la suma de los salarios en 'Offense' y 'Defense'
sum_offense_salary_by_year = offense_data.groupby('Year')['Dollars'].sum().reset_index()
sum_defense_salary_by_year = defense_data.groupby('Year')['Dollars'].sum().reset_index()
# Crear un gráfico de barras lado a lado
fig1 = px.bar(
    pd.concat([sum_offense_salary_by_year, sum_defense_salary_by_year], keys=['Offense', 'Defense']),
    x='Year',
    y='Dollars',
    color=pd.concat([sum_offense_salary_by_year, sum_defense_salary_by_year], keys=['Offense', 'Defense']).index.get_level_values(0),
    title='',
    labels={'Dollars': 'Suma de Salarios'},
)
# Configuraciones del diseño
fig1.update_layout(
    barmode='group',
    xaxis_title='Año',
    yaxis_title='Suma de Salarios',
)
# Mostrar el gráfico
st.plotly_chart(fig1, use_container_width=True)

# Texto explicativo
st.write("""
Esta gráfica de barras muestra el gasto de todos los equipos de la liga separado en jugadores ofensivos y defensivos.
Se puede observar una tendencia común en la liga invirtiendo más dinero en el ataque que en la defensa. Y al igual que 
en la gráfica anterior, se muestra tanto la tendencia creciente del gasto de los equipos, como el bajón post-COVID y su 
incremento sustancial el siguiente año.
""")
# Espaciado para mejorar la presentación
st.markdown("<br>", unsafe_allow_html=True)

# Grafico 3
st.markdown(
        "<p style='font-size: 18px; color: #4EBAE1;'><strong>Comparación entre el equipo que más invirtió ese año y los "
        "equipos exitosos""</strong></p>",unsafe_allow_html=True)
# Obtener los ganadores, finalistas y semi-finalistas de cada año
superbowl_data = {
    'Year': [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'Winner': ['Seahawks', 'Patriots', 'Broncos', 'Patriots', 'Eagles', 'Patriots', 'Chiefs', 'Buccaneers', 'Rams', 'Chiefs','-'],
    'Finalist': ['Broncos', 'Seahawks', 'Panthers', 'Falcons', 'Patriots', 'Rams', '49ers', 'Chiefs', 'Bengals', 'Eagles','-'],
    'SemiFinalist1': ['49ers', 'Colts', 'Cardinals', 'Patriots', 'Vikings', 'Saints', 'Titans', 'Packers', 'Chiefs', 'Bengals','-'],
    'SemiFinalist2': ['Patriots', 'Packers', 'Patriots', 'Steelers', 'Jaguars', 'Chiefs', 'Packers', 'Bills', '49ers', '49ers','-'],
}
# Crear un DataFrame con los datos de la Super Bowl
superbowl_df = pd.DataFrame(superbowl_data)
# Agrupar por año y equipo, y calcular la suma de los salarios
sum_salary_by_team_year = df_nfl.groupby(['Year', 'Team'])['Dollars'].sum().reset_index()
# Encontrar el equipo que más gastó cada año
team_with_max_salary_by_year = sum_salary_by_team_year.loc[sum_salary_by_team_year.groupby('Year')['Dollars'].idxmax()]
# Unir los DataFrames para incluir información de la Super Bowl
comparison_table = pd.merge(team_with_max_salary_by_year, superbowl_df, how='left', on='Year')
# Crear un gráfico de tabla interactiva con Plotly
fig2 = go.Figure(data=[go.Table(
    header=dict(values=['Año', 'Equipo que más gastó', 'Ganador', 'Finalista', 'Semi-Finalista 1', 'Semi-Finalista 2']),
    cells=dict(values=[comparison_table['Year'], comparison_table['Team'],comparison_table['Winner'],
                       comparison_table['Finalist'],comparison_table['SemiFinalist1'], comparison_table['SemiFinalist2']])
)])
# Mostrar el gráfico interactivo
st.plotly_chart(fig2, use_container_width=True)

# Texto explicativo
st.write("""
Con el fin de estudiar la relación entre el gasto de dinero de los equipos en sus jugadores y el éxito de los mismos,
esta tabla muestra el equipo que gastó más dinero en salarios ese año y los últimos cuatro equipos en el torneo. Como
se puede apreciar, el único caso donde el equipo que más gastó en salarios, ganó la superbowl ese mismo año y quedó
segundo el año siguiente es el de los Seahawks, no obstante el resto de años no se puede apreciar una relación directa
entre los mismos.
""")
# Espaciado para mejorar la presentación
st.markdown("<br>", unsafe_allow_html=True)

# Gráfico 4
st.markdown(
        "<p style='font-size: 18px; color: #4EBAE1;'><strong>Gasto promedio por posición""</strong></p>",
    unsafe_allow_html=True)
# Calcular el gasto promedio por posición
average_spending_by_position = df_nfl_no_off_def.groupby('Position')['Dollars'].mean().reset_index()

# Crear la gráfica de distribución del gasto promedio por posición
average_spending_chart = alt.Chart(average_spending_by_position).mark_bar().encode(
    x=alt.X('mean(Dollars):Q', title='Gasto Promedio (Dólares)'),
    y=alt.Y('Position:N', title='Posición'),
    tooltip=['Position', alt.Tooltip('mean(Dollars)', title='Gasto Promedio (Dólares)')]
)
# Mostrar la nueva gráfica en Streamlit
st.altair_chart(average_spending_chart, use_container_width=True)

# Texto explicativo
st.write("""
En esta gráfica podemos observar con más detalle la distribución del gasto promedio por posición y como se había 
mencionado antes, OL, EDGE y CB son los mejores pagados curiosamente ya que EDGE y CB son posiciones defensivas y como
se ha mostrado anteriormente, los equipos invierten más dinero en los salarios de jugadores ofensivos. Por otra parte,
RB es la posición peor pagada en toda la liga pese a ser una posición muy lesiva.
""")
# Espaciado para mejorar la presentación
st.markdown("<br>", unsafe_allow_html=True)

# Grafico 5
st.markdown(
        "<p style='font-size: 18px; color: #4EBAE1;'><strong>Distribución del gasto por posición""</strong></p>",
    unsafe_allow_html=True)
# Crear gráfico de caja y bigotes para mostrar la distribución del gasto por posición
boxplot_chart = alt.Chart(df_nfl_no_off_def).mark_boxplot().encode(
    x=alt.X('Position:N', title='Posición'),
    y=alt.Y('Dollars:Q', title='Gasto (Dólares)'),
    color='Position:N'
)
# Mostrar el gráfico en Streamlit
st.altair_chart(boxplot_chart, use_container_width=True)

# Texto explicativo
st.write("""
Como se puede observar en la gráfica, la distribución de todas la posiciones es bastante alta lo que indica que no todos
los equipos pagan a sus jugadores de la misma manera, cada equipo prioriza alguna posición.
""")
