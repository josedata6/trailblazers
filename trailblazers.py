import pandas as pd

# Load the conjoint data from the CSV file
file_path = "Portland_Trail_Blazers.csv"
df = pd.read_csv(file_path)

# Display the first few rows (optional)
print(df.head())

# Define the attribute groups
attributes = {
    "Game Package": ['3-game', '6-game', '10-game'],
    "Price": ['$15 Per Seat Per Game', '$25 Per Seat Per Game', '$35 Per Seat Per Game', '$60 Per Seat Per Game'],
    "Seat Location": ['300 Behind the Baskets', '300 Corner', '300 Midcourt', '200 Midcourt'],
    "Promotion": ['Priority Playoff Tickets', 'Hot Dog and Soda', 'Trail Blazers Apparel', '$20 Gift Certificiate', 'No Promotion']
}

# Calculate the range for each attribute group
attribute_ranges = {}
for attr, cols in attributes.items():
    values = df[cols].iloc[0]
    attribute_ranges[attr] = values.max() - values.min()

# Convert to DataFrame and calculate importance percentages
importance_df = pd.DataFrame.from_dict(attribute_ranges, orient='index', columns=['Utility Range'])
importance_df['Importance %'] = 100 * importance_df['Utility Range'] / importance_df['Utility Range'].sum()
importance_df.sort_values(by='Importance %', ascending=False, inplace=True)

# Show the result
print("\nAttribute Importance:\n")
print(importance_df)

####################################################################################################
#################### bar chart showing the importance of each attribute ############################

import pandas as pd
import matplotlib.pyplot as plt

# Load the conjoint data
file_path = "Portland_Trail_Blazers.csv"
df = pd.read_csv(file_path)

# Define the attribute groups
attributes = {
    "Game Package": ['3-game', '6-game', '10-game'],
    "Price": ['$15 Per Seat Per Game', '$25 Per Seat Per Game', '$35 Per Seat Per Game', '$60 Per Seat Per Game'],
    "Seat Location": ['300 Behind the Baskets', '300 Corner', '300 Midcourt', '200 Midcourt'],
    "Promotion": ['Priority Playoff Tickets', 'Hot Dog and Soda', 'Trail Blazers Apparel', '$20 Gift Certificiate', 'No Promotion']
}

# Calculate the range (max - min utility) for each attribute
attribute_ranges = {}
for attr, cols in attributes.items():
    values = df[cols].iloc[0]
    attribute_ranges[attr] = values.max() - values.min()

# Create a DataFrame to show relative importance
importance_df = pd.DataFrame.from_dict(attribute_ranges, orient='index', columns=['Utility Range'])
importance_df['Importance %'] = 100 * importance_df['Utility Range'] / importance_df['Utility Range'].sum()
importance_df.sort_values(by='Importance %', ascending=False, inplace=True)

# Plot the importance bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(importance_df.index, importance_df['Importance %'], color='orange')
plt.title('Attribute Importance in Ticket Package Attractiveness')
plt.ylabel('Importance (%)')
plt.xlabel('Attribute')
plt.xticks(rotation=45)

# Add percentage labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.1f}%', ha='center', va='bottom')

plt.tight_layout()
plt.show()

###########################################################
# Generate seat location and price utility combinations
price_cols = ['$15 Per Seat Per Game', '$25 Per Seat Per Game', '$35 Per Seat Per Game', '$60 Per Seat Per Game']
location_cols = ['300 Behind the Baskets', '300 Corner', '300 Midcourt', '200 Midcourt']

price_utils = df[price_cols].iloc[0]
location_utils = df[location_cols].iloc[0]

recommendations = []
for location in location_cols:
    for price in price_cols:
        total_utility = location_utils[location] + price_utils[price]
        recommendations.append({
            'Seat Location': location,
            'Price': price,
            'Total Utility': total_utility
        })

# Create a DataFrame sorted by utility (descending)
recommendations_df = pd.DataFrame(recommendations).sort_values(by='Total Utility', ascending=False)

# Display recommendation table
print("\nPrice Recommendations (Ranked by Total Utility):\n")
print(recommendations_df.to_string(index=False))

####################################################################################################
################### Should the Trail Blazers Raise/Lower Prices?


import pandas as pd

# Load the conjoint data
df = pd.read_csv("Portland_Trail_Blazers.csv")

