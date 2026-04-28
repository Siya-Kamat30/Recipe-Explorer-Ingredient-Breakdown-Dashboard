# 🍽️ Recipe Explorer & Ingredient Breakdown Dashboard

An interactive Power BI dashboard that allows users to explore recipes visually and drill into detailed ingredient and nutrition information — designed with a clean, magazine-style UI and built end-to-end from raw data to final insights.

## 🖼️ Dashboard Preview

![Recipe Explorer Dashboard](<img width="1434" height="800" alt="Dashboard_Video" src="https://github.com/user-attachments/assets/7b5e39aa-87bd-4b5f-8a50-198ffd929752" />)

## Project Motivation

While learning Power BI and data modeling, I wanted to build a project that was:
1. Realistic (based on real-world messy data)
2. End-to-end (data cleaning → modeling → visualization)
3. User-focused, not just charts for the sake of charts

Food & recipes felt like a perfect domain to explore data modeling, drill-through, visuals, and UX thinking together.

This is the first project I built completely on my own, without following a tutorial step-by-step.

## Dataset
### Source: 
Kaggle – Food Ingredients and Recipe Dataset with Images

### Contents:

1. Recipe names
2. Ingredients
3. Instructions
4. Recipe images
5. Cleaned Ingredients

### ⚠️ Important challenge:
The dataset did not provide structured ingredient quantities or units.
All quantities and units were embedded inside unstructured instruction text.

To make the dashboard more insightful, additional attributes (nutrition, difficulty, cuisine, cost, ratings) were synthetically created purely for visualization and storytelling purposes.

## Data Cleaning & Feature Engineering

A major part of this project involved structuring unstructured text data.

### Key steps performed using Python & Power Query:

1. Parsed recipe instructions to extract ingredients

2. Identified and separated:
    1. Ingredient name
    2. Quantity
    3. Unit of measurement

3. Normalized ingredient names (e.g., spelling & formatting)

4. Created separate columns for:
   1. Ingredient
   2. Quantity
   3. Unit

5. Generated unique IDs for recipes and ingredients
6. Removed duplicates and inconsistencies

7. Curated a clean subset of recipes for focused analysis

👉 This step transformed raw text data into an analytical-ready fact table, enabling proper data modeling and visualization.

## Data Modeling (Star Schema)
The model follows a star schema for performance and clarity:
### Dimension Tables

1. dim_recipes – recipe metadata + image URLs

2. dim_ingredients – normalized ingredient names

3. dim_recipe_attributes – nutrition, cuisine, difficulty, cost

### Fact Table

1. fact_ingredients – recipe-ingredient relationships with quantities

### This structure enables:

1. Drill-through between pages

2. Flexible filtering

3. Clean DAX measures

## Dataset Scope Decision

The original dataset contained approximately 13,000 recipes.
For this project, I cleaned and structured the full dataset, but intentionally selected 10 representative recipes for the final dashboard to:
1. Improve dashboard performance
2. Maintain visual clarity
3. Focus on UX and storytelling rather than scale alone

The project architecture supports scaling to the full dataset if required.

## Dashboard Features
### 🔹 Page 1 – Recipe Explorer

   1. Magazine-style layout

   2. Recipe cards with images & titles

   3. Interactive preview card

   4. Drill-through button to detailed view

### 🔹 Page 2 – Recipe Details

   1. Large recipe image & title

   2. Ingredient list with quantities

   3. Nutritional breakdown (donut chart)

   4. Cuisine, difficulty, cost indicators

   5. Ratings visualization

### 🔹 Interactivity

   1. Drill-through navigation
   2. Cross-filtering
   3. Dynamic visuals based on recipe selection

## Tools & Skills Used
### Tools
1. Power BI Desktop
2. Python (for data cleaning)
3. Git & GitHub
4. VS Code
### Skills Demonstrated
1. Data cleaning & transformation
2. Star schema data modeling
3. DAX measures
4. Drill-through & conditional navigation
5. Dashboard UX & layout design
6. Image handling in Power BI
7. End-to-end BI project execution

## Future Improvements
1. Add real nutritional data
2. Weekly meal planning functionality
3. Grocery list generation
## 🙌 Acknowledgements

Kaggle community for the dataset

Power BI & data visualization community for inspiration

⭐ If you found this project interesting, feel free to star the repository!
