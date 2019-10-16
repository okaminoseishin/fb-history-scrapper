import scrapy
import pandas
import random


class FacebookSpider(scrapy.Spider):

    name = 'conversations'
    conversations = dict()
    start_urls = ['https://mbasic.facebook.com']

    def __init__(self, email: str, password: str, **kwargs):
        # self.person, self.text, self.time = list(), list(), list()
        self.email, self.password = email, password
        super().__init__(**kwargs)

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formxpath='//form[contains(@action, "login")]',
            formdata={'email': self.email, 'pass': self.password},
            callback=self.parse_home)

    def parse_home(self, response):
        href = (
            'https://mbasic.facebook.com/messages/'
            '?ref_component=mbasic_home_header'
            '&ref_page=%2Fwap%2Fprofile_timeline.php&refid=17')
        return scrapy.Request(url=href, callback=self.parse_page)

    def parse_page(self, response):
        conversations = scrapy.Selector(text=response.body).xpath(
            '//h3/a/@href').extract()
        for conversation in conversations:
            yield scrapy.Request(
                url=f'https://mbasic.facebook.com{conversation}',
                meta={'conversation': dict(
                    person=list(), text=list(), time=list())},
                callback=self.parse_conversation)

    def parse_conversation(self, response):
        person, text, time = list(), list(), list()
        for message in scrapy.Selector(text=response.body).xpath(
                '//div[@id="messageGroup"]/div/div').extract():
            person.append(scrapy.Selector(text=message).xpath(
                '//div/div/a/strong/text()').extract())
            text.append(scrapy.Selector(text=message).xpath(
                '//div/div/div/span/text()').extract())
            time.append(scrapy.Selector(text=message).xpath(
                '//div/div/abbr/text()').extract())
        response.meta['conversation']['person'].extend(person[::-1])
        response.meta['conversation']['text'].extend(text[::-1])
        response.meta['conversation']['time'].extend(time[::-1])
        try:
            yield scrapy.Request(
                url='https://mbasic.facebook.com{}'.format(
                    scrapy.Selector(text=response.body).xpath(
                        '//div[@id="see_older"]/a/@href').extract()[0]
                ), callback=self.parse_conversation,
                meta={'conversation': response.meta['conversation']})
        except IndexError:
            filename = f'../conversations/{random.randint(10000, 99999)}.json'
            pandas.DataFrame({
                'person': response.meta['conversation']['person'],
                'text': response.meta['conversation']['text'],
                'time': response.meta['conversation']['time']
            }).to_json(filename, orient='records', lines=True)
