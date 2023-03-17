from bs4 import BeautifulSoup
import requests

def getEffects():
    url = "https://hearthstone.fandom.com/wiki/Ability"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content,"html.parser")
    nonKeyWord = soup.find("span", id = "Other_abilities")
    effects = [tag.text for tag in nonKeyWord.findAllPrevious("big")]
    return effects

if __name__ == '__main__':
    getEffects()
