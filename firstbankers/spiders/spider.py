import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import FfirstbankersItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class FfirstbankersSpider(scrapy.Spider):
	name = 'firstbankers'
	start_urls = ['https://www.firstbankers.com/Blog?page=1']

	def parse(self, response):
		post_links = response.xpath('//a[@class="button wsc_pi_button wsc_readmore"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[contains(text(),"    Next >>")]/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)

	def parse_post(self, response):
		date = response.xpath('//span[@class="wsc_info_date"]/text()').get().strip()
		title = response.xpath('//h2[@class="wsc_title"]/text()').get().strip()
		content = response.xpath('//div[@class="wsc_pi_body"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=FfirstbankersItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
