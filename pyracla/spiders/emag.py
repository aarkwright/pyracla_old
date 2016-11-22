import scrapy


class QuotesSpider(scrapy.Spider):
    name = "emag"

    allowed_domains = ["craigslist.org"]
    start_urls = ['www.emag.ro/placi_video/c']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item, price in response.css("div.product-holder-grid form.inner-form"), response.css("div.product-holder-grid form.inner-form div.bottom-container div.pret-produs-listing"):
            yield {
                'title': item.css('div.middle-container h2 a::text').extract_first().strip(),
                'price_ron': '%i.%i' % (price.css("span.price-over span.money-int::text").extract_first().strip(),
                                        price.css("span.price-over span.money-decimal::text").extract_first().strip()),
            }
