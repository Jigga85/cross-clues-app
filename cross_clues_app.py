import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Cross Clues Lite", layout="centered")

st.title("🧠 Cross Clues - Virtual Edition")

# --- WORD LIST ---
word_bank = [
    "Doctor", "Bear", "Ocean", "Rocket", "School",
    "Zoo", "Ice", "Star", "Dragon", "Glass",
    "King", "Hospital", "Fire", "Music", "Light",
    "Mountain", "Robot", "Police", "Dance", "Garden",
    "Time", "Shadow", "Space", "Tree", "Cloud",
    "Shirt", "Day", "Book", "Gold", "Wind"
]

# --- SESSION STATE INIT ---
if "column_words" not in st.session_state:
    selected_words = random.sample(word_bank, 10)
    st.session_state.column_words = selected_words[:5]
    st.session_state.row_words = selected_words[5:]
    st.session_state.secret_coord = None
    st.session_state.show_secret = False
    st.session_state.clue = ""

# --- AXES LABELS ---
grid_labels_cols = ['A', 'B', 'C', 'D', 'E']
grid_labels_rows = ['1', '2', '3', '4', '5']

# --- DISPLAY ENHANCED GRID WITH LABELS AND AXIS WORDS ---
st.markdown("### 🗺️ Game Grid with Axis Words")

grid_matrix = [['' for _ in range(6)] for _ in range(6)]

# Fill in column labels
for j, col in enumerate(grid_labels_cols):
    grid_matrix[0][j + 1] = col
    grid_matrix[1][j + 1] = st.session_state.column_words[j]

# Fill in row labels and row words
for i, row in enumerate(grid_labels_rows):
    grid_matrix[i + 1][0] = row
    grid_matrix[i + 1][1] = st.session_state.row_words[i]

# Convert to DataFrame
formatted_grid = pd.DataFrame(grid_matrix).fillna('')
formatted_grid.index = [''] * 6
formatted_grid.columns = [f'\u00a0{i}' for i in range(6)]  # unique invisible-ish column names

# Display as static table
st.table(formatted_grid)

# --- CLUE-GIVER SECTION ---
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
    word1 = st.session_state.column_words[col_index]
    word2 = st.session_state.row_words[row_index]
    st.info("Use these two hidden words to give a one-word clue.")
    st.text_input("Give a one-word clue:", key="clue")

# --- GUESSING SECTION ---
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
