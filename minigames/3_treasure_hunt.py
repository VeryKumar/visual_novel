import streamlit as st
import random

# Function to provide clues
def get_clue(selected_location, treasure_location):
    clues = {
         ('Cave', 'Forest'): "The echoes in the cave won't help you find the treasure.",
        ('Forest', 'Cave'): "The dense forest obscures your path to the treasure.",
        ('Mountain', 'Lake'): "The treasure isn't high up on the mountain peaks.",
        ('Lake', 'Mountain'): "The calm lake holds no secrets to the treasure's whereabouts.",
        ('Cave', 'Mountain'): "The cave is too dark to reveal the treasure.",
        ('Mountain', 'Cave'): "The mountain's height offers no advantage in this hunt.",
        ('Forest', 'Lake'): "The sounds of the forest drown out the clues.",
        ('Lake', 'Forest'): "The still waters are far from the rustling leaves where the treasure lies.",
        ('Cave', 'Lake'): "The cave's dampness contrasts the dry treasure location.",
        ('Lake', 'Cave'): "The open waters reflect a different location for the treasure.",
        ('Forest', 'Mountain'): "The forest floor is too level to hide this treasure.",
        ('Mountain', 'Forest'): "The mountain air is too crisp for where the treasure is hidden.",
        ('Abandoned Castle', 'Cave'): "The castle's ruins hold more secrets than the empty cave.",
        ('Cave', 'Abandoned Castle'): "The cave's solitude is far from the historic walls of the treasure.",
        # Add more clues for different combinations
    }
    return clues.get((selected_location, treasure_location), "This location doesn't seem right.")

# Initialize game state
if 'treasure_location' not in st.session_state:
    st.session_state['treasure_location'] = random.choice(['Cave', 'Forest', 'Mountain', 'Lake', 'Abandoned Castle'])
if 'attempts_left' not in st.session_state:
    st.session_state['attempts_left'] = 3  # Total attempts allowed
if 'selected_location' not in st.session_state:
    st.session_state['selected_location'] = ''

st.title("Treasure Hunt Mini-Game")

# Select location
st.session_state['selected_location'] = st.selectbox("Choose a location to search for the treasure:", ['Cave', 'Forest', 'Mountain', 'Lake', 'Abandoned Castle'])

# Search button
if st.button("Search here!"):
    if st.session_state['selected_location'] == st.session_state['treasure_location']:
        st.balloons()
        st.success(f"Congratulations! You found the treasure in the {st.session_state['selected_location']}!")
    else:
        st.session_state['attempts_left'] -= 1
        if st.session_state['attempts_left'] > 0:
            clue = get_clue(st.session_state['selected_location'], st.session_state['treasure_location'])
            st.warning(f"No treasure in the {st.session_state['selected_location']}. {clue}")
            st.write(f"Attempts left: {st.session_state['attempts_left']}")
        else:
            st.error(f"You've run out of attempts! The treasure was in the {st.session_state['treasure_location']}.")

# Restart the game
if st.button("Restart Game"):
    st.session_state['treasure_location'] = random.choice(['Cave', 'Forest', 'Mountain', 'Lake', 'Abandoned Castle'])
    st.session_state['attempts_left'] = 3
    st.session_state['selected_location'] = ''
    st.rerun()
