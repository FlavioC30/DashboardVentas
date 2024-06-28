import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# Page configuration
st.set_page_config(
    page_title="Dashboard FlavioCesar",
    page_icon="🐈",
    layout="wide",
    initial_sidebar_state="expanded")

# Cargar datos
file_path = 'ventas.xlsx'
data = pd.read_excel(file_path)

# Transformar datos
data['Date'] = pd.to_datetime(data['Date'])
data['YearMonth'] = data['Date'].dt.to_period('M').astype(str)

# Eliminar valores nulos en las columnas usadas para los filtros
data.dropna(subset=['Date', 'Pais', 'IdCliente', 'Descripcion'], inplace=True)

# Título del Dashboard
st.title('🌟 Dashboard de Ventas 🌟')
st.markdown('### Resumen de ventas y rendimiento 📊')

# Animación Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets4.lottiefiles.com/packages/lf20_dHJiUx.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json, speed=1, width=700, height=300, key="dashboard")

# Filtros en la barra lateral con expanders
with st.sidebar:
    st.title('🕒 Filtros')
    with st.expander("📅 Filtro por Fechas"):
        start_date = st.date_input('Fecha de inicio', data['Date'].min())
        end_date = st.date_input('Fecha de fin', data['Date'].max())
    with st.expander("🌍 Filtro por País"):
        country_filter = st.selectbox('Selecciona País', ['Todos'] + list(data['Pais'].unique()))
    with st.expander("👥 Filtro por Cliente"):
        customer_filter = st.selectbox('Selecciona Cliente', ['Todos'] + list(data['IdCliente'].unique()))
    with st.expander("🛍️ Filtro por Producto"):
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

# Primera fila de KPIs
st.markdown("## 🔑 KPIs Principales")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric('Ventas Totales', f'${total_sales:,.2f}', delta="Mejora respecto al mes anterior", delta_color="inverse")

with col2:
    st.metric('Cantidad de Ventas', f'{total_quantity:,.0f}')

with col3:
    st.metric('Número de Clientes', f'{num_customers}')

with col4:
    st.metric('Ventas Trimestrales', f'${quarterly_sales.sum():,.2f}')

# Segunda fila de gráficos
st.markdown("## 📈 Gráficos de Ventas")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader('📅 Ventas Totales por Mes')
    monthly_sales = filtered_data.groupby('YearMonth')['Total'].sum().reset_index()
    fig = px.bar(monthly_sales, x='YearMonth', y='Total', title="Ventas Totales por Mes",
                 labels={'YearMonth':'Mes', 'Total':'Ventas Totales'}, color='Total', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader('🌍 Ventas por País')
    country_sales = filtered_data.groupby('Pais')['Total'].sum().reset_index()
    fig = px.pie(country_sales, values='Total', names='Pais', title="Ventas por País", hole=.3,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

# Tercera fila de gráficos
col3, col4 = st.columns([2, 1])

with col3:
    st.subheader('🛍️ Ventas por Producto')
    product_sales = filtered_data.groupby('Descripcion')['Cantidad'].sum().reset_index()
    fig = px.bar(product_sales, x='Descripcion', y='Cantidad', title="Ventas por Producto",
                 labels={'Descripcion':'Producto', 'Cantidad':'Cantidad Vendida'}, color='Cantidad', color_continuous_scale='Viridis')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader('📊 Ventas Trimestrales')
    fig = go.Figure(data=[go.Scatter(x=quarterly_sales.index, y=quarterly_sales.values, mode='lines+markers', line=dict(color='firebrick'))])
    fig.update_layout(title='Ventas Trimestrales', xaxis_title='Fecha', yaxis_title='Ventas Totales')
    st.plotly_chart(fig, use_container_width=True)

# Cuarta fila de gráficos
col5, col6 = st.columns(2)

with col5:
    st.subheader('🛍️ Ventas por Producto y País')
    product_country_sales = filtered_data.groupby(['Descripcion', 'Pais'])['Total'].sum().unstack().fillna(0)
    fig = px.bar(product_country_sales, title="Ventas por Producto y País", labels={'value':'Ventas Totales'}, barmode='group')
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader('📋 Datos Filtrados')
    st.dataframe(filtered_data)

# Agregar un mapa interactivo de ventas por país
st.markdown("## 🌍 Mapa de Ventas")
fig = px.scatter_geo(filtered_data, locations="Pais", locationmode='country names', color="Total",
                     hover_name="Pais", size="Total", projection="natural earth", title="Distribución Geográfica de Ventas")
st.plotly_chart(fig, use_container_width=True)

# Footer con Copyright
st.markdown("""
<style>
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("## Gracias por usar el Dashboard NG")

# Información adicional en el sidebar
st.sidebar.write("🔢 Información adicional")
st.sidebar.write("Número de Ventas: ", filtered_data['Total'].count())
st.sidebar.write("Número de Clientes: ", filtered_data['IdCliente'].nunique())

# Footer con Copyright
st.markdown("""
<hr style="border:2px solid gray"> </hr>
<center>
<p style="font-size:12px; color:gray;">&copy; 2024 Flavio Cesar Flores</p>
</center>
""", unsafe_allow_html=True)
