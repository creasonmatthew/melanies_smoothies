# Import python packages
import streamlit as st
import requests
import pandas as pd
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
my_dataframe = session.sql("select FRUIT_NAME,SEARCH_ON FROM smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()
# st.dataframe(data=my_dataframe, use_container_width=True)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     (my_dataframe),
# )

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,pd_df['FRUIT_NAME']
    ,max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        fv_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        # pd_df2 = fv_df.to_pandas()
        # st.dataframe(pd_df2)

    #st.write(ingredients_string)

    my_insert_stmt = """ INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
            VALUES ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button('Submit Order')
  
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
