import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import time
import re
import csv
import webbrowser
import math  
import pandas as pd

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


def wuxiaScript(link, chapter_number):
    url = link + str(chapter_number)
    #url = "https://wuxiaworld.com/novel/overgeared/og-chapter-" + chapterNumber
    try:
        data_extracted = requests.get(url)
    except:
        return False, chapter_number, url
    if data_extracted.status_code != 200:
        return False, chapter_number, url
    soup = BeautifulSoup(data_extracted.text, 'html.parser')
    title = soup.select(
        "#content-container > div.section > div > div.panel.panel-default > div:nth-child(1) > div.caption.clearfix > div:nth-child(3) > h4")
    if str(title) == "[]":
        return False, chapter_number, url
    if re.search("\\(Teaser\\)", str(title)) is not None:
        return False, chapter_number, url
    next_chapter_number = int(chapter_number) + 1
    return True, next_chapter_number, url


def mangadexScript(link, chapter_number):
    try:
        data_extracted = requests.get(link)
    except:
        return False, chapter_number, link
    if data_extracted.status_code != 200:
        return False, chapter_number, link
    soup = BeautifulSoup(data_extracted.text, 'html.parser')

    row_number = 2
    while(True):
        flag = ""
        try:
            flag = soup.select("#content > div.edit.tab-content > div > div:nth-child(" + str(row_number) + ") > div > div > div.chapter-list-flag.col-auto.text-center.order-lg-4 > span")
        except:                 
            return False, chapter_number, link

        print(flag)
        if str(flag) == "[]":
            #print(link)
            return False, chapter_number, link

        if row_number > 30 or (re.search("title=\"English\"", str(flag)) is not None):
            break
        row_number += 1
        
    
    last_chapter_element = soup.select(
        "#content > div.edit.tab-content > div > div:nth-child(" + str(row_number) + ") > div > div > div.col.col-lg-5.row.no-gutters.align-items-center.flex-nowrap.text-truncate.pr-1.order-lg-2 > a"
    )    #content > div.edit.tab-content > div > div:nth-child(3)> div > div > div.chapter-list-flag.col-auto.text-center.order-lg-4 > span

    last_chapter_element_trimmed = re.search("Ch\. \d{1,4}(\.\d)?", str(last_chapter_element))
    last_chapter_number = str(last_chapter_element_trimmed.group(0))[4:]

    if last_chapter_number != str(chapter_number):
        url = "https://mangadex.org" + str(re.search("href=\"/chapter/\d{1,}\"", str(last_chapter_element)).group(0)[6:-1])
        return True, last_chapter_number, url
    else:
        return False, chapter_number, link
    

def leviatanScript(link, chapter_number):
    try:
        data_extracted = requests.get(link)
    except:
        return False, chapter_number, link
    if data_extracted.status_code != 200:
        return False, chapter_number, link
    soup = BeautifulSoup(data_extracted.text, 'html.parser')

    last_chapter_element = ""

    try:
        last_chapter_element = soup.select("#content > div > div.row > div.col-lg-9.col-md-8.col-xs-12.text-muted > div.row.py-2 > div > div.card.p-4 > div > div:nth-child(1) > div > a.item-author.text-color")
    except:
        return False, chapter_number, link

    last_chapter_element_trimmed = re.search("Chapter \d{1,4}", str(last_chapter_element))
    last_chapter_number = str(last_chapter_element_trimmed.group(0))[8:]

    if last_chapter_number != str(chapter_number):
        url = str(re.search("href=\".*\"", str(last_chapter_element)).group(0)[6:-1])
        return True, last_chapter_number, url
    else:
        return False, chapter_number, link


def mangakakalotScript(link, chapter_number):
    try:
        data_extracted = requests.get(link)
    except:
        return False, chapter_number, link
    if data_extracted.status_code != 200:
        return False, chapter_number, link
    soup = BeautifulSoup(data_extracted.text, 'html.parser')

    last_chapter_element = ""

    try:
        last_chapter_element = soup.select("body > div.body-site > div.container.container-main > div.container-main-left > div.panel-story-chapter-list > ul > li:nth-child(1) > a")
    except:
        return False, chapter_number, link

    last_chapter_element_trimmed = re.search("Chapter \d{1,4}(\.\d)?", str(last_chapter_element))
    last_chapter_number = str(last_chapter_element_trimmed.group(0))[8:]
    if last_chapter_number != str(chapter_number):
        url = str(re.search("href=\"[^\"]*\"", str(last_chapter_element)).group(0)[6:-1])
        return True, last_chapter_number, url
    else:
        return False, chapter_number, link


