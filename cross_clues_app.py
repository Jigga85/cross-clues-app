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

# --- DISPLAY COLUMN AND ROW WORDS ---
st.markdown("### 📋 Word Axes")

col_table = "| Column | Word |
|--------|------|"
for i, letter in enumerate(grid_labels_cols):
    col_table += f"\n| {letter} | {st.session_state.column_words[i]} |"
st.markdown(col_table)

row_table = "| Row | Word |
|-----|------|"
for i, number in enumerate(grid_labels_rows):
    row_table += f"\n| {number} | {st.session_state.row_words[i]} |"
st.markdown(row_table)

# --- DISPLAY EMPTY GRID ---
st.markdown("### 🗺️ Grid Coordinates")
grid_table = "| | A | B | C | D | E |
|--|--|--|--|--|--|"
for row in grid_labels_rows:
    row_str = f"| {row} | " + " | ".join([" " for _ in grid_labels_cols]) + " |"
    grid_table += f"\n{row_str}"
st.markdown(grid_table)

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
