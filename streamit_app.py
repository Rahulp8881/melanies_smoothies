# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

st.title ('Pending Smoothie Orders')
st.write ('choose the fruit as you want')

NAME_ON_ORDER = st.text_input('Name on smoothie:')
st.write('The name on smoothe is', NAME_ON_ORDER)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
   editable_df = st.experimental_data_editor(my_dataframe)
   submitted = st.button('Submit')
   if submitted:
    
      og_dataset = session.table("smoothies.public.orders")
      edited_dataset = session.create_dataframe(editable_df)
    
      try:
         og_dataset.merge(edited_dataset
                     , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
         st.success("someone cliked the button")
      except:
         st.text('something went wrong')
   else:
       st.success('there is no pending order right now')
st.stop()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
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
