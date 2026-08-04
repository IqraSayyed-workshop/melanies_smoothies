# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Page title
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write("Orders that need to be filled.")

# Get Snowflake session
session = get_active_session()

# Get pending orders
my_dataframe = session.table("smoothies.public.orders") \
    .filter(col("ORDER_FILLED") == False) \
    .collect()

# If there are pending orders, display them
if len(my_dataframe) > 0:

    editable_df = st.data_editor(
        my_dataframe,
        use_container_width=True
    )

    submitted = st.button("Submit")

    if submitted:

        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        og_dataset.merge(
            edited_dataset,
            (og_dataset["ORDER_UID"] == edited_dataset["ORDER_UID"]),
            [
                when_matched().update(
                    {"ORDER_FILLED": edited_dataset["ORDER_FILLED"]}
                )
            ]
        )

        st.success("Orders updated successfully!")

else:
    st.info("There are no pending orders right now.")
