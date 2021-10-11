import scrapy

from scrapy_splash import SplashRequest
from pypi.items import ProjectItem

class PypiSpider(scrapy.Spider):
    name = 'pypispider'
    start_urls = ['https://pypi.org/search/?q=&o=&c=Topic+%3A%3A+Scientific%2FEngineering']

    # https://pepy.tech/project/{project_name} is useful for seeing download statistics

    def parse(self, response):
        project_list_items = response.xpath('//div[@class="left-layout__main"]/form/div/ul/li')
        for project in project_list_items:
            link = project.xpath('.//a/@href').get() # get the link from the list item
            yield scrapy.Request(response.urljoin(link), self.project_page_parser)

        next_page_link = response.xpath('//div[contains(@class, "button-group--pagination")]//a[contains(text(), "Next")]/@href').get()
        if next_page_link:
            yield scrapy.Request(response.urljoin(next_page_link), self.parse)

    def project_page_parser(self, response):
        project_item = {'owners': [], 'owners_urls': []}
        project_item['name'] = response.url.split('/')[-2]
        project_item['url'] = response.url
        project_item['description'] = response.xpath('//p[@class="package-description__summary"]/text()').get()
        maintainers = response.xpath('(//span[@class="sidebar-section__maintainer"])[1]/../span/a')
        for maintainer in maintainers:
            project_item['owners_urls'].append(response.urljoin(maintainer.xpath('./@href').get()))
            project_item['owners'].append(maintainer.xpath('./@aria-label').get())

        yield SplashRequest(f'https://pepy.tech/project/{project_item["name"]}/',
                            self.project_downloads_parser,
                            args={'wait': 5.5},
                            cb_kwargs=dict(project_item=project_item))

    def project_downloads_parser(self, response, project_item):
        project_item['downloads'] = int(response.xpath('//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6"]/text()').get())
        yield ProjectItem(**project_item)