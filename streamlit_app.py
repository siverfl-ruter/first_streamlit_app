# This is code for the streamlit app
import streamlit
import pandas as pd
import snowflake.connector
import requests
from urllib.error import URLError

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

def get_fruity_data(choice):
  # Add frutyvice api call
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + choice)
  # Normalize the json response and load to DF
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_normalized = get_fruity_data(fruit_choice)
    # Display df
    streamlit.dataframe(fruityvice_normalized)
    
except URLError as e:
  streamlit.error(e)


streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


fruit_choice = streamlit.text_input('What fruit would you like to add?')
my_data_rows.append(fruit_choice)
streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
