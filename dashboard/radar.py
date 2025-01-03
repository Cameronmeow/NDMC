import json
import streamlit as st
import pandas as pd
from streamlit_elements import mui, nivo
from .dashboard import Dashboard


class Radar(Dashboard.Item):

    DEFAULT_DATA = [
        { "taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114 },
        { "taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72 },
        { "taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99 },
        { "taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30 },
        { "taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103 },
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._theme = {
            "dark": {
                "background": "#252526",
                "textColor": "#FAFAFA",
                "tooltip": {
                    "container": {
                        "background": "#3F3F3F",
                        "color": "FAFAFA",
                    }
                }
            },
            "light": {
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        }

    def __call__(self, csv_path,year):
        try:
            diseasedata = pd.read_csv(csv_path)
            diseasedata.rename(columns={"State/UT": "States/UTs"}, inplace=True)

            # Melt the dataframe to long format
            df_melted = diseasedata.melt(
                id_vars=["States/UTs"],
                var_name="Year-Disease",
                value_name="Cases"
            )

            # Split "Year-Disease" into separate columns
            df_melted[["Year", "Disease"]] = df_melted["Year-Disease"].str.split("-", expand=True)

            # Filter data for the given year
            df_filtered = df_melted[df_melted["Year"] == str(year)]

            radar_data = df_filtered.pivot_table(
                index="States/UTs",
                columns="Disease",
                values="Cases",
                aggfunc="sum",
                fill_value=0
            ).reset_index()

            data = radar_data.to_dict(orient="records")
            keys = radar_data.columns[1:]
        except Exception as e:
            st.error(f"Error processing data: {e}")
            return
        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar():
                mui.icon.Radar()
                mui.Typography(f"Disease Cases in {year}", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Radar(
                    data=data,
                    theme=self._theme["dark" if self._dark_mode else "light"],
                    keys=keys.tolist(),
                    indexBy="States/UTs",
                    valueFormat=">-.2f",
                    margin={"top": 70, "right": 80, "bottom": 40, "left": 80},
                    borderColor={"from": "color"},
                    gridLabelOffset=36,
                    dotSize=10,
                    dotColor={"theme": "background"},
                    dotBorderWidth=2,
                    motionConfig="wobbly",
                    legends=[
                        {
                            "anchor": "top-left",
                            "direction": "column",
                            "translateX": -50,
                            "translateY": -40,
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemTextColor": "#999",
                            "symbolSize": 12,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ]
                )
