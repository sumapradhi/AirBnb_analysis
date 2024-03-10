# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import folium
from streamlit_folium import folium_static
import plotly.express as px

# Setting up page configuration
icon = Image.open("C:\\GUVI\\NewVM\\AirBNB\\airbnb_icon.png")
st.set_page_config(page_title= "Airbnb",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                  )
st.markdown('<h1 style="color: yellow;text-align: center;">AIRBNB ANALYSIS</h1>', unsafe_allow_html=True)
                           

# SETTING-UP BACKGROUND IMAGE
def setting_bg():
    st.markdown(f""" <style>.stApp {{
                        background: url("https://wallpapers.com/images/high/hot-air-balloon-aesthetic-tr06lqmdztyn7wsm.webp");
                        background-size: cover}}
                     </style>""",unsafe_allow_html=True)
setting_bg()

                             

# Creating option menu in the side bar
with st.sidebar:
    st.sidebar.image("C:\\GUVI\\NewVM\\AirBNB\\airbnb_icon.png",use_column_width=False)
    st.write("-------------------")
    selected = option_menu("Menu", ["Home",
                                    "Dataframe Creation",
                                    "Explore",
                                    "Selecting Property"], 
                           icons=["house","graph-up-arrow","bar-chart-line", "gear"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "18px", "text-align": "centre", "margin": "-2px", "--hover-color": "#93D4AE"},
                                   "nav-link-selected": {"background-color": "#0b5394"}}
                          )



# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient("mongodb+srv://sumapradhi:Sumathy2024@cluster0.zapmxfg.mongodb.net")
db = client.sample_airbnb
col = db.listingsAndReviews


# READING THE CLEANED DATAFRAME
df = pd.read_csv('C:\\GUVI\\NewVM\\AirBNB\\Airbnb_data.csv')

# HOME PAGE
if selected == "Home":
    # Title Image
    
    st.write("--------------------------")
    top_placeholder = st.empty()
    col1,col2 = st.columns(2,gap= 'medium')
    col1.markdown("## :orange[Domain] :_Travel Industry, Property Management, and Tourism_")
    col1.markdown("## :orange[Technologies used]:_Python, Pandas, Plotly, Streamlit, MongoDB_")
    col1.markdown("## :orange[Objective] :_This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends._")
    col2.markdown("#   ")
    col2.markdown("#   ")
    top_placeholder.text(" ")

# OVERVIEW PAGE
if selected == "Dataframe Creation":
    # Placeholder for top of the page
    top_placeholder = st.empty()

    # Set header for the section
    st.subheader(':violet[Converting RawData into Dataframe]:')   
    col1, col2 = st.columns(2)

    # RAW DATA TAB
    with col1:
        # RAW DATA
        st.write("Raw data")
        st.write(col.find_one())
    # DATAFRAME TAB
    with col2:
        # DATAFRAME FORMAT
        st.write("Dataframe")
        st.write(df)
    
    # Scroll to the top of the page
    top_placeholder.text(" ")

def update_layout_and_display_chart(fig):
    fig.update_layout(xaxis_title="Room Type", yaxis_title="Number of Listings")
    st.plotly_chart(fig, use_container_width=True)

def display_filtered_df_and_map(filtered_df):
    st.subheader("Filtered Data Table")
    st.write(filtered_df[['Country','Property_type','Room_type', 'Amenities']])
    
    map = folium.Map(location=[filtered_df['Latitude'].mean(), filtered_df['Longitude'].mean()], zoom_start=10)
    for index, row in filtered_df.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']]).add_to(map)
    folium_static(map)

