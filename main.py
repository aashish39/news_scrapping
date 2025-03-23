import psycopg2

hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = '1234'
port_id = 5432

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS DataLinks")

# Create Table In Database
create_script = ("""
            CREATE TABLE DataLinks(
                 ID SERIAL PRIMARY KEY,
                 links Varchar(1000));
""")
cur.execute(create_script)
insert_script="INSERT INTO DataLinks (links) Values(%s)"
# cur.execute(,)
# Create Add Values to created Table
lst = ['www.google.com','www.yahoo.com','www.bing.com','www.duckduckgo.com','www.amazon.com']
cur.executemany(insert_script,[(link,) for link in lst])
# for x in lst:
#  cur.execute("""INSERT INTO Datalinks(links) Values ()""")

cur.execute("SELECT * FROM Datalinks")
print(cur.fetchall())

conn.commit()
cur.close()
conn.close()


# import scrapy
# import psycopg2

# # Database Connection
# hostname = 'localhost'
# database = 'postgres'
# username = 'postgres'
# pwd = '1234'
# port_id = 5432

# conn = psycopg2.connect(
#     host=hostname,
#     dbname=database,
#     user=username,
#     password=pwd,
#     port=port_id
# )

# class DataSpiderSpider(scrapy.Spider):
#     name = "data_spider"
#     allowed_domains = ["prnewswire.com"]
#     start_urls = ["https://www.prnewswire.com/"]

#     def parse(self, response):
#         get_data = response.css('nav')
#         data_links = get_data.css("ul.nav-tier")
#         for news_links in data_links:
#             for link in news_links.css("li a::attr(href)")[1:2]:
#                 if link:
#                     yield response.follow(
#                         f"https://www.prnewswire.com/{link.get()}",
#                         callback=self.data_verse,
#                         meta={"inside_link": f"https://www.prnewswire.com/{link.get()}"}
#                     )

#     def data_verse(self, response):
#         example_value = response.meta.get("inside_link")
#         get_links = response.css("div.page-list ul.pagination li a::attr(href)")

#         cur = conn.cursor()
#         cur.execute("DROP TABLE IF EXISTS DataLinks")

#         # Create Table In Database
#         create_script = """
#             CREATE TABLE DataLinks (
#                 ID SERIAL PRIMARY KEY,
#                 links VARCHAR(1000)
#             );
#         """
#         cur.execute(create_script)

#         insert_script = "INSERT INTO DataLinks (links) VALUES (%s)"

#         for x in get_links:
#             if x:
#                 yield response.follow(
#                     f"{example_value + x.get()}",
#                     callback=self.get_pages_link,
#                     meta={"insert_script": insert_script, "cursor": cur}
#                 )

#         cur.execute("SELECT * FROM DataLinks")
#         conn.commit()
#         cur.close()
#         conn.close()

#     def get_pages_link(self, response):
#         insert_script = response.meta.get("insert_script")
#         cur = response.meta.get("cursor")

#         get_html_links = response.css('div.card-list div.row div.card a::attr(href)')
#         links = []
#         for lnk in get_html_links:
#             links.append(lnk.get())

#         cur.executemany(insert_script, [(link,) for link in links])