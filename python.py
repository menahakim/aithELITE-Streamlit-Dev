#testing push


import streamlit as st
from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection parameters
uri = ""
user = ""
password = ""


logo_path = "images/aitheletego.png"
st.image("images/aitheletego.png", width=150)  

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

def get_player_data(player_name, session):
    """
    Fetches yards per rush and rushing attempts for a specified player from the Neo4j database.
    
    Parameters:
    - player_name: str, the name of the player to search for.
    - session: Neo4j database session for executing the query.
    
    Returns:
    - A dictionary with 'yds_per_rush' and 'rushing_attempts' if data is found, or None otherwise.
    """
    # Cypher query to fetch the player's yards per rush and rushing attempts
    query = """
    MATCH (p:Player)-[:PLAYS]->(:Position)-[:HAS_STAT]->(s:Stat)
    WHERE p.name = $player_name
    RETURN s.yds_per_rush AS yds_per_rush, s.rushing_attempts AS rushing_attempts
    """
    result = session.run(query, player_name=player_name)
    record = result.single()  # Assuming there's only one record for each player

    if record:
        # Return the fetched data as a dictionary
        return {
            "yds_per_rush": record["yds_per_rush"],
            "rushing_attempts": record["rushing_attempts"]
        }
    else:
        # Return None if no data was found
        return None
def get_player_data_with_relationship(player_name, session):
    query = """
        MATCH (p:Player)-[:HAS_STAT_VALUE]->(s:`Stat Value`)
        WHERE p.name = $player_name AND s.stat_name = 'yds_per_rush'
        RETURN s.value AS yds_per_rush, s.rushing_attempts AS rushing_attempts
    """
    result = session.run(query, player_name=player_name)
    record = result.single()

    if record:
        return {
            'yds_per_rush': record['yds_per_rush'],
            'rushing_attempts': record['rushing_attempts']
        }
    else:
       return None

def find_yards_per_rush_for_player(driver):
    st.write("You selected 'Find Yards Per Rush for a Player'.")

    # Fetch player names for the dropdown
    query = "MATCH (p:Player) RETURN p.name AS name ORDER BY name"
    result_list = run_neo4j_query(driver, query)
    player_names = [record['name'] for record in result_list]

    # Dropdown to select a player
    player_name = st.selectbox('Select a Player for Yards Per Rush', player_names, key='ypr_player')

    # Button to fetch data
    if st.button('Find Yards Per Rush'):
        # Assuming `session` should be created usinag the provided `driver`
        with driver.session() as session:
            player_data = get_player_data_with_relationship(player_name, session)

            if player_data:
                yards_per_rush = player_data['yds_per_rush']
                rushing_attempts = player_data['rushing_attempts']
                st.success(f"Yards per rush for {player_name}: {yards_per_rush}, based on {rushing_attempts} attempts.")
            else:
                st.error("Player not found or no stats available. Please check the name and try again.")




# Function to display school roster
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
    query = "MATCH (p:Player) RETURN p.name AS name ORDER BY name"
    result_list = run_neo4j_query(driver, query)

    # Extract player names from the result
    player_names = [record['name'] for record in result_list]

    # Dropdown to select a player
    player_name = st.selectbox('Select a Player', player_names)

    # Adjusted query to retrieve the player's home_town_id property
    hometown_query = f"""
    MATCH (p:Player {{name: '{player_name}'}})
    RETURN p.home_town_id AS hometown
    """
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
        ["Compare 2 Players", "Display School Roster", "Find Player's Hometown", "Find Yards Per Rush for a Player"]
    )

    if action == "Compare 2 Players":
        compare_players(driver)
    elif action == "Display School Roster":
        display_school_roster(driver)
    elif action == "Find Player's Hometown":
        find_player_hometown(driver)
    elif action == "Find Yards Per Rush for a Player":
        find_yards_per_rush_for_player(driver)

if __name__ == "__main__":
    main()