def webtoonsScript(link, chapter_number):
    try:
        data_extracted = requests.get(link)
    except:
        return False, chapter_number, link
    if data_extracted.status_code != 200:
        return False, chapter_number, link
    soup = BeautifulSoup(data_extracted.text, 'html.parser')

    last_chapter_element = ""

    try:
        last_chapter_element = soup.select("#_listUl > li:nth-child(1) > a > span.tx")
        last_chapter_url_element = soup.select("#_listUl > li:nth-child(1) > a")
    except:
        return False, chapter_number, link

    last_chapter_element_trimmed = re.search("#\d{1,4}", str(last_chapter_element))
    last_chapter_number = str(last_chapter_element_trimmed.group(0))[1:]
    if last_chapter_number != str(chapter_number):
        url = str(re.search("href=\"[^\"]*\"", str(last_chapter_url_element)).group(0)[6:-1]).replace("amp;", "")
        return True, last_chapter_number, url
    else:
        return False, chapter_number, link



def openBrowser(link, popup):
    webbrowser.open(link)
    popup.destroy()


def popupmsg(msg, link, count):
    popup = tk.Tk()
    popup.wm_title("New Chapter")
    if count > 0:
        msg += " (+" + str(count) + ")"
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack(side="left")
    B2 = ttk.Button(popup, text="Go to website", command= lambda: openBrowser(link, popup))
    B2.pack(side="right")
    popup.mainloop()


#time.sleep(180)
#while True:
#time.sleep(600)
#with open("info.csv", newline='') as csv_file:
csv_info = pd.read_csv("info.csv", dtype={'nextChapter': object})
csv_header = csv_info.columns

rowNumber = 0
for row in csv_info.values:
    #get csv info
    name = row[0]
    website = row[1]
    link = row[2]
    chapter = int(row[4]) if math.modf(float(row[4]))[0] == 0 else row[4]
    msg = str(row[3])
    tracking = str(row[5]) == "True"
    if(not tracking):
        continue
    is_new_chapter = False
    atleast_one_new_chapter = False
    start_chapter = chapter
    new_chapter = -1
    msg_new_chapter = -1
    true_link = ""
    msg_link = ""

    count = -1
    #check if there is a new manga
    while(True):
        if website == "wuxia":
            is_new_chapter, new_chapter, true_link = wuxiaScript(link, chapter)
        elif website == "mangadex":
            is_new_chapter, new_chapter, true_link = mangadexScript(link, chapter)
        elif website == "leviatan":
            is_new_chapter, new_chapter, true_link = leviatanScript(link, chapter)
        elif website == "mangakakalot":
            is_new_chapter, new_chapter, true_link = mangakakalotScript(link, chapter)
        elif website == "webtoons":
            is_new_chapter, new_chapter, true_link = webtoonsScript(link, chapter)
        else:
            continue

        if(not is_new_chapter):
            break
        
        chapter = new_chapter
        count += 1
        if count == 0:
            msg_new_chapter = new_chapter
            msg_link = true_link
            atleast_one_new_chapter = True 
            if website == "mangadex" or website == "leviatan" or website == "mangakakalot":
                count = float(new_chapter) - float(start_chapter)
    
    if(atleast_one_new_chapter):
        if math.modf(float(new_chapter))[0] == 0:
            csv_info["nextChapter"][rowNumber] = str(int(new_chapter))
        else:
            csv_info["nextChapter"][rowNumber] = str(new_chapter)
        

    #message
    if atleast_one_new_chapter:
        if website == "wuxia":
            msg_new_chapter -= 1
        msg = msg.replace("###", str(msg_new_chapter), -1)
        popupmsg(msg, msg_link, int(count - 1) if math.modf(count)[0] == 0 else count - 1)

    rowNumber += 1


csv_info.to_csv("info.csv", index=False)
