import feedparser
import smtplib
from collections import namedtuple
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# a namedtuple representing an article: headline, link
ArticleInfo = namedtuple('ArticleInfo', ('headline', 'link'))


class Article(object):
    '''
    Class containg all articles collected from one blog in a dictionary

    Attributes:
        articles: Dictionary containing all articles
    '''

    def __init__(self):
        '''
        Initializes articles as an empty dictionary
        '''
        self.articles = {}

    def add_article(self, number, headline, link):
        '''
        Creates a ArticleInfo instance with (headline, link) using key 'number'

        Argumnets:
            number: int, The article number
            headline: str, The headline for the article
            link: str, The link to the article
        '''
        self.articles[number] = ArticleInfo(headline, link)

    def get_articles(self):
        '''
        Returns the dictionary containing the articles

        Returns:
            A dictionary
        '''
        return self.articles


class Links(object):
    '''
    Class containing all the articles from all blogs in a dictionary.

    Attributes:
        blog: A dictionary with key: blog name, value: articles from blog
    '''

    def __init__(self):
        '''
        Initializes blog as an empty dictionary
        '''
        self.blog = {}

    def add_blog(self, name):
        '''
        Creates an instance of Article() under the key 'name.'

        Arguments:
            name: str, The name of the blog

        Returns:
            The instance of Aritcle() created
        '''
        self.blog[name] = Article()
        return self.blog[name]

    def get_links(self):
        '''
        Returns the dictionary containing all the articles
        '''
        return self.blog


# the urls of the blogs I am obtaining the news fromS
urls = ["http://planetpython.org/rss20.xml",
        "https://www.reddit.com/r/Python/.rss",
        "http://machinelearningmastery.com/blog/feed/",
        "http://news.mit.edu/rss/topic/artificial-intelligence2",
        "https://mlweekly.com/issues.rss",
        "https://towardsdatascience.com/feed/",
        "https://psychologytoday.com/topics/relationships/feed"]


def compile_links(urls):
    '''
    Iterates over the blogs
    Obtains their articles as an instance of Links class

    Arguments:
        urls: list, the urls of the blogs to be used

    Returns:
        Instance of Links class containing articles
    '''

    # creating a new instance of Links
    links = Links()
    for url in urls:
        feed = feedparser.parse(url)

        # adding the current blog to the instance
        try:
            blog = links.add_blog(feed['feed']['title'])
        except KeyError:
            print(f'Invalid url: {url}\n')

        for count, entry in enumerate(feed['entries'], 1):
            # adding the current article to the instance
            blog.add_article(count, entry['title'], entry['link'])
    return links


def compile_file(links):
    '''
    Function which creates HTML file out of articles from blogs

    Arguments:
        links: Links instance, containing articles from blogs

    Returns:
        str, name of the file created
    '''

    with open('links.html', 'w+', encoding='utf-8') as html_file:

        soup_object = BeautifulSoup(html_file, 'html5lib')
        title = soup_object.new_tag("title")
        title.append("Your Python News For Today!")
        soup_object.head.append(title)

        for title, articles in links.items():

            # creating a h3 header tag with title of the blog
            new_tag = soup_object.new_tag("h3", id=title)
            new_tag.append(f'{title}')
            soup_object.body.append(new_tag)

            # creating an unordered list to display the links from RSS
            new_tag = soup_object.new_tag("ul", id=f'links from {title}')
            soup_object.find('h3', id=title).insert_after(new_tag)

            # using the namedtuple to obtain headline, link of each article
            for headline, link in articles.get_articles().values():

                # creating a proper list object
                new_tag = soup_object.new_tag("li")
                new_tag.append(soup_object.new_tag('a', href=link))
                new_tag.a.append(headline)
                soup_object.find('ul', id=f'links from {title}').append(new_tag)

        # updating the html file
        html_file.write(str(soup_object.prettify()))
        return html_file.name


def mail(filename):
    '''
    Function which mails the file to an email address

    Arguments:
        filename: str, name of the file to be mailed
    '''
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
    attachment_part = MIMEBase('application', 'octet-stream')
    attachment_part.set_payload(attachment.read())
    encoders.encode_base64(attachment_part)
    attachment_part.add_header('content-disposition',
                              'attachment', filename=filename)

    message.attach(attachment_part)
    message = message.as_string()

    # connecting to server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    # sending mail
    server.sendmail(sender, recipient, message)
    server.quit()


def main():
    links = compile_links(urls)
    filename = compile_file(links.get_links())
    mail(filename)
    print("Finished")


if __name__ == '__main__':
    main()
