import scrapy
from scrapy import Request
from scrapy.http import Response

class NewsScraping(scrapy.Spider):
    name = 'News_The_Guardian'

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        yield scrapy.Request('https://www.theguardian.com/')
    def parse(self, response: Response, **kwargs):

        def next_new():
            #The nextnew variable is receiving the paths referring to the default name that the site divides its content into, capturing its Url
            next_new = response.xpath('//div[@ id="container-headlines"]//a/@href').getall() + \
                       response.xpath('//div[@ id="container-spotlight"]//a/@href').getall() + \
                       response.xpath('//div[@ id="container-news-extra"]//a/@href').getall() + \
                       response.xpath('//div[@ id="container-sport"]//a/@href').getall() + \
                       response.xpath('//div[@ id="container-opinion"]//a/@href').getall() + \
                       response.xpath('//div[@ id="container-lifestyle"]//a/@href').getall() + \
                       response.xpath('//div[@ id="container-culture"]//a/@href').getall() + \
                       response.xpath('//div[@ id="container-across-the-country"]//a/@href').getall() + \
                       response.xpath('//div[@ id="container-the-rural-network"]//a/@href').getall() + \
                       response.xpath('//div[@ id="container-around-the-world"]//a/@href').getall()
            return (next_new)
        #Function mapping all pages from homepage

        def title():
            title_details = response.xpath('//div[@ data-gu-name="headline"]//h1/text()').get()
            title_div = response.xpath('//div[@ data-gu-name="headline"]//h1/span/text()').get()
            title_pag = response.xpath('/html/head/title/text()').get()

            if title_details is not None:
                return (title_details)
            elif title_div is not None:
                return (title_div)
            else:
                return (title_pag)
        #Function checks the possibilities of presenting the title according to the found identification patterns and returns the text to the title variable

        def tags():
            tags = response.xpath('//ul[@ role="list"]//a/text()').getall()
            unique_tags = set(tags)  # Converte a lista em um conjunto para remover duplicatas
            return unique_tags

        def author():
            author_details = response.xpath('//a[@ rel="author"]/text()').getall()
            author_div = response.xpath('//address [@aria-label="Contributor info"]//span/text()').getall()
            author = ''
            if author_details:
                author += ', '.join(author_details)
            else:
                author += ', '.join(author_div)
            return author
        #Function checks the possibilities of presenting the title according to the found identification patterns and returns the text to the author variable

        def date():
            date_details = response.xpath('//details/text()').get()
            date_div = response.xpath('//div[@style="--mobile-color:inherit;"]/text()').get()
            if date_details is not None:
                return (date_details)
            if date_div is not None:
                return (date_div)
        #Function checks the possibilities of presenting the title according to the found identification patterns and returns the text to the date variable

        def link():
            link = response.xpath('/html/head/link[@ rel="canonical"]/@href').get()
            return (link)
        #Function returns the url to link variable

        def content():
            paragraphs = response.xpath('//article//div[@ id="maincontent"]//p/text()').getall()
            content = ''
            for paragraph in paragraphs:
                content = content + paragraph
            return (content)
        #Function to findall paragraphs on the page, capture their texts with the help of a looping and return the concatenated content

        title = title()              #fill in the variables with the functions above
        author = author()
        date = date()
        link = link()
        content = content()
        tags = tags()
        yield {
            'Title': title,
            'Author': author,
            'Date': date,
            'Content': content,
            'Tags': tags,
            'Link': link
        }               # fills in a dictionary with the information obtained and presents


        for next_page in next_new():
            yield scrapy.Request('https://www.theguardian.com/' + next_page, callback=self.parse)
        #Loop to watch each url returned by the "next_new" function
