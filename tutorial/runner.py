from scrapy.cmdline import execute


SPIDER_NAME = "mobiles"
##C://Work/sourceCodeTest/ndsc2019/ndsc2019/tutorial/tutorial/spiders/
ROOT = "D://Code/Python/ndsc2019/tutorial/tutorial/spiders/"

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