---
# Enhancing Web Scraping with Scrapy, Splash, and Playwright

This demonstration showcases the synergy between Scrapy, Splash, and Playwright for efficient web scraping tasks.

Sometimes, when dealing with dynamic websites and AJAX requests, Splash might encounter limitations. In such cases, switching to Playwright can provide a robust alternative.

### Instructions to Run the Script:

1. **Install Dependencies**:
   - Ensure Scrapy is installed. You can follow the installation guide [here](https://doc.scrapy.org/en/latest/intro/install.html). Using Anaconda environment is recommended for better management.

2. **Install Additional Plugins**:
   - Install Scrapy Splash plugin: [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)
   - Install Scrapy Playwright plugin: [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright)

3. **Setup Splash**:
   - Run Splash Docker container:
     ```
     docker run -p 8050:8050 scrapinghub/splash
     ```

4. **Run the Script**:
   - Execute the Scrapy spider:
     ```
     scrapy crawl a104 -O 104.json
     ```

By following these steps, you can seamlessly utilize the combined power of Scrapy, Splash, and Playwright to scrape data from various websites efficiently.
