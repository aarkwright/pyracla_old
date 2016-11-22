import scrapy


class EMAGSpider(scrapy.Spider):
    name = "emag"

    allowed_domains = ["emag.ro"]
    start_urls = ["http://www.emag.ro/placi_video/c"]

    def parse(self, response):
        top_level = response.css("div.product-holder-grid form.inner-form")
        for item, price in top_level.css("form.inner-form"), \
                           top_level.css("form.inner-form div.bottom-container div.pret-produs-listing"):
            yield {
                'title': item.css('div.middle-container h2 a::text').extract_first().strip(),
                'price_ron': '%i.%i' % (price.css("span.price-over span.money-int::text").extract_first().strip(),
                                        price.css("span.price-over span.money-decimal::text").extract_first().strip()),
            }
