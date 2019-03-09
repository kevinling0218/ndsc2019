from scrapy.cmdline import execute


SPIDER_NAME = "mobiles"
##"C://Work/sourceCodeTest/ndsc2019/teamCode/ndsc2019/data_complementary/webcrawler/spiders/
##D://Code/Python/ndsc2019/data_complementary/webcrawler/spiders/
ROOT = "D://Document/life/learning/DataScience/National_Data_Science_Competition/teamCode/ndsc2019/data_complementary/webcrawler/spiders/"

try:
    # execute(
    #     [
    #         'scrapy',
    #         'crawl',
    #         SPIDER_NAME,
    #         '-o',
    #         SPIDER_NAME + '.json',
    #     ]
    # )
    # execute(['scrapy','runspider', 'C://Work/sourceCodeTest/ndsc2019/ndsc2019/tutorial/tutorial/spiders/quotes_spider.py'])
    execute(['scrapy','runspider', ROOT+SPIDER_NAME+'_spider.py'])
except SystemExit:
    pass