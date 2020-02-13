import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import time
import re
import csv
import webbrowser
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
    return True, chapter_number, link

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
csv_info = pd.read_csv("info.csv")
csv_header = csv_info.columns

rowNumber = 0
for row in csv_info.values:
    #get csv info
    name = row[0]
    website = row[1]
    link = row[2]
    chapter = row[4]
    msg = str(row[3]).replace("###", str(chapter), -1)
    tracking = str(row[5]) == "True"
    if(not tracking):
        continue
    is_new_chapter = False
    atleast_one_new_chapter = False
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
    
    if(atleast_one_new_chapter):
        csv_info["nextChapter"][rowNumber] = new_chapter
        #csv_info[count, "nextChapter"] = new_chapter
        print(csv_info["nextChapter"][rowNumber])
        csv_info.to_csv("info.csv", index=False)

    #message
    if atleast_one_new_chapter:
        popupmsg(msg, msg_link, count)

    rowNumber += 1
