import streamlit as st
import random

# Game initialization
if 'treasure_location' not in st.session_state:
    st.session_state['treasure_location'] = random.choice(['Cave', 'Forest', 'Mountain', 'Lake', 'Abandoned Castle'])
if 'attempts' not in st.session_state:
    st.session_state['attempts'] = 5  # For example, give the player 5 attempts

# Game interface
st.title("Treasure Hunt Mini-Game")

# Check if the game is already won or lost
if 'game_over' in st.session_state and st.session_state['game_over']:
    st.write("Game Over! Restart to play again.")
elif 'found_treasure' in st.session_state and st.session_state['found_treasure']:
    st.success("Congratulations! You found the treasure!")
else:
    st.write("Choose a location to search for the treasure:")

    locations = ['Cave', 'Forest', 'Mountain', 'Lake', 'Abandoned Castle']
    for loc in locations:
        if st.button(loc):
            if loc == st.session_state['treasure_location']:
                st.session_state['found_treasure'] = True
                st.success(f"You found the treasure in the {loc}!")
            else:
                st.session_state['attempts'] -= 1
                if st.session_state['attempts'] <= 0:
                    st.session_state['game_over'] = True
                    st.error("You've run out of attempts! Game Over.")
                else:
                    st.warning(f"The treasure is not in the {loc}. Attempts remaining: {st.session_state['attempts']}")

# Option to restart the game
if st.button("Restart Game"):
    st.session_state['treasure_location'] = random.choice(locations)
    st.session_state['attempts'] = 5
    st.session_state['game_over'] = False
    st.session_state['found_treasure'] = False
    st.experimental_rerun()
