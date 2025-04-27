import streamlit as st
import os
from PIL import Image
import base64

#
# local run: streamlit run streamlit_app.py
#

# Define the path to the image folder
image_folder = os.path.join(os.getcwd(), "images")

# Define the list of units and map them to local .jpg image file paths in the /images folder
unit_images = {
    "Crawler": "crawler.jpg",
    "Fang": "fang.jpg",
    "Hound": "hound.jpg",
    "Marksman": "marksman.jpg",
    "Arclight": "arclight.jpg",
    "Wasp": "wasp.jpg",
    "Mustang": "mustang.jpg",
    "Sledgehammer": "sledgehammer.jpg",
    "Steel Ball": "steelball.jpg",
    "Stormcaller": "stormcaller.jpg",
    "Phoenix": "phoenix.jpg",
    "Phantom Ray": "phantom_ray.jpg",
    "Tarantula": "tarantula.jpg",
    "Sabertooth": "sabertooth.jpg",
    "Rhino": "rhino.jpg",
    "Hacker": "hacker.jpg",
    "Wraith": "wraith.jpg",
    "Scorpion": "scorpion.jpg",
    "Vulcan": "vulcan.jpg",
    "Fortress": "fortress.jpg",
    "Melting Point": "melting_point.jpg",
    "Sandworm": "sandworm.jpg",
    "Raiden": "raiden.jpg",
    "Overlord": "overlord.jpg",
    "War Factory": "war_factory.jpg",
    "Fire Badger": "fire_badger.jpg",
    "Typhoon": "typhoon.jpg",
    "Farseer": "farseer.jpg",
    "Abyss": "abyss.jpg"
}

st.set_page_config(
    layout = 'wide',
    page_title = 'Mechabellum Unit Counters'
)

#cols_per_row = 13  # 12 items per row
#cols_per_row_output = 16
# make it configurable for different screens
cols_per_row = st.sidebar.slider(
    "Select the number of columns per row:",
    min_value=2,
    max_value=24,
    value=10,  # Default value
    step=1
)
cols_per_row_output = st.sidebar.slider(
    "Select the number of columns per row for output:",
    min_value=5,
    max_value=24,
    value=12, # Default value
    step=1
)
show_sliders = st.sidebar.checkbox("Show Weight Sliders")

#
# db
#
# Initialize session state to track selected units (checkboxes)
if 'selected_units' not in st.session_state:
    st.session_state.selected_units = []
if 'weights' not in st.session_state:
    st.session_state.weights = {unit: 1 for unit in unit_images.keys()}

# Helper function to convert image to base64
def get_image_as_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Create a list to keep track of unit names and images in a grid
unit_list = list(unit_images.keys())
num_units = len(unit_list)
# Loop through the units and create the grid layout
for i in range(0, num_units, cols_per_row):
    cols = st.columns(cols_per_row)
    for j, unit in enumerate(unit_list[i:i+cols_per_row]):
        with cols[j]:
            #c = st.container()

            # Add or remove the unit from the selected_units list based on the checkbox state
            if st.checkbox(f" ", key=f"checkbox:{unit}", value=(unit in st.session_state.selected_units)):
                if unit not in st.session_state.selected_units:
                    st.session_state.selected_units.append(unit)
            else:
                if unit in st.session_state.selected_units:
                    st.session_state.selected_units.remove(unit)

            # Determine the border based on the updated state
            if unit in st.session_state.selected_units:
                border_style = "border: 3px solid black;"
            else:
                border_style = "border: 3px solid transparent;"  # Invisible border for layout consistency

            # Render the image with the correct border style AFTER the checkbox state is determined
            img_path = os.path.join(image_folder, unit_images[unit])
            img_base64 = get_image_as_base64(img_path)

            # Display the image first with the appropriate border
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="data:image/jpeg;base64,{img_base64}" style="width:100%; {border_style} border-radius: 10px;">
                    <p>{unit}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Add a weight slider below each unit (range 1 to 5)
            if show_sliders and unit in st.session_state.selected_units:
                st.session_state.weights[unit] = st.slider(f" ", key=f"slider:{unit}", min_value=1, max_value=5, value=st.session_state.weights[unit])

# Display the output: sorted list of selected units
#st.write("Selected Units:")
#st.write(sorted(st.session_state.selected_units))

