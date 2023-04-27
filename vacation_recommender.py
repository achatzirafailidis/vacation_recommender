### Import libraries
import streamlit as st
import pandas as pd 
from PIL import Image
from recommender import *

sea_image = Image.open('/home/alex/Spiced/final_project/streamlit/2789823612')
city_image = Image.open('/home/alex/Spiced/final_project/streamlit/18013817255')
mountain_image = Image.open('/home/alex/Spiced/final_project/streamlit/5798623418')

#st.title("Vacation Recommender")
#st.markdown('A recommendation engine leveraging ML to identify and propose holiday destinations, based on user input')

feature_df = pd.read_csv('/home/alex/Spiced/final_project/full_feature_list.csv')
#tags100 = pd.read_csv('/home/alex/Spiced/final_project/tags100_file.csv', names=['destination', 'tags'])
#print(feature_df)
with st.sidebar:
    st.image('/home/alex/Spiced/final_project/streamlit/Spiced_Logo_Dark.png')
    st.markdown('# Vacation recommender')
    st.markdown('## Alex')
    #page = st.selectbox("Choose a page", ["page1", "page2"])


st.header('What appeals to you?')
with st.form(key="recommender"):

#st.image(sea_image, width=200)
#st.image(city_image, width=200)
#st.image(mountain_image, width=200)

    col1, col2, col3 = st.columns(3)

    with col1:
        #st.header("Sea")
        st.image(sea_image, width=200)
        sea = st.checkbox('Sea')

    with col2:
        #st.header("Mountain")
        st.image(mountain_image, width=200)
        mountain = st.checkbox( 'Mountain')

    with col3:
        #st.header("City")
        st.image(city_image, width=200)
        city = st.checkbox('City')

    #label_options = ['Sea', 'Mountain', 'City']

    #page = st.radio(label='Check one option', options=label_options, horizontal=True)
    #feature_df = feature_df[feature_df['label']==page]
    #print(feature_df)

    #st.header('How would you describe your ideal place in a sentence?')

    user_input = st.text_input('Describe your ideal place in a sentence')
    #st.write('The current movie title is','function')

    #st.header('When do you want to go?')


    #feature_df = feature_df[feature_df['months'].str.contains(option)]
    #print(feature_df['months'].str.contains(option))
    #st.write('You selected:', option)

    col1, col2, col3 = st.columns(3)

    with col1:
        #st.header("Sea")
        option = st.selectbox(
        'Choose your travel month',
        ('---','January', 'February', 'March', 'April', 'June', 'July', 'August', 'September', 'October', 'November', 'December'))

    with col3:
        #st.header("City")
        st.write('')
        st.write('')
        button = st.form_submit_button(label='Show me recommendations')
        
    number_of_locations = int(sea) + int(mountain) + int(city)

    month = option

    st.markdown('# ')

    if button:
        if number_of_locations != 1:
            st.write('Please choose one location only')
        elif len(user_input) < 10:
            st.write('Please provide a longer text')
        elif month=='---':
            st.write('Please choose a month')
        else:
            location = "Sea" * sea + "Mountain" * mountain + "City" * city
            df = recommendation_calc(text = user_input, feature=location)
            st.write(df)