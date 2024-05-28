import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor
import pandas as pd

# Snowflake parameter
conn_params = {
    "user": "zhemma523",
    "password": "Mayday_523",
    "account": "CHPVMZF-CH77012",
    "warehouse": "COMPUTE_WH"
    #"database": "SNOWFLAKE_SAMPLE_DATA",
    #"schema": "TPCH_SF1"
}

# connection
ctx = snowflake.connector.connect(**conn_params)
cs = ctx.cursor(DictCursor)

# title
gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, black, pink);
    background: linear-gradient(to right, black, pink);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div class="gradient-text">DIA Chat</div>
"""

st.markdown(gradient_text_html, unsafe_allow_html=True)

st.caption("Talk with your own data")

#select a model, here is just a sample, without real connection with the models
st.markdown("<p style='color: pink;'>Please select a model</p>", unsafe_allow_html=True)
model = st.radio(
    "",
    options=["Exxeta Pro", "Llama 3-70B", "GPT-3.5", "Snowflake Arctic"],
    index=0,
    horizontal=True,
)

# database list
cs.execute("SHOW DATABASES")
databases = [db['name'] for db in cs]

#select a database
st.markdown("<p style='color: pink;'>Please select a database</p>", unsafe_allow_html=True)
selected_db = st.radio(
    "",
    options=databases,
    index=0,
    horizontal=True,
)

# Or Create a checkbox to allow users to select a database
#selected_db = st.selectbox("choose a database", databases)

#schema list
#cs.exucute(f"USE DATABASE {selected_db}")
cs.execute("SHOW SCHEMAS")
schemas = [schema['name'] for schema in cs]

#select a schema
st.markdown("<p style='color: pink;'>Please select a schema</p>", unsafe_allow_html=True)
selected_schema = st.radio(
    "",
    options=databases,
    index=0,
    horizontal=True,
)

# User input box
input_text = st.text_input("What can I do for you?")

# convert_to_sql function. Here are just some examples for the sake of demonstration, subsequently we should enrich the content with the help of GPT's model
def convert_to_sql(input_content):
    input_content = input_content.lower()

    if input_content == "view all customer":
        return f"SELECT * FROM customer;"
    elif input_content == "tell me the number of customers":
        return f"SELECT COUNT(*) FROM customer;"
    elif input_content == "check out the latest orders":
        return f"SELECT * FROM orders ORDER BY O_ORDERDATE DESC LIMIT 1;"
    #elif input_content == "tell me the top 10 key account":
    #    return f";"
    else:
        return "I'm sorry I can't recognize your query, please replace it with another way"


# send button
if st.button('send'):
    if input_text:
        # Here you need to convert the user's natural language into a SQL query
        # This may require natural language processing or some sort of mapping logic
        sql_query = convert_to_sql(input_text)
        
        # Switching databases
        cs.execute(f"USE ROLE ACCOUNTADMIN")
        cs.execute(f"USE DATABASE {selected_db}")
        cs.execute(f"USE SCHEMA TPCH_SF1")
        
        # Executing SQL Queries
        cs.execute(sql_query)
        rows = cs.fetchall()
        if rows:
            columns = [col[0] for col in cs.description]
            results = pd.DataFrame(rows, columns=columns)
            #show query result and drop the index col
            result_no_index = results.reset_index(drop=True)
            st.dataframe(result_no_index)
            
        else:
            st.write("No results found.")
    else:
        st.error("Please enter a query.")

# Close connection
cs.close()
ctx.close()

# Running the Streamlit application
# streamlit run your_script.py
