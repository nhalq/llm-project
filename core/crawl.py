from enum import *
from typing import *
from langchain_community.document_loaders import FireCrawlLoader


class FireCrawlScrapeFormat(Enum):
    MARKDOWN = "markdown",
    HTML = "html",
    RAW_HTML = "rawHtml",
    LINKS = "links",
    SCREENSHOT = "screenshot",
    SCREENSHOT_FULLPAGE = "screenshot@fullPage",
    EXTRACT = "extract"


class FireCrawlScrapeOptions:
    formats: Optional[List[FireCrawlScrapeFormat]]

    def __init__(self, *, formats: Optional[List[FireCrawlScrapeFormat]] = None):
        self.formats = formats


class FireCrawlParams:
    limit: Optional[int]
    formats: Optional[List[FireCrawlScrapeFormat]]
    scrapeOptions: Optional[FireCrawlScrapeOptions]

    def __init__(self, *,
                 limit: Optional[int] = None,
                 formats: Optional[List[FireCrawlScrapeFormat]] = None,
                 scrapeOptions: Optional[FireCrawlScrapeOptions] = None):
        self.limit = limit
        self.formats = formats
        self.scrapeOptions = scrapeOptions


class FireCrawlLoaderWrapper(FireCrawlLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init__firecrawl()

    def __init__firecrawl(self):
        origin_crawl_url = self.firecrawl.crawl_url

        def override_crawl_url(*args, **kwargs):
            r = origin_crawl_url(*args, **kwargs)
            return r['data'] if 'data' in r else r

        # Workaround fix for firecrawl-py sdk
        self.firecrawl.crawl_url = override_crawl_url


def create(url: str, *,
           api_key: Optional[str] = None,
           api_url: Optional[str] = None,
           params: Optional[FireCrawlParams] = None) -> FireCrawlLoader:
    if params is None:
        formats = [FireCrawlScrapeFormat.MARKDOWN]
        scrapeOptions = FireCrawlScrapeOptions(formats=formats)
        params = FireCrawlParams(limit=8,
                                 formats=formats,
                                 scrapeOptions=scrapeOptions)

    firecrawl_loader = FireCrawlLoaderWrapper(url=url, mode='crawl', params=params,
                                              api_key=api_key, api_url=api_url)
    return firecrawl_loader
