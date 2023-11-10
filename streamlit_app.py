from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt


@st.cache()
def load_data():
    src_file = Path.cwd() / "data" / "raw" / "EPA_fuel_economy_summary.csv"
    raw_df = pd.read_csv(src_file)
    return raw_df


# Load data and determine valid values
df = load_data()
min_year = int(df["year"].min())
max_year = int(df["year"].max())

# Add ALL as an option to make it easier to select all
valid_makes = ["ALL"] + sorted(df["make"].unique())

# Get the top 5 as the default
default_makes = df["make"].value_counts().nlargest(5).index.tolist()

# Setup the UI
st.title("Simple Sidebar Example")
make = st.sidebar.multiselect("Select a make:", valid_makes, default=default_makes)
year_range = st.sidebar.slider(
    label="Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

# Filter data based on inputs
year_filter = df["year"].between(year_range[0], year_range[1])
if "ALL" in make:
    # Dummy filter to include all makes
    make_filter = True
else:
    make_filter = df["make"].isin(make)

plot_df = df[make_filter & year_filter]

avg_fuel_economy = plot_df["fuelCost08"].mean().round(0)
st.sidebar.metric("Average", avg_fuel_economy)

# Plot the data
fig = px.histogram(
    plot_df,
    x="fuelCost08",
    color="class_summary",
    labels={"fuelCost08": "Annual Fuel Cost"},
    nbins=40,
    title="Fuel Cost Distribution",
)

altair_chart = (
    alt.Chart(plot_df)
    .mark_tick()
    .encode(y="fuel_type_summary", x="barrels08")
    .properties(width=600)
)

# Display the output results
st.write(fig)
st.write(altair_chart)



# import altair as alt
# import numpy as np
# import pandas as pd
# import streamlit as st

# """
# # Welcome to Streamlit!

# Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
# If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
# forums](https://discuss.streamlit.io).

# In the meantime, below is an example of what you can do with just a few lines of code:
# """

# num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
# num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

# indices = np.linspace(0, 1, num_points)
# theta = 2 * np.pi * num_turns * indices
# radius = indices

# x = radius * np.cos(theta)
# y = radius * np.sin(theta)

# df = pd.DataFrame({
#     "x": x,
#     "y": y,
#     "idx": indices,
#     "rand": np.random.randn(num_points),
# })

# st.altair_chart(alt.Chart(df, height=700, width=700)
#     .mark_point(filled=True)
#     .encode(
#         x=alt.X("x", axis=None),
#         y=alt.Y("y", axis=None),
#         color=alt.Color("idx", legend=None, scale=alt.Scale()),
#         size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
#     ))
