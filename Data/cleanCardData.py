import re
# from ScrapeEffects import getEffects, getClasses
from os import path

def cleanData(effectDic, classDic):
    data = {}
    cards = []
    classes = classDic
    sets = {}
    basedir = path.abspath(path.dirname(__file__))
    with open(path.join(basedir, "hearthstone.csv") , encoding="utf8") as file:
        cols = file.readline().split(',')
        # for n, col in enumerate(cols):
        #     print(str(n)+" "+col)
        for line in file:
            card = {}
            csvRow = line.strip().split(",")
            if ((csvRow[4] == "Minion") or (csvRow[4] == "Spell")) and (csvRow[3] != "Tavern Brawl"):
                # print(line)
                # print(csvRow)
                card["id"] = csvRow[0]
                card["name"] = csvRow[2]
                card["type"] = csvRow[4]
                card["effect"] = []
                card["class"] = []
                
                # index of first text occurence
                i = 5
                # card has text, must account for commas in text
                if csvRow[i]:
                    fullText = ""

                    while True:
                        text = re.sub('\n'," ",csvRow[i])
                        text = re.sub("\\\\n"," ",text)
                        text = re.sub("<b>|</b>|\"","",text)
                        fullText = fullText + text + " "
                        i += 1

                        if (csvRow[i] in classes) or (csvRow[i] == ""):
                            card["text"] = fullText
                            break

                    
                    for effect in effectDic:
                        if effect in card["text"]:
                            effectDic[effect] += 1
                            card["effect"].append(effect)

                else:
                    card["text"] = None
                    i = 6

                addValToDic(csvRow[3], sets)
                card["set"] = csvRow[3]

                # card is multiclassed
                if csvRow[-1]:
                    j = -1
                    while True:
                        cardClass = "".join(c for c in csvRow[j] if c.isalpha())
                        addValToDic(cardClass,classes)
                        card["class"].append(cardClass)
                        if "[" in csvRow[j]:
                            break
                        j += -1
                
                # not multiclassed
                else:
                    addValToDic(csvRow[i], classes)
                    card["class"].append(csvRow[i])
                
                card["rarity"] = csvRow[i+2]
                card["health"] = int(float(csvRow[i+3])) if  csvRow[i+3] else None
                
                # account for commas in mechanic col
                cur = i+4
                while True:
                    cur += 1
                    if "\'name\'" in csvRow[cur]:
                        continue
                    else:
                        break
                card["mana"] = int(float(csvRow[cur+2]))
                card["attack"] = int(float(csvRow[cur+3])) if csvRow[cur+3] else None
                cards.append(card)

    data["cards"] = cards
    data["classes"] = classes
    data["sets"] = sets
    data["effects"] = effectDic
    return data

def addValToDic(val, dic):
    if val in dic:
        dic[val] += 1
    else:
        dic[val] = 1

def printDicByLine(dic):
    for key in dic:
        print("{} {}".format(key, dic[key]))
    print(len(dic))
    print(max( [len(name) for name in dic.keys()] ))
    print()

def main():
    effectDic = getEffects()
    classDic = getClasses()
    ret = cleanData(effectDic, classDic)
    # m = 0
    for card in ret["cards"]:
        if len(card['class'])>1:
            print(card)
        # if card['text']:
        #     m = max(m,len(card['text']))
        # else:
        #     # print(card)
        #     if card['text'] == "":
        #         print(card)
    print(len(ret['cards']))
    # print(m)
    # print(max([len(card['id']) for card in ret["cards"] ] ))
    printDicByLine(ret["classes"])
    printDicByLine(ret["sets"])
    printDicByLine(ret["effects"])

if __name__ == '__main__':
    main()
