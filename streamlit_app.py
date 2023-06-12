import streamlit
import pandas

streamlit.title('Hello World!')

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page.
streamlit.dataframe(my_fruit_list)

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries']) 
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display the table on the page

streamlit.dataframe(fruits_to_show)

import requests

streamlit.header("Fruityvice Fruit Advice!")
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ "Kiwi")
# take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
streamlit.text("The food load list contains:")

my_data_row_normalized = pandas.json_normalize(my_data_row.json())
streamlit.dataframe(my_data_row_normalized)

# Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

#This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
