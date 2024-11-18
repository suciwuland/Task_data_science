import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set the style for Seaborn
sns.set(style='dark')

# Load data
full_data = pd.read_csv("full_data.csv") 

# Preprocessing
full_data['order_purchase_timestamp'] = pd.to_datetime(full_data['order_purchase_timestamp'])
full_data['order_delivered_customer_date'] = pd.to_datetime(full_data['order_delivered_customer_date'])
full_data['order_estimated_delivery_date'] = pd.to_datetime(full_data['order_estimated_delivery_date'])
full_data['delivery_delay'] = (full_data['order_delivered_customer_date'] - full_data['order_estimated_delivery_date']).dt.days

# Streamlit App
st.title("E-Commerce Dashboard")

# Date filter
st.sidebar.header("Filter by Date")
start_date = st.sidebar.date_input("Start Date", full_data['order_purchase_timestamp'].min())
end_date = st.sidebar.date_input("End Date", full_data['order_purchase_timestamp'].max())

filtered_data = full_data[
    (full_data['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
    (full_data['order_purchase_timestamp'] <= pd.Timestamp(end_date))
]

# Total Sales
total_sales = len(filtered_data)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Sales", f"{total_sales:,}")

# Total Order Status Count in a 3x4 grid
st.subheader("Total Order Status Count")

# Define the status order and count
order_status_counts = filtered_data['order_status'].value_counts()

# Create columns for 3 rows and 4 columns grid
cols = st.columns(4)

# Loop through each order status and display in each column, filling rows as needed
for i, (status, count) in enumerate(order_status_counts.items()):
    row = i // 4  # Calculate the row index (integer division by 4)
    col = i % 4  # Calculate the column index (modulo 4)
    
    # Use st.container to group the status cards in the layout
    with cols[col]:
        st.metric(f"{status}", f"{count:,}")

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")
filtered_data['year_month'] = filtered_data['order_purchase_timestamp'].dt.to_period('M')
monthly_sales = filtered_data.groupby('year_month').size()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=monthly_sales.index.astype(str), y=monthly_sales.values, marker='o', ax=ax)
ax.set_title("Monthly Sales Trend")
ax.set_xlabel("Year-Month")
ax.set_ylabel("Sales Count")
plt.xticks(rotation=45)
st.pyplot(fig)

# Top 10 Product Categories
st.subheader("Top 10 Product Categories")
top_categories = (
    filtered_data['product_category_name_english']
    .value_counts()
    .head(10)
    .sort_values(ascending=False)
)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_categories.values, y=top_categories.index, palette='magma', ax=ax)
ax.set_title("Top 10 Product Categories")
ax.set_xlabel("Sales Count")
ax.set_ylabel("Product Category")
st.pyplot(fig)

# Bottom 10 Product Categories
st.subheader("Bottom 10 Product Categories")
bottom_categories = (
    filtered_data['product_category_name_english']
    .value_counts()
    .tail(10)
    .sort_values(ascending=True)
)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=bottom_categories.values, y=bottom_categories.index, palette='cool', ax=ax)
ax.set_title("Bottom 10 Product Categories")
ax.set_xlabel("Sales Count")
ax.set_ylabel("Product Category")
st.pyplot(fig)

# Delivery Delay Distribution
st.subheader("Delivery Delay Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data['delivery_delay'], bins=20, kde=False, color='coral', ax=ax)
ax.set_title("Delivery Delay Distribution")
ax.set_xlabel("Delivery Delay (Days)")
ax.set_ylabel("Number of Orders")
st.pyplot(fig)

# Payment Method Distribution
st.subheader("Payment Method Distribution")
payment_counts = filtered_data['payment_type'].value_counts()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=payment_counts.index, y=payment_counts.values, palette='viridis', ax=ax)
ax.set_title("Payment Method Distribution")
ax.set_xlabel("Payment Type")
ax.set_ylabel("Transaction Count")
st.pyplot(fig)

# Review Score Distribution
st.subheader("Review Score Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data['review_score'], bins=5, kde=False, color='blue', ax=ax)
ax.set_title("Review Score Distribution")
ax.set_xlabel("Review Score")
ax.set_ylabel("Number of Reviews")
st.pyplot(fig)

# Customer State Distribution
st.subheader("Customer Distribution by State")
state_sales = filtered_data['customer_state'].value_counts()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=state_sales.values, y=state_sales.index, palette='viridis', ax=ax)
ax.set_title("Customer Distribution by State")
ax.set_xlabel("Customer Count")
ax.set_ylabel("State")
st.pyplot(fig)
