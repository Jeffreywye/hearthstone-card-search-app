

def main():
    with open("hearthstone.csv", encoding="utf8") as file:
        count = 0
        for line in file:
            print(count)
            count += 1

        print(count)

if __name__ == '__main__':
    main()
