from shutil import which

# Scrapy settings for custom_site_crawler1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

LOG_FILE = 'my_spider.log'

BOT_NAME = 'extract.scraping.scrapy'

SPIDER_MODULES = ['extract.scraping.scrapy.spiders']
NEWSPIDER_MODULE = 'extract.scraping.scrapy.spiders'

DRIVER_NAME = 'firefox'
DRIVER_EXECUTABLE_PATH = which('geckodriver')
DRIVER_ARGUMENTS = ['-headless']
BROWSER_EXECUTABLE_PATH = which('firefox')

SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS = ['-headless', '-lang=en']
SELENIUM_BROWSER_EXECUTABLE_PATH = which('firefox')

# # # Local settings
# SELENIUM_DRIVER_NAME = 'firefox'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('./extract/geckodriver')
# # '/Users/milandm/Documents/Projects/sigint/geckodriver'
# SELENIUM_DRIVER_ARGUMENTS = ['-headless', '-lang=en']
# SELENIUM_BROWSER_EXECUTABLE_PATH = which('/Applications/Firefox.app/Contents/MacOS/firefox-bin')


DOWNLOADER_MIDDLEWARES = {
    'extract.scraping.scrapy.middlewares.CustomSiteCrawlerSpiderMiddleware': 800
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'custom_site_crawler1 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'custom_site_crawler1.middlewares.TechcrunchListSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'custom_site_crawler1.middlewares.TechcrunchListDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'extract.scraping.scrapy.pipelines.DataPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue'

CONCURRENT_REQUESTS = 32
REACTOR_THREADPOOL_MAXSIZE = 20

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
