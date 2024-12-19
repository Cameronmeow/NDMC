import pandas as pd
import geopandas as gpd
import streamlit as st
import plotly.express as px
import plotly.validators.surface
# Sample data preparation

# st.markdown(
#     """
#     <style>
#     /* Change the background color of the sidebar */
#     [data-testid="stSidebar"] {
#         background-color: #2C3E50;
#     }
#
#     /* Change the color of the header text in the sidebar */
#     [data-testid="stSidebar"] h1 {
#         color: #FFFFFF; /* White */
#     }
#
#     /* Optional: Style other sidebar elements (like text) */
#     [data-testid="stSidebar"] .css-1v0mbdj {
#         color: #FFFFFF;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
diseasedata = pd.read_csv('DiseaseData.csv')

data = { #sample data
    "States/UTs": [
        "Andaman and Nicobar Islands", "Andhra Pradesh", "Assam", "Bihar","Chhattisgarh","Dadra and Nagar Haveli","Daman and Diu","Goa","Gujarat","Jharkhand","Karnataka","Kerala","Lakshadweep","Madhya Pradesh","Maharashtra","Odisha","Puducherry","Tamil Nadu","Telangana","Uttar Pradesh","West Bengal"
    ],
    "2008_Lymphoedema": [75,138931,776,212536,5814,107,176,191,2529,86949,16782,10886,283,3399,53468,61784,1539,34431,0,77980,45862],
    "2008_Hydrocele": [25,6696,968,164543,7283,0,70,100,2049,36392,2520,413,87,7448,38118,30633,184,8060,0,37739,32190],
    # "2009_Lymphoedema": [159, 154061, 60, 1300, 3500, 800, 50, 15, 3100, 500],
    # "2009_Hydrocele": [85, 6864, 25, 850, 1250, 450, 15, 10, 1050, 175],
}

# df = pd.DataFrame(data)
df_melted = diseasedata.melt( #this step for easier visualization
    id_vars=["States/UTs"],
    var_name="Year-Disease",
    value_name="Cases"
)
# # Split Year and Disease into separate columns
df_melted[["Year", "Disease"]] = df_melted["Year-Disease"].str.split("-", expand=True)
df_melted.drop(columns=["Year-Disease"], inplace=True)

# Load Indian states GeoJSON
shapefile_path = "./india_state_geo.json"  # Replace with your GeoJSON file path
gdf = gpd.read_file(shapefile_path)

# Verify columns in GeoJSON
print(gdf.columns)
print(gdf.head())

# Merge data with GeoJSON
# Update the key column (`NAME_1`) based on your GeoJSON structure
gdf["NAME_1"] = gdf["NAME_1"].str.strip()  # Clean up whitespace if necessary
df_melted["States/UTs"] = df_melted["States/UTs"].str.strip()

merged = gdf.merge(df_melted, left_on="NAME_1", right_on="States/UTs", how="left")
# merged = gdf.merge(df2_melted, left_on="NAME_1", right_on="States/UTs", how="left")

# Streamlit App
st.title("Disease Dashboard: Lymphoedema and Hydrocele Cases in India")
st.sidebar.header("Filters")

# Sidebar filters
year = st.sidebar.selectbox("Select Year", sorted(df_melted["Year"].unique()))
disease = st.sidebar.selectbox("Select Disease", ["Lymphoedema", "Hydrocele"])

# Filter data
filtered_data = merged[(merged["Year"] == year) & (merged["Disease"] == disease)]

# Plotting
fig = px.choropleth(
    filtered_data,
    geojson=filtered_data.geometry,
    locations=filtered_data.index,
    color="Cases",
    title=f"{disease} Cases in {year}",
    color_continuous_scale="Viridis",
    hover_name="States/UTs",
    hover_data={"Year": True, "Disease": True, "Cases": True, "States/UTs": False},  # Customize displayed fields
)

fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig)
