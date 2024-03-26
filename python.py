#testing push


import streamlit as st
from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection parameters
uri = "neo4j+s://722a0a63.databases.neo4j.io:7687"
user = "neo4j"
password = "1z9uUXRk4_WQxCbSpJE3qFiJPqRZPeyTXjyFa5kqeZA"

# Function to connect to Neo4j
def connect_to_neo4j(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))

# Function to execute Neo4j queries
def run_neo4j_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        # Convert result set to a list
        result_list = list(result)
        return result_list

# Function to compare two players and display their properties in a table
def compare_players(driver):
    st.write("You selected 'Compare 2 Players'.")
    
    # Retrieve player names from Neo4j
    query = "MATCH (p:Player) RETURN p.name AS name ORDER BY name"
    result_list = run_neo4j_query(driver, query)

    # Extract player names from the result
    player_names = [record['name'] for record in result_list]

    # Dropdowns to select two players
    player1 = st.selectbox('Select Player 1', player_names)
    player2 = st.selectbox('Select Player 2', player_names)

    # Display selected players
    st.write(f'### Player 1: {player1}')
    st.write(f'### Player 2: {player2}')

    # Retrieve properties of the selected players
    query_player1 = f"MATCH (p:Player {{name: '{player1}'}}) RETURN p"
    query_player2 = f"MATCH (p:Player {{name: '{player2}'}}) RETURN p"

    result_player1 = run_neo4j_query(driver, query_player1)
    result_player2 = run_neo4j_query(driver, query_player2)

    if result_player1 and result_player2:
        # Display properties in two tables side by side
        col1, col2 = st.columns(2)

        with col1:
            st.write("### Player 1 Properties")
            display_properties(result_player1[0]['p'])

        with col2:
            st.write("### Player 2 Properties")
            display_properties(result_player2[0]['p'])
    else:
        st.write("One or both of the selected players were not found in the database.")

# Function to display properties in a table
def display_properties(player):
    properties = player.keys()
    rows = []
    for prop in properties:
        rows.append([prop, player[prop]])
    st.table(rows)

# Function to find a specific stat
def find_specific_stat(driver):
    st.write("You selected 'Find Specific Stat'.")
    # Your code for finding specific stats goes here

# Function to search the whole team
def search_whole_team(driver):
    st.write("You selected 'Search Whole Team'.")
    # Your code for searching the whole team goes here

# Streamlit app
def main():
    st.title("AithELITE Coach Helper")

    # Neo4j connection
    driver = connect_to_neo4j(uri, user, password)

    # Dropdown menu to select action
    action = st.selectbox("Select an action", ["Compare 2 Players", "Find Specific Stat", "Search Whole Team"])

    if action == "Compare 2 Players":
        compare_players(driver)
    elif action == "Find Specific Stat":
        find_specific_stat(driver)
    elif action == "Search Whole Team":
        search_whole_team(driver)

if __name__ == "__main__":
    main()
