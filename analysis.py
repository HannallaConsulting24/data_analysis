import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
file_path = r"C:\Users\Administrator\Downloads\processed_el3mdany1.xlsx"
df = pd.read_excel(file_path)

# Check required columns
required_columns = ['Ins', 'class', 'Net Profit', 'Highest Net Profit']
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
st.title("🔍 Net Profit Changes Analysis for Ins + Class")
st.write("This tool helps analyze profit changes between two periods for different insurance classes.")

# Explanation
st.markdown("### How to Use this Tool:")
st.markdown("1. **Select an Insurance (INS) and Class** to focus the analysis on a specific group.")
st.markdown("2. **View the data table** to see the raw profit values and calculated changes.")
st.markdown("3. **Explore different charts** that visualize how profits have changed over time.")
st.markdown("4. **Check summary statistics** for a deeper understanding of trends.")

# Filter for selected INS and Class
st.subheader("🔎 Select an Insurance and Class for Analysis")
ins_selected = st.selectbox("Select an INS", sorted(df['Ins'].dropna().unique()))
class_selected = st.selectbox("Select a Class", sorted(df[df['Ins'] == ins_selected]['class'].unique()))

df_filtered = df[(df['Ins'] == ins_selected) & (df['class'] == class_selected)]

# Display filtered data table
st.subheader(f"📊 Data Table for {ins_selected} - {class_selected}")
st.write("This table shows the profit values before and after, along with the calculated change.")
st.dataframe(df_filtered[['Ins', 'class', 'Net Profit', 'Highest Net Profit', 'Net Profit Change']])

# Net Profit Change Chart
st.subheader("📈 Net Profit Before vs. After")
st.write("This bar chart compares the net profit before and after for the selected class.")
fig_net = px.bar(
    df_filtered, x='class', y=['Net Profit', 'Highest Net Profit'],
    barmode='group', title='Net Profit Before vs. After per Class',
    labels={'value': 'Net Profit', 'variable': 'Period'}
)
st.plotly_chart(fig_net)

# Net Profit Change Distribution
st.subheader("📊 Distribution of Profit Changes")
st.write("This histogram shows the distribution of net profit changes, helping identify trends in profit shifts.")
fig_change_dist = px.histogram(
    df_filtered, x='Net Profit Change', nbins=20,
    title='Distribution of Net Profit Change'
)
st.plotly_chart(fig_change_dist)

# Net Profit Change per INS
st.subheader("📉 Net Profit Change per INS")
st.write("This bar chart displays how much the net profit changed for the selected insurance.")
fig_net_ins = px.bar(
    df_filtered, x='Ins', y='Net Profit Change',
    title='Net Profit Change per INS', labels={'Net Profit Change': 'Change in Net Profit'}
)
st.plotly_chart(fig_net_ins)

# Class-wise Net Profit Distribution
st.subheader("📊 Profit Change Across Classes")
st.write("This box plot helps visualize how different classes have experienced profit changes.")
fig_class_dist = px.box(
    df_filtered, x='class', y='Net Profit Change',
    title='Net Profit Change Distribution per Class'
)
st.plotly_chart(fig_class_dist)

# Summary of Changes
st.subheader("📉 Summary of Profit Changes")
st.write("This table summarizes the changes in net profit for the selected insurance and class.")
st.dataframe(df_filtered[['Ins', 'class', 'Net Profit Change']])

# Analytical Statistics
st.subheader("📊 Key Analytical Statistics")
st.write("These statistical values help understand the overall impact of profit changes.")
st.write("**📌 Average Net Profit Change:**", df_filtered['Net Profit Change'].mean())
st.write("**📌 Median Net Profit Change:**", df_filtered['Net Profit Change'].median())
st.write("**📌 Standard Deviation of Net Profit Change:**", df_filtered['Net Profit Change'].std())
st.write("**📌 Total Net Profit Before:**", df['Net Profit'].sum())
st.write("**📌 Total Net Profit After:**", df['Highest Net Profit'].sum())
st.write("**📌 Total changes in Net Profit:**", df['Highest Net Profit'].sum()-df['Net Profit'].sum())
