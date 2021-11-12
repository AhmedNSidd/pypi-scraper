import scrapy
import json

from scrapy_splash import SplashRequest
from pypi.items import ProjectItem

class PypiSpider(scrapy.Spider):
    name = 'pypispider'

    def start_requests(self):
        with open('/Users/ahmedsiddiqui/Desktop/Workspace/UVic/Fall_2021/SENG480B/pypi-scraper/data/all_egg_names_downloads.json',) as f:
            data = json.load(f)
            for row in data['projects']:
                yield scrapy.Request(
                    url=f'https://pypi.org/project/{row["egg_name"]}/',
                    callback=self.parse,
                    cb_kwargs=dict(download_count=row["egg_downloads"])
                )

    def parse(self, response, download_count):
        project_item = {'owners': [], 'owners_urls': []}
        project_item['name'] = response.url.split('/')[-2]
        # We don't really need the url to the egg but I'm leaving the code in here in case we need it later.
        # project_item['url'] = response.url
        # We don't really need the description but I'm leaving the code in here in case we need it later. 
        # project_item['description'] = response.xpath('//p[@class="package-description__summary"]/text()').get()
        project_item['downloads'] = download_count
        maintainers = response.xpath('(//span[@class="sidebar-section__maintainer"])[1]/../span/a')
        for maintainer in maintainers:
            project_item['owners_urls'].append(response.urljoin(maintainer.xpath('./@href').get()))
            project_item['owners'].append(maintainer.xpath('./@aria-label').get())

        # get the release date
        min_year = 9999
        dates = response.xpath('//p[@class="release__version-date"]/time/text()').getall()
        for date in dates:
            date = date.strip()
            year = int(date[-4:])
            min_year = year if min_year > year else min_year
        
        project_item['release_year'] = min_year

        yield ProjectItem(**project_item)
