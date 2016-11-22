import scrapy


class QuotesSpider(scrapy.Spider):
    name = "emag"

    def start_requests(self):
        urls = ['www.emag.ro/placi_video/c']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'emag-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
