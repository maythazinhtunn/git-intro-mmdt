import pandas as pd
import requests

# Constants
COVID_DATA_URL = "https://raw.githubusercontent.com/owid/covid-19-data/refs/heads/master/public/data/latest/owid-covid-latest.json"
CITIES_DATA_URL = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/refs/heads/master/json/cities.json"

def fetch_json_data(url):
    """Fetch JSON data from a given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad responses (e.g., 404)
    return response.json()

def process_covid_data(raw_data):
    """Convert COVID-19 JSON data into a DataFrame."""
    country_dataframes = [
        pd.json_normalize(data).assign(iso_country_code=country_code)
        for country_code, data in raw_data.items()
    ]
    return pd.concat(country_dataframes, ignore_index=True)

def print_dataset_summary(name, df):
    """Print summary of a dataset."""
    print(f"\n{name} Summary:")
    print(df.head(), "\n")
    print("Columns:", df.columns.tolist())
    print("Shape:", df.shape, "\n")

def main():
    # Fetch data
    covid_raw_data = fetch_json_data(COVID_DATA_URL)
    cities_raw_data = fetch_json_data(CITIES_DATA_URL)

    # Convert to DataFrames
    cities_df = pd.DataFrame(cities_raw_data)
    covid_df = process_covid_data(covid_raw_data)

    # Print dataset summaries
    for name, df in [("COVID Data", covid_df), ("Cities Data", cities_df)]:
        print_dataset_summary(name, df)

    # Merge datasets on country name
    merged_df = pd.merge(cities_df, covid_df, left_on='country_name', right_on='location', how='inner')

    # Print merged dataset summary
    print_dataset_summary("Merged Data", merged_df)

if __name__ == "__main__":
    main()