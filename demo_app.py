import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('vehicles_us.csv')
st.markdown("""
# Cars' Sales and ADs

This app displays the graphical information of the data contained in the car sales and ads dataset below.

### Data Viewer
""")

# Add new columns to the dataset
df['manufacturer'] = df['model'].apply(lambda x: x.split(' ')[0])
df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d')
df['vehicle_age'] = (df['date_posted'].dt.year) - df['model_year']
df['mileage_per_year'] = df['odometer'] / df['vehicle_age']
df['month_year_posted'] = df['date_posted'].apply(lambda x: x.strftime('%Y-%m'))

# Replace the infs in mileage_per_year column with the respective value in odometer column since the vehicle age is 0
not_inf_mileage = df.query('mileage_per_year != "inf"')
df['new_mileage_per_year'] = (
                            df['mileage_per_year']
                            .where(df['mileage_per_year']
                            .isin(not_inf_mileage['mileage_per_year']), df['odometer'])
                            .round(2)
)
del df['mileage_per_year']
df['new_mileage_per_year'].fillna(0, inplace=True)
df.rename(columns={'new_mileage_per_year': 'mileage'}, inplace=True)

# Replace the 'inf' in mileage column with 0 since their odometer is 0
df['mileage'].replace([np.inf, -np.inf], 0, inplace=True)
df

cbox = st.checkbox('Manufacturers with more than 1000 listings', value=True)
if cbox:
    df1 = df.groupby('manufacturer').filter(lambda x: len(x) >= 1000).reset_index(drop=True)
df1

def df_histograms(df, x, color):
    """
    This function plot histograms for display
    """
    fig = px.histogram(df, x=x, color=color, opacity=0.75)
    st.write(fig)

date_options = st.select_slider(options=np.sort(df['month_year_posted'].unique()), label='Choose the date (in month and year) of ads you would like to explore')


st.markdown("""
### **Explore Car Types**

Take a look at car types by different manufacturers and by their ads dates. Select two different car types you wish to explore and compare in the dropdowns below.
""")
# Create two selectbox that'll allow user select two car types to visualize
type_list = sorted(df['type'].unique())
type_1 = st.selectbox('Select type #1',
                        type_list,
                        index=type_list.index('SUV'))
type_2 = st.selectbox('Select type #2',
                        type_list,
                        index=type_list.index('truck'))

mask_filter = (df['type'] == type_1) | (df['type'] == type_2)
df_filtered = df[mask_filter]

st.markdown('**Manufacturers and their Car Types**')
df_histograms(df_filtered, 'manufacturer', 'type')

st.markdown('**Ads Dates and Car Types**')
df_histograms(df_filtered, 'month_year_posted', 'type')

st.markdown('**Number of Days Listed and Car Types**')
df_histograms(df_filtered, 'days_listed', 'type')

st.markdown('**Price by Manufacturer**')
fig = px.histogram(df_filtered,
                    x='price',
                    color='type',
                    opacity=0.7,
                    nbins=30,
                    histnorm='percent',
                    barmode='overlay')
st.write(fig)


st.markdown("""
### **Explore Conditions**

Take a look at conditions by different maunfacturers and car types. Select two different car types you wish to explore and compare in the dropdowns below.
""")

# Create two sele
st.markdown('**Manufacturer and their Conditions**')
df_histograms(df, 'manufacturer', 'condition')

st.markdown('**Car Types and their Conditions**')
df_histograms(df, 'type', 'condition')

st.markdown('**Model Year and their Conditions**')
df_histograms(df, 'model_year', 'condition')


st.markdown('**Ads Date by Manufacturer**')
fig = px.histogram(df,
                    x='month_year_posted',
                    color='type',
                    histnorm='percent')
st.write(fig)
