import time
import pandas as pd
import pycountry
import matplotlib.pyplot as plt
import seaborn as sns

# Start timing the entire process
start_time = time.time()

# Step 1: Load datasets
load_start = time.time()
spotify_df = pd.read_csv("universal_top_spotify_songs.csv")
age_df = pd.read_csv("MedianAge.csv")
load_end = time.time()
print(f"Time to load datasets: {load_end - load_start:.2f} seconds")

# Step 2: Convert country codes to names using pycountry
convert_start = time.time()
def code_to_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return None  # Handle invalid or missing codes

spotify_df["country_name"] = spotify_df["country"].apply(code_to_name)
convert_end = time.time()
print(f"Time to convert country codes: {convert_end - convert_start:.2f} seconds")

# Step 3: Calculate average tempo per country
tempo_start = time.time()
avg_tempo_per_country = spotify_df.groupby("country_name")["tempo"].mean().reset_index()
tempo_end = time.time()
print(f"Time to calculate average tempo: {tempo_end - tempo_start:.2f} seconds")

# Step 4: Extract most recent average age (2025)
age_start = time.time()
age_df["average_age"] = age_df["2025"]
age_df = age_df[["Country", "average_age"]]
age_end = time.time()
print(f"Time to extract average age: {age_end - age_start:.2f} seconds")

# Step 5: Merge datasets
merge_start = time.time()
merged_df = pd.merge(avg_tempo_per_country, age_df, left_on="country_name", right_on="Country")
merge_end = time.time()
print(f"Time to merge datasets: {merge_end - merge_start:.2f} seconds")

# Step 6: Calculate deviation (difference between tempo and age)
deviation_start = time.time()
merged_df["deviation"] = merged_df["tempo"] - merged_df["average_age"]
deviation_end = time.time()
print(f"Time to calculate deviation: {deviation_end - deviation_start:.2f} seconds")

# Step 7: Plot the results
plot_start = time.time()

# Set the style for the plots
sns.set(style="whitegrid")

# Scatter Plot: Average Age vs. Average Tempo
plt.figure(figsize=(10, 6))
sns.scatterplot(x="average_age", y="tempo", data=merged_df, hue="country_name", s=100, palette="viridis")
plt.title("Average Age vs. Average Tempo by Country", fontsize=16)
plt.xlabel("Average Age (2025)", fontsize=12)
plt.ylabel("Average Tempo (BPM)", fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")  # Move legend outside the plot
plt.tight_layout()

# Bar Chart: Deviation (Tempo - Age) by Country
plt.figure(figsize=(12, 6))
sns.barplot(x="country_name", y="deviation", data=merged_df, palette="coolwarm")
plt.title("Deviation (Tempo - Average Age) by Country", fontsize=16)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Deviation (Tempo - Age)", fontsize=12)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Stop timing before showing the plots
plot_end = time.time()
print(f"Time to generate plots: {plot_end - plot_start:.2f} seconds")

# End timing the entire process (before plots are displayed)
end_time = time.time()
print(f"\nTotal execution time (excluding plot display): {end_time - start_time:.2f} seconds")

# Show the plots
plt.show()