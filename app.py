import pandas as pd
import plotly.express as px
import streamlit as st

#info 
st.markdown("""
### Fuente de Datos
Los datos se recolectaron de la plataforma del Banco Mundial: [Inflación, deflactor del PIB (anual %)](https://datos.bancomundial.org/indicador/NY.GDP.DEFL.KD.ZG.AD?end=2023&skipRedirection=true&start=2023)

### Código Fuente
Puedes ver y modificar el código en el siguiente repositorio de GitHub: [Repositorio de GitHub](https://github.com/MrDnck/inflacion-world)

### Autor
Tu Nombre

Celular: +591 12345678  
Correo electrónico: tu.email@ejemplo.com
""")



# Cargar y limpiar el dataset
file_path = 'API_NY.GDP.DEFL.KD.ZG.AD_DS2_es_csv_v2_1861822.csv'
data = pd.read_csv(file_path)

# Renombrar las columnas adecuadamente
data.columns = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'] + list(range(1960, 2024))

# Seleccionar solo las columnas relevantes
data = data[['Country Name', 'Country Code'] + list(range(1960, 2024))]

# Derretir el DataFrame para tener un formato largo
data_melted = data.melt(id_vars=['Country Name', 'Country Code'], var_name='Year', value_name='Inflation')

# Filtrar datos no disponibles
data_melted = data_melted.dropna(subset=['Inflation'])

# Convertir el año a tipo int
data_melted['Year'] = data_melted['Year'].astype(int)

# Configurar la aplicación de Streamlit
st.title('Análisis de la Inflación por País')
st.subheader('Seleccione los países que desea visualizar:')

# Segmentador para seleccionar países
countries = st.multiselect(
    'Países',
    options=data_melted['Country Name'].unique(),
    default=['Bolivia', "Venezuela", "Chile"]
)

# Filtrar los datos según los países seleccionados
filtered_data = data_melted[data_melted['Country Name'].isin(countries)]

# Crear el gráfico de líneas
fig_line = px.line(
    filtered_data,
    x='Year',
    y='Inflation',
    color='Country Name',
    labels={'Inflation': 'Inflación (%)', 'Year': 'Año'},
    title='Inflación Anual por País',
    color_discrete_sequence=px.colors.qualitative.Dark24
)

# Mostrar el gráfico de líneas
st.plotly_chart(fig_line)

# Crear un mapa interactivo
st.subheader('Mapa interactivo de la inflación por país:')

# Seleccionar el año para el mapa
year = st.select_slider('Seleccione el año', options=list(range(1960, 2024)), value=2023)

# Filtrar los datos para el año seleccionado
data_year = data_melted[data_melted['Year'] == year]

# Crear el mapa coroplético
fig_map = px.choropleth(
    data_year,
    locations='Country Code',
    color='Inflation',
    hover_name='Country Name',
    color_continuous_scale='Agsunset',
    labels={'Inflation': 'Inflación (%)'},
    title=f'Inflación por País en {year}'
)

# Mostrar el mapa
st.plotly_chart(fig_map)
