# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.sql("select FRUIT_NAME FROM smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     (my_dataframe),
# )

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
            VALUES ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button('Submit Order')

    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    #st.text(smoothiefroot_response.json())
    sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

  
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
