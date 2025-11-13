# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:' , name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# Display the full list of options in a table format as shown in the image
st.dataframe(data=my_dataframe, use_container_width=True) 

# Convert Snowpark dataframe to a list for the multiselect options
st_my_dataframe = my_dataframe.to_pandas()
ingredients_list = st_my_dataframe['FRUIT_NAME'].tolist()

ingredients_selected = st.multiselect(
    'Choose up to 5 ingredients:',
    ingredients_list
)

if ingredients_selected:
    # Use join to create the ingredients string cleanly
    ingredients_string = ', '.join(ingredients_selected)

    # st.write(ingredients_string) # Optional debug output shown in the image
    st.text(ingredients_string) # Optional debug output shown in the image

    # Define the insert statement here (this fixes the NameError in the original snippet)
    my_insert_stmt = f"""
        insert into smoothies.public.orders (ingredients)
        values ('{ingredients_string}')
    """
    
    # st.write(my_insert_stmt) # Optional debug output shown in the image

    # Execute the SQL insert immediately
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


