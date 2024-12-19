import json
from streamlit_elements import html, nivo, mui
from .dashboard import Dashboard
import pandas as pd

class DiseasePie(Dashboard.Item):
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

    def __call__(self, csv_path, year, disease):
        # Load and preprocess data
        diseasedata = pd.read_csv(csv_path)
        diseasedata.rename(columns={"State/UT": "States/UTs"}, inplace=True)
        df_melted = diseasedata.melt(
            id_vars=["States/UTs"],
            var_name="Year-Disease",
            value_name="Cases"
        )
        df_melted[["Year", "Disease"]] = df_melted["Year-Disease"].str.split("-", expand=True)
        df_filtered = df_melted[(df_melted["Year"] == year) & (df_melted["Disease"] == disease)]

        # Prepare data for the pie chart
        pie_data = [
            {"id": row["States/UTs"], "label": row["States/UTs"], "value": row["Cases"]}
            for _, row in df_filtered.iterrows()
        ]

        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, }, elevation=1):
            with self.title_bar():
                mui.icon.PieChart()
                mui.Typography(f"{disease} Cases in {year}", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Pie(
                    data=pie_data,
                    theme=self._theme["dark" if self._dark_mode else "light"],
                    margin={"top": 80, "right": 0, "bottom": 80, "left": 40},
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    borderWidth=1,
                    borderColor={
                        "from": "color",
                        "modifiers": [
                            ["darker", 0.2],
                        ]
                    },
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="grey",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={"from": "color"},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={
                        "from": "color",
                        "modifiers": [
                            ["darker", 2]
                        ]
                    },
                    defs=[
                        {
                            "id": "dots",
                            "type": "patternDots",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "size": 4,
                            "padding": 1,
                            "stagger": True
                        },
                        {
                            "id": "lines",
                            "type": "patternLines",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "rotation": -45,
                            "lineWidth": 6,
                            "spacing": 10
                        }
                    ],
                    fill=[
                        {"match": {"id": "ruby"}, "id": "dots"},
                        {"match": {"id": "scala"}, "id": "lines"},                     
                        { "match": { "id": "c" }, "id": "dots" },
                        { "match": { "id": "go" }, "id": "dots" },
                        { "match": { "id": "python" }, "id": "dots" },
                        { "match": { "id": "scala" }, "id": "lines" },
                        { "match": { "id": "lisp" }, "id": "lines" },
                        { "match": { "id": "elixir" }, "id": "lines" },
                        { "match": { "id": "javascript" }, "id": "lines" }
                    ],

                    legend_class="custom-legend",
                    legends=[
                        {
                            "anchor": "bottom-left",
                            "direction": "column",  # Stack legends vertically
                            "justify": False,
                            "translateX": -10,
                            "translateY": 50,
                            "itemsSpacing": 4,
                            "itemWidth": 100,
                            "itemHeight": 18,
                            "itemTextColor": "#999",
                            "itemDirection": "left-to-right",
                            "itemOpacity": 1,
                            "symbolSize": 18,
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



