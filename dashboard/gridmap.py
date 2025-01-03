import pandas as pd
import geopandas as gpd
import plotly.express as px
import streamlit as st


class GridMap:
    def __init__(self):
        pass

    def __call__(self, csv_path, geojson_path, start_year, end_year, disease, color_scale):
        # Load data
        data = pd.read_csv(csv_path)
        data["States/UTs"] = data["States/UTs"].str.strip()
        data["Short Form"] = data["Short Form"].str.strip()
        gdf = gpd.read_file(geojson_path)
        gdf["NAME_1"] = gdf["NAME_1"].str.strip()

        # Melt and preprocess data
        data_melted = data.melt(
            id_vars=["States/UTs", "Short Form"], var_name="Year-Disease", value_name="Cases"
        )
        data_melted[["Year", "Disease"]] = data_melted["Year-Disease"].str.split("-", expand=True)
        data_melted.drop(columns=["Year-Disease"], inplace=True)

        # Generate 4 evenly spaced years within the range
        try:
            year_range = ["2008","2009","2010","2011"]
            # selected_years = sorted(set(year_range))  # Ensure uniqueness
            # selected_years = list(map(str, sorted(selected_years[:4])))  # Take up to 4 years as strings
        except Exception as e:
            st.error(f"Error processing year range: {e}")
            return

        # List to hold the maps
        maps = []

        
        filtered_data = gdf.merge(
                    data_melted[(data_melted["Year"] == "2008") & (data_melted["Disease"] == disease)],
                    left_on="NAME_1",
                    right_on="States/UTs",
                    how="left"
                )

                # Handle missing cases
        filtered_data["Cases"].fillna(0, inplace=True)

        total_cases = filtered_data["Cases"].sum()

                # Add text for hover information
        filtered_data["text"] = (
                    filtered_data["Short Form"] + "<br>Cases: " + filtered_data["Cases"].astype(int).astype(str)
                )

                # Create a map for the year
        fig = px.choropleth(
                    filtered_data,
                    geojson=filtered_data.geometry,
                    locations=filtered_data.index,
                    color="Cases",
                    title=f"{disease} Cases in {"2008"} - Total Cases: {total_cases:,}",
                    color_continuous_scale=color_scale,
                    hover_name="NAME_1",
                    hover_data={"text": True, "Cases": False},
                )
        fig.update_geos(
                    fitbounds="locations",
                    visible=False,
                )
        fig.update_layout(
                    title_font=dict(size=16, family="Arial Black, Arial, sans-serif", color="black"),
                    geo=dict(fitbounds="locations", visible=False),
                    margin=dict(l=20, r=20, t=60, b=20),
                    height=300,  # Height of each map
                    width=300,   # Width of each map
                )

        maps.append(fig)
        filtered_data = gdf.merge(
                    data_melted[(data_melted["Year"] == "2009") & (data_melted["Disease"] == disease)],
                    left_on="NAME_1",
                    right_on="States/UTs",
                    how="left"
                )

                # Handle missing cases
        filtered_data["Cases"].fillna(0, inplace=True)

        total_cases = filtered_data["Cases"].sum()

                # Add text for hover information
        filtered_data["text"] = (
                    filtered_data["Short Form"] + "<br>Cases: " + filtered_data["Cases"].astype(int).astype(str)
                )

                # Create a map for the year
        fig = px.choropleth(
                    filtered_data,
                    geojson=filtered_data.geometry,
                    locations=filtered_data.index,
                    color="Cases",
                    title=f"{disease} Cases in {"2009"} - Total Cases: {total_cases:,}",
                    color_continuous_scale=color_scale,
                    hover_name="NAME_1",
                    hover_data={"text": True, "Cases": False},
                )
        fig.update_geos(
                    fitbounds="locations",
                    visible=False,
                )
        fig.update_layout(
                    title_font=dict(size=16, family="Arial Black, Arial, sans-serif", color="black"),
                    geo=dict(fitbounds="locations", visible=False),
                    margin=dict(l=20, r=20, t=60, b=20),
                    height=300,  # Height of each map
                    width=300,   # Width of each map
                )

        maps.append(fig)
        filtered_data = gdf.merge(
                    data_melted[(data_melted["Year"] == "2010") & (data_melted["Disease"] == disease)],
                    left_on="NAME_1",
                    right_on="States/UTs",
                    how="left"
                )

                # Handle missing cases
        filtered_data["Cases"].fillna(0, inplace=True)

        total_cases = filtered_data["Cases"].sum()

                # Add text for hover information
        filtered_data["text"] = (
                    filtered_data["Short Form"] + "<br>Cases: " + filtered_data["Cases"].astype(int).astype(str)
                )

                # Create a map for the year
        fig = px.choropleth(
                    filtered_data,
                    geojson=filtered_data.geometry,
                    locations=filtered_data.index,
                    color="Cases",
                    title=f"{disease} Cases in {"2010"} - Total Cases: {total_cases:,}",
                    color_continuous_scale=color_scale,
                    hover_name="NAME_1",
                    hover_data={"text": True, "Cases": False},
                )
        fig.update_geos(
                    fitbounds="locations",
                    visible=False,
                )
        fig.update_layout(
                    title_font=dict(size=16, family="Arial Black, Arial, sans-serif", color="black"),
                    geo=dict(fitbounds="locations", visible=False),
                    margin=dict(l=20, r=20, t=60, b=20),
                    height=300,  # Height of each map
                    width=300,   # Width of each map
                )

        maps.append(fig)
        filtered_data = gdf.merge(
                    data_melted[(data_melted["Year"] == "2011") & (data_melted["Disease"] == disease)],
                    left_on="NAME_1",
                    right_on="States/UTs",
                    how="left"
                )

                # Handle missing cases
        filtered_data["Cases"].fillna(0, inplace=True)

        total_cases = filtered_data["Cases"].sum()

                # Add text for hover information
        filtered_data["text"] = (
                    filtered_data["Short Form"] + "<br>Cases: " + filtered_data["Cases"].astype(int).astype(str)
                )

                # Create a map for the year
        fig = px.choropleth(
                    filtered_data,
                    geojson=filtered_data.geometry,
                    locations=filtered_data.index,
                    color="Cases",
                    title=f"{disease} Cases in {"2011"} - Total Cases: {total_cases:,}",
                    color_continuous_scale=color_scale,
                    hover_name="NAME_1",
                    hover_data={"text": True, "Cases": False},
                )
        fig.update_geos(
                    fitbounds="locations",
                    visible=False,
                )
        fig.update_layout(
                    title_font=dict(size=16, family="Arial Black, Arial, sans-serif", color="black"),
                    geo=dict(fitbounds="locations", visible=False),
                    margin=dict(l=20, r=20, t=60, b=20),
                    height=300,  # Height of each map
                    width=300,   # Width of each map
                )

        maps.append(fig)
        # Check if at least one map is created
        if not maps:
            st.error("No maps could be created. Please check your data or inputs.")
            return

        # Render the 4 maps side by side
        # col1, col2, col3, col4 = st.columns(4)
        print(len(maps))
        
        st.plotly_chart(maps[0], use_container_width=True)
        st.plotly_chart(maps[1], use_container_width=True)
        st.plotly_chart(maps[2], use_container_width=True)
        st.plotly_chart(maps[3], use_container_width=True)
