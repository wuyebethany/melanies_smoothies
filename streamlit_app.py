import streamlit as st
from snowflake.snowpark.functions import col, when_matched  # ← fixed import, plural
from snowflake.snowpark.context import get_active_session
import requests

session = get_active_session()  # ← define session first

st.title(":cup_with_straw: Pending Smoothie Orders! :cup_with_straw:")
st.write("**Orders that need to be filled**")

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == False).to_pandas()

if not my_dataframe.empty:
    editable_df = st.data_editor(
        my_dataframe,
        column_config={
            "ORDER_FILLED": st.column_config.CheckboxColumn("Order Filled?")
        },
        disabled=["INGREDIENTS", "NAME_ON_ORDER"],
    )
    if st.button("Submit"):
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        og_dataset.merge(
            edited_dataset,
            og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'],
            [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
        )
        st.success("Orders updated!", icon="✅")
        st.rerun()
else:
    st.write("No pending orders.")

# Smoothiefroot nutrition info
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())  # ← use .json() to display actual data
