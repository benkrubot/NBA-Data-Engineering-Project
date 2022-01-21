import requests
from bs4 import BeautifulSoup
import json
import time
import csv


class ZillowScraper():
    results = []
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-encoding': 'gzip, deflate, br',
      'accept-language': 'en-US,en;q=0.9',
      'cache-control': 'max-age=0',
      'cookie': 'JSESSIONID=EB571A07AC44E3ED6227B7CFAA68701E; zguid=23|%24b4060a78-3c1b-4157-8a5c-33990a0e7a9e; zgsession=1|ebe51709-ab45-40e3-add7-b4f04099cac0; g_state={"i_p":1642760836536,"i_l":1}; G_ENABLED_IDPS=google; AWSALB=cJ4NTgpP9u6/j9MS3N5/bPVRUErz8XNsot4hmJXn9Z/G4B+/9DM4LRSXoHNiu6hwfzltxoybXBMFlvcuNjA1bNmEXBIi1ILNkW7tbglEoMH6GFUDJcNwKKg/Gu7x; AWSALBCORS=cJ4NTgpP9u6/j9MS3N5/bPVRUErz8XNsot4hmJXn9Z/G4B+/9DM4LRSXoHNiu6hwfzltxoybXBMFlvcuNjA1bNmEXBIi1ILNkW7tbglEoMH6GFUDJcNwKKg/Gu7x; search=6|1645345917630%7Crect%3D45.2222507158421%252C-122.44966763085938%252C44.581624651472396%252C-123.52907436914063%26rid%3D20317%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26fs%3D0%26fr%3D1%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26excludeNullAvailabilityDates%3D0%09%0920317%09%09%09%09%09%09',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14150.87.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.124 Safari/537.36',
}
  




    def fetch(self, url, params):
            response = requests.get(url, headers=self.headers, params=params)
            print(response.status_code)
            return response

    def parse(self, response):
        content = BeautifulSoup(response, 'lxml')
        deck = content.find('ul', {'class': 'photo-cards photo-cards_wow photo-cards_short'})
        for card in deck.contents:
            script = card.find('script', {'type': 'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])

                self.results.append({
                    'latitude': script_json['geo']['latitude'],
                    'longitude': script_json['geo']['longitude'],
                    'floorSize': script_json['floorSize']['value'],
                    'url': script_json['url'],
                    'price': card.find('div', {'class': 'list-card-price'}).text
                })

    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def run(self):
        url = 'https://www.zillow.com/salem-or/rentals'

        for page in range(1, 13):
            params = {
                'searchQueryState': '{"pagination":{"currentPage": %s},"mapBounds":{"west":-123.52907436914063,"east":-122.44966763085938,"south":44.581624651472396,"north":45.2222507158421},"regionSelection":[{"regionId":20317,"regionType":6}],"isMapVisible":false,"filterState":{"fsba":{"value":false},"fsbo":{"value":false},"nc":{"value":false},"fore":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"fr":{"value":true},"ah":{"value":true}},"isListVisible":true}' %page
            }
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv()


if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()
