import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Dashboard FlavioCesar",
    page_icon="🐈",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Cargar datos
file_path = 'ventas.xlsx'
data = pd.read_excel(file_path)

# Transformar datos
data['Date'] = pd.to_datetime(data['Date'])
data['YearMonth'] = data['Date'].dt.to_period('M')

# Eliminar valores nulos en las columnas usadas para los filtros
data.dropna(subset=['Date', 'Pais', 'IdCliente', 'Descripcion'], inplace=True)

# Título del Dashboard
st.title('Dashboard de Ventas')
st.markdown('### Resumen de ventas y rendimiento')

# Filtros en la barra lateral con expanders
with st.sidebar:
    st.title('🕒 Dashboard NG')
    with st.expander("Filtro por Fechas"):
        start_date = st.date_input('Fecha de inicio', data['Date'].min())
        end_date = st.date_input('Fecha de fin', data['Date'].max())
    with st.expander("Filtro por País"):
        country_filter = st.selectbox('Selecciona País', ['Todos'] + list(data['Pais'].unique()))
    with st.expander("Filtro por Cliente"):
        customer_filter = st.selectbox('Selecciona Cliente', ['Todos'] + list(data['IdCliente'].unique()))
    with st.expander("Filtro por Producto"):
        product_filter = st.selectbox('Selecciona Producto', ['Todos'] + list(data['Descripcion'].unique()))

# Aplicar filtros
filtered_data = data[
    (data['Date'] >= pd.to_datetime(start_date)) &
    (data['Date'] <= pd.to_datetime(end_date))
]

if country_filter != 'Todos':
    filtered_data = filtered_data[filtered_data['Pais'] == country_filter]
if customer_filter != 'Todos':
    filtered_data = filtered_data[filtered_data['IdCliente'] == customer_filter]
if product_filter != 'Todos':
    filtered_data = filtered_data[filtered_data['Descripcion'] == product_filter]

# KPIs principales
total_sales = filtered_data['Total'].sum()
total_quantity = filtered_data['Cantidad'].sum()
num_customers = filtered_data['IdCliente'].nunique()
quarterly_sales = filtered_data.resample('Q', on='Date')['Total'].sum()

# Primera fila de gráficos
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.metric('Ventas Totales', f'${total_sales:,.2f}')
    st.metric('Cantidad de Ventas', f'{total_quantity:,.0f}')
    st.metric('Número de Clientes', f'{num_customers}')

with col2:
    st.subheader('Ventas Totales por Mes')
    monthly_sales = filtered_data.groupby('YearMonth')['Total'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.bar(monthly_sales['YearMonth'].astype(str), monthly_sales['Total'])
    ax.set_xlabel('Mes')
    ax.set_ylabel('Ventas Totales')
    ax.set_title('Ventas Totales por Mes')
    st.pyplot(fig)

    st.subheader('Ventas por Producto')
    product_sales = filtered_data.groupby('Descripcion')['Cantidad'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.bar(product_sales['Descripcion'], product_sales['Cantidad'])
    ax.set_xlabel('Producto')
    ax.set_ylabel('Cantidad Vendida')
    ax.set_title('Ventas por Producto')
    ax.set_xticklabels(product_sales['Descripcion'], rotation=90)
    st.pyplot(fig)

with col3:
    st.subheader('Ventas por País')
    country_sales = filtered_data.groupby('Pais')['Total'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(country_sales['Total'], labels=country_sales['Pais'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title('Ventas por País')
    st.pyplot(fig)

    st.subheader('Ventas Trimestrales')
    st.line_chart(quarterly_sales)

# Segunda fila de gráficos
col4, col5 = st.columns([2, 1])

with col4:
    st.subheader('Ventas por Producto y País')
    product_country_sales = filtered_data.groupby(['Descripcion', 'Pais'])['Total'].sum().unstack().fillna(0)
    st.bar_chart(product_country_sales)

with col5:
    st.subheader('Datos Filtrados')
    st.dataframe(filtered_data)
