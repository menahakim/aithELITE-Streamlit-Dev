import streamlit as st
from neo4j import GraphDatabase

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

# Function to compare two players
# Function to compare two players
# Function to compare two players
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

# Function to find a specific stat
def find_specific_stat(driver):
    st.write("You selected 'Find Specific Stat'.")
    # Your code for finding specific stats goes here

# Function to search the whole team
def search_whole_team(driver):
    st.write("You selected 'Search Whole Team'.")
    # Your code for searching the whole team goes here

def find_player_hometown(driver):
    st.write("You selected 'Find Player's Hometown'.")

    # Retrieve player names from Neo4j
    query = "MATCH (p:Player) RETURN p.name AS name ORDER BY name"
    result_list = run_neo4j_query(driver, query)

    # Extract player names from the result
    player_names = [record['name'] for record in result_list]

    # Dropdown to select a player
    player_name = st.selectbox('Select a Player', player_names)

    # Query to find the player's hometown
    hometown_query = f"MATCH (p:Player {{name: '{player_name}'}}) RETURN p.hometown AS hometown"
    hometown_result = run_neo4j_query(driver, hometown_query)

    # Extract and display the hometown if available
    if hometown_result:
        hometown = hometown_result[0]['hometown']
        st.write(f"### {player_name}'s Hometown: {hometown}")
    else:
        st.write("Hometown not found.")


# Streamlit app

def main():
    st.title("AithELITE Coach Helper")

    # Neo4j connection
    driver = connect_to_neo4j(uri, user, password)

    # Dropdown menu to select action
    action = st.selectbox(
        "Select an action",
        ["Compare 2 Players", "Find Specific Stat", "Search Whole Team", "Find Player's Hometown"]  # Added new action
    )

    if action == "Compare 2 Players":
        compare_players(driver)
    elif action == "Find Specific Stat":
        find_specific_stat(driver)
    elif action == "Search Whole Team":
        search_whole_team(driver)
    elif action == "Find Player's Hometown":  # New condition for the new action
        find_player_hometown(driver)

