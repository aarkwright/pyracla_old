from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector


class EMAGSpider(Spider):
    name = "emag"

    allowed_domains = ["emag.ro"]
    urls = ["http://www.emag.ro/placi_video/c"]

    def start_requests(self):
        for url in self.urls:
            yield Request(url, callback=self.parse_menu)

    def parse_product(self, reponse):
        pass

    def parse_menu(self, response):

        categs = response.xpath('//nav[@id = "emg-mega-menu"]/ul/li/div/div/div[@class = "emg-megamenu-column"]/a[@class = "emg-megamenu-link"][not(a/@class="emg-megamen-link.is-heading")]')

        # href for first (Laptopuri) element:
        for categ in categs:
            categ.xpath('@href')

        # get categories
        navbar = response.css("div.emg-top-menu.emg-fluid-top-menu nav")
        categs = navbar.css("ul li")


        # Get the correct next page indicator
        for _e in response.css("div.emg-pagination-box a.emg-icon-holder"):
            if len(_e.css("span.icon-i44-go-right").extract()) == 1:  # should be only one Next page indicator.
                next_page = _e.css("::attr(href)").extract_first()
            else:
                next_page = None  # end of the line

        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield Request(next_page, callback=self.parse_menu)  # , dont_filter=False)
