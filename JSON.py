import requests

class CountryCurrencyInfo:
    def __init__(self, url):
        self.url = url
        self.data = None  # to store the fetched data

    def fetch_data(self):
        """Fetch JSON data from the given API URL"""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.data = response.json()
            print("Data fetched successfully.")
        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)

    def display_country_currency_info(self):
        """Display country name, currency names, and symbols"""
        if not self.data:
            print("No data to display. Please fetch data first.")
            return

        for country in self.data:
            name = country.get("name", {}).get("common", "N/A")
            currencies = country.get("currencies", {})
            currency_info = []

            for code, info in currencies.items():
                currency_name = info.get("name", "N/A")
                symbol = info.get("symbol", "N/A")
                currency_info.append(f"{currency_name} ({symbol})")

            print(f"{name}: {', '.join(currency_info)}")

    def display_countries_with_currency(self, currency_name_filter):
        """Display countries that use a specific currency (case-insensitive match)"""
        if not self.data:
            print("No data to filter. Please fetch data first.")
            return

        print(f"\nCountries using currency: {currency_name_filter.upper()}")
        found = False
        for country in self.data:
            name = country.get("name", {}).get("common", "N/A")
            currencies = country.get("currencies", {})
            for code, info in currencies.items():
                currency_name = info.get("name", "").lower()
                if currency_name_filter.lower() in currency_name:
                    print(name)
                    found = True
                    break
        if not found:
            print(f"No countries found using {currency_name_filter}.")

    def display_dollar_countries(self):
        """Display countries using any form of Dollar currency"""
        self.display_countries_with_currency("dollar")

    def display_euro_countries(self):
        """Display countries using Euro currency"""
        self.display_countries_with_currency("euro")


# Usage
if __name__ == "__main__":
    url = "https://restcountries.com/v3.1/all"
    country_info = CountryCurrencyInfo(url)

    country_info.fetch_data()
    country_info.display_country_currency_info()
    country_info.display_dollar_countries()
    country_info.display_euro_countries()
