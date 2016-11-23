from scrapy.spiders import Spider
from scrapy.http import Request


class EMAGSpider(Spider):
    name = "emag"

    allowed_domains = ["emag.ro"]
    urls = ["http://www.emag.ro/"]

    def start_requests(self):
        for url in self.urls:
            yield Request(url, callback=self.parse_menu)

    def parse_menu(self, response):

        # Get all proper categories [no header categories]
        categs = response.xpath(
            '//nav[@id = "emg-mega-menu"]/ul/li/div/div/div[@class = "emg-megamenu-column"]/a[@class = "emg-megamenu-link"][not(a/@class="emg-megamen-link.is-heading")]')

        # Get link href for first (Laptopuri) element:
        #self.results = {}
        for categ in categs:
            category_name = categ.xpath('text()').extract_first()
            category_href = categ.xpath('@href').extract_first()
            products = yield Request(response.urljoin(category_href), callback=self.parse_categ)

            #results = {'name': category_name, 'link': category_href, 'products': products}

            yield {
                'name': category_name,
                'link': category_href,
                'products': products,
            }


    def parse_categ(self, response):

        products = response.xpath('//div[@class = "product-holder-grid"]/form[@class = "inner-form"]')

        for product in products:
            yield {
                'title': product.css("div.middle-container h2 a::text").extract_first().strip(),
                'price_ron': float('{}.{}'.format(product.css(
                    "div.bottom-container div.pret-produs-listing span.price-over span.money-int::text").extract_first().replace(
                    ".", ""), product.css(
                    "div.bottom-container div.pret-produs-listing span.price-over sup.money-decimal::text").extract_first())), }

        _np = response.xpath(
            '//div[@id = "emg-pagination-numbers"]/a[@class = "emg-icon-holder"]/span[@class = "icon-i44-go-right"]')
        next_page = _np.xpath('ancestor::a[@class = "emg-icon-holder"]/@href').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield Request(next_page, callback=self.parse_categ)  # , dont_filter=False)
