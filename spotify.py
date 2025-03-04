import pandas as pd

df = pd.read_csv('universal_top_spotify_songs.csv')

df['tempo'] = pd.to_numeric(df['tempo'], errors='coerce')

# Calculate the average tempo per country
average_tempo_per_country = df.groupby('country')['tempo'].mean().reset_index()

average_tempo_per_country.columns = ['Country', 'Average Tempo']

print(average_tempo_per_country)

df = pd.read_csv('universal_top_spotify_songs.csv')

# Count the number of songs per country
songs_per_country = df['country'].value_counts().reset_index()

songs_per_country.columns = ['Country', 'Number of Songs']

# Display the result
print(songs_per_country)