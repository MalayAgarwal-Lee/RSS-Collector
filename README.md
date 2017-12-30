# RSS-Collector

I used to rely on Google Feed to obtain my news related to Python. But, Google changed its policies and decided to show news (and content) based on the user's location.
Usually, Indian news sources (at least the conventional ones) do not cover topics like programming languages. So, suddenyl, I found my feed void of any Python news.

Enter this script. 
Here, I use the feedparser, smtplib and email modules to create a text file containing content from two Python blogs and mail them to myself. So long, Google dependency!

The blogs I used:

[Planet Python](http://planetpython.org/)

[Python on Reddit](https://www.reddit.com/r/Python/)
