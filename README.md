##NDMC

### Introduction

#### Project Structure
Element   | Description
:--------:|:-----------
/.streamlit  | 
/.streamlit/├──config.toml | This contains some styling used as global style of the project
/dashboard | This folder contains the files for the project
/dashboard/__init__.pt | The file imports various modules from the same package (modules within the same directory) and exposes them\
/dashboard/card.py |  Can use to provide description and photos of the disease in question 
/dashboard/datagrid.py | Will use to display the data in a tabular form 
/dashboard/india_state_geo.json | used to generate the map
/dashboard/map.py | map component
/dashboard/pie.py | pie chart component
/dashboard/player.py | Maybe will be used to have a video of instructions on how to run the file 
/dashboard/radar.py | Radar chart component
/streamlit_app.py | Main page file

### To run in your own repository

#### Available elements and objects

Here is a list of elements and objects you can import in your app:

Element   | Description
:--------:|:-----------
elements  | Create a frame where elements will be displayed.
dashboard | Build a draggable and resizable dashboard.
mui       | Material UI (MUI) widgets and icons.
html      | HTML objects.
editor    | Monaco code and diff editor that powers Visual Studio Code.
nivo      | Nivo chart library.
media     | Media player.
sync      | Callback to synchronize Streamlit's session state with elements events data.
lazy      | Defer a callback call until another non-lazy callback is called.

Download and install python
Download and install Visual Studio Code
Install the following libraries
pip install streamlit 
pip install pandas
pip install pathlib
pip install streamlit_elements
pip install types 
pip install geopandas
pip install plotly.express
pip install abc
pip install uuid
pip install contextlib

####
To run the file type this in the command line 
python -m streamlit run streamlit_app.py

