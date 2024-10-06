import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the dataframe index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

# New features added below
categories = df['Category'].unique()
selected_category = st.selectbox("Select a Category", categories)

subcategories = df[df['Category'] == selected_category]['Sub-Category'].unique()
selected_subcategories = st.multiselect("Select Sub-Categories", subcategories)

if selected_subcategories:
    filtered_data = df[(df['Category'] == selected_category) & (df['Sub-Category'].isin(selected_subcategories))]

    st.write("### (3) Show a line chart of sales for the selected items in (2)")
    sales_data = filtered_data.groupby(filtered_data.index)['Sales'].sum()
    st.line_chart(sales_data)

    st.write("### (4) Show three metrics for the selected items in (2): total sales, total profit, and overall profit margin (%)")
    total_sales = filtered_data['Sales'].sum()
    total_profit = filtered_data['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Overall Profit Margin (%)", f"{overall_profit_margin:.2f}%")

    st.write("### (5) Use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
    overall_average_margin = (df['Profit'].sum() / df['Sales'].sum() * 100) if df['Sales'].sum() > 0 else 0
    delta = overall_profit_margin - overall_average_margin
    st.metric("Overall Profit Margin (%)", f"{overall_profit_margin:.2f}%", delta=f"{delta:.2f}%", delta_color="inverse")
