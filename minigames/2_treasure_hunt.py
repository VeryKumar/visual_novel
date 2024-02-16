import streamlit as st
import pydeck as pdk
import random

# Define treasure locations with coordinates
treasure_locations = {
    'Cave': {'lat': 37.7749, 'lon': -122.4194},
    'Forest': {'lat': 37.8715, 'lon': -122.2730},
    'Mountain': {'lat': 37.8025, 'lon': -122.4057},
    'Lake': {'lat': 37.8044, 'lon': -122.2711},
    'Abandoned Castle': {'lat': 37.8719, 'lon': -122.2585}
}

# Initialize game
if 'treasure_location' not in st.session_state:
    st.session_state['treasure_location'] = random.choice(list(treasure_locations.keys()))
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False
if 'selected_location' not in st.session_state:
    st.session_state['selected_location'] = list(treasure_locations.keys())[0]

# Function to create the map
def create_map(treasure_locations, selected_location):
    # Create a list of PyDeck markers for each location
    markers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=[{
                "latitude": loc['lat'],
                "longitude": loc['lon']
            }],
            get_position=["longitude", "latitude"],
            get_color=[255, 0, 0, 160] if key == selected_location else [0, 0, 255, 160],
            get_radius=10000,
            pickable=True
        )
        for key, loc in treasure_locations.items()
    ]

    # Set the view to the selected marker
    view_state = pdk.ViewState(
        latitude=treasure_locations[selected_location]['lat'],
        longitude=treasure_locations[selected_location]['lon'],
        zoom=10,
        pitch=0
    )

    # Render the map with the markers
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=markers
    ))

# Streamlit interface
st.title("Treasure Hunt Mini-Game")

# Drop-down to select a location
if not st.session_state['game_over']:
    st.session_state['selected_location'] = st.selectbox("Choose a location to search for the treasure:", list(treasure_locations.keys()))

# Display the map
create_map(treasure_locations, st.session_state['selected_location'])

# Confirm button
if st.button("Search here!"):
    if st.session_state['selected_location'] == st.session_state['treasure_location']:
        st.success(f"Congratulations! You found the treasure in the {st.session_state['selected_location']}!")
        st.session_state['game_over'] = True
    else:
        st.error(f"No treasure in the {st.session_state['selected_location']}. Try another location.")

# Restart the game
if st.button("Restart Game"):
    st.session_state['treasure_location'] = random.choice(list(treasure_locations.keys()))
    st.session_state['game_over'] = False
    st.session_state['selected_location'] = list(treasure_locations.keys())[0]
    st.experimental_rerun()
