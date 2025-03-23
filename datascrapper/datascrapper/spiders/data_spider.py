import scrapy
import json
import pymongo
from bs4 import BeautifulSoup
import requests



print("Welcome to pyMongo")
client = pymongo.MongoClient("mongodb://localhost:27017/")
print(client)
db = client['News_Data']
collection = db['News_Data_Pagewise']




class DataSpiderSpider(scrapy.Spider):
    name = "data_spider"
    allowed_domains = ["prnewswire.com"]
    start_urls = ["https://www.prnewswire.com/"]
    # file_path = r"G:\scrappy - Copy\data.json"
    # dict ={"links":[],"link_data":[]}
    def parse(self, response):
        get_data = response.css('nav')
        data_links = get_data.css("ul.nav-tier")
        for news_links in data_links:
            for link in news_links.css("li a::attr(href)")[1:]:
                if link:
                    yield response.follow(
                        f"https://www.prnewswire.com/{link.get()}",
                        callback=self.data_verse,
                        meta={
                            "inside_link": f"https://www.prnewswire.com/{link.get()}"}
                    )


    def data_verse(self, response):
        example_value = response.meta.get("inside_link")
        get_links = response.css("div.page-list ul.pagination li a::attr(href)")

        for x in get_links:
            if x:
                yield response.follow(
                    f"{example_value + x.get()}",
                    callback=self.get_pages_link
                )
    
            # cur.execute("SELECT * FROM DataLinks")

    def get_pages_link(self, response):
        get_html_links = response.css('div.card-list div.row div.card a::attr(href)')
        links = []
        for lnk in get_html_links:
            yield response.follow(lnk.get(),self.parse_news_page,meta={'page_link':lnk.get()})

        #     self.dict['links'].append(lnk.get())
        
        # with open(self.file_path, "w") as file:
        #     json.dump(self.dict, file, indent=4)    
                
    def parse_news_page(self,response):
        page_link = "https://www.prnewswire.com" + response.meta.get("page_link")
        response = requests.get(page_link)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        webpage_text = soup.get_text()
        cleaned_text = ' '.join(webpage_text.split())  
        if cleaned_text:
            dictionary = {'link':page_link,'data':cleaned_text}
            collection.insert_one(dictionary)


        # get_data = response.css('div.col-lg-10 p::text').getall()
        # txt = ",".join(get_data)


        # self.dict['links'].append(page_link)
        # self.dict['link_data'].append(txt)
        # dictionary = {'link':page_link,'data':txt}
        # collection.insert_one(dictionary)
        # with open(self.file_path, "w") as file:
        #     json.dump(self.dict, file, indent=4)    
        # yield{
        #     'link':txt
        # }

    # def get_page_data(link):
    #     response = requests.get(link)
    #     html_content = response.text
    #     soup = BeautifulSoup(html_content, 'html.parser')
    #     webpage_text = soup.get_text()
    #     cleaned_text = ' '.join(webpage_text.split())        
    #     return cleaned_text