import requests

class Brewery:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.brewery_type = data.get('brewery_type')
        self.city = data.get('city')
        self.state = data.get('state')
        self.website_url = data.get('website_url')

    def has_website(self):
        return bool(self.website_url)

class BreweryAPI:
    BASE_URL = 'https://api.openbrewerydb.org/breweries'

    def __init__(self):
        self.session = requests.Session()

    def fetch_by_state(self, state, per_page=50):
        breweries = []
        page = 1
        while True:
            params = {'by_state': state, 'per_page': per_page, 'page': page}
            resp = self.session.get(self.BASE_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            if not data:
                break
            breweries.extend(Brewery(item) for item in data)
            page += 1
        return breweries

class BreweryAnalyzer:
    def __init__(self, breweries):
        self.breweries = breweries

    def list_names(self):
        return [b.name for b in self.breweries]

    def count(self):
        return len(self.breweries)

    def type_counts_by_city(self):
        city_types = {}
        for b in self.breweries:
            city_types.setdefault(b.city, {})
            city_types[b.city].setdefault(b.brewery_type, 0)
            city_types[b.city][b.brewery_type] += 1
        return city_types

    def breweries_with_websites(self):
        return [b for b in self.breweries if b.has_website()]

if __name__ == '__main__':
    states = ['alaska', 'maine', 'new_york']
    api = BreweryAPI()

    for state in states:
        breweries = api.fetch_by_state(state)
        analyzer = BreweryAnalyzer(breweries)

        # 1) List names
        print(f"\nBreweries in {state.title()}")
        for name in analyzer.list_names():
            print(f" - {name}")

        # 2) Count
        print(f"Total breweries in {state.title()}: {analyzer.count()}")

        # 3) Types by city
        print(f"Brewery types by city in {state.title()}: ")
        for city, types in analyzer.type_counts_by_city().items():
            print(f" {city}:")
            for t, cnt in types.items():
                print(f"    {t}: {cnt}")

        # 4) With websites
        with_sites = analyzer.breweries_with_websites()
        print(f"Breweries with websites in {state.title()} ({len(with_sites)}):")
        for b in with_sites:
            print(f" - {b.name}: {b.website_url}")
