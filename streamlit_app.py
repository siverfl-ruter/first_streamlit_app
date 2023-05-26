# This is code for the streamlit app
import streamlit
import pandas as pd

streamlit.title("My Parents New Healthy Diner")
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
  
  
streamlit.title("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

# Add frutyvice api call
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

# Normalize the json response and load to DF
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Display df
streamlit.dataframe(fruityvice_normalized)
