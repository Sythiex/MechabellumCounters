import pandas as pd

file_path = "Mechabellum Unit Counters.xlsx"
df = pd.read_excel(file_path)
df = df.set_index(df.columns[0]) # This makes the first column (unit names) the index
df = df.astype(str) # ensure all values are strings

max_unit_length = max(len(unit) for unit in df.index) + 2 # Compute the maximum length of the unit names + 2 spaces for extra padding

# Build the formatted dictionary as a string
formatted_output = "unit_matrix = {\n"
for unit, row in df.iterrows():
    spacing = " " * (max_unit_length - len(unit)) # Calculate the number of spaces to add after the colon
    values = ", ".join(row.tolist()) # Convert the row's values into a comma separated string
    formatted_output += f'    "{unit}":{spacing}[{values}],\n'
formatted_output += "}"

print(formatted_output)