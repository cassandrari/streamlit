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
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
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

st.write("## Your additions")
#Add a drop down for Category
selected_category = st.selectbox("Select a Category:", df["Category"].unique())

#Add a multi-select for Sub_Category in the selected Category
sub_categories = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_sub_categories = st.multiselect("Select Sub-Categories:", sub_categories)

#Show a line chart of sales for the selected items in (2)
if selected_sub_categories:
    filtered_data = df[(df["Category"] == selected_category) & (df["Sub_Category"].isin(selected_sub_categories))]
    sales_by_month_filtered = filtered_data.groupby(pd.Grouper(key='Order_Date', freq='M')).agg({"Sales": "sum", "Profit": "sum"})
    
    st.line_chart(sales_by_month_filtered["Sales"])
    
    #Show three metrics for the selected items in (2): total sales, total profit, and overall profit margin (%)
    total_sales = filtered_data["Sales"].sum()
    total_profit = filtered_data["Profit"].sum()
    overall_profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
    
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Overall Profit Margin (%)", f"{overall_profit_margin:.2f}%", delta=overall_profit_margin - (df["Profit"].sum() / df["Sales"].sum() * 100 if df["Sales"].sum() > 0 else 0))

