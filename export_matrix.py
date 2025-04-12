import pandas as pd
import streamlit_app as app

df = pd.DataFrame.from_dict(app.unit_matrix, orient='index')
df.to_csv('unit_matrix.csv')