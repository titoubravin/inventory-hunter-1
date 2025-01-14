from scraper.common import ScrapeResult, Scraper, ScraperFactory


class AmazonScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.body.select_one('h1#title > span#productTitle')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.select_one('#aod-price-0 > span > span.a-offscreen')
        if not tag:
            tag = self.soup.body.select_one('#aod-price-1 > span > span.a-offscreen')
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for {price_str}'
            
        # check for add to cart button
        tag = self.soup.body.select_one('#aod-offer-price')
        if tag:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'

@ScraperFactory.register
class AmazonScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'amazon'

    @staticmethod
    def get_driver_type():
        return 'selenium'

    @staticmethod
    def get_result_type():
        return AmazonScrapeResult
