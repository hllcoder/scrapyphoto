from scrapy.crawler import CrawlerProcess
from scrapy.conf import get_project_settings
import sys


def main():
    spider = sys.argv[1]
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    process.crawl(spider)
    process.start()


if __name__ == '__main__':
    main()
