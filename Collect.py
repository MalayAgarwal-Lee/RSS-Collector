import feedparser

#TODO - Get a list of links from the websites
#TODO - Compile them into a text file which has links that can be clicked (.md maybe)
#TODO - Email the file as an attachment to myself

urls = ["http://planetpython.org/rss20.xml", "https://www.reddit.com/r/Python/.rss"]

def compileLinks(urls):
    links = {}
    for url in urls:
        pass

def compileFile():
    pass

def mail():
    pass

def main():
    links = compileLinks(urls)

if __name__ == '__main__':
    main()
