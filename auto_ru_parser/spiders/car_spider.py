import json
import scrapy


from ..items import CarItem


class CarSpider(scrapy.Spider):
    name = 'car_spider'

    start_urls = [
        'https://auto.ru/moskva/cars/bmw/used/',
        'https://auto.ru/moskva/cars/volkswagen/used/',
        'https://auto.ru/moskva/cars/nissan/used/',
        'https://auto.ru/moskva/cars/mercedes/used/',
        'https://auto.ru/moskva/cars/toyota/used/',
        'https://auto.ru/moskva/cars/audi/used/',
        'https://auto.ru/moskva/cars/mitsubishi/used/',
        'https://auto.ru/moskva/cars/skoda/used/',
        'https://auto.ru/moskva/cars/volvo/used/',
        'https://auto.ru/moskva/cars/honda/used/',
        'https://auto.ru/moskva/cars/infiniti/used/',
        'https://auto.ru/moskva/cars/lexus/used/',

    ]

    def response_is_ban(self, request, response):
        return b'banned' in response.body

    def exception_is_ban(self, request, exception):
        return None

    def parse(self, response, **kwargs):
        cars_list = response.css('div.ListingItem-module__main')
        # Iterating through all cars list
        for car in cars_list:
            # get particular car detailed view link
            car_url = car.css('a.ListingItemTitle-module__link::attr(href)').get()

            if car_url:
                car_url = response.urljoin(car_url)
                yield scrapy.Request(car_url, callback=self.parse_attributes)

        next_page = response.css('a.ListingPagination-module__next::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_attributes(self, response):
        raw_data = response.xpath('//div[@id="sale-data-attributes"]/@data-bem').get()
        data = json.loads(raw_data)

        car = CarItem()
        car['bodyType'] = response.xpath('//meta[@itemprop="bodyType"]/@content').get()
        car['brand'] = response.xpath('//meta[@itemprop="brand"]/@content').get()
        car['color'] = response.xpath('//meta[@itemprop="color"]/@content').get()
        car['engineDisplacement'] = response.xpath('//meta[@itemprop="engineDisplacement"]/@content').get()
        car['enginePower'] = response.xpath('//meta[@itemprop="enginePower"]/@content').get()
        car['enginePower'] = response.xpath('//meta[@itemprop="description"]/@content').get()
        car['fuelType'] = response.xpath('//meta[@itemprop="fuelType"]/@content').get()
        car['mileage'] = data['sale-data-attributes']['km-age']
        car['modelDate'] = response.xpath('//meta[@itemprop="modelDate"]/@content').get()
        car['numberOfDoors'] = response.xpath('//meta[@itemprop="numberOfDoors"]/@content').get()
        car['productionDate'] = response.xpath('//meta[@itemprop="productionDate"]/@content').get()
        car['transmission'] = response.xpath('//meta[@itemprop="vehicleTransmission"]/@content').get()
        car['owners'] = response.xpath('//li[@class="CardInfoRow CardInfoRow_ownersCount"]/span[2]/text()').get()
        car['pts'] = response.xpath('//li[@class="CardInfoRow CardInfoRow_pts"]/span[2]/text()').get()
        car['drive'] = response.xpath('//li[@class="CardInfoRow CardInfoRow_drive"]/span[2]/text()').get()
        car['state'] = response.xpath('//li[@class="CardInfoRow CardInfoRow_state"]/span[2]/text()').get()
        car['customs'] = response.xpath('//li[@class="CardInfoRow CardInfoRow_customs"]/span[2]/text()').get()
        car['price'] = data['sale-data-attributes']['price']

        return car
