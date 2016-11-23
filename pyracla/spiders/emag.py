from scrapy.spiders import Spider
from scrapy.http import Request


class EMAGSpider(Spider):
    name = "emag"

    allowed_domains = ["emag.ro"]
    url = "http://www.emag.ro/placi_video/c"

    def start_requests(self):
        yield Request(self.url, callback=self.parse)

    def parse(self, response):
        for item in response.css("div.product-holder-grid form.inner-form"):
            yield {
                'title': item.css("div.middle-container h2 a::text").extract_first().strip(),
                'price_ron': float('{}.{}'.format(
                    item.css(
                        "div.bottom-container div.pret-produs-listing span.price-over span.money-int::text").extract_first().replace(
                        ".", ""),
                    item.css(
                        "div.bottom-container div.pret-produs-listing span.price-over sup.money-decimal::text").extract_first())),
            }

        next_page = response.css("div.emg-pagination-box a.emg-icon-holder::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield Request(next_page, callback=self.parse) #, dont_filter=False)
