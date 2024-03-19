import scrapy
from scrapy_splash import SplashRequest

class A104Spider(scrapy.Spider):
    name = "a104"
    allowed_domains = ["www.104.com.tw"]
    # Replace the keyword with the keyword you want to search in 104.com.tw
    keyword = "scrapy"

    # Define variables outside of the Lua script
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    wait_time = 1
    # Below scroll_times simulates how many pages you want to scrape from the website listing
    scroll_times = 5
    scroll_wait = 2

    # Lua script for scrolling down the page, simulating user behavior for infinite scrolling
    script = f"""
        function main(splash, args)
            splash:set_user_agent("{user_agent}") 
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait({wait_time}))
            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {{ return document.body.scrollHeight; }}"
            )
            for _ = 1, {scroll_times} do
                scroll_to(0, get_body_height())
                splash:wait({scroll_wait})
            end

            return {{
                html = splash:html()
            }}
        end
    """

    # This method is called when the spider is created, Splash is used to render the page
    def start_requests(self):
        yield SplashRequest(
            url=f"https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword={self.keyword}",
            callback=self.parse, 
            endpoint="execute", 
            args={
                'lua_source': self.script
            })

    def parse(self, response):
        jobs = response.xpath("//div[@id='js-job-content']/article[not(@data-jobsource='hotjob_chr')]")

        for job in jobs:
            job_date = job.xpath(".//span[@class='b-tit__date']/text()").get().strip()
            job_title = job.xpath("normalize-space(.//h2/a)").get()
            job_title_link = job.xpath("normalize-space(.//h2/a/@href)").get().replace('//', '')
            job_company = job.xpath(".//li/a/text()").get().strip()
            job_intro = job.xpath("normalize-space(.//ul[contains(@class,'job-list-intro')])").get()
            job_desc = job.xpath("normalize-space(.//p)").get()
            job_tags = job.xpath(".//div[contains(@class, 'job-list-tag')]/a/text()").getall()
            
            yield scrapy.Request(
                url=f"https://{job_title_link}",
                callback=self.parse_job_detail,
                meta={
                    'playwright': True,
                    'playwright_include_page': True,
                    'date': job_date,
                    'title': job_title,
                    'link': job_title_link,
                    'company': job_company,
                    'intro': job_intro,
                    'desc': job_desc,
                    'tags': job_tags
                }
            )

    # This Method is Playwright specific
    async def parse_job_detail(self, response):
        job_detail = response.meta['playwright_page']
        await job_detail.close()

        jobs = []
        for detail in response.css('p.job-description__content::text').getall():
            # Remove newline and tab characters
            detail_cleaned = detail.replace('\n', '').replace('\t', '')
            jobs.append(detail_cleaned.strip())

        yield {
            'date': response.meta['date'],
            'title': response.meta['title'],
            'link': response.meta['link'],
            'company': response.meta['company'],
            'intro': response.meta['intro'],
            'desc': response.meta['desc'],
            'tags': response.meta['tags'],
            'detail': jobs
        }