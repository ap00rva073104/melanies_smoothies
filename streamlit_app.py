# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f"Customize Your Smoothie!:cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom Smoothie
    """
)


# Get the Name input (must be defined before the ingredients selection logic)
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)


session = get_active_session()

# --- Data Fetching Logic ---
my_dataframe = session.table("smoothies.public.fruit_options")

# Extract only the FRUIT_NAME column to a list for the multiselect options
ingredients_names = [row[0] for row in my_dataframe.select(col('FRUIT_NAME')).collect()]

# Use the list of names for the options
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    ingredients_names
)
# -----------------------------

# Variable to hold the final SQL statement for submission
my_insert_stmt = ""

if ingredients_list:
    # 1. Prepare the ingredients string
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    st.write("You selected:", ingredients_string)

    # 2. Correct the SQL INSERT Statement: 
    #    It must include both 'ingredients' AND 'name_on_order' columns 
    #    to match the two values provided.
    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients, name_on_order)
    values ('{ingredients_string.strip()}', '{name_on_order}')"""

    # st.write(my_insert_stmt) # Uncomment this if you want to see the SQL command being generated

# ----------------------------------------------------------------------------------
# The Submit Button and Insertion logic are placed here, after the definition of all
# UI elements above, to ensure they are rendered correctly and are clickable.
# ----------------------------------------------------------------------------------

time_to_insert = st.button('Submit Order')

if time_to_insert:
    if not name_on_order:
        st.error("Please enter a name for your smoothie before submitting.")
    elif not ingredients_list:
        st.error("Please select at least one ingredient.")
    else:
        # Execute the SQL command
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!')
        # st.stop() # Optional: Uncomment this line if you want the app to stop after a successful order.
