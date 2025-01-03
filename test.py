import json
import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

from dashboard import DiseaseMap,DiseasePercentMap,GridMap  # Import DiseaseMap

# selected_year = st.session_state.get("selected_year", "2008")  # Default: 2008
# selected_disease = st.session_state.get("selected_disease", "Lymphoedema")  # Default: Lymphoedema


def show_color_scale(colors):
    """
    Generates a horizontal bar showing the color scale.
    Converts hex colors to RGB for plotting.
    """
    from matplotlib.colors import to_rgb

    # Convert hex color codes to RGB
    rgb_colors = [to_rgb(color) for color in colors]
    rgb_array = [rgb_colors]  # Create a 2D array-like structure

    # Create the figure
    fig, ax = plt.subplots(figsize=(6, 0.5))
    ax.imshow(rgb_array, extent=[0, len(colors), 0, 1], aspect="auto")
    ax.axis("off")
    
    # Save the figure to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
    buf.seek(0)
    plt.close(fig)
    return buf


def preset_color_picker():
    """
    Displays a selectbox for preset color scales and their visual previews.
    """
    preset_scales = {
        "Red-Blue": ["#ff0000", "#0000ff"],
        "Green-Yellow": ["#00ff00", "#ffff00"],
        "Purple-Orange": ["#800080", "#ffa500"],
        "Blues": sns.color_palette("Blues", 10).as_hex(),
        "Coolwarm": sns.color_palette("coolwarm", 10).as_hex(),
        "Viridis": sns.color_palette("viridis", 10).as_hex(),
    }

    selected_scale = st.sidebar.selectbox(
        "Select a Preset Color Scale",
        options=list(preset_scales.keys()),
    )

    # Display the selected color scale preview
    st.sidebar.image(show_color_scale(preset_scales[selected_scale]), use_container_width=True)
    return preset_scales[selected_scale]

def main_page(color_scale, year, disease):
    """
    Main page with a single map for the selected year and disease.
    :param w: Dashboard object for Streamlit Elements.
    :param color_scale: Selected color scale for the map.
    :param year: Year to visualize.
    :param disease: Disease to visualize.
    """
    with elements("main_page"):
       
            map_component = DiseaseMap()
            map_component(
                csv_path="DiseaseData.csv",
                geojson_path="india_telengana.geojson",
                year=year,
                disease=disease,
                color_scale=color_scale
            )   

def compare_years_page(start_year, end_year, disease, color_scale):
    """
    Compare years page displaying 4 maps side by side.
    """
    st.markdown("### Compare Disease Data Across Selected Years")
    comparison = GridMap()
    comparison(
        csv_path="DiseaseData.csv",
        geojson_path="india_telengana.geojson",
        start_year=start_year,
        end_year=end_year,
        disease=disease,
        color_scale=color_scale,
    )
def percent_page(color_scale, year, disease):
    """
    Main page with a single map for the selected year and disease.
    :param w: Dashboard object for Streamlit Elements.
    :param color_scale: Selected color scale for the map.
    :param year: Year to visualize.
    :param disease: Disease to visualize.
    """
    with elements("main_page"):
       
            map_component = DiseasePercentMap()
            map_component(
                csv_path="DiseaseData.csv",
                geojson_path="india_telengana.geojson",
                year=year,
                disease=disease,
                color_scale=color_scale
            )  

def main():
    st.write(
        """
        ✨ Disease Dashboard [![GitHub][github_badge]][github_link] 
        =====================

        This project is an interactive Disease Dashboard built with Streamlit, designed to visualize 
       disease-related data across Indian states.

        [github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
        [github_link]: https://github.com/Cameronmeow/NDMC
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

    if "current_page" not in state:
        state.current_page = "main"

    # Sidebar filters
    st.sidebar.title("Disease Map Settings")

    # File uploads
    csv_path = st.sidebar.file_uploader("Upload Disease Data CSV", type="csv")
    geojson_path = st.sidebar.file_uploader("Upload GeoJSON File", type="geojson")

    # Page selection
    page_options = ["Main Page", "Compare Years","Percentage"]
    state.current_page = st.sidebar.radio("Select Page", page_options)

    if csv_path:
        diseasedata = pd.read_csv(csv_path)
        df_melted = diseasedata.melt(
            id_vars=["States/UTs", "Short Form"],
            var_name="Year-Disease",
            value_name="Cases"
        )
        df_melted[["Year", "Disease"]] = df_melted["Year-Disease"].str.split("-", expand=True)
        df_melted.drop(columns=["Year-Disease"], inplace=True)
        df_melted["States/UTs"] = df_melted["States/UTs"].str.strip()
        df_melted["Short Form"] = df_melted["Short Form"].str.strip()

        # Sidebar filters
        st.sidebar.markdown("### Year Selection")
        year = st.sidebar.slider(
            "Select a year:",
            min_value=int(df_melted["Year"].min()),
            max_value=int(df_melted["Year"].max()),
            value=int(df_melted["Year"].min())
        )
        disease = st.sidebar.selectbox("Select Disease", df_melted["Disease"].unique())

        st.sidebar.markdown("### Range Selection")
        start_year = st.sidebar.number_input(
            "Start Year",
            min_value=int(df_melted["Year"].min()),
            value=int(df_melted["Year"].min())
        )
        end_year = st.sidebar.number_input(
            "End Year",
            min_value=start_year,
            value=start_year + 1
        )
        if start_year > end_year:
            st.sidebar.error("Start Year cannot be greater than End Year.")
        year_range = list(range(start_year, end_year + 1))
    else:
        st.info("Please upload the CSV file to proceed.")
        return

    # Color scale picker
    # color_start = st.sidebar.color_picker("Pick starting color", "#ff0000")
    # color_end = st.sidebar.color_picker("Pick ending color", "#0000ff")
    # color_scale = [color_start, color_end]
    color_scale = preset_color_picker()

    # Initialize dashboard
    

    # Main content based on selected page
    if state.current_page == "Main Page":
        if csv_path and geojson_path:
            main_page(color_scale, str(year), disease)
        else:
            st.error("Please upload both the CSV and GeoJSON files to proceed.")
    elif state.current_page == "Percentage":
        if csv_path and geojson_path:
            percent_page(color_scale, str(year), disease)
        else:
            st.error("Please upload both the CSV and GeoJSON files to proceed.")
    elif state.current_page == "Current Page":
        if csv_path and geojson_path:
            compare_years_page(start_year, end_year, disease, color_scale)
        else:
            st.error("Please upload both the CSV and GeoJSON files to proceed.")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()