S = 5 # unit wins, >95% HP left with nearly no damage
A = 4 # unit wins, 60-95% HP left
B = 3 # unit wins, 10-60% HP left
C = 2 # unit wins, <10% HP left
D = 1 # unit loose, Opponent is damaged
F = 0 # unit loose, Opponent >95% HP
unit_matrix = {
    "Crawler":        [C, B, D, A, F, F, A, D, A, A, F, F, D, B, D, A, F, C, F, A, A, D, F, F, D, F, D, D, F],
    "Fang":           [D, C, D, A, F, B, D, F, C, F, A, B, D, D, D, A, F, F, F, C, B, D, B, B, D, F, F, D, F],
    "Hound":          [A, A, C, D, D, F, C, D, D, B, F, F, D, C, D, D, F, D, D, D, C, D, F, F, D, D, D, D, F],
    "Marksman":       [D, D, B, C, S, D, D, D, D, D, A, D, B, D, D, S, A, C, B, D, D, D, D, A, D, A, C, D, B],
    "Arclight":       [S, S, B, F, C, F, A, D, D, F, F, F, D, F, D, D, F, D, D, F, F, D, F, F, F, B, D, D, F],
    "Wasp":           [S, D, S, C, S, C, D, S, S, S, B, D, S, S, A, S, F, A, A, A, B, S, B, B, A, S, D, D, C],
    "Mustang":        [D, B, D, B, D, B, C, F, F, D, A, C, D, D, D, B, D, D, F, D, D, D, B, B, D, D, D, D, D],
    "Sledgehammer":   [A, S, B, C, A, F, S, C, D, B, F, F, D, D, D, B, F, F, D, F, D, D, F, F, F, D, B, D, F],
    "Steel Ball":     [D, D, B, C, A, F, A, B, C, A, F, F, B, D, A, F, F, D, B, C, B, D, F, F, D, B, A, C, F],
    "Stormcaller":    [D, S, D, B, S, F, D, D, D, C, F, F, B, B, F, S, F, S, A, B, A, F, F, F, D, D, A, D, F],
    "Phoenix":        [S, F, S, D, S, D, D, S, A, S, C, S, S, S, S, S, A, S, S, S, D, S, D, C, A, S, B, D, C],
    "Phantom Ray":    [A, D, S, C, S, C, D, S, S, S, C, C, S, S, S, S, A, S, S, S, D, S, D, C, A, S, B, D, C],
    "Tarantula":      [A, A, B, D, B, F, B, B, D, D, F, F, C, D, D, C, F, D, B, D, D, D, F, F, D, B, A, D, F],
    "Sabertooth":     [D, C, D, C, S, F, B, B, A, D, F, F, A, C, B, A, F, B, A, D, D, D, F, F, D, A, A, A, F],
    "Rhino":          [C, C, B, C, A, F, B, B, D, S, F, F, B, D, C, A, F, A, A, D, F, D, F, F, F, A, A, A, F],
    "Hacker":         [D, F, C, F, A, F, D, D, S, F, F, F, D, D, D, C, F, D, D, F, D, D, F, F, F, A, A, D, F],
    "Wraith":         [S, B, S, D, S, S, B, A, A, S, D, D, A, A, A, S, C, A, A, A, F, A, D, D, A, S, D, D, F],
    "Scorpion":       [D, S, A, D, A, F, A, A, S, D, F, F, B, D, D, A, F, C, S, D, D, D, F, F, D, S, S, B, F],
    "Vulcan":         [S, S, A, D, B, F, S, B, D, D, F, F, D, D, D, C, F, D, C, D, D, D, F, F, D, A, B, D, F],
    "Fortress":       [D, D, C, B, S, F, C, A, D, D, F, F, A, C, A, S, F, B, A, C, F, D, D, F, D, S, A, A, F],
    "Melting Point":  [D, D, D, C, A, D, C, A, D, D, B, B, A, B, S, S, S, A, S, S, C, B, A, B, B, A, A, A, A],
    "Sandworm":       [B, B, B, S, S, F, B, A, D, S, F, F, B, B, C, A, F, B, A, C, D, C, F, F, D, S, A, A, F],
    "Raiden":         [S, D, S, C, S, D, D, S, S, S, A, A, S, S, S, S, S, S, S, S, D, B, C, D, S, S, A, B, D],
    "Overlord":       [S, D, S, D, S, D, D, S, S, S, D, D, S, S, S, S, S, S, S, S, D, S, B, C, S, S, A, A, A],
    "War Factory":    [B, A, A, A, S, F, A, S, A, B, F, F, S, A, A, D, F, A, S, B, D, A, F, F, C, S, A, A, F],
    "Fire Badger":    [S, S, B, D, D, F, A, C, D, A, F, F, D, D, D, D, F, F, D, F, D, D, F, F, F, C, B, D, F],
    "Typhoon":        [A, S, B, D, B, S, B, D, D, D, D, D, B, D, F, D, C, F, D, D, D, D, D, D, D, D, C, D, D],
    "Farseer":        [C, A, A, D, A, A, B, B, D, C, C, C, C, D, D, B, A, D, B, D, D, D, D, D, D, B, C, C, D],
    "Abyss":          [S, S, S, C, S, B, A, S, S, S, D, D, S, S, S, S, S, S, S, S, D, S, A, D, S, S, A, B, C],
}

