import re
from ScrapeEffects import getEffects

def findEffect(text, store):
    # print(text)
    effects = re.findall('<b>(.*?)</b>', text)
    for effect in effects:
        clean = re.sub(":","",effect)
        clean = re.sub(repr("\n")," ",clean)
        # print(clean)
        if clean not in store:
            if ("<b>" in clean) or ("</b>" in clean) or (repr('\n') in clean):
                print(text)
                print(effects)
                print()
            store.add(clean)
    # print()

def cleanData(effectDic):
    data = {}
    with open("hearthstone.csv", encoding="utf8") as file:
        file.readline()
        for line in file:
            card = line.strip().split(",")
            if (card[4] == "Minion") or (card[4] == "Spell"):
                pass

                # card has text
                if card[5]:
                    pass 

def createRow():
    row = {}
    return row

def main():
    effectDic = getEffects()
    with open("hearthstone.csv", encoding="utf8") as file:
        count = 0
        # print(file.readline().strip().split(","))
        for line in file:
            card = line.strip().split(",")
            if (card[4] == "Minion") or (card[4] == "Spell"):
                count += 1
                # card had text
                if card[5]:
                    pass

        print(count)
        for effect in effectDic:
            print(effect)

if __name__ == '__main__':
    main()
