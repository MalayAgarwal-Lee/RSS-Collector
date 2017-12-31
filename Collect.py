import feedparser
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import  MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

urls = ["http://planetpython.org/rss20.xml", "https://www.reddit.com/r/Python/.rss"]

def compileLinks(urls):
    links = {}
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

            #creating header with title of the blog
            newTag = soupObject.new_tag("h3", id = title)
            soupObject.body.append(newTag)
            soupObject.find('h3', id = title).append(f'{title}')

            #creating a list to display the links from RSS
            newTag = soupObject.new_tag("ul", id = f'links from {title}')
            soupObject.find('h3', id = title).insert_after(newTag)

            for number, details in items.items():

                #I am avoiding this link as parsing error due to an invalid character
                #pops up here
                if details['link'] != 'https://www.codementor.io/edmondatto/build-a-command-line-application-that-consumes-a-public-api-here-s-how-f7hxbuxm2':

                    #creating a proper list object
                    string =  soupObject.new_string(details['title'])
                    newTag = soupObject.new_tag("li", id = str(number))
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
