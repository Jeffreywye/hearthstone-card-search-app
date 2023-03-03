

def main():
    with open("cards.xls") as file:
        count = 0
        for line in file:
            count += 1

        print(count)

if __name__ == '__main__':
    main()
