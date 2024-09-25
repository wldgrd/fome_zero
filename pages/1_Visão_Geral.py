#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=            LIBRARIES          =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

import pandas as pd
import inflection 
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image #import PIL.Image as imgpil
from folium.plugins import MarkerCluster

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=            FUNCTIONS          =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

def country_name(country_id):
    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }
    return COUNTRIES[country_id]
    
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
        
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

def color_name(color_code):
    COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }
    return COLORS[color_code]
    
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df
    
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

def remove_duplicatas(dataframe):
    duplicado = df1.duplicated()
    linhas_nao_duplicadas = duplicado == False
    dataframe = dataframe.loc [ linhas_nao_duplicadas, :]
    return dataframe.reset_index(drop = True) ## Drop = True server para derrubar a coluna com o índice antigo
    
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

def convert_to_dollar(valor, moeda):
    moedas_em_dolar = {
    # cotação do dólar feita em 29/08/2024 às 14h30 
    'Botswana Pula(P)'       : 0.075,
    'Brazilian Real(R$)'     : 0.18,
    'Dollar($)'              : 1.00,
    'Emirati Diram(AED)'     : 0.27,
    'Indian Rupees(Rs.)'     : 0.012,
    'Indonesian Rupiah(IDR)' : 0.000065,
    'NewZealand($)'          : 0.62098,
    'Pounds(£)'              : 1.316396,
    'Qatari Rial(QR)'        : 0.27,
    'Rand(R)'                : 0.056,
    'Sri Lankan Rupee(LKR)'  : 0.0033,
    'Turkish Lira(TL)'       : 0.029
    }
    return valor * moedas_em_dolar[moeda]

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#           LOADING DATA         =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=


df = pd.read_csv('zomato.csv')
df1 = df.copy()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=          TREATING THE  DATA         =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

#renaming data frame columns
df1 = rename_columns(df1) 

#removing column with just one value
df1 = df1.drop(['switch_to_order_menu'], axis = 1) 

#droping the nan values of cuisines
df1 = df1.dropna(subset=['cuisines']) ##deletando valores nan

#Removing duplicates
df1 = remove_duplicatas(df1)

#Categorizing the cuisines column by the first argument of the string (italian, japanese, brazilian -- > italian)
df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else x)

#creating the column 'country_names'
df1['country_name'] = df1['country_code'].apply(country_name)

#creating the column 'color_name'
df1['color_name'] = df1['rating_color'].apply(color_name)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=            CODE STRUCTURE           =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=


#seting the emoticon and the title of the page
st.set_page_config( page_title = 'Visão Geral', page_icon ='🌎', layout = 'wide')
st.markdown("<h1 style='text-align: center;'>Visão Geral 🌎</h1>", unsafe_allow_html=True)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#-#=             SIDE BAR           =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

st.sidebar.divider()

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.image('logo1.jpeg', width = 150)
    with col2:
        st.image('fomeZero.png', width = 137)
    st.sidebar.markdown( """---""" )

    country = st.multiselect(
        'Selecione os Países',
        sorted(['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey']),
        default = ['Australia', 'Brazil', 'Canada', 'England', 'Qatar', 'South Africa']
        )

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=         LIGANDO OS FILTROS          =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

linhas_selecionadas = df1['country_name'].isin(country)
df1 = df1.loc[linhas_selecionadas, :]


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

st.tabs(['Geral'])

with st.container():
    st.markdown("<h1 style='text-align: center;'>Métricas</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        restaurants = df1['restaurant_id'].nunique()
        col1.metric('Restaurantes', restaurants)
        
    with col2:
        countries = df1['country_code'].nunique()
        col2.metric('Países', countries)
        
    with col3:
        cities = df1['city'].nunique()
        col3.metric('Cidades', cities)
        
    with col4:
        votes = df1['votes'].sum()
        col4.metric('Avaliações', votes)

    with col5: 
        cuisines = df1['cuisines'].nunique()
        col5.metric('Tipos de Culinária', cuisines)
            
            
            

    
    with st.container():
        st.header('Mapa')
        f = folium.Figure(width=1920, height=1080)

        m = folium.Map(max_bounds=True).add_to(f)
        
        marker_cluster = MarkerCluster().add_to(m)
        
        for _, line in df1.iterrows():
        
            name = line["restaurant_name"]
            price_for_two = line["average_cost_for_two"]
            cuisine = line["cuisines"]
            currency = line["currency"]
            rating = line["aggregate_rating"]
            color = f'{line["color_name"]}'
        
            html = "<p><strong>{}</strong></p>"
            html += "<p>Price: {},00 ({}) para dois"
            html += "<br />Type: {}"
            html += "<br />Aggragate Rating: {}/5.0"
            html = html.format(name, price_for_two, currency, cuisine, rating)
        
            popup = folium.Popup(
                folium.Html(html, script=True),
                max_width=500,
            )
        
            folium.Marker(
                [line["latitude"], line["longitude"]],
                popup=popup,
                icon=folium.Icon(color=color, icon="home", prefix="fa"),
            ).add_to(marker_cluster)


            
        folium_static( m, width = 1024 , height = 768 )


    







