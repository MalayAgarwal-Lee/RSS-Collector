import feedparser
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import  MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#the urls of the blogs I am obtaining the news from
urls = ["http://planetpython.org/rss20.xml", "https://www.reddit.com/r/Python/.rss", "http://machinelearningmastery.com/blog/feed/", "http://news.mit.edu/rss/topic/artificial-intelligence2", "http://mlweekly.com/issues.rss", "https://towardsdatascience.com/feed/"]

def avoidUrls():
    avoid = ['http://feeds.doughellmann.com/~r/doughellmann/python/~3/_tlxn_DttE0/', 'https://medium.com/@yanastrokova/%D0%BD%D0%B5-%D0%B7%D0%BD%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%D0%B0-%D0%BD%D0%B5-%D0%BE%D1%81%D0%B2%D0%BE%D0%B1%D0%BE%D0%B6%D0%B4%D0%B0%D0%B5%D1%82-%D0%BE%D1%82-%D0%BE%D1%82%D0%B2%D0%B5%D1%82%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8-2-cbb40d3e9346?source=rss------machine_learning-5',]

    for url in avoid:
        yield url

def compileLinks(urls):
    links = {}

    #creating the dictionary
    #the dictionary has the following structure:
    #{'blog-name': {'article number': {'title': <headline>, 'link': <link>}}}
    for url in urls:
        feed = feedparser.parse(url)
        title = feed['feed']['title']
        links[title] = {}
        i = 1
        for entry in feed['entries']:
            links[title][i] = {}
            links[title][i]['title'] = entry['title']
            links[title][i]['link'] = entry['link']
            i += 1

    return links

def compileFile(links):

    with open('links.html', 'w+') as htmlFile:

        soupObject = BeautifulSoup(htmlFile, 'html5lib')
        title = soupObject.new_tag("title")
        title.append("Your Python News For Today!")
        soupObject.head.append(title)
        for title, items in links.items():

            #creating a h3 header tag with title of the blog
            newTag = soupObject.new_tag("h3", id = title)
            newTag.append(f'{title}')
            soupObject.body.append(newTag)

            #creating an unordered list to display the links from RSS
            newTag = soupObject.new_tag("ul", id = f'links from {title}')
            soupObject.find('h3', id = title).insert_after(newTag)

            avoid = avoidUrls()
            for number, details in items.items():

                headline = details['title']
                #checking for Em dash
                #cannot be handled by write(), so being replaced
                emDash = '\u2014'
                if emDash in details['title']:
                    headline = headline.replace(emDash, '-', headline.count(emDash))

                #avoiding some problematic urls
                if details['link'] not in avoid:
                    #creating a proper list object
                    newTag = soupObject.new_tag("li")
                    newTag.append(soupObject.new_tag('a', href = details['link']))
                    newTag.a.append(headline)
                    soupObject.find('ul', id = f'links from {title}').append(newTag)

        #updating the html file
        htmlFile.write(str(soupObject.prettify()))
        return htmlFile.name

def mail(filename):
    sender = 'rssfeedlinks1@gmail.com'
    recipient = 'malay.agarwal261016@outlook.com'
    password = 'MakingLifeEasier'
    subject = 'Your Python headlines for today!'

    #constructing message
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject

    attachment = open(filename, 'rb')

    #constructing attachment
    attachmentPart = MIMEBase('application', 'octet-stream')
    attachmentPart.set_payload(attachment.read())
    encoders.encode_base64(attachmentPart)
    attachmentPart.add_header('content-disposition', 'attachment', filename = filename)

    message.attach(attachmentPart)
    message = message.as_string()

    #connecting to server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    #sending mail
    server.sendmail(sender, recipient, message)
    server.quit()


def main():
    links = compileLinks(urls)
    filename = compileFile(links)
    mail(filename)
    print("Finished")

if __name__ == '__main__':
    main()
