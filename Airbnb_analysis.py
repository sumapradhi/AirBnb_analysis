# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

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
    selected = option_menu("Menu", ["Home","Dataframe Creation","Price Analysis and Visualization","Explore"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
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
    col1.markdown("## :orange[Domain] : Travel Industry, Property Management, and Tourism ✈️")
    col1.markdown("## :orange[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    col1.markdown("## :orange[Objective] : This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
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



if selected == "Price Analysis and Visualization":
    # Placeholder for top of the page
    top_placeholder = st.empty() 
 
   # GETTING USER INPUTS
    selected_country = st.selectbox('Select Country', sorted(df['Country'].unique()))
    country_df = df[df['Country'] == selected_country]  # Filter the DataFrame based on selected country
    prop = st.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique(),primaryColor="blue"))
    selected_room_type = st.radio('Select Room Type', sorted(df['Room_type'].unique()))
    # Define price range slabs
    price_slabs = {
    "1 - 1000": (1, 1000),
    "1001 - 5000": (1001, 5000),
    "5001 - 10000": (5001, 10000),
    "10001 - 50000": (10001, 50000)
    }

    selected_price_slab = st.selectbox('Select Price Range', list(price_slabs.keys()))

    # Get price range from selected slab
    price_range = price_slabs[selected_price_slab]

    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country == "{selected_country}" & Room_type == "{selected_room_type}" & Property_type in {prop} & Price >= {price_range[0]} & Price <= {price_range[1]}'

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

            # Updating layout and displaying the chart
            fig.update_layout(xaxis_title="Room Type", yaxis_title="Number of Listings")
            st.plotly_chart(fig, use_container_width=True)
            
            
# Display the map with st.map()
df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)

# Display the map with st.map()
st.map(df, zoom=2)

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

#Country-wise Property Availability Heatmap
# Grouping the data by country and summing the availability

fig = px.density_heatmap(df, x='Country', y='Availability_365')

# Update the layout
fig.update_layout(
    title='Country-wise Property Availability',
    xaxis_title='Country',
    yaxis_title='Availability (Days)'

)
# Show the plot
st.plotly_chart(fig)


       
       