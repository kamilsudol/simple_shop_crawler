import requests as req
import re
import math
import multiprocessing


def results(x, price):
    if "https://allegrolokalnie.pl/oferta" in x:
        test = req.get(x)
        try:
            p = str(re.split('>|<', test.text.split("title")[1])[1].split(": ")[1].split(" ")[0]).split(",")
            p = int(p[0]) + float(p[1])/100

            if p <= price:
                print(
                    re.split('>|<', test.text.split("title")[1])[1])
        except IndexError:
            print(re.split('>|<', test.text.split("title")[1])[1])
    else:
        test = req.get(x)
        try:
            p = float(test.text.split("\"")[
                          test.text.split("\"").index("amount") + 2])
            if p <= price:
                print(
                    test.text.split("\"")[test.text.split("\"").index("offerName") + 2] + " CENA: " + str(p))
        except ValueError:
            print(
                test.text.split("\"")[test.text.split("\"").index("offerName") + 2] + " CENA: LICYTACJA")


def show(pattern, queue):
    try:
        result = set()
        r = req.get("https://allegro.pl/" + str(pattern[0]) + "?string=" + str(pattern[1]))
        amount = re.split(':|,', r.text.split("\"")[r.text.split("\"").index("listingResultsCount") + 1])[1]
        count_pages = int(math.ceil(int(amount) / 60))

        for i in range(1, count_pages + 1):
            r = req.get("https://allegro.pl/" + str(pattern[0]) + "?string=" + str(pattern[1]) + "&p=" + str(i))
            for x in r.text.split("\""):
                if "https://allegro.pl/oferta" in x or "https://allegrolokalnie.pl/oferta" in x:
                    result.add(x)

        for x in result:
            results(x, float(pattern[2]))

    except ConnectionError:
        print("Connection interrupted!")


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    set_of = [[], []] # TEMPLATE: [[CATEGORY, NAME, PRICE], etc...]
    # processes = []
    # for x in set:
    #     processes.append(multiprocessing.Process(None, show, args=(x, queue)))
    #
    # for x in processes:
    #     x.start()
    for x in set_of:
        show(x, queue)