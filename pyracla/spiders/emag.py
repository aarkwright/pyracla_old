import scrapy


class EMAGSpider(scrapy.Spider):
    name = "emag"

    allowed_domains = ["emag.ro"]
    start_urls = ["http://www.emag.ro/placi_video/c"]

    def parse(self, response):
        for item in response.css("div.product-holder-grid form.inner-form"):
            yield {
                'title': item.css("div.middle-container h2 a::text").extract_first(),
                'price_ron': '{}.{:2d}ron'.format(int(item.css("div.bottom-container div.pret-produs-listing span.price-over span.money-int::text").extract_first().replace(".", "")),
                                        int(item.css("div.bottom-container div.pret-produs-listing span.price-over span.money-decimal::text").extract_first())),
            }
