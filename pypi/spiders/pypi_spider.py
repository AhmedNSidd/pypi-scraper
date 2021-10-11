import scrapy
import json

from scrapy_splash import SplashRequest
from pypi.items import ProjectItem

class PypiSpider(scrapy.Spider):
    name = 'pypispider'

    def start_requests(self):
        with open('/Users/ahmedsiddiqui/Desktop/Workspace/UVic/Fall_2021/SENG480B/pypi-scraper/data/top-pypi-packages.json',) as f:
            data = json.load(f)
            for row in data['rows']:
                yield scrapy.Request(
                    url=f'https://pypi.org/project/{row["project"]}/',
                    callback=self.parse,
                    cb_kwargs=dict(download_count=row["download_count"])
                )

    def parse(self, response, download_count):
        project_item = {'owners': [], 'owners_urls': []}
        project_item['name'] = response.url.split('/')[-2]
        project_item['url'] = response.url
        project_item['description'] = response.xpath('//p[@class="package-description__summary"]/text()').get()
        project_item['downloads'] = download_count
        maintainers = response.xpath('(//span[@class="sidebar-section__maintainer"])[1]/../span/a')
        for maintainer in maintainers:
            project_item['owners_urls'].append(response.urljoin(maintainer.xpath('./@href').get()))
            project_item['owners'].append(maintainer.xpath('./@aria-label').get())

        yield ProjectItem(**project_item)
