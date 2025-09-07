# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie.
  """
)

name_on_order = st.text_input("Name on Smoothi")
st.write("The Name on the smoothi will be: "+ name_on_order)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))

st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list =st.multiselect('Choose five incredients: '
                                , my_dataframe
                                , max_selections=5)
st.write("Choose up to 5 ingredients")

if ingredients_list:
    
        ingredients_string = ''
        
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '
            st.subheader(fruit_chosen + ' Nutrition Information')
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

      #  my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
      #      values ('""" + ingredients_string + """')"""
        my_insert_stmt = """ insert into smoothies.public.orders(NAME_ON_ORDER, ingredients)
            values ('""" + name_on_order + """','""" + ingredients_string + """')"""

    
        #st.write(my_insert_stmt)
        #st.stop()
    
        time_to_insert = st.button("Submit order")

        if time_to_insert:
            session.sql(my_insert_stmt).collect()
           # st.success('Your Smoothie is ordered!', icon="✅")
            st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")
