import streamlit as st
from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection parameters
uri = "neo4j+s://722a0a63.databases.neo4j.io:7687"
user = "neo4j"
password = "1z9uUXRk4_WQxCbSpJE3qFiJPqRZPeyTXjyFa5kqeZA"


logo_path = "images/aitheletego.png"
st.image("images/aitheletego.png", width=150)  # Adjust width as needed

# Function to connect to Neo4j
def connect_to_neo4j(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))
# Function to execute Neo4j queries
def run_neo4j_query(driver, query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return list(result)


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
    st.sidebar.write("You selected 'Find Specific Stat'.")

    # Retrieve player names from Neo4j
    query = "MATCH (p:Player) RETURN p.name AS name ORDER BY name"
    result_list = run_neo4j_query(driver, query)

    # Extract player names from the result
    player_names = [record['name'] for record in result_list]

    # Dropdown to select a player
    player_name = st.sidebar.selectbox('Select a Player', player_names)

    if player_name:
        # Adjusted query to retrieve the player's specific stat
        stat_query = f"""
        MATCH (p:Player {{name: '{player_name}'}})
        RETURN p.stat AS stat
        """
        stat_result = run_neo4j_query(driver, stat_query)

        # Extract and display the stat if available
        if stat_result:
            stat = stat_result[0]['stat']
            st.write(f"### {player_name}'s Specific Stat: {stat}")
        else:
            st.write("Stat not found.")

        # Adjusted query to retrieve related stats
        related_stats_query = f"""
        MATCH (p:Player {{name: '{player_name}'}})-[:HAS_STAT]->(s:Stat)
        RETURN s.name AS stat_name
        """
        related_stats_result = run_neo4j_query(driver, related_stats_query)

        # Extract related stats
        related_stats = [record['stat_name'] for record in related_stats_result]

        # Dropdown to select related stats
        selected_stat = st.sidebar.selectbox('Select a Related Stat', related_stats)

        if selected_stat:
            # Additional actions for the selected related stat
            st.write(f"### Selected Related Stat: {selected_stat}")


def display_school_roster(driver):
    st.write("You selected 'Display School Roster'.")

    # Step 1: Select a School (existing code)
    school_query = "MATCH (s:School) RETURN s.name AS name, s.id AS id ORDER BY name"
    school_result_list = run_neo4j_query(driver, school_query)
    
    if not school_result_list:
        st.write("No schools found.")
        return
    
    school_options = {record['name']: record['id'] for record in school_result_list}
    selected_school_name = st.selectbox('Select a School', list(school_options.keys()))
    selected_school_id = school_options[selected_school_name]

    # Displaying the selected School ID for debugging
    st.write(f"Selected School ID: {selected_school_id}")  # This line can be commented out or removed after confirming it works

    # Step 2: Fetch and Display the Roster for the Selected School
    roster_query = """
    MATCH (s:School {id: $schoolId})-[:HAS_PROGRAM]->(p:Program)
    -[:HAS_SEASON]->(season:Season)-[:ON_ROSTER]->(player:Player)
    RETURN season.name AS seasonName, player.first_name + ' ' + player.last_name AS playerName
    ORDER BY seasonName, playerName
    """
    roster_result = run_neo4j_query(driver, roster_query, {'schoolId': selected_school_id})

    if roster_result:
        st.write(f"### Roster for {selected_school_name}:")
        current_season = None
        for record in roster_result:
            if record['seasonName'] != current_season:
                current_season = record['seasonName']
                st.write(f"#### Season: {current_season}")
            st.write(f"- {record['playerName']}")
    else:
        st.write("No players found on this school's roster.")

def find_player_hometown(driver):
    st.write("You selected 'Find Player's Hometown'.")

    # Retrieve player names from Neo4j
    query = "MATCH (p:Player) RETURN p.team_roster_name AS name ORDER BY name"
    result_list = run_neo4j_query(driver, query)

    # Extract player names from the result
    if result_list:
        player_names = [record['name'] for record in result_list]
    else:
        player_names = []

    if player_names:
        # Dropdown to select a player
        player_name = st.selectbox('Select a Player', player_names)

        # Adjusted query to retrieve the player's home_town_id property using the selected player name
        hometown_query = f"""
        MATCH (p:Player {{team_roster_name: '{player_name}'}})
        RETURN p.home_town_id AS hometown
        """
        hometown_result = run_neo4j_query(driver, hometown_query)

        # Extract and display the hometown if available
        if hometown_result and hometown_result[0]['hometown']:
            hometown = hometown_result[0]['hometown']
            st.write(f"### {player_name}'s Hometown: {hometown}")
        else:
            st.write("Hometown not found.")
    else:
        st.write("No players found in the database.")


# Streamlit app is here 
def main():
    st.title("AithELITE Coach Helper")

    # Neo4j connection
    driver = connect_to_neo4j(uri, user, password)
    #how is the day ended 
    # Dropdown menu to select action
    action = st.selectbox(
        "Select an action",
        ["Compare 2 Players", "Find Specific Stat", "Display School Roster", "Find Player's Hometown"]
    )

    if action == "Compare 2 Players":
        compare_players(driver)
    elif action == "Search Stats By Name":
        find_specific_stat(driver)
    elif action == "Display School Roster":
        display_school_roster(driver)
    elif action == "Find Player's Hometown":
        find_player_hometown(driver)
    

if __name__ == "__main__":
    main()
