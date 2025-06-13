import streamlit as st
import random

st.set_page_config(page_title="Cross Clues Lite", layout="centered")

st.title("🧠 Cross Clues - Virtual Edition")

# --- WORD LIST ---
word_bank = [
    "Doctor", "Bear", "Ocean", "Rocket", "School",
    "Zoo", "Ice", "Star", "Dragon", "Glass",
    "King", "Hospital", "Fire", "Music", "Light",
    "Mountain", "Robot", "Police", "Dance", "Garden",
    "Time", "Shadow", "Space", "Tree", "Cloud"
]

# --- SESSION STATE ---
if "grid_words" not in st.session_state:
    st.session_state.grid_words = random.sample(word_bank, 25)
    st.session_state.secret_coord = None
    st.session_state.show_secret = False
    st.session_state.clue = ""

# --- GRID SETUP ---
grid_labels_cols = ['A', 'B', 'C', 'D', 'E']
grid_labels_rows = ['1', '2', '3', '4', '5']
grid_matrix = [[st.session_state.grid_words[i*5 + j] for j in range(5)] for i in range(5)]

st.markdown("### 📋 Word Grid")
grid_table = "| | A | B | C | D | E |\n|--|--|--|--|--|--|"
for i, row in enumerate(grid_matrix):
    row_str = f"| {i+1} | " + " | ".join(row) + " |"
    grid_table += f"\n{row_str}"
st.markdown(grid_table)

# --- SELECT CLUE-GIVER ---
st.markdown("### 🎯 Clue-Giver")
if st.button("🎲 Draw a Secret Coordinate"):
    rand_col = random.choice(grid_labels_cols)
    rand_row = random.choice(grid_labels_rows)
    st.session_state.secret_coord = f"{rand_col}{rand_row}"
    st.session_state.show_secret = True
    st.session_state.clue = ""

if st.session_state.show_secret:
    st.success(f"Your secret coordinate is: **{st.session_state.secret_coord}**")
    col_index = grid_labels_cols.index(st.session_state.secret_coord[0])
    row_index = grid_labels_rows.index(st.session_state.secret_coord[1])
    word = grid_matrix[row_index][col_index]
    st.info("The intersecting words are hidden — clue-giver knows them.")
    st.text_input("Give a one-word clue:", key="clue")

# --- TEAM GUESS ---
st.markdown("### 🧠 Team Guess")
guess = st.text_input("What coordinate do you think matches the clue? (e.g., B3)")
if guess:
    if guess.upper() == st.session_state.secret_coord:
        st.success("✅ Correct guess!")
    else:
        st.error(f"❌ Wrong. The correct answer was {st.session_state.secret_coord}")

# --- RESET ---
if st.button("🔁 Reset Game"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()
