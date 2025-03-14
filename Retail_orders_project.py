import mysql.connector
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def get_connection():
    if "conn" not in st.session_state or not st.session_state.conn.is_connected():
        st.session_state.conn = mysql.connector.connect(
            host=st.secrets["gateway01.ap-southeast-1.prod.aws.tidbcloud.com"],
            user=st.secrets["3QUsgxAxK8dDXTK.root"],
            password=st.secrets["wdQNGsQeVe8OQUkE"],
            database=st.secrets["Retail_orders"]
        )
    return st.session_state.conn

# Function to execute queries
def run_query(query):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Fetch column names
        column_names = [i[0] for i in cursor.description]
        
        # Fetch data
        data = cursor.fetchall()
        
        # Convert to Pandas DataFrame
        df = pd.DataFrame(data, columns=column_names)
        
        cursor.close()  # Close the cursor
        return df
    except Exception as e:
        st.error(f"Query execution failed: {e}")
        return pd.DataFrame()

# Streamlit UI
st.title("📊 Data Analysis with SQL")

# Sidebar Selection
category = st.sidebar.radio("Choose a Category:", ["Business Insights", "SQL Queries"])

# Business Insights Queries
business_queries = {
    "Top-Selling Products": "SELECT product_id, sub_category, SUM(quantity * sale_price) AS total_revenue FROM orders_part2 GROUP BY product_id ORDER BY total_revenue DESC LIMIT 10;",
    "Monthly Sales Analysis": """SELECT YEAR(STR_TO_DATE(o.order_date, '%d-%m-%Y')) AS year, 
        MONTH(STR_TO_DATE(o.order_date, '%d-%m-%Y')) AS month,
        SUM(p.sale_price) AS total_sales
        FROM orders_part1 o
        JOIN orders_part2 p ON o.product_id = p.product_id
        WHERE STR_TO_DATE(o.order_date, '%d-%m-%Y') IS NOT NULL
        GROUP BY year, month
        ORDER BY year, month;""",

    "Product Performance": """SELECT o.product_id, p.sub_category,
    SUM(p.sale_price) AS total_revenue,
    SUM(p.profit) AS total_profit,
    ROUND(SUM(p.profit) / NULLIF(SUM(p.sale_price), 0), 1) AS profit_margin,
    COUNT(o.product_id) AS total_orders,
    ROW_NUMBER() OVER (ORDER BY SUM(p.sale_price) DESC) AS revenue_rank,
    CASE 
        WHEN (SUM(p.profit) / NULLIF(SUM(p.sale_price), 0)) > 0.5 THEN 'High Profit'
        WHEN (SUM(p.profit) / NULLIF(SUM(p.sale_price), 0)) BETWEEN 0.2 AND 0.5 THEN 'Medium Profit'
        ELSE 'Low Profit'
    END AS profit_category
    FROM orders_part1 o
    JOIN orders_part2 p ON o.product_id = p.product_id
    GROUP BY o.product_id, p.sub_category
    HAVING total_revenue > 1000  -- Filtering out low-revenue products
    ORDER BY total_revenue DESC LIMIT 25;""",

    "Regional Sales Analysis":  """SELECT orders_part1.region, 
    SUM(orders_part2.sale_price * orders_part2.quantity) AS total_revenue, 
    COUNT(orders_part1.order_id) AS total_orders
    FROM orders_part1 
    JOIN orders_part2  
    ON orders_part1.product_id = orders_part2.product_id
    GROUP BY orders_part1.region
    ORDER BY total_revenue DESC;""",

    "Discount Analysis":"""SELECT orders_part2.sub_category, product_id, SUM(quantity*sale_price) AS total_sales, SUM(discount) AS total_dicount,
                 (SUM(discount) / SUM(sale_price * quantity)) * 100 AS discount_percentage
                 FROM orders_part2
                 WHERE discount_percent>20
                 GROUP BY product_id, sub_category
                 ORDER BY discount_percentage DESC;"""
}
# SQL Queries
sql_queries = {
    "Top 10 Highest Revenue Generating Products":"""SELECT 
    product_id, sub_category,
    SUM(sale_price) AS total_revenue
FROM orders_part2
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10;""",

    "Top 5 Cities with Highest Profit Margins":"""SELECT 
    o.city,
    SUM(p.profit) AS total_profit,
    SUM(p.sale_price * p.quantity) AS total_revenue,
    (SUM(p.profit) / SUM(p.sale_price * p.quantity)) * 100 AS profit_margin
FROM orders_part1 o
JOIN orders_part2 p ON o.product_id = p.product_id
GROUP BY o.city
ORDER BY profit_margin DESC
LIMIT 5;

""",
    "Total Discount Given Per Category": """SELECT 
    o.category, 
    SUM(p.discount) AS total_discount
FROM orders_part1 o
JOIN orders_part2 p ON o.product_id = p.product_id
GROUP BY o.category
ORDER BY total_discount DESC LIMIT 3;
 """,
    "Average Sale Price per Product Category": """SELECT orders_part1.category, AVG(orders_part2.list_price - (orders_part2.list_price * orders_part2.discount_percent / 100)) AS avg_sale_price
FROM orders_part1
JOIN orders_part2 ON orders_part1.product_id = orders_part2.product_id
GROUP BY orders_part1.category DESC LIMIT 3;
 """,
    "Region with Highest Average Sale Price":"""SELECT orders_part1.region, AVG(orders_part2.list_price - (orders_part2.list_price * orders_part2.discount_percent / 100)) AS avg_sale_price
FROM orders_part1
JOIN orders_part2 ON orders_part1.product_id = orders_part2.product_id
GROUP BY orders_part1.region
ORDER BY avg_sale_price DESC
LIMIT 1;
 """,
    "Total Profit Per Category": """SELECT orders_part1.category, SUM((orders_part2.list_price - orders_part2.cost_price) * orders_part2.quantity) AS total_profit
FROM orders_part1
JOIN orders_part2 ON orders_part1.product_id = orders_part2.product_id
GROUP BY orders_part1.category DESC LIMIT 3;
 """,
    "Top 3 Segments with Highest Quantity of Orders": """SELECT orders_part1.segment, SUM(orders_part2.quantity) AS total_orders
FROM orders_part1
JOIN orders_part2 ON orders_part1.product_id = orders_part2.product_id
GROUP BY orders_part1.segment
ORDER BY total_orders DESC
LIMIT 3;
 """,
    "Average Discount Percentage Per Region": """SELECT orders_part1.region, AVG(orders_part2.discount_percent) AS avg_discount
FROM orders_part1
 JOIN orders_part2 ON orders_part1.product_id = orders_part2.product_id
GROUP BY orders_part1.region DESC;
 """,
    "Product Category with Highest Total Profit": """SELECT o.category, SUM((p.list_price - p.cost_price) * p.quantity) AS total_profit
FROM orders_part1 o
JOIN orders_part2 p ON o.product_id = p.product_id
GROUP BY o.category
ORDER BY total_profit DESC
LIMIT 1;
 """,
    "Total Revenue Generated Per Year": """SELECT 
    YEAR(STR_TO_DATE(o.order_date, '%d-%m-%Y')) AS year, 
    SUM(p.quantity * p.list_price) AS total_revenue
FROM orders_part1 o
JOIN orders_part2 p ON o.product_id = p.product_id
WHERE STR_TO_DATE(o.order_date, '%d-%m-%Y') IS NOT NULL
GROUP BY year
ORDER BY year;
 """,
 
    "Least Profitable Product Category": "SELECT o.category, SUM((p.list_price - p.cost_price) * p.quantity) AS total_profit FROM orders_part1 o JOIN orders_part2 p ON o.product_id = p.product_id GROUP BY o.category ORDER BY total_profit ASC LIMIT 2;",
    "Region with the Lowest Total Orders": "SELECT o.region, COUNT(o.order_id) AS total_orders FROM orders_part1 o GROUP BY o.region ORDER BY total_orders ASC LIMIT 2;",
    "Average Order Value Per Region": "SELECT o.region, AVG(P.quantity * p.list_price) AS avg_order_value FROM orders_part1 o JOIN orders_part2 p ON o.product_id = p.product_id GROUP BY o.region;",
    "Total Number of Orders Per Year": """SELECT YEAR(STR_TO_DATE(o.order_date, '%d-%m-%Y')) AS year, 
    COUNT(o.order_id) AS total_orders
FROM orders_part1 o
WHERE STR_TO_DATE(o.order_date, '%d-%m-%Y') IS NOT NULL
GROUP BY year
ORDER BY year;""",
    "Top 3 Most Profitable Products": "SELECT p.product_id, p.sub_category, SUM((p.list_price - p.cost_price) * p.quantity) AS total_profit FROM orders_part1 o JOIN orders_part2 p ON o.product_id = p.product_id GROUP BY p.product_id ORDER BY total_profit DESC LIMIT 3;",
    "Most Popular Ship Mode": "SELECT o.ship_mode, COUNT(o.order_id) AS order_count FROM orders_part1 o GROUP BY o.ship_mode ORDER BY order_count DESC LIMIT 1;",
    "Most Frequently Ordered Product": "SELECT p.product_id, p.sub_category, COUNT(o.order_id) AS order_count FROM orders_part1 o JOIN orders_part2 p ON o.product_id = p.product_id GROUP BY p.product_id ORDER BY order_count DESC LIMIT 1;",
    "Percentage of Orders for Each Category": "SELECT o.category, COUNT(o.order_id) * 100.0 / (SELECT COUNT(*) FROM orders_part1) AS percentage_of_orders FROM orders_part1 o GROUP BY o.category DESC LIMIT 4;",
    "Average Profit Per Order for Each City": "SELECT o.city, AVG((p.list_price - p.cost_price) * P.quantity) AS avg_profit_per_order FROM orders_part1 o JOIN orders_part2 p ON o.product_id = p.product_id GROUP BY o.city ORDER BY avg_profit_per_order DESC;",
    "Top 3 Most Popular Product Categories by Total Quantity Sold": "SELECT o.category, SUM(p.quantity) AS total_quantity_sold FROM orders_part1 o JOIN orders_part2 p ON o.product_id = p.product_id GROUP BY o.category ORDER BY total_quantity_sold DESC LIMIT 3;"
}

