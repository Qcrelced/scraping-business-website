from modules import nav_google


def main():
    choice = int(input("choice : "))
    match choice:
        case 1:
            villes = [
                'perpignan',
                'narbonne'
            ]
            for ville in villes:
                nav_google.search(ville)
        case 2:
            nav_google.search(str(input("City : ")))


if __name__ == '__main__':
    main()
