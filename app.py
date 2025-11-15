import streamlit as st
import datetime
from geopy.geocoders import Nominatim
import pandas as pd
import requests

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
'''
d = st.date_input(
    "When do you want to visit Louvre? (yyyy/mm/dd)",
    datetime.date(2025, 11, 15))
st.write('Visit scheduled to:', d)

t = st.time_input('Which time do you want to be picked up', datetime.time(8, 45))
st.write('Pick up at: ', t)


'''
Pickup address:
'''

geolocator = Nominatim(user_agent="app")

def get_lat_lon_p(p_address):
    p_location = geolocator.geocode(p_address)
    if p_location:
        return p_location.latitude, p_location.longitude
    return None, None

# st.title("Address → Coordinates")

p_address = st.text_input("Enter an pickup address or location:")

'''
if st.button("Get Pickup Coordinates"):
    if p_address.strip():
        p_lat, p_lon = get_lat_lon_p(p_address)
        if p_lat is not None:
            st.success(f"Latitude: {p_lat}, Longitude: {p_lon}")

            df = pd.DataFrame([[p_lat, p_lon]], columns=["lat", "lon"])
            st.map(df, zoom=12)
        else:
            st.error("Could not find coordinates.")
    else:
        st.warning("Please enter a valid address.")
'''
p_lat, p_lon = get_lat_lon_p(p_address)
'''
- Dropoff address:
'''

# geolocator = Nominatim(user_agent="app")

def get_lat_lon_d(d_address):
    d_location = geolocator.geocode(d_address)
    if d_location:
        return d_location.latitude, d_location.longitude
    return None, None

# st.title("Address → Coordinates")

d_address = st.text_input("Enter dropoff address:")


'''
if st.button("Get Dropoff Coordinates"):
    if d_address.strip():
        d_lat, d_lon = get_lat_lon_d(d_address)
        if d_lat is not None:
            st.success(f"Latitude: {d_lat}, Longitude: {d_lon}")

            df = pd.DataFrame([[d_lat, d_lon]], columns=["lat", "lon"])
            st.map(df, zoom=12)
        else:
            st.error("Could not find coordinates.")
    else:
        st.warning("Please enter a valid address.")
'''
d_lat, d_lon = get_lat_lon_d(d_address)
'''
- passenger count
'''
passengers = st.slider("Select total passengers", min_value=0, max_value=7, value=1)
st.write('Total passengers on trip: ', passengers)

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

# enviar = st.button('Price prediction')

#url = 'https://taxifare.lewagon.ai/predict'

if st.button('Price prediction'):

    #st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')
    #if enviar:

    # junta data e hora em um datetime único (formato padrão usado em APIs de ML)
    # datetime_trip = datetime.combine(d.date(), t.time())
    datetime_trip = f'{d} {t}'

    # monta o payload conforme a API espera
    payload = {
        "pickup_datetime": datetime_trip,
        "pickup_latitude": p_lat,
        "pickup_longitude": p_lon,
        "dropoff_latitude": d_lat,
        "dropoff_longitude": d_lon,
        "passenger_count": passengers
    }

    st.write("📦 *Payload enviado para a API:*")
    st.json(payload)

    # URL da API
    url = 'https://taxifare.lewagon.ai/predict'

    try:
        response = requests.get(url, params=payload)

        if response.status_code == 200:
            resultado = response.json()
            preco = resultado.get("fare", None)

            if preco is not None:
                st.success(f"💰 Preço estimado: **US$ {preco:.2f}**")
            else:
                st.error("A API respondeu, mas não retornou o campo 'prediction'.")
                st.json(resultado)

        else:
            st.error(f"Erro ao chamar a API: Status {response.status_code}")
            st.write(response.text)

    except Exception as e:
        st.error("❌ Erro de conexão com a API.")
        st.write(e)

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
