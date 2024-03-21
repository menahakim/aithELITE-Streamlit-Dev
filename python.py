import streamlit as st
from neo4j import GraphDatabase

# Neo4j connection parameters
uri = "neo4j+s://dba86135.databases.neo4j.io"
user = "neo4j"
password = "_B66GrNLR3uk6AZ8SA9hKewOGxLyJK4J8q7rt8d9q00"

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

# Streamlit app
def main():
    st.title("College Football Graph Explorer")

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
