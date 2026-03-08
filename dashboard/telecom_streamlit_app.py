import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("telecom_dashboard_data.csv")

st.title("Telecom Network Coverage Analytics Dashboard")

st.markdown("""
This dashboard analyzes telecom tower distribution across India
to identify infrastructure density, regional clusters, and potential
network expansion opportunities.
""")

# Sidebar filters
st.sidebar.header("Filters")

tech_filter = st.sidebar.multiselect(
    "Select Network Technology",
    options=df["radio"].unique(),
    default=df["radio"].unique()
)

cluster_filter = st.sidebar.multiselect(
    "Select Cluster",
    options=df["cluster"].unique(),
    default=df["cluster"].unique()
)

filtered_df = df[
    (df["radio"].isin(tech_filter)) &
    (df["cluster"].isin(cluster_filter))
]

st.subheader("Telecom Tower Distribution Map")

map_india = folium.Map(location=[20,78], zoom_start=5)

sample_df = filtered_df.sample(2000)

for _, row in sample_df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["long"]],
        radius=2,
        color="blue",
        fill=True
    ).add_to(map_india)

st_folium(map_india)

st.subheader("Network Technology Distribution")

fig, ax = plt.subplots()
filtered_df["radio"].value_counts().plot(kind="bar", ax=ax)
st.pyplot(fig)

st.subheader("Telecom Density Heatmap")

fig2, ax2 = plt.subplots()

sns.kdeplot(
    x=filtered_df["long"],
    y=filtered_df["lat"],
    fill=True,
    ax=ax2
)

st.pyplot(fig2)