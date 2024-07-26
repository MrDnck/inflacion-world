import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np

# Información sobre el proyecto
st.markdown("""
### Fuente de Datos
Los datos se recolectaron de la plataforma del Banco Mundial: [Inflación, deflactor del PIB (anual %)](https://datos.bancomundial.org/indicador/NY.GDP.DEFL.KD.ZG.AD?end=2023&skipRedirection=true&start=2023)

### Código Fuente
Puedes ver y modificar el código en el siguiente repositorio de GitHub: [Repositorio de GitHub](https://github.com/MrDnck/inflacion-world)

### Autor
Cristian Catari
            
Celular: +591 70562921
            
Correo electrónico: cristian.catari.ma@gmail.com
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

# Predicción de inflación
st.subheader('Predicción de la inflación:')

# Seleccionar el país para la predicción
country = st.selectbox('Seleccione un país para la predicción:', data_melted['Country Name'].unique(), index=list(data_melted['Country Name'].unique()).index('Bolivia'))

# Filtrar los datos para el país seleccionado
country_data = data_melted[data_melted['Country Name'] == country]

# Entrenar el modelo de regresión lineal
model = LinearRegression()
X = country_data[['Year']]
y = country_data['Inflation']
model.fit(X, y)

# Seleccionar el año para la predicción
pred_years = st.slider('Seleccione el rango de años para la predicción (Regresión lineal):', min_value=2024, max_value=2030, value=(2024, 2025))

# Realizar la predicción
future_years = pd.DataFrame(np.array(range(pred_years[0], pred_years[1] + 1)).reshape(-1, 1), columns=['Year'])
pred_inflations = model.predict(future_years)

# Crear un DataFrame con las predicciones
pred_data = pd.DataFrame({
    'Year': future_years['Year'],
    'Inflation': pred_inflations,
    'Country Name': country
})

# Combinar los datos históricos con las predicciones
combined_data = pd.concat([country_data, pred_data])

# Crear el gráfico de líneas con predicciones
fig_pred = px.line(
    combined_data,
    x='Year',
    y='Inflation',
    color='Country Name',
    labels={'Inflation': 'Inflación (%)', 'Year': 'Año'},
    title=f'Inflación Anual y Predicción para {country}',
    color_discrete_sequence=px.colors.qualitative.Dark24
)

# Añadir una línea para diferenciar las predicciones
fig_pred.add_scatter(x=pred_data['Year'], y=pred_data['Inflation'], mode='lines', name='Predicción', line=dict(dash='dash', color='red'))

# Mostrar el gráfico de líneas con predicciones
st.plotly_chart(fig_pred)

st.write(f'La inflación predicha para {country} entre los años {pred_years[0]} y {pred_years[1]} es:')
for year, infl in zip(pred_data['Year'], pred_data['Inflation']):
    st.write(f'{year}: {infl:.2f}%')
