import pandas as pd
import geopandas as gpd
import plotly.express as px
from streamlit_elements import mui
import streamlit as st

class DiseaseMap:
    def __init__(self, dashboard, x, y, w, h, minW=6, minH=10):
        self.dashboard = dashboard
        self.x, self.y, self.w, self.h = x, y, w, h
        self.minW, self.minH = minW, minH

    def __call__(self, csv_path, geojson_path, year, disease):
        # Load data
        data = pd.read_csv(csv_path)
        data["States/UTs"] = data["States/UTs"].str.strip()

        gdf = gpd.read_file(geojson_path)
        gdf["NAME_1"] = gdf["NAME_1"].str.strip()

        data_melted = data.melt(
            id_vars=["States/UTs"], var_name="Year-Disease", value_name="Cases"
        )
        data_melted[["Year", "Disease"]] = data_melted["Year-Disease"].str.split("-", expand=True)
        data_melted.drop(columns=["Year-Disease"], inplace=True)

        merged = gdf.merge(
            data_melted, left_on="NAME_1", right_on="States/UTs", how="left"
        )
        filtered_data = merged[(merged["Year"] == year) & (merged["Disease"] == disease)]

        # Plot
        fig = px.choropleth(
            filtered_data,
            geojson=filtered_data.geometry,
            locations=filtered_data.index,
            color="Cases",
            title=f"{disease} Cases in {year}",
            color_continuous_scale="Viridis",
            hover_name="NAME_1",
        )
        fig.update_geos(fitbounds="locations", visible=False)

        # Add to the dashboard
        with self.dashboard(x=self.x, y=self.y, w=self.w, h=self.h, minW=self.minW, minH=self.minH):
            mui.Box(sx={"padding": 2})
            mui.Typography("Disease Map")
            st.plotly_chart(fig, use_container_width=True)
