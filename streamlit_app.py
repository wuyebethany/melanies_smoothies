# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

st.title(f":cup_with_straw: Pending Smoothie Orders! :cup_with_straw:")
st.write(
  """
  **Orders that need to be filled**
  """
)

og_dataset = session.table("smoothies.public.orders")
my_dataframe = og_dataset.filter(col("ORDER_FILLED") == False).to_pandas()

if not my_dataframe.empty:
    editable_df = st.data_editor(
        my_dataframe,
        column_config={
            "ORDER_FILLED": st.column_config.CheckboxColumn("Order Filled?")
        },
        disabled=["INGREDIENTS", "NAME_ON_ORDER"],
    )

    if st.button("Submit"):
        for _, row in editable_df.iterrows():
            if row["ORDER_FILLED"]:
                session.sql(
                    f"UPDATE smoothies.public.orders SET order_filled = TRUE WHERE name_on_order = '{row['NAME_ON_ORDER']}'"
                ).collect()
        st.success("Orders updated!", icon="✅")
        st.rerun()
else:
    st.write("No pending orders.")

