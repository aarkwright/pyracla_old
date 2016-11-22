import scrapy


class EMAGSpider(scrapy.Spider):
    name = "emag"

    allowed_domains = ["emag.ro"]
    start_urls = ["http://www.emag.ro/placi_video/c"]

    def parse(self, response):
        for item in response.css("div.product-holder-grid"):
            yield {
                'title': item.css('form.inner-form div.middle-container h2 a::text').extract_first().strip(),
                'price_ron': '%i.%i' % (item.css("form.inner-form div.bottom-container div.pret-produs-listing span.price-over span.money-int::text").extract_first().strip(),
                                        item.css("form.inner-form div.bottom-container div.pret-produs-listing span.price-over span.money-decimal::text").extract_first().strip()),
            }
