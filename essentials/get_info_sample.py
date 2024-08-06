import os
from typing import Dict, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

SECTORS_API_KEY = os.getenv("SECTORS_API_KEY")

headers = {"Authorization": SECTORS_API_KEY}


def get_info(stock: str, section: Optional[str] = None) -> Dict:
    """
    Fetches the report for a specified stock and section.

    :param stock: The stock ticker symbol (e.g., 'BBRI').
    :param section:  The section of the report to retrieve (e.g., 'financials').
                   If not specified, defaults to None. Can be a comma-separated list of sections.
    :return: A dictionary containing the response JSON data.
    """
    assert len(stock) == 4, "Stock symbol must be 4 characters long"

    url = f"https://api.sectors.app/v1/company/report/{stock}/"
    if section:
        valid_sections = [
            "overview",
            "valuation",
            "future",
            "peers",
            "financials",
            "dividend",
            "management",
            "ownership",
        ]

        sections = section.split(",")
        # Assert that all sections in the list are valid
        invalid_sections = [sec for sec in sections if sec not in valid_sections]
        assert (
            not invalid_sections
        ), f"Invalid sections: {', '.join(invalid_sections)}. Must be one of {valid_sections}."

        url += f"?sections={section}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": "An error occurred while fetching the data."}


response = get_info("BBRI", "financials")
response2 = get_info("BMRI")
print(response)
print(response2["overview"])
