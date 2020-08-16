import csv


def load_data_to_dictionary():
    dictionary = {}
    with open("jmena.csv", "r", encoding="utf-8") as file:

        years = file.readline().strip().split(",")

        for line in file:
            data = line.split(",")
            name = data[0]
            dictionary[name] = {}
            for year in range(int(years[1]), int(years[-1]) + 1):
                col = years.index(str(year))
                count = int(data[col])
                dictionary[name][year] = count
        return dictionary


def n_most_popular_for_given_year(dct, n, year):
    dictionary = dct
    num = []

    my_list = [(dictionary[name][year], name) for name in dictionary]
    my_list.sort(reverse=True)
    for count, name in my_list:
        num.append(name)
        if len(num) == n + 1:
            return num[1:]


def most_popular_in_what_year(dct, name):
    dictionary = dct
    num1 = 0
    if name not in dictionary.keys():
        return

    for year in dictionary[name]:
        num2 = dictionary[name][year]
        if num2 > num1:
            num1 = num2
            output = year
    return output


def maximal_increase(dict, name):
    dictionary = dict
    num1 = 0
    difference_old = 0
    if name not in dictionary.keys():
        return

    for year in dictionary[name]:
        num2 = dictionary[name][year]
        if year != 1950:
            difference_new = num2 - num1
            if difference_new > difference_old:
                output = year
                difference_old = difference_new
        num1 = num2
    return output - 1


def maximal_decrease(dict, min_occurence):
    dictionary = dict
    percentage_old = 0
    num1 = 1

    for name in dictionary.keys():
        for year in dictionary[name]:
            num2 = dictionary[name][year]
            if year != 1950 and num1 >= min_occurence:
                percent = (num2 * 100) / num1
                percentage_new = 100 - percent

                if percentage_new > percentage_old:
                    highest_percentage = round(percentage_new)
                    output_name = name
                    output_year = year - 1
                    percentage_old = percentage_new
                    output = (
                        output_name, output_year, int(highest_percentage))
            num1 = num2
    return output


def max_increase_for_each_year(dict):
    dictionary = dict
    output = []
    old_difference = 0
    output_name = 0

    keys = list(dictionary.keys())

    for year in dictionary[keys[0]]:
        for name in dictionary:

            if year > 1950 and name != "SOUČET":
                num2 = dictionary[name][year]
                num1 = dictionary[name][year - 1]
                difference = num2 - num1

                if difference > old_difference:
                    old_difference = difference
                    output_name = name

        if output_name is not 0:
            output.append(output_name)
        old_difference = 0

    return output


print(load_data_to_dictionary())
print(n_most_popular_for_given_year(load_data_to_dictionary(), 3, 2000))
print(most_popular_in_what_year(load_data_to_dictionary(), "DAVID"))
print(maximal_increase(load_data_to_dictionary(), "DAVID"))
print(maximal_decrease(load_data_to_dictionary(), 100))
print(max_increase_for_each_year(load_data_to_dictionary()))


########################################################################
#               Nasleduje kod testu,                                   #
########################################################################


def ib113_test_load_data_to_dictionary(dct):
    print("************* TEST LOAD DATA TO DICTIONARY *************")

    if not isinstance(dct, dict):
        print("NOK: Nebyla vracena promenna typu slovnik")
        return False

    input_data = [("IVAN", 1960), ("ANNA", 2000), ("ALENA", 1982),
                  ("DAVID", 1950), ("EVA", 2010), ("HANA", 2001),
                  ("ALENA", 1990), ("BARBORA", 1982)]
    output_data = [668, 1382, 1146, 9, 358, 504, 547, 1044]
    failure = False

    for i in range(len(input_data)):
        try:
            res = dct[input_data[i][0]][input_data[i][1]]
        except KeyError:
            print("NOK, data pravdepodobne nemaji spravnou strukturu. Nebylo "
                  "mozne ziskat data pro dotaz dictionary[%s][%d]" %
                  (input_data[i][0], input_data[i][1]))
            failure = True
            break

        if not isinstance(res, int):
            failure = True
            print("NOK, Nebyla vracena hodnota typu retezec, ale typu %s" %
                  type(res))
            failure = True
            break
        if res != output_data[i]:
            failure = True
            print("NOK: Data nemaji spravnou strukturu nebo nenacitaji data "
                  "koretne. Pro jmeno %s a rok %d byl vracem vysledek %d, ale"
                  " byl ocekavan vysledek %d" %
                  (input_data[i][0], input_data[i][1], res, output_data[i]))
            failure = True
            break

    if failure:
        return False
    print("OK")
    return True


