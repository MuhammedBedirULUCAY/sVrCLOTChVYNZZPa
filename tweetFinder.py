# Muhammed Bedir ULUCAY
# 08.01.2021

import pandas as pd
import os
import webbrowser
from bs4 import BeautifulSoup
from time import perf_counter, sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Extracting tweet data like user, date etc...
def extractTweetInformation(tweet):
    name = tweet.find("span", attrs = {"class" : "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}).text
    date = tweet.find("a", attrs = {"class" : "css-4rbku5 css-18t94o4 css-901oao r-9ilb82 r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"}).text
    content = tweet.find("div", attrs = {"class" : "css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"}).text.replace("\n"," ")

    numberOfComment = tweet.find("div", attrs={"data-testid":"reply"}).text
    numberOfRetweet = tweet.find("div", attrs={"data-testid":"retweet"}).text
    numberOfLikes = tweet.find("div", attrs={"data-testid":"like"}).text

    # for more correctness
    if(numberOfComment == ''): 
        numberOfComment = '0'
    if(numberOfRetweet == ''): 
        numberOfRetweet = '0'
    if(numberOfLikes == ''): 
        numberOfLikes = '0'
    
    return {"UserName" : name, "Date" : date , "TweetContent" : content , "#ofComment" : numberOfComment
                , "#ofRetweet" : numberOfRetweet, "#ofLikes" : numberOfLikes}

# Data frame columns
columns = ["UserName", "Date", "TweetContent", "#ofComment " ,"#ofRetweet", "#ofLikes"]
df = pd.DataFrame(columns=columns)
# Using browser and URL adress to pull tweets
driver = webdriver.Chrome(ChromeDriverManager().install())


sentence = input("Enter the sentence for search : ").replace(" ","%20")
url = "https://twitter.com/search?q=" + sentence

print(f"1->Populer")
print(f"!1->Latest")
option = int(input("Choose the option : "))

if (option != 1):
    url = url + "&f=live"

driver.get(url)

# wating for the page to load
print("Waiting for the page to load")
sleep(3)

# If you want to load older tweet increase the scroll number 
scrollNumber = int(input("How many tweets rolled want to load? (Each roll has nearly 22 tweets) : "))
sCounter = 0
while sCounter < scrollNumber:
    
    # Getting source code of browser page 
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource,'html.parser')
    tweets = soup.find_all("div", attrs={"data-testid" : "tweet"})

    # Extract tweet data and load data frame
    for tweet in tweets:
        addRow = extractTweetInformation(tweet)
        df = df.append(addRow, ignore_index=True)

    # Script to scroll browser to load more tweet data 
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    counter = 0
    while counter < 1:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        else:
            lastHeight = newHeight
        counter = counter + 1

    sCounter = sCounter + 1   

#saving as csv
df.to_csv("request for startup.csv",index = False)
#converting html 
html = df.to_html()
with open('request for startup.html','w',encoding="utf-8") as f:
    f.write(html)

#opening in the browser
webbrowser.open('request for startup.html')
