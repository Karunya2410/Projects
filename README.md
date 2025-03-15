# Retail Orders Analysis Project

This project analyzes retail order data using Python and Streamlit for interactive visualization. It processes the dataset and provides insights and some queries through tables and charts.

##  Installation & Setup

### **1. Clone the Repository**

```bash
git clone https://github.com/Karunya2410/Projects.git
cd Projects
```

### **2. Install Dependencies**

Ensure you have Python installed (version 3.x recommended). Install the required libraries using:

```bash
pip install -r requirements.txt
```

Requirements file: [requirements.txt](https://github.com/Karunya2410/Projects/blob/8c263618faefc7cf2152527fb095d79d723d0a42/requirements.txt)

### **3. Run the Streamlit App**

```bash
streamlit run Retail_orders_project.py
```

Source code: [Retail_orders_project.py](https://github.com/Karunya2410/Projects/blob/8c263618faefc7cf2152527fb095d79d723d0a42/Retail_orders_project.py)

## 📊 Dataset Details

- The project uses a retail orders dataset split into two parts:
  - [orders_part1.csv](https://github.com/Karunya2410/Projects/blob/8c263618faefc7cf2152527fb095d79d723d0a42/orders_part1.csv)
  - [orders_part2.csv](https://github.com/Karunya2410/Projects/blob/8c263618faefc7cf2152527fb095d79d723d0a42/orders_part2.csv)
- The dataset should be placed in the same directory as the script (or modify the script to provide the correct path).
- Expected format: **CSV** with columns like `Order ID`, `Product`, `Quantity`, `Price`, etc.

## 🛠️ Features

- Load and analyze retail order data
- Display summary statistics
- Generate visualizations 
- Interactive filtering and exploration via Streamlit

## 🔧 Configuration

If your dataset is in a different location or format, update the script accordingly:

```python
import pandas as pd
df = pd.read_csv("path/to/your/dataset.csv")
```


Developed by [Karunya2410](https://github.com/Karunya2410). 


