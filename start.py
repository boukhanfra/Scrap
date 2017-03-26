from scrapy import Spider
from scrapy import Request
from time import sleep
from model import Model
from model.Model import session

"""
Class d'aspiration des offres sur www.leboncoin.fr
"""
class LebonCoin(Spider):
    name = 'leboncoin.com'
    start_urls = ['https://www.leboncoin.fr/annonces/offres/']
    xpath = {
        'title': '//title/text()',
        'img_url': '//div[@id="item_image"]/span/@data-imgsrc',
        'price': '//h2[@itemprop="price"]/span[@class="value"]/text()',
        'address' : '//span[@itemprop="address"]/text()',
        'description': '//p[@itemprop="description"]/text()'
    }
    i = 2
    def parse_offer(self, response):
        title = self.clean_title(response.xpath(self.xpath['title']).extract_first()),
        img_url = response.xpath(self.xpath['img_url']).extract_first(),
        price = self.clean_price(response.xpath(self.xpath['price']).extract_first()),
        city = self.get_city(response.xpath(self.xpath['address']).extract_first()),
        post_code = self.get_post_code(response.xpath(self.xpath['address']).extract_first()),
        description = response.xpath(self.xpath['description']).extract_first()
        self.create_offer(title, price, description, img_url)

    def create_category(self, label):
        label = label.replace('(pro)','')
        category = session.query(Model.Category).filter_by(label = label)
        if (category is None):
            category = Model.Category()
            category.label = label
            session.add(category)
            session.commit()
        else:
            pass

    def create_offer(self, title, price, description, link):
        o = Model.Offer()
        o.title = title
        o.price = price
        o.description = description
        o.link = link
        session.add(o)
        session.commit()
        pass
    def create_image(self, lik):
        pass
    def create_city(self):
        pass

    def parse(self, response):
        for element in response.xpath('//section[@id="listingAds"]/section/section'):
            for il in element.xpath('//ul/li[@itemtype="http://schema.org/Offer"]'):
                link = il.xpath('a/@href').extract_first()
                yield Request(
                    response.urljoin(link),
                    self.parse_offer
                )
                category = self.clean(il.xpath('a/section/p[@itemprop="category"]/text()').extract_first())
                if '(pro)' in category:
                    pro = True
                else:
                    pro = False
                self.create_category(category)
                yield {
                    'lien': il.xpath('a/@href').extract_first(),
                    'titre': self.clean(il.xpath('a/section/h2/text()').extract_first()),
                    'category': category,
                    'localisation': self.clean(il.xpath('a/section/p[@itemprop="availableAtOrFrom"]/text()').extract_first()),
                    'pro': pro
                }
        is_next_page = response.xpath('//a[@class="element page static"]/@href').extract_first()
        if is_next_page:
            next_page = self.start_urls[0] + '?o=' + str(self.i)
            self.i = self.i + 1
            if (self.i % 10 == 0):
                sleep(1)
            yield Request(
                response.urljoin(next_page),
                self.parse
            )

    def clean(self, field):
        if field is None:
            return
        field = field.replace('\n', '')
        field = field.rstrip()
        field = field.lstrip()

        return field

    def clean_price(self, price):
        if price is None:
            return
        return ''.join(e for e in price if e.isalnum())

    def get_city(self, address):
        if address is None:
            return
        return ''.join(e for e in address if e.isalpha())

    def get_post_code(self, address):
        if address is None:
            return
        return ''.join(e for e in address if e.isnumeric())

    def clean_title(self, title):
        if title is None:
            return
        return self.clean(title.replace(' - leboncoin.fr',''))