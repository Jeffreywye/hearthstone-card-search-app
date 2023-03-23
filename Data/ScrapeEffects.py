from bs4 import BeautifulSoup
import requests

"""
scrape Hearthstone wiki for Keyword effects by getting all big tags before <span id = Other_abilities>
"""
def getEffects():
    url = "https://hearthstone.fandom.com/wiki/Ability"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content,"html.parser")
    nonKeyWord = soup.find("span", id = "Other_abilities")
    effects = {tag.text : 0 for tag in nonKeyWord.findAllPrevious("big")}
    return effects

def getClasses():
    url = "https://hearthstone.fandom.com/wiki/Class"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    div = soup.find("div", class_="mw-parser-output")
    ul = div.find_all("ul")
    classes = {tag["alt"] : 0 for tag in ul[1].find_all("img",alt=True)}
    for tag in ul[2].find_all("img",alt=True):
        if tag["alt"] == "Legacy":
            continue
        classes[tag["alt"]] = 0
    return classes
    
if __name__ == '__main__':
    getEffects()
    getClasses()
