import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

SECTORS_API_KEY = os.getenv("SECTORS_API_KEY")

headers = {"Authorization": SECTORS_API_KEY}

banks = ["BBRI", "BMRI", "BBCA", "BBNI", "BRIS"]
base_url = "https://api.sectors.app/v1/company/report/"


def fetch_data(url):
    """
    Fetches the data from the specified URL and returns it as a JSON object.
    We created this from the get_info function in the previous chapter (API programming)
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": "An error occurred while fetching the data."}


def create_df(banks, save_to_csv=False, file_name="indonesia_banks.csv"):
    """
    Creates a DataFrame by fetching data from the API for each bank in the list.

    Parameters:
    - banks: List of bank identifiers.
    - save_to_csv: Boolean flag to indicate if the DataFrame should be saved to a CSV file.
    - csv_file_name: Name of the CSV file to save the DataFrame (default is "data.csv").

    Returns:
    - DataFrame with valuation data from banks of Indonesia
    """
    df_list = []

    for bank in banks:
        url = f"{base_url}{bank}/?sections=valuation"
        response = fetch_data(url)

        if "error" not in response:
            df = pd.json_normalize(response)
            if "valuation.historical_valuation" in df.columns:
                historical_df = pd.json_normalize(
                    df["valuation.historical_valuation"].explode()
                )
                historical_df["symbol"] = df["symbol"][0]
                historical_df["company_name"] = df["company_name"][0]
                historical_df = historical_df[
                    ["symbol", "company_name", "year", "pe", "pb", "ps"]
                ]
            # df["bank"] = bank
            df_list.append(historical_df)
        else:
            print(f"Error fetching data for {bank}")

    if not df_list:
        joined = pd.DataFrame()
    else:
        joined = pd.concat(df_list, ignore_index=True)

    if save_to_csv:
        joined.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")
    return joined


df = create_df(banks, save_to_csv=True, file_name="datasets/indonesia_banks_050824.csv")
print(df.tail())