def ib113_test_n_most_popular_for_given_year(dct):
    print("************* TEST N_MOST_POPULAR_FOR_GIVEN_YEAR *************")
    failure = False

    input_data = [(5, 1982), (10, 1982), (3, 2001)]
    output_data = [['JAN', 'PETR', 'MARTIN', 'LUCIE', 'TOMÁŠ'],
                   ['JAN', 'PETR', 'MARTIN', 'LUCIE', 'TOMÁŠ', 'JANA', 'JIŘÍ',
                    'MICHAL', 'PETRA', 'LENKA'], ['JAN', 'TOMÁŠ', 'JAKUB']]

    for i in range(len(input_data)):
        res = n_most_popular_for_given_year(dct, input_data[i][0],
                                            input_data[i][1])

        if not isinstance(res, list):
            failure = True
            print("NOK: Nebyla vracena hodnota typu list, ale typu %s" %
                  type(res))
            break
        if res != output_data[i]:
            failure = True
            print("NOK: Pro rok %d a pocet jmen %d byl vracen list %s, ale byl"
                  " ocekavan list %s" % (input_data[i][0], input_data[i][1],
                                         res, output_data[i]))
            break

    if not failure:
        print("OK")


def ib113_test_most_popular_in_what_year(dct):
    print("************* TEST MOST_POPULAR_IN_WHAT_YEAR *************")
    failure = False

    input_data = ["ABC", "DAVID", "EVA", "HANA", "ALENA", "BARBORA"]
    output_data = [None, 1979, 1955, 1956, 1955, 1993]

    for i in range(len(input_data)):
        res = most_popular_in_what_year(dct, input_data[i])

        if output_data[i] is None:
            if res is not None:
                failure = True
                print("NOK: Mela byt vracena hodnota None, ale byla vracena"
                      " jina hodnota typu %s)" % type(res))
                break
            continue

        if not isinstance(res, int):
            failure = True
            print("NOK: Pro jmeno %s nebyla vracena hodnota typu int, ale "
                  "typu %s" % (input_data[i], type(res)))
            break
        if res != output_data[i]:
            failure = True
            print("NOK: Pro jmeno %s byl vracen rok %d, ale byl ocekavan rok "
                  "%d." % (input_data[i], res, output_data[i]))
            break

    if not failure:
        print("OK")


def ib113_test_maximal_increase(dct):
    print("************* TEST MAXIMAL_INCREASE *************")
    failure = False

    input_data = ["ABC", "DAVID", "EVA", "HANA", "ALENA", "BARBORA"]
    output_data = [None, 1973, 1962, 1953, 1952, 1987]

    for i in range(len(input_data)):
        res = maximal_increase(dct, input_data[i])

        if output_data[i] is None:
            if res is not None:
                failure = True
                print("NOK: Mela byt vracena hodnota None, ale byla vracena"
                      " jina hodnota typu %s)" % type(res))
                break
            continue

        if not isinstance(res, int):
            failure = True
            print("NOK: Pro jmeno %s nebyla vracena hodnota typu int, ale "
                  "typu %s" % (input_data[i], type(res)))
            break
        if res != output_data[i]:
            failure = True
            print("NOK: Pro jmeno %s byl vracen rok %d, ale byl ocekavan rok "
                  "%d." % (input_data[i], res, output_data[i]))
            break

    if not failure:
        print("OK")


