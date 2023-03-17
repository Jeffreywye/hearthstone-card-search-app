import re

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
                    findEffect(card[5].strip(),effectDic)

        # print(count)
        for effect in effectDic:
            print(effect)
        print(len(effectDic))

if __name__ == '__main__':
    main()
