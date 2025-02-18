import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_csv(r"C:\Users\leand\Desktop\app\vs_data.csv"
        
    )
    return df

df = get_data_from_excel()


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
item = st.sidebar.multiselect(
    "Select Item:",
    options=df["Item"].unique(),
    default=df["Item"].unique()
)


location = st.sidebar.multiselect(
    "Select the Location:",
    options=df["Location"].unique(),
    default=df["Location"].unique(),
)


df_selection = df.query(
    "Item in @item & Location in @location"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----

st.title("Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = round(df_selection["Total Spent"].sum(), 2)

grouped = round(df_selection.groupby("Month")["Total Spent"].sum(), 2)
avg_monthly_sales = round(grouped.mean(), 2)

grouped_it = df_selection.groupby("Item")["Quantity"].count()
total_item_quantity = grouped_it.sum()

left_column, center_column, right_column = st.columns(3)
with left_column:
   with st.container(border=True):
      st.subheader("Total Sales:")
      st.subheader(f"US $ {total_sales:,.2f}")
with center_column:
   with st.container(border=True): 
     st.subheader("Average Monthly Sales:")
     st.subheader(f"US $ {avg_monthly_sales:,.2f}")
with right_column:
    with st.container(border=True):
      st.subheader("Total Items Sold:")
      st.subheader(total_item_quantity)
                     
st.markdown("""---""")

st.subheader("Monthly Total Sales Trend")
fig_product_sales = px.line(
    grouped,
    x=grouped.index,
    y="Total Spent",
    title="<b>Monthly Sales</b>",
    color_discrete_sequence=["#0083B8"] * len(grouped),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis = dict(
        tickmode = 'array',
        tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
)

# SALES BY HOUR [BAR CHART]
sales_by_item = df_selection.groupby(by=["Item"])[["Total Spent"]].sum()


fig_item_sales = px.bar(
    sales_by_item,
    x=sales_by_item.index,
    y="Total Spent",
    title="<b>Sales by item</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_item),
    template="plotly_white"
)
fig_item_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_item_sales, use_container_width=True)


st.markdown("""---""")

# Group by method and sum Total Spent
sales_by_method = df_selection.groupby(by=["Payment Method"])[["Total Spent"]].sum()
color_scale = px.colors.sequential.Aggrnyl

num_slices = len(sales_by_method)
colors = [color_scale[i % len(color_scale)] for i in range(num_slices)]

# Create a pie chart with spaced slices
fig_method_sales = px.pie(
    sales_by_method, 
    names=sales_by_method.index,  # Set 'Item' as the slice labels
    values="Total Spent",       # Set 'Total Spent' as the value for each slice
    color="Total Spent",
    color_discrete_sequence= colors,
    template="plotly_white"
)

# Add space between slices using the 'pull' parameter
fig_method_sales.update_traces(pull=[0.01] * len(sales_by_method))  # Pull each slice apart

# Update layout for aesthetics
fig_method_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
    margin=dict(t=40, b=40, l=40, r=40)  # Adjust margins for better spacing
)

grouped5 = df_selection.groupby(['Item', 'Location'])['Total Spent'].sum()

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Sales by Payment Method")
    st.plotly_chart(fig_method_sales, use_container_width=True)

with right_column:
    st.subheader("Item Sales In-store vs Takeaway")
    st.dataframe(grouped5, column_config={
        "Total Spent": st.column_config.NumberColumn(
            "Total Spent (USD)",  # Custom column name
            format="$%.2f"  # Format as currency with two decimal places
        )
    }, use_container_width=True)