# Define utilities
price_utils = df[['$15 Per Seat Per Game', '$25 Per Seat Per Game', '$35 Per Seat Per Game', '$60 Per Seat Per Game']].iloc[0]
location_utils = df[['300 Behind the Baskets', '300 Corner', '300 Midcourt', '200 Midcourt']].iloc[0]

# Define actual combos from the question
actual_combos = [
    {'Seat Location': '300 Behind the Baskets', 'Price': '$15 Per Seat Per Game'},
    {'Seat Location': '300 Corner', 'Price': '$25 Per Seat Per Game'},
    {'Seat Location': '300 Midcourt', 'Price': '$35 Per Seat Per Game'},
    {'Seat Location': '200 Midcourt', 'Price': '$60 Per Seat Per Game'},
]

# Calculate total utility for given combos
for combo in actual_combos:
    loc = combo['Seat Location']
    price = combo['Price']
    combo['Total Utility'] = location_utils[loc] + price_utils[price]

# Compare to all other combos to estimate price headroom
all_prices = ['$15 Per Seat Per Game', '$25 Per Seat Per Game', '$35 Per Seat Per Game', '$60 Per Seat Per Game']
all_locations = ['300 Behind the Baskets', '300 Corner', '300 Midcourt', '200 Midcourt']

all_combos = []
for loc in all_locations:
    for price in all_prices:
        total_utility = location_utils[loc] + price_utils[price]
        all_combos.append({
            'Seat Location': loc,
            'Price': price,
            'Total Utility': total_utility
        })

all_df = pd.DataFrame(all_combos).sort_values(by='Total Utility', ascending=False)
actual_df = pd.DataFrame(actual_combos).sort_values(by='Total Utility', ascending=False)

# Identify potential to raise/lower prices based on relative utility ranking
recommendations = []
for i, row in actual_df.iterrows():
    combo_utility = row['Total Utility']
    better_count = (all_df['Total Utility'] > combo_utility).sum()
    worse_count = (all_df['Total Utility'] < combo_utility).sum()
    midpoint = len(all_df) // 2
    action = 'Keep Price'
    if better_count <= midpoint / 2:
        action = 'Raise Price'
    elif worse_count <= midpoint / 2:
        action = 'Lower Price'
    recommendations.append({
        'Seat Location': row['Seat Location'],
        'Price': row['Price'],
        'Total Utility': round(combo_utility, 3),
        'Recommendation': action
    })

recommendations_df = pd.DataFrame(recommendations)
print("\n=== Price Adjustment Recommendations ===\n")
print(recommendations_df.to_string(index=False))

####################################################################################################
################### Should the Trail Blazers Change Promotions?

import pandas as pd

# Load the data
df = pd.read_csv("Portland_Trail_Blazers.csv")

# Extract the promo utility scores
promo_cols = [
    'Priority Playoff Tickets', 
    'Hot Dog and Soda', 
    'Trail Blazers Apparel', 
    '$20 Gift Certificiate', 
    'No Promotion'
]
promo_utils = df[promo_cols].iloc[0]

# Convert to DataFrame
promo_df = pd.DataFrame(promo_utils).reset_index()
promo_df.columns = ['Promotion Item', 'Utility']
promo_df = promo_df.sort_values(by='Utility', ascending=False)

# Calculate incremental utility compared to "No Promotion"
no_promo_utility = promo_utils['No Promotion']
promo_df['Incremental Utility'] = promo_df['Utility'] - no_promo_utility

# Recommend items with positive incremental utility
promo_df['Recommendation'] = promo_df['Incremental Utility'].apply(
    lambda x: 'Include (Free or Paid)' if x > 0 else 'Not Recommended'
)

# Display results
print("\n=== Promotional Item Utility Analysis ===\n")
print(promo_df.to_string(index=False))

####################################################################################################
############# heat map
import seaborn as sns
import matplotlib.pyplot as plt

# Prepare data for heatmap: we'll use a simple format where each row is a promo item and its incremental utility
heatmap_data = promo_df.set_index('Promotion Item')[['Incremental Utility']]

# Plot the heatmap
plt.figure(figsize=(8, 5))
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', linewidths=0.5, fmt=".3f", cbar_kws={'label': 'Incremental Utility'})
plt.title('Heatmap of Promotional Item Value (vs No Promotion)')
plt.xlabel('Promotion Value')
plt.ylabel('')
plt.tight_layout()
plt.show()
