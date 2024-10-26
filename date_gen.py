import requests
import json
from datetime import datetime, timedelta

# Define the years and base URL
start_year = 2024
end_year = 2030
base_url = "https://craigchamberlain.github.io/moon-data/api/moon-phase-data/{year}/"

# Initialize dictionary to hold new moon dates
new_moons = {}

# Loop through each year
for year in range(start_year, end_year + 1):
    # Fetch data from the API
    url = base_url.format(year=year)
    response = requests.get(url)
    
    # Check for successful request
    if response.status_code == 200:
        moon_data = response.json()
        # Filter new moon data (Phase 0)
        new_moon_dates = [entry["Date"] for entry in moon_data if entry["Phase"] == 0]
        
        # Store new moon dates for each year
        new_moons[year] = {}
        
        # Process each new moon date
        for new_moon_date in new_moon_dates:
            # Convert to datetime object for manipulation
            date_obj = datetime.fromisoformat(new_moon_date)
            date_str = date_obj.strftime("%Y-%m-%d")
            
            # Create structured data for each new moon date
            new_moons[year][date_str] = {
                "day0": {"date": date_str},
                "day1": {"date": (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")},
                "day2": {"date": (date_obj + timedelta(days=2)).strftime("%Y-%m-%d")},
                "day3": {"date": (date_obj + timedelta(days=3)).strftime("%Y-%m-%d")}
            }
    else:
        print(f"Failed to fetch data for year {year}. Status code: {response.status_code}")

# Save data to new_moons.json
with open("new_moons.json", "w") as json_file:
    json.dump(new_moons, json_file, indent=4)

print("New moon dates saved to new_moons.json")
