import feedparser
import smtplib
from collections import namedtuple
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# a namedtuple representing the structure of an article's info
ArticleInfo = namedtuple('ArticleInfo', ('headline', 'link'))


# a helper class which will contain the dictionary
# having information about the articles from each blog
class Article(object):
    def __init__(self):
        self.articles = {}

    def addArticle(self, number, headline, link):
        '''
        Creates a ArticleInfo namedtuple with headline, link using key 'number'
        :param number: The article number
        :param headline: The headline for the article
        :param link: The link to the article
        '''
        self.articles[number] = ArticleInfo(headline, link)

    def getArticles(self):
        '''
        This function returns the dictionary containing the articles
        '''
        return self.articles


# master class which will contain the main dictionary
# having all information about the various blogs
class Links(object):
    def __init__(self):
        self.blog = {}

    def addBlog(self, name):
        '''
        This function creates an instance of Article() under the key 'name.'
        :param name: The name of the blog
        :return: The instance of Article() created
        '''
        self.blog[name] = Article()
        return self.blog[name]

    def getLinks(self):
        '''
        This function returns the dictionary containing all the information
        '''
        return self.blog


# the urls of the blogs I am obtaining the news fromS
urls = ["http://planetpython.org/rss20.xml",
        "https://www.reddit.com/r/Python/.rss",
        "http://machinelearningmastery.com/blog/feed/",
        "http://news.mit.edu/rss/topic/artificial-intelligence2",
        "http://mlweekly.com/issues.rss",
        "https://towardsdatascience.com/feed/",
        "https://psychologytoday.com/topics/relationships/feed"]


def compileLinks(urls):
    '''
    '''

    # creating a new instance of Links
    links = Links()
    for url in urls:
        feed = feedparser.parse(url)
        # adding the current blog to the instance
        blog = links.addBlog(feed['feed']['title'])
        number = 1
        for entry in feed['entries']:
            # adding the current article to the instance
            blog.addArticle(number, entry['title'], entry['link'])
            number += 1
    return links


# a function which creates the HTML file out of the links
def compileFile(links):

    with open('links.html', 'w+', encoding='utf-8') as htmlFile:

        soupObject = BeautifulSoup(htmlFile, 'html5lib')
        title = soupObject.new_tag("title")
        title.append("Your Python News For Today!")
        soupObject.head.append(title)

        for title, articles in links.items():

            # creating a h3 header tag with title of the blog
            newTag = soupObject.new_tag("h3", id=title)
            newTag.append(f'{title}')
            soupObject.body.append(newTag)

            # creating an unordered list to display the links from RSS
            newTag = soupObject.new_tag("ul", id=f'links from {title}')
            soupObject.find('h3', id=title).insert_after(newTag)

            # using the namedtuple to obtain headline, link of each article
            for headline, link in articles.getArticles().values():

                # creating a proper list object
                newTag = soupObject.new_tag("li")
                newTag.append(soupObject.new_tag('a', href=link))
                newTag.a.append(headline)
                soupObject.find('ul', id=f'links from {title}').append(newTag)

        # updating the html file
        htmlFile.write(str(soupObject.prettify()))
        return htmlFile.name


# a function which emails the created file to an email address
def mail(filename):
    sender = 'rssfeedlinks1@gmail.com'
    recipient = 'malay.agarwal261016@outlook.com'
    password = 'MakingLifeEasier'
    subject = 'Your Python headlines for today!'

    # constructing message
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject

    attachment = open(filename, 'rb')

    # constructing attachment
    attachmentPart = MIMEBase('application', 'octet-stream')
    attachmentPart.set_payload(attachment.read())
    encoders.encode_base64(attachmentPart)
    attachmentPart.add_header('content-disposition', 'attachment', filename=filename)

    message.attach(attachmentPart)
    message = message.as_string()

    # connecting to server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    # sending mail
    server.sendmail(sender, recipient, message)
    server.quit()


def main():
    links = compileLinks(urls)
    filename = compileFile(links.getLinks())
    mail(filename)
    print("Finished")


if __name__ == '__main__':
    main()
