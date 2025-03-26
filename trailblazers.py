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
