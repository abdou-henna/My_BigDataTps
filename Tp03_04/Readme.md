### 📊 Amazon Customer Reviews Analysis – Digital Video Category

#### 🗂 Dataset Overview
This project uses the **Amazon Customer Reviews (Digital Video Download)** dataset, which includes user reviews from the Amazon marketplace. The original dataset was in `.tsv` format, and we filtered and cleaned it to extract meaningful features for modeling and visualization.

- **Original File**: `amazon_reviews_us_Digital_Video_Download_v1_00.tsv`
- **Size**: ~600MB+
- **Cleaned File**: `clean_amazon_reviews.csv`
- **Features Used**:
  - `star_rating`
  - `helpful_votes`
  - `total_votes`
  - `verified_purchase`
  - `is_positive` *(generated target: 1 if rating ≥ 4, else 0)*

---

#### ⚙️ Modeling Summary

A `RandomForestClassifier` was used to predict whether a review is positive based on the available features.

- **Model**: Random Forest (n_estimators=200, max_depth=10)
- **Sample size used**: 10% of the dataset
- **Accuracy**: **0.823**

##### 🧪 Classification Report

| Class       | Precision | Recall | F1-Score | Support |
|-------------|-----------|--------|----------|---------|
| Not Positive (0) | 0.74      | 0.22   | 0.34     | 16543   |
| Positive (1)     | 0.83      | 0.98   | 0.90     | 63337   |

- The model performed well for positive reviews due to class imbalance.
- Further tuning or balancing (e.g. SMOTE, class weights) may improve results.

---


## 📈 Power BI Visualizations

Using the **available visual types in Power BI** (as shown in the provided screenshot), the following charts were created based on the cleaned dataset:

### 1. **Clustered Column Chart**
- **X-axis**: `verified_purchase`
- **Y-axis**: Count of `is_positive`
- **Purpose**: Compare the number of positive vs negative reviews for verified and non-verified purchases.

### 2. **Pie Chart**
- **Legend**: `is_positive`
- **Values**: Count of reviews
- **Purpose**: Show proportion of positive vs negative reviews.

### 4. **Line or Area Chart**
- **X-axis**: `star_rating`
- **Y-axis**: Average `helpful_votes`
- **Purpose**: Show the trend between rating and helpfulness of reviews.

### 5. **Table Visual**
- **Columns**: `star_rating`, `helpful_votes`, `total_votes`, `verified_purchase`, `is_positive`
- **Purpose**: Display detailed data in a structured format.

---

#### ✅ Conclusion

This project demonstrated how to:

- Handle large `.tsv` files using `dask`
- Train a classifier on Amazon review data
- Generate performance metrics
- Visualize review behavior and verified purchase impact in Power BI

---

## 🐳 Running the Project with Docker

The project was containerized and successfully run using **Docker**, ensuring a reproducible environment for data cleaning and analysis.

### 📂 Files Included in Docker Image

- `amazon_reviews_us_Digital_Video_Download_v1_00.tsv`: Raw dataset.
- `Analyse.ipynb`: Jupyter Notebook used for data cleaning and model training.
- `PowerBiReport.pdf`: PDF export of Power BI visualizations.
- `requirements.txt`: Python dependencies for the notebook.

---