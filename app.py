import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
import matplotlib.pyplot as plt
import seaborn as sns 
from shiny import render 
from shinyswatch import theme
from shiny import reactive


# loading the dataset
penguins_df = load_penguins()

# Giving the Title
ui.page_opts(title = "Mo and Penguins", fillable = True, theme = theme.superhero)

with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize("selected_attribute", "Select Attributes", 
        ["bill_length_mm", "bill_depth_mm",
         "flipper_length_mm", "body_mass_g"])
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 10)
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 5, 50, 10)
    ui.input_checkbox_group("selected_species_list", "Select Species", 
                                ["Adelie", "Gentoo", "Chinstrap"], 
                                selected=["Adelie", "Gentoo"], inline=True)

    ui.hr(),
    ui.a("GitHub", href="https://github.com/MahammadHajiyev2024/cintel-02-data", target="_blank")
    
# This is for my bonus task where I added dynamic text output
    ui.h3("Additional Information about Selected Species")
    @render.text
    def selected_species_info():
        selected_species = input.selected_species_list()
        count = penguins_df[penguins_df["species"].isin(selected_species)].shape[0] 
        return f"Displaying data for {', '.join(selected_species)} with {count} penguins."
        
# Main Content Layout
with ui.layout_columns():
    # Data Table
    with ui.card():   
        ui.card_header("Data Table for Penguins Dataset")

        @render.data_frame
        def penguins_table():
            return render.DataTable(filtered_data())
            
    #Data Grid
    with ui.card():
        ui.card_header("Data Grid for Penguins")

        @render.data_frame
        def penguins_grid():
            return render.DataGrid(filtered_data())
                  

with ui.layout_columns():
    # Seaborn Histogram
    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram: Selected Attribute")

        # Render Seaborn histogram
        @render.plot
        def seaborn_histogram():
            selected_attribute = input.selected_attribute()
            bin_count = input.seaborn_bin_count()

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(
                data=filtered_data(),
                x=selected_attribute,
                hue="species",
                bins=bin_count,
                multiple="stack",
                ax=ax
            )
            ax.set_title(f"Seaborn Histogram of {selected_attribute} by Species")
            ax.set_xlabel(f"{selected_attribute} (mm)")
            ax.set_ylabel("Count")
            return fig

    with ui.card(full_screen=True):
        # Plotly Scatterplot
        ui.card_header("Plotly Scatterplot: Flipper Length vs Bill Length")

        # Render Plotly scatterplot
        @render_plotly
        def plotly_scatterplot():
            selected_species = input.selected_species_list()
            filtered_df = penguins_df[penguins_df["species"].isin(selected_species)]
            fig = px.scatter(
                filtered_df,
                x="flipper_length_mm",
                y="bill_length_mm",
                color="species",
                title="Scatterplot of Flipper Length vs Bill Length by Species",
                labels={
                    "flipper_length_mm": "Flipper Length (mm)",
                    "bill_length_mm": "Bill Length (mm)"
                }
            )
            return fig


    with ui.card(full_screen=True):
        # Plotly Histogram
        ui.card_header("Plotly Histogram: Body Mass by Species")
        @render_plotly
        def plotly_histogram():  
            fig = px.histogram(penguins_df, x="body_mass_g", color="species", title="Penguin Body Mass by Species")
            return fig

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    if selected_species:
        return penguins_df[penguins_df['species'].isin(selected_species)]
    else: 
        return penguins_df
    return penguins_df
