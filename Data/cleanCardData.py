import re

def findEffect(text, store):
    effects = re.findall('<b>(.*?)</b>', text)
    for effect in effects:
        clean = re.sub(":","",effect)
        if clean not in store:
            store.add(clean)

def main():
    effectDic = set()
    with open("hearthstone.csv", encoding="utf8") as file:
        count = 0
        # print(file.readline().strip().split(","))
        for line in file:
            card = line.strip().split(",")
            if (card[4] == "Minion") or (card[4] == "Spell"):
                count += 1
                # print(card[5])
                if card[5]:
                    findEffect(card[5],effectDic)

        # print(count)
        for effect in effectDic:
            print(effect)
        print(len(effectDic))

if __name__ == '__main__':
    main()