# EXPLORE PAGE
if selected == "Explore":
        
        st.header("Explore more about the Airbnb data")
        # GETTING USER INPUTS
        selected_country = st.selectbox('Select Country', sorted(df['Country'].unique()))
        # Filter DataFrame based on the selected country
        selected_country_df = df[df['Country'] == selected_country]

        #Top 10 Property Types with Room Types and Their Average Prices
        # Group by property type and room type and calculate mean price
        property_room_price_mean = selected_country_df.groupby(['Property_type', 'Room_type'])['Price'].mean().reset_index()
        # Sort property types by average price
        top_10_property_types = property_room_price_mean.groupby(['Property_type', 'Room_type']).mean().reset_index().nlargest(10, 'Price')

        # Create bar chart
        fig = px.bar(top_10_property_types, x='Property_type', y='Price', color='Room_type',
                    title=f'Top 10 Property Types with Room Types and Their Average Prices in {selected_country}',
                    labels={'Property_type': 'Property Type', 'Price': 'Average Price', 'Room_type': 'Room Type'})
        st.plotly_chart(fig, use_container_width=True)


        #Top 10 Properties Based on Review Scores
        # Sort the DataFrame based on review scores in descending order
        top_review_properties = df.sort_values(by='Review_scores', ascending=False).head(10)
        # Create bar chart
        fig = px.bar(top_review_properties, x='Property_type', y='Review_scores', 
                    title='Top 10 Properties Based on Highest Review Scores',
                    labels={'Property_type': 'Property Type', 'Review_scores': 'Review Score'})
        st.plotly_chart(fig, use_container_width=True)
 
        # Assuming you have a DataFrame named df with multiple categorical columns
        # Define the categorical columns you want to analyze
        categorical_columns = ['Property_type', 'Room_type', 'Bed_type','Cancellation_policy']

        # Create subplots for each categorical column
        fig = px.bar()

        for i, column in enumerate(categorical_columns):
        # Group by the current categorical column and calculate the count of each category
            data = df.groupby(column).size().reset_index(name='Count')

        # Create a bar chart for the current categorical column
            fig = px.bar(data, x=column, y='Count', title=f'Available Properties based on {column}')

        # Show the plot
            st.plotly_chart(fig, use_container_width=True)


        #Top 10 Property Types with Room Types and Their Average Prices
        fig = px.bar(top_10_property_types, x='Property_type', y='Price', color='Room_type',
                    title=f'Top 10 Property Types with Room Types and Their Average Prices in {selected_country}',
                    labels={'Property_type': 'Property Type', 'Price': 'Average Price', 'Room_type': 'Room Type'})
        st.plotly_chart(fig, use_container_width=True)

# Create a scatter plot to visualize the relationship between review scores and prices
        fig = px.scatter(selected_country_df, x='Review_scores', y='Price', color='Property_type',
                        title='Property type, Review scores vs price',
                        labels={'Review_scores': 'Review Scores', 'Price': 'Price'},
                        hover_data=['Property_type', 'Review_scores', 'Price'])

        # Show the scatter plot
        st.plotly_chart(fig, use_container_width=True)
 
        # Assuming you have a DataFrame named df with multiple categorical columns
        # Define the categorical columns you want to analyze
        categorical_columns = ['Property_type', 'Room_type', 'Bed_type','Cancellation_policy']

        # Create subplots for each categorical column
        fig = px.bar()

        for i, column in enumerate(categorical_columns):
        # Group by the current categorical column and calculate the count of each category
            data = df.groupby(column).size().reset_index(name='Count')

        # Create a bar chart for the current categorical column
            fig = px.bar(data, x=column, y='Count', title=f'Available Properties based on {column}')

        # Show the plot
            st.plotly_chart(fig, use_container_width=True)


if selected == "Selecting Property":
    # Placeholder for top of the page
        top_placeholder = st.empty() 
    
        # GETTING USER INPUTS
        selected_country = st.selectbox('Select Country', sorted(df['Country'].unique()))
        country_df = df[df['Country'] == selected_country]  # Filter the DataFrame based on selected country
        prop = st.multiselect('Select Property_type', sorted(df['Property_type'].unique()), sorted(df['Property_type'].unique()))
        selected_room_type = st.radio('Select Room Type', sorted(df['Room_type'].unique()))
        price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
        
        # CONVERTING THE USER INPUT INTO QUERY
        query = f"Country == '{selected_country}' & Room_type == '{selected_room_type}' & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}"

        # Filter the DataFrame based on the query
        filtered_df = df.query(query)

        # CREATING COLUMNS
        col1,col2 = st.columns(2,gap='medium')

        with col1:
                
                # TOP 10 PROPERTY TYPES BAR CHART
                df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
                fig = px.bar(df1,
                            title='Top 10 Property Types',
                            x='Listings',
                            y='Property_type',
                            orientation='h',
                            color='Property_type',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True) 
                
                # TOP 10 HOSTS BAR CHART
                df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
                fig = px.bar(df2,
                            title='Top 10 Hosts with Highest number of Listings',
                            x='Listings',
                            y='Host_name',
                            orientation='h',
                            color='Host_name',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)
                
                
        with col2:
                
                # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
                room_type_counts = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
                # Creating the bar chart
                fig = px.bar(room_type_counts, x="Room_type", y="counts", 
                title="Total Listings in each Room Type",
                color="Room_type",
                color_discrete_sequence=px.colors.qualitative.Set1)

        update_layout_and_display_chart(fig)

        # Display the filtered DataFrame table and the map
        display_filtered_df_and_map(filtered_df)

        
