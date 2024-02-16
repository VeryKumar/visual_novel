import streamlit as st

# # Example function to handle a turn
# def handle_turn(action):
#     # Update game state based on action
#     # Return text describing what happened
#     return "Player chose to {}".format(action)

# # Initialize session state
# if 'battle_log' not in st.session_state:
#     st.session_state['battle_log'] = "Battle begins!\n"

# # Layout
# st.title("Battle Game")

# col1, col2 = st.columns(2)

# with col1:
#     st.header("Player")
#     player_health = st.progress(100)
#     # Add more player stats here

# with col2:
#     st.header("Enemy")
#     enemy_health = st.progress(100)
#     # Add more enemy stats here

# # Action buttons
# if st.button("Attack"):
#     st.session_state['battle_log'] += handle_turn("attack") + "\n"
# if st.button("Defend"):
#     st.session_state['battle_log'] += handle_turn("defend") + "\n"
# # Add more actions here

# # Battle log
# st.text_area("Battle Log", st.session_state['battle_log'], height=150)

import streamlit as st

# Move class definition
class Move:
    def __init__(self, name, type, power, description):
        self.name = name
        self.type = type
        self.power = power
        self.description = description

# Updated Character class definition
class Character:
    def __init__(self, name, session_state_key, max_health, moves):
        self.name = name
        self.session_state_key = session_state_key
        self.max_health = max_health
        self.moves = moves

    @property
    def health(self):
        return st.session_state[self.session_state_key]

    @health.setter
    def health(self, value):
        st.session_state[self.session_state_key] = value

    def is_defeated(self):
        return self.health <= 0

# Initialize session state for health
if 'player_health' not in st.session_state:
    st.session_state['player_health'] = 100  # Initial health

if 'enemy_health' not in st.session_state:
    st.session_state['enemy_health'] = 100  # Initial health

# Initialize moves
move1 = Move("Thunderbolt", "Attack", 25, "A strong electric attack.")
move2 = Move("Heal", "Heal", 20, "Restores health.")
move3 = Move("Fire Blast", "Attack", 30, "A fiery attack.")
move4 = Move("Blizzard", "Attack", 30, "A chilling attack.")

# Initialize characters
player = Character("Player", 'player_health', 100, [move1, move2, move3, move4])
enemy = Character("Enemy", 'enemy_health', 100, [move1, move1, move1, move1])

# Function to execute a move
def execute_move(attacker, defender, move):
    if move.type == "Attack":
        damage = move.power
        defender.health = max(defender.health - damage, 0)
    elif move.type == "Heal":
        healed_amount = move.power
        attacker.health = min(attacker.health + healed_amount, attacker.max_health)

    action_result = f"{attacker.name} used {move.name}."
    if move.type == "Attack":
        action_result += f" {defender.name} took {damage} damage."
    elif move.type == "Heal":
        action_result += f" {attacker.name} healed {healed_amount} HP."

    return action_result

# Function to handle a turn
def handle_turn(player_move_index):
    global player, enemy

    # Player's turn
    player_action = execute_move(player, enemy, player.moves[player_move_index])
    st.session_state['battle_log'] += player_action + "\n"

    # Check for defeat after each turn
    if enemy.is_defeated():
        st.session_state['battle_log'] += f"{enemy.name} is defeated!\n"
        return
    if player.is_defeated():
        st.session_state['battle_log'] += f"{player.name} is defeated!\n"
        return

    # Enemy's turn (always uses the first move)
    enemy_action = execute_move(enemy, player, enemy.moves[0])
    st.session_state['battle_log'] += enemy_action + "\n"

# Streamlit interface
st.title("Turn-Based Battle")

# Display health bars
col1, col2 = st.columns(2)
with col1:
    st.image("/Users/varunkumar/Development/visual_novel/minigames/assets/player.png", width=200)  # Replace with your player image path
    st.progress(player.health / player.max_health)

with col2:
    st.image("/Users/varunkumar/Development/visual_novel/minigames/assets/enemy.png", width=200)  # Replace with your enemy image path
    st.progress(enemy.health / enemy.max_health)

# Action buttons
for i, move in enumerate(player.moves):
    if st.button(move.name):
        handle_turn(i)
        st.rerun()

# Initialize battle log
if 'battle_log' not in st.session_state:
    st.session_state['battle_log'] = ""

# Display battle log
st.text_area("Battle Log", st.session_state['battle_log'], height=250)
