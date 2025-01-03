import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from folium.plugins import HeatMap
import folium

# Load the dataset
data_path = './synthetic_traffic_accident_data.csv'  # Path to synthetic dataset
data = pd.read_csv(data_path)

# Display dataset information
print("Dataset Info:")
print(data.info())
print("\nFirst 5 Rows:")
print(data.head())

# Check for missing values
print("\nMissing Values:")
print(data.isnull().sum())

# Convert Start_Time to datetime format
data['Start_Time'] = pd.to_datetime(data['Start_Time'])

# Extract relevant time-based features
data['Hour'] = data['Start_Time'].dt.hour
data['Day_of_Week'] = data['Start_Time'].dt.day_name()
data['Month'] = data['Start_Time'].dt.month_name()

# Visualize Accident Frequency by Time of Day
plt.figure(figsize=(12, 6))
sns.countplot(x='Hour', data=data, order=range(0, 24))
plt.title('Accident Frequency by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Accidents')
plt.show()

# Visualize Accident Frequency by Day of the Week
plt.figure(figsize=(12, 6))
sns.countplot(x='Day_of_Week', data=data, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.title('Accident Frequency by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Accidents')
plt.show()

# Weather Condition Analysis
plt.figure(figsize=(12, 6))
weather_counts = data['Weather_Condition'].value_counts().head(10)
sns.barplot(x=weather_counts.values, y=weather_counts.index, palette='viridis')
plt.title('Top 10 Weather Conditions During Accidents')
plt.xlabel('Number of Accidents')
plt.ylabel('Weather Condition')
plt.show()

# Road Condition Analysis
plt.figure(figsize=(12, 6))
road_counts = data['Road_Condition'].value_counts().head(10)
sns.barplot(x=road_counts.values, y=road_counts.index, palette='coolwarm')
plt.title('Top 10 Road Conditions During Accidents')
plt.xlabel('Number of Accidents')
plt.ylabel('Road Condition')
plt.show()

# Accident Hotspots Visualization (Heatmap)
heatmap_data = data[['Start_Lat', 'Start_Lng']]
heatmap_map = folium.Map(location=[data['Start_Lat'].mean(), data['Start_Lng'].mean()], zoom_start=6)
HeatMap(heatmap_data.values, radius=10).add_to(heatmap_map)

# Save the map as HTML (optional)
heatmap_map.save('accident_hotspots.html')

# Clustering Accident Locations using KMeans
kmeans = KMeans(n_clusters=10, random_state=42)
data['Cluster'] = kmeans.fit_predict(data[['Start_Lat', 'Start_Lng']])

# Visualize Clusters on a Map
cluster_map = folium.Map(location=[data['Start_Lat'].mean(), data['Start_Lng'].mean()], zoom_start=6)
for _, row in data.iterrows():
    folium.CircleMarker(
        location=[row['Start_Lat'], row['Start_Lng']],
        radius=3,
        color=f'#{row["Cluster"] * 3:02x}{row["Cluster"] * 7:02x}ff',
        fill=True
    ).add_to(cluster_map)

# Save the cluster map as HTML (optional)
cluster_map.save('cluster_map.html')

# Summary Statistics
print("\nSummary Statistics:")
print(data.describe())

# Save cleaned data (optional)
data.to_csv('cleaned_synthetic_traffic_accident_data.csv', index=False)
