# RSS-Collector

I used to rely on Google Feed to obtain my news related to Python. But, Google changed its policies and decided to show news (and content) based on the user's location.
Usually, Indian news sources (at least the conventional ones) do not cover topics like programming languages. So, suddenly, I found my feed void of any Python news.

Enter this script. 
Here, I use the feedparser, smtplib and email modules to create a text file containing content from two Python blogs and mail them to myself. So long, Google dependency!

Other than getting Data Science related news, I also enjoy reading psychological articles on relationships. So, that too is included here.

In the version under the master branch, I compiled the headlines and the links from each blog into a text file. Here, I am compiling them into an HTML file in order to make all the links directly accessible from the file itself. 
Open the file in a browser and you'll see the utility. 

Feedback is appreciated!

The blogs I used:

[Planet Python](http://planetpython.org/)

[Python on Reddit](https://www.reddit.com/r/Python/)

[Machine Learning Mastery](machinelearningmastery.com/blog/)

[MIT News - Artificial Intelligence](http://news.mit.edu/topic/artificial-intelligence2)

[Machine Learning Weekly](http://mlweekly.com/)

[Towards Data Science](https://towardsdatascience.com/)

[Pyschology Today - Relationships](https://psychologytoday.com/topics/relationships/)