# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched

# Write directly to the app
st.title(f":cup_with_straw: pending smoothie :cup_with_straw:")
st.write(
  """Orders that need to be filled.
  """
)

# Get the current credentials

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)


if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button("Submit")
    
    if submitted:
        
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        
        try:     
            og_dataset.merge(edited_dataset
            , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
            , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
            st.success('Orders updated!', icon = '👍')
        except:
            st.write('Something went wrong', icon = '👎')
     #my_update_stmt = """update smoothies.public.orders set order_filled = true
     #  where name_on_order = 'huhu'"""
     #st.write(my_update_stmt)
     #session.sql(my_update_stmt).collect()
else:    
    st.success('There is no pending order right now!', icon = '👍')
