import pandas as pd
import random

# Preload dataset
df = pd.read_csv('blockchain_app/final_indian_food_cleaned.csv')

# Basic cleaning
df.fillna(df.median(numeric_only=True), inplace=True)
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)

# Standardize Veg/NonVeg
df['VegNovVeg'] = df['VegNovVeg'].str.lower().str.strip()

# High sugar foods and deep fried foods (for diabetes filtering)
high_sugar_foods = [
    'gulab jamun', 'jalebi', 'rasgulla', 'kaju katli', 'barfi', 'laddu',
    'soan papdi', 'chum chum', 'sandesh', 'halwa', 'kheer', 'payasam', 'sheer khurma',
    'chocolate', 'ice cream'
]
deep_fried_foods = [
    'samosa', 'kachori', 'pakora', 'bhatura', 'vada', 'poori', 'bhaji', 'fried chicken',
    'fish fry', 'aloo tikki'
]

# --- Helper Functions ---

def filter_veg(df, diet_preference):
    """Filter only vegetarian items if required."""
    if diet_preference == "veg":
        df = df[df['VegNovVeg'] == 'veg']
    return df

def filter_hba1c_friendly(df, has_diabetes):
    """Filter out high-sugar and deep-fried foods if diabetic."""
    if has_diabetes == "yes":
        df = df[~df['Food_items'].str.lower().isin(high_sugar_foods + deep_fried_foods)]
    return df

def check_curry_or_dal(meal, meal_type):
    """Ensure lunch/dinner has at least one curry or dal."""
    curry_or_dal_keywords = ['curry', 'dal', 'gravy', 'masala', 'korma', 'sambar']
    if meal_type.lower() in ["lunch", "dinner"]:
        has_curry_or_dal = any(
            any(keyword in item.lower() for keyword in curry_or_dal_keywords)
            for item in meal
        )
        if not has_curry_or_dal:
            # Add a random curry or dal if not already present
            curry_or_dal_items = df[df['Food_items'].str.lower().str.contains('|'.join(curry_or_dal_keywords))]['Food_items'].tolist()
            if curry_or_dal_items:
                meal.append(random.choice(curry_or_dal_items))
    return meal

# --- Main Function Called from views.py ---

def generate_diet_plan_from_input(age, diet_preference, weight, height, goal, has_diabetes):
    """
    Generate a 7-day diet plan based on user input.
    """
    # Apply filters
    filtered_df = df.copy()
    filtered_df = filter_veg(filtered_df, diet_preference)
    filtered_df = filter_hba1c_friendly(filtered_df, has_diabetes)

    # Day names
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Final Diet Plan
    diet_plan = {}

    for day in day_names:
        day_plan = {}

        # Breakfast
        breakfast_options = filtered_df[filtered_df['Breakfast'] == 1]['Food_items'].tolist()
        if len(breakfast_options) >= 3:
            day_plan['Breakfast'] = random.sample(breakfast_options, 3)
        else:
            day_plan['Breakfast'] = breakfast_options

        # Lunch
        lunch_options = filtered_df[filtered_df['Lunch'] == 1]['Food_items'].tolist()
        if len(lunch_options) >= 3:
            lunch = random.sample(lunch_options, 3)
        else:
            lunch = lunch_options
        lunch = check_curry_or_dal(lunch, "Lunch")
        day_plan['Lunch'] = lunch

        # Dinner
        dinner_options = filtered_df[filtered_df['Dinner'] == 1]['Food_items'].tolist()
        if len(dinner_options) >= 3:
            dinner = random.sample(dinner_options, 3)
        else:
            dinner = dinner_options
        dinner = check_curry_or_dal(dinner, "Dinner")
        day_plan['Dinner'] = dinner

        diet_plan[day] = day_plan

    return diet_plan
