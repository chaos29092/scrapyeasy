import scrapy
from scrapy.item import Field
from scrapy.loader.processors import TakeFirst,Join,MapCompose
import re

def strip_dot(value):
    if value:
        value = value.rstrip()
    return value

def clean_suppliers_num(value):
    if value:
        value = re.sub("\D", "", value)
    return value

class productListItem(scrapy.Item):
    ranking = Field(output_processor=TakeFirst())
    company_id = Field(output_processor=TakeFirst())
    cas = Field(output_processor=TakeFirst())
    cas_company_id = Field(output_processor=TakeFirst())

class productsItem(scrapy.Item):
    cas = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    suppliers_num = Field(input_processor=MapCompose(clean_suppliers_num),output_processor=TakeFirst())
    top = Field()

class supplierItem(scrapy.Item):
    url = Field(output_processor=TakeFirst())
    contact = Field(output_processor=TakeFirst())
    tel = Field(output_processor=TakeFirst())
    phone = Field(output_processor=TakeFirst())
    fax = Field(output_processor=TakeFirst())
    email = Field(output_processor=TakeFirst())
    website = Field(output_processor=TakeFirst())
    address = Field(output_processor=TakeFirst())
    country = Field(output_processor=TakeFirst())
    pc = Field(output_processor=TakeFirst())

class exampleItem(scrapy.Item):
    cas = Field(output_processor=TakeFirst())
    categories = Field()
    synonyms = Field(output_processor=MapCompose(strip_dot))