import json
import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

from dashboard import Dashboard, Card, DataGrid, Radar, Player, DiseasePie, DiseaseMap  # Import DiseaseMap

# selected_year = st.session_state.get("selected_year", "2008")  # Default: 2008
# selected_disease = st.session_state.get("selected_disease", "Lymphoedema")  # Default: Lymphoedema

def main():
    st.write(
        """
        ✨ Disease Dashboard [![GitHub][github_badge]][github_link] 
        =====================

        This project is an interactive Disease Dashboard built with Streamlit, designed to visualize 
       disease-related data across Indian states.

        [github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
        [github_link]: https://github.com/okld/streamlit-elements
        """

    )

    # with st.expander("GETTING STARTED"):
    #     st.write((Path(__file__).parent / "README.md").read_text())

    st.markdown(
        """
        <style>
        .custom-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }
        .custom-legend .legend-item {
            display: flex;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    diseasedata = pd.read_csv('DiseaseData.csv')
    df_melted = diseasedata.melt( #this step for easier visualization
        id_vars=["States/UTs"],
        var_name="Year-Disease",
        value_name="Cases"
    )
    # # Split Year and Disease into separate columns
    df_melted[["Year", "Disease"]] = df_melted["Year-Disease"].str.split("-", expand=True)
    df_melted.drop(columns=["Year-Disease"], inplace=True)

    df_melted["States/UTs"] = df_melted["States/UTs"].str.strip()

    # merged = gdf.merge(df_melted, left_on="NAME_1", right_on="States/UTs", how="left")
    # merged = gdf.merge(df2_melted, left_on="NAME_1", right_on="States/UTs", how="left")

    # Streamlit App
    st.title("Disease Dashboard: Lymphoedema and Hydrocele Cases in India")
    st.sidebar.header("Filters")

    # Sidebar filters
    st.sidebar.markdown("### Year Selection")
    year = st.sidebar.slider(
        "Move the slider to select a year:", 
        min_value=int(df_melted["Year"].min()), 
        max_value=int(df_melted["Year"].max()), 
        value=int(df_melted["Year"].min()), 
        step=1
    )
    year = str(year)
    disease = st.sidebar.selectbox("Select Disease", ["Lymphoedema", "Hydrocele"])

    LYMPHODEMA = ("Lymphedema is a chronic condition that causes swelling in the body's tissues due to a buildup of lymph fluid")
    HYDROCELE = ("A hydrocele is a buildup of fluid in the scrotum, the pouch of skin that holds the testicles")
 

    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            # editor=Editor(board, 0, 0, 6, 11, minW=3, minH=3),
            # player=Player(board, 0, 12, 6, 10, minH=5),
            pie=DiseasePie(board, 6, 0, 6, 10, minW=6, minH=10),
            radar=Radar(board, 12, 7, 3, 7, minW=2, minH=4),
            card=Card(board, 6, 7, 3, 7, minW=5, minH=6),
            # data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
            map=DiseaseMap(board, 12, 0, 6, 12, minW=6, minH=12),  # New Map Component
        )
        state.w = w

        # w.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
        # w.editor.add_tab("Data grid", json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
        # w.editor.add_tab("Radar chart",json.dumps({"csv_path": str(Path(__file__).parent / "DiseaseData.csv"), "year": year}, indent=2), "json")

        # # Pie chart default tab setup
        # w.editor.add_tab("Pie chart", json.dumps({"csv_path": str(Path(__file__).parent / "DiseaseData.csv"), "year": year, "disease": disease}, indent=2), "json")

        # # Map default tab setup
        # w.editor.add_tab(
        #     "Disease map",
        #     json.dumps(
        #         {
        #             "csv_path": str(Path(__file__).parent / "DiseaseData.csv"),
        #             "geojson_path": str(Path(__file__).parent / "india_state_geo.json"),
        #             "year": year,
        #             "disease": disease,
        #         },
        #         indent=2,
        #     ),
        #     "json",
        # )

    else:
        w = state.w

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            # w.editor()
            # w.player()
            # if disease=='Lymphoedema':
                # w.card(content = "Lymphedema is a chronic condition that causes swelling in the body's tissues due to a buildup of lymph fluid",disease = disease,year = year,image=str(Path(__file__).parent / "Lymphoedema.png"))
            # elif disease=='Hydrocele':
                # w.card(content= "A hydrocele is a buildup of fluid in the scrotum, the pouch of skin that holds the testicles",disease = disease,year = year,image = str(Path(__file__).parent / "Hydrocele.webp"))
            # Retrieve content for the pie chart
            # pie_config = json.loads(w.get_content("Pie chart"))
            # w.pie(pie_config["csv_path"], pie_config["year"], pie_config["disease"])
            w.pie(
                csv_path = "DiseaseData.csv",
                year = year,
                disease = disease
            )
            # Pass year and disease from the sidebar to the map component
            w.map(
                csv_path="DiseaseData.csv",             # Path to the CSV file
                geojson_path="india_state_geo.json",    # Path to GeoJSON file
                year=year,                              # Sidebar-selected year
                disease=disease                         # Sidebar-selected disease
            )
             # Radar Component
            radar_data = df_melted[df_melted["Year"] == year]  # Filter for selected year
            radar_data = radar_data.pivot_table(
                index="States/UTs",
                columns="Disease",
                values="Cases",
                aggfunc="sum",
                fill_value=0
            ).reset_index()
            w.radar(
                csv_path="DiseaseData.csv",
                year=year
            )
           
            # w.data_grid(w.editor.get_content("Data grid"))


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
