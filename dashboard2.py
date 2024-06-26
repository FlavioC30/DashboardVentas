import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

# Data for the dashboard
# Sales data by month
sales_data = {
    'Month': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    'Sales': [4, 5, 3, 4, 5, 3, 2, 2, 2, 1, 0, 0],
    'Product 1': [2, 3, 2, 3, 4, 2, 1, 1, 1, 0, 0, 0],
    'Product 2': [1, 2, 1, 2, 3, 1, 0, 0, 0, 0, 0, 0],
    'Product 3': [3, 4, 3, 4, 5, 3, 2, 2, 2, 1, 0, 0],
    'Product 4': [2, 3, 2, 3, 4, 2, 1, 1, 1, 0, 0, 0]
}
sales_df = pd.DataFrame(sales_data)

# Product sales data
product_sales = {
    'Product': ['Producto 1', 'Producto 2', 'Producto 3', 'Producto 4', 'Producto 5'],
    'Sales': [450, 800, 250, 450, 320]
}
product_sales_df = pd.DataFrame(product_sales)

# Country sales data
country_sales = {
    'Country': ['USA', 'CAR', 'NOR', 'POR', 'ITA'],
    'Sales': [3, 6, 25, 9, 4]
}
country_sales_df = pd.DataFrame(country_sales)

# Sales data by year
year_sales = {
    'Year': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    'Sales': [1, 2, 4, 3, 5, 6]
}
year_sales_df = pd.DataFrame(year_sales)

# Creating the dashboard layout
col1, col2, col3 = st.columns([1, 2, 1])

# Column 1: Filters
with col1:
    st.header("DASHBOARD NG")
    st.markdown("---")
    st.subheader("FILTRO POR FECHAS")
    st.button("Filtro")
    st.markdown("---")
    st.subheader("FILTRO POR PAIS")
    st.button("Filtro")
    st.markdown("---")
    st.subheader("FILTRO POR CLIENTE")
    st.button("Filtro")
    st.markdown("---")
    st.subheader("FILTRO POR PRODUCTO")
    st.button("Filtro")

# Column 2: Main dashboard
with col2:
    st.header("DASHBOARD VENTAS")
    st.markdown("---")
    st.subheader("RESUMEN DE VENTAS Y RENDIMIENTO")
    st.markdown("---")
    
    # Total sales
    st.subheader("VENTAS TOTALES")
    st.metric(label="", value="$499948", delta=None)
    
    # Sales by month
    st.subheader("VENTAS POR MES")
    fig, ax = plt.subplots()
    ax.bar(sales_df['Month'], sales_df['Sales'])
    ax.bar(sales_df['Month'], sales_df['Product 1'], label='Product 1')
    ax.bar(sales_df['Month'], sales_df['Product 2'], label='Product 2')
    ax.bar(sales_df['Month'], sales_df['Product 3'], label='Product 3')
    ax.bar(sales_df['Month'], sales_df['Product 4'], label='Product 4')
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    ax.set_xticks(sales_df['Month'])
    ax.set_xticklabels(sales_df['Month'], rotation=90)
    st.pyplot(fig)
    
    # Sales by product
    st.subheader("VENTAS DE PRODUCTO")
    for i in range(len(product_sales_df)):
        st.markdown(f"**{product_sales_df['Product'][i]}**   |   ${product_sales_df['Sales'][i]}")
    
    # Sales by country
    st.subheader("VENTAS POR PRODUCTO Y PAIS")
    fig, ax = plt.subplots()
    ax.bar(country_sales_df['Country'], country_sales_df['Sales'])
    ax.set_xlabel("Country")
    ax.set_ylabel("Sales")
    st.pyplot(fig)
    
    # Sales by year
    st.subheader("VENTAS POR PAIS")
    fig, ax = plt.subplots()
    ax.pie(x=[58, 23, 9], labels=['united kingdom', 'australia', ''], autopct='%1.0f%%')
    ax.axis('equal')
    st.pyplot(fig)

# Column 3: Metrics
with col3:
    st.subheader("CANTIDAD DE VENTAS")
    st.metric(label="", value="45787", delta=None)
    st.markdown("---")
    st.subheader("NUMERO DE CLIENTES")
    st.metric(label="", value="345", delta=None)
    st.markdown("---")
    st.subheader("VENTAS TRIDIMENCIONALES")
    fig, ax = plt.subplots()
    ax.plot(year_sales_df['Year'], year_sales_df['Sales'])
    ax.set_xlabel("Year")
    ax.set_ylabel("Sales")
    ax.set_xticks(year_sales_df['Year'])
    ax.set_xticklabels(year_sales_df['Year'], rotation=90)
    st.pyplot(fig)