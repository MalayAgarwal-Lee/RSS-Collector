import feedparser
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import  MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#the urls of the blogs I am obtaining the news from
urls = ["http://planetpython.org/rss20.xml", "https://www.reddit.com/r/Python/.rss", "http://machinelearningmastery.com/blog/feed/", "http://news.mit.edu/rss/topic/artificial-intelligence2", "http://mlweekly.com/issues.rss", "https://medium.com/feed/tag/machine-learning"]

def avoidUrls():
    avoid = ['https://www.codementor.io/edmondatto/build-a-command-line-application-that-consumes-a-public-api-here-s-how-f7hxbuxm2','http://pyarab.com/2017/12/python-send-email.html', 'https://www.numfocus.org/blog/communicating-feedback-as-a-service-notes-from-the-disc-unconference/', 'http://feeds.doughellmann.com/~r/doughellmann/python/~3/_tlxn_DttE0/', 'https://medium.com/@yanastrokova/%D0%BD%D0%B5-%D0%B7%D0%BD%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%D0%B0-%D0%BD%D0%B5-%D0%BE%D1%81%D0%B2%D0%BE%D0%B1%D0%BE%D0%B6%D0%B4%D0%B0%D0%B5%D1%82-%D0%BE%D1%82-%D0%BE%D1%82%D0%B2%D0%B5%D1%82%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8-2-cbb40d3e9346?source=rss------machine_learning-5']

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
            soupObject.body.append(newTag)
            soupObject.find('h3', id = title).append(f'{title}')

            #creating an unordered list to display the links from RSS
            newTag = soupObject.new_tag("ul", id = f'links from {title}')
            soupObject.find('h3', id = title).insert_after(newTag)

            avoid = avoidUrls()
            for number, details in items.items():

                #I am avoiding these links
                #the first one has a special character in the headline
                #the second is in Arabic
                #they cannot be handled by .write() method
                if details['link'] not in avoid:

                    #creating a proper list object
                    string =  soupObject.new_string(details['title'])
                    newTag = soupObject.new_tag("li", id = f'{number}-{title}')
                    newTag.append(soupObject.new_tag('a', href = details['link']))
                    newTag.a.append(string)
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
