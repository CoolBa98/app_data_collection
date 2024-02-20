import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import base64
import plotly.express as px

st.set_page_config(
	page_title="TP DATA COLLECTION",
	layout="wide"
)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string=base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp{{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('bg.png')
site_np={
	"https://dakar-auto.com/senegal/voitures-4": 2744,
	"https://dakar-auto.com/senegal/motos-and-scooters-3": 8,
	"https://dakar-auto.com/senegal/location-de-voiture-19": 40
}

st.sidebar.header("User input")
url = st.sidebar.selectbox("URL du site à scraper:",
                           ["https://dakar-auto.com/senegal/voitures-4",
                            "https://dakar-auto.com/senegal/motos-and-scooters-3",
                            "https://dakar-auto.com/senegal/location-de-voiture-19"
                            ])

option = st.sidebar.selectbox("Option:",
                           ["Scrape with beautifulsoup",
                            "Download scraped data",
                            "Dashbord of the data",
                            "Fill the form"
                            ])

st.markdown("""<h1 style="text-align: center"> TP DATA COLLECTION GROUPE 3 <h1>""", unsafe_allow_html=True)
st.markdown("""<h4 style="text-align: center"> This app performs webscraping of data from """
            + url +
            """ over multiples pages. And we can also download scraped data from the app directy without scraping them. <h4>""",
            unsafe_allow_html=True)

# BEAUTIFULSOUP
if option == "Scrape with beautifulsoup":
    nombre_page = st.sidebar.number_input(f"Nombre de page à scraper(1 - {site_np[url]})",
                            min_value=1,
                            max_value=site_np[url],
                            step=1)
    
    if st.sidebar.button("Lancer"):
        if url == "https://dakar-auto.com/senegal/voitures-4":
            
            voitures = []

            for page in range(1, nombre_page + 1):
                url = f"https://dakar-auto.com/senegal/voitures-4?page={page}"
                res = get(url)
                data = bs(res.text, "html.parser")
                container = data.find("div", class_="listings-cards row")
                cars = container.find_all("div", class_="listing-card__content__inner")
                
                for car in cars:
                
                    marque = car.find("h2", class_="listing-card__header__title mb-md-2 mb-0").text.split()[0]
                    annee = car.find("h2", class_="listing-card__header__title mb-md-2 mb-0").text.split()[-1]
                    prix = car.find("h3", class_="listing-card__header__price font-weight-bold text-uppercase mb-0").text.replace('CFA', '').replace('F', '').replace('\n', '').replace('\u202f', '').strip()
                    adresse = car.find("div", class_="col-12 entry-zone-address").text.replace('\n', '')
                    kilometrage = car.find("div", class_="col-12 listing-card__properties d-none d-sm-block").text.strip().split()[2]
                    boite_vitesse = car.find("div", class_="col-12 listing-card__properties d-none d-sm-block").text.strip().split()[-2]
                    carburant = car.find("div", class_="col-12 listing-card__properties d-none d-sm-block").text.strip().split()[-1]
                    proprietaire = ' '.join(car.find("p", class_="time-author m-0").text.split()[1:])
                
                    obj = {
                        "marque": marque,
                        "annee": annee,
                        "prix": prix,
                        "adresse": adresse,
                        "kilometrage": kilometrage,
                        "boite_vitesse": boite_vitesse,
                        "carburant": carburant,
                        "proprietaire": proprietaire
                    }
                    voitures.append(obj)

            df = pd.DataFrame(voitures)

            st.write(f"Data dimension: {df.shape[0]} rows and {df.shape[1]} columns.")
            st.write(df)

        elif url == "https://dakar-auto.com/senegal/motos-and-scooters-3":
            
            motos = []

            for page in range(1, nombre_page + 1):
                url = f"https://dakar-auto.com/senegal/motos-and-scooters-3?&page={page}"
                res = get(url)
                data = bs(res.text, "html.parser")
                container = data.find("div", class_="listings-cards row")
                bikes = container.find_all("div", class_="listing-card__content__inner")
                
                for bike in bikes:
                
                    try:
                        marque = bike.find("h2", class_="listing-card__header__title mb-md-2 mb-0").text.split()[0]
                        annee = bike.find("h2", class_="listing-card__header__title mb-md-2 mb-0").text.split()[-1]
                        prix = bike.find("h3", class_="listing-card__header__price font-weight-bold text-uppercase mb-0").text.replace('CFA', '').replace('F', '').replace('\n', '').replace('\u202f', '').strip()
                        adresse = bike.find("div", class_="col-12 entry-zone-address").text.replace('\n', '')
                        kilometrage = bike.find("div", class_="col-12 listing-card__properties d-none d-sm-block").text.strip().split()[2]
                        proprietaire = ' '.join(bike.find("p", class_="time-author m-0").text.split()[1:])
                    
                        obj = {
                            "marque": marque,
                            "annee": annee,
                            "prix": prix,
                            "adresse": adresse,
                            "kilometrage": kilometrage,
                            "proprietaire": proprietaire
                        }
                        motos.append(obj)
                    except:
                        pass

            df = pd.DataFrame(motos)

            st.write(f"Data dimension: {df.shape[0]} rows and {df.shape[1]} columns.")
            st.write(df)
        else:
            
            voitures_location = []

            for page in range(1, nombre_page + 1):
                url = f"https://dakar-auto.com/senegal/location-de-voitures-19?&page={page}"
                res = get(url)
                data = bs(res.text, "html.parser")
                container = data.find("div", class_="listings-cards row")
                vls = container.find_all("div", class_="listing-card__content__inner")
                
                for vl in vls:
                
                    try:
                        marque = vl.find("h2", class_="listing-card__header__title mb-md-2 mb-0").text.split()[0]
                        annee = vl.find("h2", class_="listing-card__header__title mb-md-2 mb-0").text.split()[-1]
                        prix = vl.find("h3", class_="listing-card__header__price font-weight-bold text-uppercase mb-0").text.replace('CFA', '').replace('F', '').replace('\n', '').replace('\u202f', '').strip()
                        adresse = vl.find("div", class_="col-12 entry-zone-address").text.replace('\n', '')
                        proprietaire = ' '.join(vl.find("p", class_="time-author m-0").text.split()[1:])
                    
                        obj = {
                            "marque": marque,
                            "annee": annee,
                            "prix": prix,
                            "adresse": adresse,
                            "proprietaire": proprietaire
                        }
                        voitures_location.append(obj)
                    except:
                        pass

            df = pd.DataFrame(voitures_location)
            
            st.write(f"Data dimension: {df.shape[0]} rows and {df.shape[1]} columns.")
            st.write(df)
        
        st.download_button(
            label="Download data as csv",
            data=df.to_csv().encode(),
            file_name="data.csv",
            mime="text/csv"
        )

#
        
# WEB SCRAPER
if option == "Download scraped data":
    if url == "https://dakar-auto.com/senegal/voitures-4":
        df = pd.read_csv('url1.csv')
        st.write(f"Data dimension: {df.shape[0]} rows and {df.shape[1]} columns.")
        st.write(pd.read_csv('url1.csv'))

    elif url == "https://dakar-auto.com/senegal/motos-and-scooters-3":
        df = pd.read_csv('url2.csv')
        st.write(f"Data dimension: {df.shape[0]} rows and {df.shape[1]} columns.")
        st.write(df)
    else:
        df = pd.read_csv('url3.csv')
        st.write(f"Data dimension: {df.shape[0]} rows and {df.shape[1]} columns.")
        st.write(df)
    
    st.download_button(
        label="Download data as csv",
        data=df.to_csv().encode(),
        file_name="data.csv",
        mime="text/csv"
    )
#
    
# KOBO
if option == "Fill the form":
    st.markdown("""
                <iframe src=https://ee.kobotoolbox.org/i/mQgZ6ONY width="800" height="600"></iframe>
                """,
                unsafe_allow_html=True)
#

# DASHBORD
if option == "Dashbord of the data":
    if url == "https://dakar-auto.com/senegal/voitures-4":
        df = pd.read_csv('url1_db.csv')
        
        col1, col2 = st.columns(2)
        with col1:
            df1 = df['Marque'].value_counts()[:5]
            fig = px.bar(df1, x=df1.index, y=df1.values, color=df1.index, labels=["Marques", "Nombre de voitures"], title='Top 5 des marques de voitures les plus vendues')
            st.plotly_chart(fig)

        with col2:
            couleurs = {
                'Essence': 'cyan',
                'Diesel': 'green',
                'Hybrides': 'red'
            }
            df2 = df['Carburant'].value_counts()
            fig = px.bar(df2, x=df2.index, y=df2.values, color=df2.index, color_discrete_map=couleurs, labels=["Type de carburant", "Nombre de voitures"], title='Nombre de voiture par type de carburant')
            st.plotly_chart(fig)

    elif url == "https://dakar-auto.com/senegal/motos-and-scooters-3":
        df = pd.read_csv('url2_db.csv')
        
        col1, col2 = st.columns(2)
        with col1:
            df1 = df['Marque'].value_counts()[:5]
            fig = px.bar(df1, x=df1.index, y=df1.values, color=df1.index, labels=["Marques", "Nombre de motos/scooter"], title='Top 5 des marques de motos/scooter les plus vendus')
            st.plotly_chart(fig)

        with col2:
            df2 = df['Adresse'].value_counts()[:10]
            fig = px.pie(df2, values=df2.values, names=df2.index, title='Top 10 des situations géo. vendant le plus de motos/scooters')
            st.plotly_chart(fig)

    else:
        df = pd.read_csv('url3.csv')
        df1 = df['Marque'].value_counts()[:10]
        fig = px.bar(df1, x=df1.index, y=df1.values, color=df1.index, labels=["Marques", "Nombre de voitures"], title='Top 5 des marques de voitures les plus mise en location')
        st.plotly_chart(fig)
