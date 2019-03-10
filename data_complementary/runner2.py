import scrapy
from scrapy.crawler import CrawlerProcess
from webcrawler.spiders import mobiles_spider

process = CrawlerProcess()



process.crawl(mobiles_spider)

process.start() # the script will block here until all crawling jobs are finished