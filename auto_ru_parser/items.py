# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bodyType = scrapy.Field()
    brand = scrapy.Field()
    color = scrapy.Field()
    engineDisplacement = scrapy.Field()
    enginePower = scrapy.Field()
    fuelType = scrapy.Field()
    mileage = scrapy.Field()
    modelDate = scrapy.Field()
    numberOfDoors = scrapy.Field()
    productionDate = scrapy.Field()
    transmission = scrapy.Field()
    vendor = scrapy.Field()
    description = scrapy.Field()
    owners = scrapy.Field()
    pts = scrapy.Field()
    drive = scrapy.Field()
    state = scrapy.Field()
    customs = scrapy.Field()
    price = scrapy.Field()