def ib113_test_maximal_decrease(dct):
    print(
        "************* TEST MAXIMAL_DECREASE *************")
    failure = False

    input_data = [50, 100, 400, 500, 1000]
    output_data = [("RADOMÍRA", 1971, 88), ("RADOMÍRA", 1971, 88),
                   ("ANETA", 2012, 63), ("ANETA", 2012, 63),
                   ("VOJTĚCH", 2012, 60)]

    for i in range(len(input_data)):
        res = maximal_decrease(dct, input_data[i])

        if not isinstance(res, tuple):
            failure = True
            print("NOK: Nebyla vracena hodnota typu tuple, ale typu %s" %
                  type(res))
            break

        if not isinstance(res[0], str) or not isinstance(res[1], int) or \
                not isinstance(res[2], int):
            failure = True
            print("NOK: Nebyla vracena hodnota typu tuple(str, int, int), ale "
                  "typu tuple(%s, %s, %s)" % (
                      type(res[0]), type(res[1]), type(res[2])))
            break

        if res[0] != output_data[i][0] or res[1] != output_data[i][1] or \
                        res[2] != output_data[i][2]:
            failure = True
            print("NOK: Pro minimalne pocet jmen %d bylo vraceno jmeno %s, "
                  "rok %d a pokles %d, ale bylo ocekavano jmeno %s, rok %d "
                  "a pokles %d." % (
                      input_data[i], res[0], res[1], res[2], output_data[i][0],
                      output_data[i][1], output_data[i][2]))
            break

    if not failure:
        print("OK")


def ib113_test_max_increase_for_each_year(dct):
    print("************* TEST MAX_INCREASE_FOR_EACH_YEAR *************")
    failure = False

    output_data = ["JIŘÍ", "JIŘÍ", "ALENA", "MIROSLAV", "ZDENĚK", "JANA",
                   "LUBOŠ", "DANA", "PETR", "PETR", "IVA", "PAVEL", "PAVEL",
                   "IVANA", "PAVLÍNA", "PETRA", "MARTIN", "MARTIN", "RADEK",
                   "MARTIN", "MARTIN", "RADKA", "MAREK", "PETRA", "TOMÁŠ",
                   "PETRA", "KATEŘINA", "MICHAELA", "LUKÁŠ", "LUCIE", "LUCIE",
                   "VERONIKA", "LUKÁŠ", "JAKUB", "LUCIE", "VERONIKA", "LUCIE",
                   "TOMÁŠ", "TEREZA", "JAKUB", "DAVID", "DANIEL", "KRISTÝNA",
                   "DOMINIK", "DOMINIK", "KRISTÝNA", "TEREZA", "DOMINIK",
                   "MATĚJ", "NATÁLIE", "ELIŠKA", "ADAM", "MATĚJ", "ADAM",
                   "ADAM", "JAKUB", "ADAM", "MATYÁŠ", "MATYÁŠ", "VOJTĚCH",
                   "SOFIE", "MATYÁŠ", "NEZJIŠTĚNO"]

    res = max_increase_for_each_year(dct)
    if not isinstance(res, list):
        failure = True
        print("NOK: Nebyla vracena hodnota typu list, ale typu %s" %
              type(res))
    elif len(res) != len(output_data):
        failure = True
        print("NOK: Seznam ma delku %d ale je ocekavana delka %d" % (
            len(res), len(output_data)))
    else:
        for i in range(len(res)):
            if res[i] != output_data[i]:
                failure = True
                print(
                    "NOK: Pro rok %d bylo vraceno jmeno %s, ale bylo ocekavano"
                    " jmeno %s" % (i + 1951, res[i], output_data[i]))
                break

    if not failure:
        print("OK")


# Hlavni funkce volana automaticky po spusteni programu.
if __name__ == '__main__':
    dct = load_data_to_dictionary()
    if ib113_test_load_data_to_dictionary(dct):
        ib113_test_n_most_popular_for_given_year(dct)
        ib113_test_most_popular_in_what_year(dct)
        ib113_test_maximal_increase(dct)
        ib113_test_maximal_decrease(dct)
        ib113_test_max_increase_for_each_year(dct)
