import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

urls = ["http://planetpython.org/rss20.xml",
        "https://www.reddit.com/r/Python/.rss"]


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
    with open('links.txt', 'w') as file:
        for title, items in links.items():
            file.write(f'{title}\n')
            for number, details in items.items():
                headline = details['title']
                link = details['link']
                try:
                    file.write(f"\t{number}. {headline} - {link}\n")
                except:
                    continue
            file.write("\n")

        return file.name


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

    with open(filename, 'rb') as attachment:

        # constructing attachment
        attachmentPart = MIMEBase('application', 'octet-stream')
        attachmentPart.set_payload(attachment.read())
        encoders.encode_base64(attachmentPart)
        attachmentPart.add_header('content-disposition',
                                  'attachment', filename=filename)

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
    filename = compileFile(links)
    mail(filename)
    print("Finished")


if __name__ == '__main__':
    main()