# add individual units with tech. <Unit Name>: <Tech Name>
unit_overrides = {} # todo: test and add units with tech

def get_counter_score(selected_units, unit_matrix, weights):
    base_units = list(unit_matrix.keys())

    if unit_overrides:
        for unit_override in unit_overrides.keys(): # loop through the unit overrides (units with tech)
            base_unit = unit_override.split(':', 1)[0] # get the base unit name
            matrix_scores = unit_matrix[base_unit].copy()  # make a copy of the base unit scores
            for unit_to_modify in unit_overrides[unit_override].keys(): # loop through the units that have overrides
                unit_to_modify_index = base_units.index(unit_to_modify) # get the index of the unit to modify
                matrix_scores[unit_to_modify_index] = unit_overrides[unit_override][unit_to_modify] # replace the score with the override score
            unit_matrix[unit_override] = matrix_scores # add the modified unit to the unit matrix

    scores = {unit: 0 for unit in list(unit_matrix.keys())}
    div = {unit: 0 for unit in list(unit_matrix.keys())}

    for selected_unit in selected_units:
        for unit, counters in unit_matrix.items():
            index = base_units.index(selected_unit)
            scores[unit] += counters[index] * weights[selected_unit]
            div[unit] += weights[selected_unit]

    if (len(selected_units) > 0):
        scores = {k: scores[k] / div[k] if scores[k]>0 else 0 for k in scores.keys()}
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
# Function to classify units into tiers based on score
def classify_by_tier(best_counters):
    tier_bins = {
        "S Tier (4-5 points)": [],
        "A Tier (3-4 points)": [],
        "B Tier (2-3 points)": [],
        "C Tier (1-2 points)": [],
        "D/F Tier (0-1 point)": []
    }

    for unit, score in best_counters:
        unit += f' - {round(score, 2)}'
        if 4 < score <= 5:
            tier_bins["S Tier (4-5 points)"].append(unit)
        elif 3 < score <= 4:
            tier_bins["A Tier (3-4 points)"].append(unit)
        elif 2 < score <= 3:
            tier_bins["B Tier (2-3 points)"].append(unit)
        elif 1 < score <= 2:
            tier_bins["C Tier (1-2 points)"].append(unit)
        else:
            tier_bins["D/F Tier (0-1 point)"].append(unit)

    return tier_bins

selected_units = st.session_state.selected_units
# Normalize the weights to make their sum equal to 1
raw_weights = st.session_state.weights
total_weight = sum(raw_weights.values())
weights = {unit: weight / total_weight for unit, weight in raw_weights.items()}

best_counters = get_counter_score(selected_units, unit_matrix, weights)
tiered_counters = classify_by_tier(best_counters)

# Display the best counter units in matrix format
st.write("Best Counter Units by Tier:")
for tier, units in tiered_counters.items():
    st.markdown(f"**{tier}**")
    if units:  # Only display if there are units in the tier
        cols = st.columns(cols_per_row_output)
        for idx, unit in enumerate(units):
            # Pull unit name from display string
            if ":" in unit:
                base_unit = unit.split(':', 1)[0]
            else:
                base_unit = unit.split('-', 1)[0]
            base_unit = base_unit.strip()

            img_path = os.path.join(image_folder, unit_images[base_unit])
            img_base64 = get_image_as_base64(img_path)

            with cols[idx % cols_per_row_output]:
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="data:image/jpeg;base64,{img_base64}" style="width:100%; border-radius: 10px;">
                        <p style="margin: 0; text-align: center; height: 3.5em; line-height: 1.15em; font-size: 1em;">
                            {unit}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )