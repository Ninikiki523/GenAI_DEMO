import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor
import pandas as pd

# Snowflake parameter
conn_params = {
    "user": "zhemma523",
    "password": "Mayday_523",
    "account": "CHPVMZF-CH77012",
    "warehouse": "COMPUTE_WH",
    "database": "SNOWFLAKE_SAMPLE_DATA",
    "schema": "TPCH_SF1"
}

# connection
ctx = snowflake.connector.connect(**conn_params)
cs = ctx.cursor(DictCursor)

# title
st.title('Exxeta Chatbot')

# database list
cs.execute("SHOW DATABASES")
databases = [db['name'] for db in cs]

# Create a checkbox to allow users to select a database
selected_db = st.selectbox("choose a database", databases)

# User input box
input_text = st.text_input("What can I do for you?")
# convert_to_sql function

def convert_to_sql(input_content):
    input_content = input_content.lower()

    if input_content == "view all customer":
        return f"SELECT * FROM customer;"
    elif input_content == "tell me the number of customers":
        return f"SELECT COUNT(*) FROM customer;"
    elif input_content == "check out the latest orders":
        return f"SELECT * FROM orders ORDER BY O_ORDERDATE DESC LIMIT 1;"
    #elif input_content == "tell me the top 10 key account":
    #    return f"SELECT * FROM orders ORDER BY O_ORDERDATE DESC LIMIT 1;"
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
        cs.execute(f"USE DATABASE SNOWFLAKE_SAMPLE_DATA")
        cs.execute(f"USE SCHEMA TPCH_SF1")
        
        # Executing SQL Queries
        cs.execute(sql_query)
        rows = cs.fetchall()
        columns = [col[0] for col in cs.description]
        results = pd.DataFrame(rows, columns=columns)
        st.write(results)
        st.stop()
        # Show query results
        if results:
            st.dataframe(df)
        else:
            st.write("No results found.")
    else:
        st.error("Please enter a query.")

# Close connection
cs.close()
ctx.close()

# Running the Streamlit application
# streamlit run your_script.py
