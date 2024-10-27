### Shipment Price Prediction Project Setup Guide

**Project Name:** `shipment-price-prediction`

**Brief Description:**
The Shipment Price Prediction project leverages advanced machine learning algorithms to transform the logistics and supply chain industry. This solution focuses on predicting shipment prices with exceptional accuracy, providing businesses with the tools to optimize transportation strategies, reduce costs, and improve overall operational efficiency.

#### 🚀 Getting Started

**1. Environment Setup:**
   ```bash
   conda create --prefix venv python==3.8 -y
   conda activate venv/
   ```

**2. Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

**3. MongoDB Configuration:**
   - Dataset is sourced from `notebooks/data` and stored in MongoDB.
   - Ensure MongoDB is installed and running.
   - Set the `MONGO_DB_URL` environment variable in your system.
   - Data is stored in the database named `"shipmentdata"` and collection named `"ship"`.

**4. Run the Application:**
   ```bash
   python app.py
   ```

#### 🛠️ Built with

- **Flask:** Web framework for building the application.
- **Python 3.8:** Programming language for development.
- **Machine Learning:** Utilizing Scikit-learn for predictive modeling.
- **MongoDB:** NoSQL database for storing and managing shipment data.
- **Industrial Use Cases:** Tailored for real-world logistics and supply chain applications.



#### 🌐 Application Usage

1. Access the application through a web browser.
2. Input shipment parameters (distance, weight, etc.).
3. Receive accurate predictions for shipment prices.
4. Explore dynamic pricing strategies based on real-time data.

**Note:** Ensure the `MONGO_DB_URL` environment variable is set before running the application.

This setup guide provides a foundation for deploying and utilizing the Shipment Price Prediction project. By combining machine learning with practical industry insights, this project aims to empower businesses to make informed decisions in the dynamic landscape of logistics and supply chain management.