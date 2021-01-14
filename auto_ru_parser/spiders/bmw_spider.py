import scrapy


class BmwSpider(scrapy.Spider):
    name = 'bmw_spider'

    start_urls = [
        'https://auto.ru/moskva/cars/bmw/used/'
    ]

    def parse(self, response, **kwargs):
        # Iterating through all cars list
        for car in response.css('div.ListingItem-module__main'):
            # get particular car detailed view link
            details_page = car.css('a.ListingItemTitle-module__link::attr(href)').get()

            if details_page is not None:
                details_page = response.urljoin(details_page)
                yield scrapy.Request(details_page, callback=self.parse_attributes)

        next_page = response.css('a.ListingPagination-module__next::attr(href)').get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_attributes(self, response):
        card = response.css('ul.CardInfo')
        condition_index = card.css('li.CardInfoRow span::text').getall().index('Состояние') + 1
        return {
            'bodyType': card.css('li.CardInfoRow a::text')[1].get(),
            'brand': 'BMW',
            'color': card.css('li.CardInfoRow a::text')[2].get(),
            'engineDisplacement': card.css('li.CardInfoRow div::text').get().split()[0],
            'enginePower': card.css('li.CardInfoRow div::text').get().split()[3],
            'fuelType': card.css('li.CardInfoRow a::text')[-1].get(),
            'mileage': card.css('li.CardInfoRow span::text')[2].get().replace('\xa0', '')[:-2],
            'productionDate': card.css('li.CardInfoRow a::text')[0].get(),
            'vehicleTransmission': card.css('li.CardInfoRow span::text')[9].get(),
            'owners': card.css('li.CardInfoRow span::text')[17].get().replace('\xa0', ' '),
            'PTS': card.css('li.CardInfoRow span::text')[19].get(),
            'drive': card.css('li.CardInfoRow span::text')[11].get(),
            'wheel': card.css('li.CardInfoRow span::text')[13].get(),
            'condition': card.css('li.CardInfoRow span::text')[condition_index].get(),
        }
