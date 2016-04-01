import scrapy,os,re

class StealSpider(scrapy.Spider):
    name = "steal"
    allowed_domains = ["fruitday.com"]
    start_urls = [
        "http://www.fruitday.com/",
        "http://www.fruitday.com/prolist/index/40",
        "http://www.fruitday.com/prolist/index/277",
        "http://www.fruitday.com/prolist/index/43",
        "http://www.fruitday.com/login",
        "http://www.fruitday.com/register"
    ]

    def parse(self, response):
        file_type =  response.headers['Content-Type']

        if file_type=='text/css':
            urls = self.css_parse_urls(response)
        elif file_type=='text/html':
            urls = self.html_parse_urls(response)
        else:
            urls = []

        for url in urls:
            request = scrapy.Request(url,callback=self.parse)
            yield request
        filename = self.parse_file_dir(response)
        self.write_file(response.body,filename)

    def css_parse_urls(self,response):
        urls = re.findall(r'background: url\([\'|"]?(.*?)[\'|"]?\)',response.body,re.S)
        return urls
        pass

    def html_parse_urls(self,response):
        urls = []
        link = response.xpath('//link/@href')
        urls += self.customs_parse_urls(link,response)
        script = response.xpath('//script/@src')
        urls += self.customs_parse_urls(script,response)
        img = response.xpath('//img/@src')
        urls += self.customs_parse_urls(img,response)
        #a = response.xpath('//a/@href')
        #urls += self.customs_parse_urls(a,response)
        return  urls
        pass

    def customs_parse_urls(self,links,response):
        urls = []
        for href in links:
            url = response.urljoin(href.extract())
            if url.find('www.'+self.allowed_domains[0]) > -1:
                urls.append(url)
        return  urls
        pass

    def parse_file_dir(self,response):
        url = response.urljoin(response.url)
        index = url.find('?')
        if index > -1:
            url = url[0:index]
        url = url.replace('http://www.'+ self.allowed_domains[0] ,'').rstrip('/')
        if  url.find('.') < 0:
            url += '/index.html'
        return './dowmload/fruitday/'+url

    def write_file(self,body,filename):
        print filename
        if os.path.exists(filename) :
            print filename + ' exit'
        else:
            filepartition = filename.rpartition('/')
            print filepartition[0];
            if not os.path.exists(filepartition[0]) :
                print filepartition[0]
                os.makedirs(filepartition[0])
            with open(filename, 'wb') as f:
                f.write(body)
        pass


