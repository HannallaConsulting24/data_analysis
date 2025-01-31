import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
file_path = r"final3.xlsx"
df = pd.read_excel(file_path)

# Check required columns
required_columns = ['Script','NDC','Ins', 'class','Prescriber', 'Net Profit','NDC for Highest Net Profit', 'Highest Net Profit']
if not all(col in df.columns for col in required_columns):
    st.error("⚠️ The file does not contain the required columns for analysis.")
    st.stop()

# Ensure class names are sorted and displayed correctly
df['class'] = df['class'].astype(str)  # Convert to string to avoid selection issues

# Remove empty values from 'Ins' column
df = df.dropna(subset=['Ins'])

# Calculate changes
df['Net Profit Change'] = df['Highest Net Profit'] - df['Net Profit']

# Streamlit UI setup
st.title("🔍 Comprehensive Net Profit Analysis for Ins + Class")
st.write("This tool provides a deep dive into profit variations across different insurance classes.")

# Explanation
st.markdown("### How to Use this Tool:")
st.markdown("1. **Select an Insurance (INS) and Class** to focus the analysis on a specific group.")
st.markdown("2. **View the detailed data table** including key prescribers, scripts, and NDC codes.")
st.markdown("3. **Explore enhanced visualizations** showing various profit trends.")
st.markdown("4. **Check extended summary statistics** for in-depth insights.")

# Filter for selected INS and Class
st.subheader("🔎 Select an Insurance and Class for Analysis")
ins_selected = st.selectbox("Select an INS", sorted(df['Ins'].dropna().unique()))
class_selected = st.selectbox("Select a Class", sorted(df[df['Ins'] == ins_selected]['class'].unique()))

df_filtered = df[(df['Ins'] == ins_selected) & (df['class'] == class_selected)]

# Display enhanced data table
st.subheader(f"📊 Detailed Data Table for {ins_selected} - {class_selected}")
st.write("This table includes additional details like Script ID, NDC, and Prescriber.")
st.dataframe(df_filtered[['Script', 'NDC', 'NDC for Highest Net Profit', 'Prescriber', 'Ins', 'class', 'Net Profit', 'Highest Net Profit', 'Net Profit Change']])

# Net Profit Change Chart
st.subheader("📈 Net Profit Before vs. After by Class")
fig_net = px.bar(
    df_filtered, x='class', y=['Net Profit', 'Highest Net Profit'],
    barmode='group', title='Net Profit Comparison Before vs. After',
    labels={'value': 'Net Profit', 'variable': 'Period'}
)
st.plotly_chart(fig_net)

# Net Profit Change Distribution
st.subheader("📊 Histogram of Profit Changes")
fig_change_dist = px.histogram(
    df_filtered, x='Net Profit Change', nbins=20,
    title='Distribution of Net Profit Change'
)
st.plotly_chart(fig_change_dist)

# Top Prescribers by Net Profit Contribution
st.subheader("🏥 Top Prescribers Impacting Net Profit")
fig_prescribers = px.bar(
    df_filtered.groupby('Prescriber')['Net Profit'].sum().reset_index(),
    x='Prescriber', y='Net Profit', title='Net Profit Contribution by Prescriber'
)
st.plotly_chart(fig_prescribers)

# Top NDC Codes Affecting Net Profit
st.subheader("💊 Top NDC Codes by Profitability")
fig_ndc = px.bar(
    df_filtered.groupby('NDC')['Net Profit'].sum().reset_index(),
    x='NDC', y='Net Profit', title='Net Profit by NDC Code'
)
st.plotly_chart(fig_ndc)

# Class-wise Net Profit Distribution
st.subheader("📊 Profit Change Across Classes")
fig_class_dist = px.box(
    df_filtered, x='class', y='Net Profit Change',
    title='Net Profit Change Distribution per Class'
)
st.plotly_chart(fig_class_dist)

# Summary of Changes
st.subheader("📉 Summary of Profit Changes")
st.dataframe(df_filtered[['Ins', 'class', 'Net Profit Change']])

# Enhanced Analytical Statistics
st.subheader("📊 Extended Statistical Insights")
st.write("**📌 Average Net Profit Change:**", df_filtered['Net Profit Change'].mean())
st.write("**📌 Median Net Profit Change:**", df_filtered['Net Profit Change'].median())
st.write("**📌 Standard Deviation of Net Profit Change:**", df_filtered['Net Profit Change'].std())
st.write("**📌 Total Net Profit Before:**", df['Net Profit'].sum())
st.write("**📌 Total Net Profit After:**", df['Highest Net Profit'].sum())
st.write("**📌 Total Changes in Net Profit:**", df['Highest Net Profit'].sum() - df['Net Profit'].sum())
