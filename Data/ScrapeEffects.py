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

if __name__ == '__main__':
    getEffects()
