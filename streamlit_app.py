# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title('custom smoothies')
st.write('chose the fruit')

NAME_ON_ORDER = st.text_input('name of smoothie')
st.write('name of smoothe', NAME_ON_ORDER)

cnx = st.connection("snoflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    'chose top 5 ingredients'
    ,my_dataframe
)


if ingredients_list:    
   ingredients_string = ''
   #name_on_order=''
   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
       #st.write(ingredients_string)
       #st.stop()
       my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" +NAME_ON_ORDER+ """')"""

       st.write(my_insert_stmt)
       #st.stop()

       #if ingredients_string:
       time_to_insert = st.button('Submit Order')
       if time_to_insert:
          session.sql(my_insert_stmt).collect()           
          st.success('Your Smoothie is ordered!', icon="✅")