# Select Query Based on Category
if category == "Business Insights":
    selected_query = st.selectbox("Select an Insight:", list(business_queries.keys()))
    if st.button("Run Query"):
        data = run_query(business_queries[selected_query])
        st.write("### Query Results")
        st.dataframe(data)  # Display Table
        
        # Generate Charts
        if not data.empty:
            if "product_id" in data.columns:
                fig = px.bar(data, x="product_id" or "city", y="total_revenue", title="Top-Selling Products")
                st.plotly_chart(fig)
            elif "total_sales" in data.columns:
                fig = px.line(data, x="month", y="total_sales", title="Monthly Sales Trend")
                st.plotly_chart(fig)
            elif "city" in data.columns and "profit_margin" in data.columns:
                fig = px.bar(data, x="city", y="profit_margin", title="Top 5 Cities with Highest Profit Margins", color="total_profit")
                st.plotly_chart(fig)
            elif "region" in data.columns and "total_revenue" in data.columns:
                fig = px.bar(data, x="region", y="total_revenue", title="Total Revenue by Region", color="total_orders")
                st.plotly_chart(fig)

elif category == "SQL Queries":
    selected_query = st.selectbox("Select a Query:", list(sql_queries.keys()))
    if st.button("Run Query"):
        data = run_query(sql_queries[selected_query])
        st.write("### Query Results")
        st.dataframe(data)  # Display Table
        
        # Generate Charts
        if not data.empty:
            if "product_id" in data.columns:
                fig = px.bar(data, x="product_id", y="total_revenue", title="Revenue by Product")
                st.plotly_chart(fig)
            
