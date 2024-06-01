import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Set the page configuration at the start of the script
st.set_page_config(layout="wide")

df = pd.read_csv('data4test.csv')

# Function to get the records with values in the selected years and their counts
def get_records_by_years(years):
    record_counts = df.groupby('rn')['year'].apply(lambda x: sum(x.isin(years)))
    
    rn_data = {
        f"All {len(years)} years": {
            "rns": df.loc[df['rn'].isin(record_counts[record_counts == len(years)].index)]['rn'].tolist(),
            "count": len(df.loc[df['rn'].isin(record_counts[record_counts == len(years)].index)]['rn'])
        },
        f"All {len(years) - 1} years": {
            "rns": df.loc[df['rn'].isin(record_counts[record_counts == len(years) - 1].index)]['rn'].tolist(),
            "count": len(df.loc[df['rn'].isin(record_counts[record_counts == len(years) - 1].index)]['rn'])
        },
        f"All {len(years) - 2} years": {
            "rns": df.loc[df['rn'].isin(record_counts[record_counts == len(years) - 2].index)]['rn'].tolist(),
            "count": len(df.loc[df['rn'].isin(record_counts[record_counts == len(years) - 2].index)]['rn'])
        },
        f"All {len(years) - 3} years": {
            "rns": df.loc[df['rn'].isin(record_counts[record_counts == len(years) - 3].index)]['rn'].tolist(),
            "count": len(df.loc[df['rn'].isin(record_counts[record_counts == len(years) - 3].index)]['rn'])
        },
        "1 year": {
            "rns": df.loc[df['rn'].isin(record_counts[record_counts == 1].index)]['rn'].tolist(),
            "count": len(df.loc[df['rn'].isin(record_counts[record_counts == 1].index)]['rn'])
        }
    }
    
    return rn_data

# Function to plot time-series line graphs
def plot_timeseries(rn):
    record_df = df[df['rn'] == rn]
    
    # Create the figure
    fig = go.Figure()
    
    # Add the traces for each attribute
    fig.add_trace(go.Scatter(x=record_df['year'], y=record_df['wt'], mode='lines+markers', name='Weight'))
    fig.add_trace(go.Scatter(x=record_df['year'], y=record_df['ht'], mode='lines+markers', name='Height'))
    fig.add_trace(go.Scatter(x=record_df['year'], y=record_df['bmi'], mode='lines+markers', name='BMI'))
    fig.add_trace(go.Scatter(x=record_df['year'], y=record_df['sbp'], mode='lines+markers', name='Systolic BP'))
    fig.add_trace(go.Scatter(x=record_df['year'], y=record_df['dbp'], mode='lines+markers', name='Diastolic BP'))
    fig.add_trace(go.Scatter(x=record_df['year'], y=record_df['hb'], mode='lines+markers', name='Hemoglobin'))
    fig.add_trace(go.Scatter(x=record_df['year'], y=record_df['chol'], mode='lines+markers', name='Cholesterol'))
    fig.add_trace(go.Scatter(x=record_df['year'], y=record_df['hdl'], mode='lines+markers', name='HDL'))
    fig.add_trace(go.Scatter(x=record_df['year'], y=record_df['ldl'], mode='lines+markers', name='LDL'))
    
    # Customize the layout
    fig.update_layout(
        title=f"Trends for Record {rn} แสดงค่าโดยแตะที่จุดของปี",
        xaxis_title="Year",
        yaxis_title="Value",
        height=800,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

# Streamlit app
st.title("DHV วิเคราะห์ Time-series Trend")

# Get the unique years in the data
unique_years = df['year'].unique()

# Display the record IDs (RNs) that have data for the selected years and their counts
rn_data = get_records_by_years(unique_years)

for years, rn_info in rn_data.items():
    if rn_info['rns']:
        st.write(f"Records with data for {years} ({rn_info['count']}): {', '.join(map(str, rn_info['rns']))}")

# Select a record class and record ID
record_class = st.selectbox("Select the record class", rn_data.keys())
record_id = st.selectbox("Select a record ID", rn_data[record_class]['rns'])

# Plot the time-series line graphs
if st.button("Plot Trends"):
    fig = plot_timeseries(record_id)
    st.plotly_chart(fig, use_container_width=True)