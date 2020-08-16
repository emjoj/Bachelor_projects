from random import randint


class Attack(object):

    def __init__(self, name, power, accuracy, stamina):
        self.name = name
        self.power = power
        self.accurancy = accuracy
        self.stamina = stamina

    def get_name(self):

        return self.name

    def get_power(self):

        return self.power

    def get_stamina(self):

        return self.stamina

    def is_hit(self):

        r = randint(0,100)
        if r <= self.accurancy:
            return True
        return False

    def count_hit(self):

        r = randint(80, 120)
        return int(self.power*(r/100))

    def __str__(self):

        return "{n}: Power = {p}, Accuracy = {a}, Stamina = {s},".format(n = self.name,p = self.power, a = self.accurancy, s = self.stamina)


# --------------------------------------------------------
#   Prisera
# --------------------------------------------------------
class Creature(object):

    def __init__(self, name, full_health, full_energy, speed, attacks):

        self.name = name
        self.full_health = full_health
        self.full_energy = full_energy
        self.speed = speed
        self.attacks = attacks
        self.health = full_health
        self.energy = full_energy


    def get_name(self):

        return self.name

    def get_health(self):

        return int(self.health)

    def get_energy(self):

        return int(self.energy)

    def get_speed(self):

        return self.speed

    def get_attack(self, option):

        if len(self.attacks) > option:
            return self.attacks[option]

        else:
            return None

    def get_random_attack(self):

        r = randint(0,len(self.attacks)-1)
        return r


    def decrease_health(self, wounds):

        if self.health - wounds < 0:
            self.health = 0
        else:
            self.health -= wounds


    def decrease_energy(self, effort):

        if self.energy - effort < 0:
            self.energy = 0
        else:
            self.energy -= effort

    def rest(self):

        if self.energy + self.full_energy//10 <= self.full_energy:
            self.energy += self.full_energy//10
        else:
            self.energy = self.full_energy


    def is_attack_makeable(self, attack):

        if attack.stamina <= self.energy:
            return True
        else:
            return False


    def is_dead(self):

        if self.health == 0:
            return True
        else:
            return False


    def get_lowest_attack_energy(self):

        x = []
        for i in range(len(self.attacks)):
           x.append(self.attacks[i].stamina)
        x.sort()
        return x[0]

    def resolve_hit(self, attack, defender):

        self.decrease_energy(self.attacks[attack].stamina)
        if self.attacks[attack].is_hit():
            wounds = self.attacks[attack].count_hit()
            defender.decrease_health(wounds)
            return int(wounds)

        return 0

    def print_attacks(self):

        for i in range(len(self.attacks)):
            print(self.attacks[i].name, end=" ")


    def __str__(self):

        return str(self.name)+ ":" + " Health = " + str(self.health) + "/" + str(self.full_health) + "  Energy " + str(self.energy) + "/" + str(self.full_energy)


# --------------------------------------------------------
#  Zapas
# --------------------------------------------------------\
class Match(object):

    def __init__(self, name, energy, health, speed, attack):
        self.name = name
        self.full_energy = energy
        self.full_health = health
        self.speed = speed
        self.attack = attack


class Match:
    def __init__(self, creatures, mode, players_creature):

        self.lst_of_creatures = creatures
        self.mode = mode
        self.players_creature = players_creature

    def run(self):

        game = True
        self.start_the_game()
        attacker = self.one_turn()
        while game != False:
            self.print_creatures_info(attacker)
            self.fight(attacker)
            attacker = self.change_of_players(attacker)
            if self.lst_of_creatures[attacker].is_dead():
                game = False
            else:
                input("Press ENTER to continue ...")


    def change_of_players(self,attacker):
        if attacker == 0:
            return 1
        else:
            return 0


    def start_the_game(self):
        print()
        print("=" * 35, "Match Game", "=" * 35 + "\n")
        print("The Match begins !")

    def print_creatures_info(self,player):
        print()
        print("=" * 35, self.lst_of_creatures[player].name, "Turn", "=" * 35 + "\n")
        print()
        for creature in range(len(self.lst_of_creatures)):
            print(self.lst_of_creatures[creature].__str__())
        print()

        for attack in range(len(self.lst_of_creatures[player].attacks)):
            print("["+ str(attack + 1)+"]",self.lst_of_creatures[player].attacks[attack].__str__())


    def get_option(self, attacker):
        if self.mode == 2 or self.players_creature == attacker:
            human = int(input("Choose an attack"))
            print(">> You have chosen", self.lst_of_creatures[attacker].attacks[human-1].name)
            return human - 1
        elif self.mode == 1 and self.players_creature != attacker:
            computer = self.lst_of_creatures[attacker].get_random_attack()
            print(">> Computer has chosen",self.lst_of_creatures[attacker].attacks[computer].name)
            return int(computer)


    def fight(self, attacker):
        print()
        self.lines()
        if self.check_energy(attacker):
            return
        attack = self.get_option(attacker)
        defender = self.enemy(attacker)

        if self.lst_of_creatures[attacker].is_attack_makeable(self.lst_of_creatures[attacker].attacks[attack]):
            wound = self.lst_of_creatures[attacker].resolve_hit(attack,self.lst_of_creatures[defender])
            if wound == 0:
                print(">>",self.lst_of_creatures[attacker].name,"missed",)

            else:
                if self.check_death(defender):
                    print(str(self.lst_of_creatures[defender].name) + " has been defeated. "
                          + str(self.lst_of_creatures[attacker].name)+ " is a winner !! ")
                else:
                    print(">>",self.lst_of_creatures[defender].name,"was hit and lost",wound,"points of health")
        else:
            self.lst_of_creatures[attacker].rest()
            print(">>", self.lst_of_creatures[attacker].name,
                  "does not have enough energy for this attack. \n>> He should take a rest")
        self.lines()

    def check_energy(self, attacker):
        if self.lst_of_creatures[attacker].energy < self.lst_of_creatures[attacker].get_lowest_attack_energy():
            self.lst_of_creatures[attacker].rest()
            print(">>", self.lst_of_creatures[attacker].name, "is having a nap")
            self.lines()
            return True


    def check_death(self,defender):
        if self.lst_of_creatures[defender].is_dead():
            return True
        return False



    def enemy(self,attacker):
        if attacker == 0:
            return 1
        else:
            return 0


    def one_turn(self):

        if self.lst_of_creatures[0].speed > self.lst_of_creatures[1].speed:
            return 0
        elif self.lst_of_creatures[0].speed == self.lst_of_creatures[1].speed:
            r = randint(0, 1)
            return r
        else:
            return 1

    def lines(self):
        print("-" * 45)


dragon_attacks = [
    Attack('Fire breath', 70, 40, 25),
    Attack('Kick', 20, 20, 10),
    Attack('Tail slash', 35, 80, 15),
    Attack('Tail twist', 50, 50, 20)]

spider_attacks = [
    Attack('Web', 25, 90, 15),
    Attack('Bite', 20, 50, 10),
    Attack('Acid splash', 40, 60, 20),]

dragon = Creature("Drogon", 80, 60, 10, dragon_attacks)
green_dragon = Creature("Viserion", 60, 85, 3, spider_attacks)


def test_choose_creature(creature_a, creature_b):
    print()
    print("\t name \t health  energy  speed")
    print("1. " ,creature_a.name," \t",creature_a.full_health,"\t",creature_a.full_energy,"\t",creature_a.speed)
    print("2. " ,creature_b.name,"\t",creature_b.full_health,"\t",creature_b.full_energy,"\t",creature_b.speed)
    return int(input("What creature should be yours?: "))


mode = int(input("Zadejte mod hry - (1) Single player (2) Multiplayer: "))
player = test_choose_creature(dragon, green_dragon)


match = Match([dragon, green_dragon], mode, player - 1)
match.run()


########################################################################
#               Nasleduje kod testu,                                   #
########################################################################

def test_is_hit():
    print("************* TEST IS_HIT *************")

    attack = Attack('Fire breath', 100, 50, 25)
    counter = 0

    for i in range(10000):
        if attack.is_hit():
            counter += 1

    if counter > 8000 or counter < 2000:
        print("NOK: Funkce vracila %d uspechu z 10000 ale melo by byt vraceno"
              " cca 5000 uspechu." % counter)
        return False

    print("OK")
    return True


def test_count_hit():
    print("************* TEST COUNT_HIT *************")

    attack = Attack('Fire breath', 100, 50, 25)
    if attack.get_power() <= 0:
        print("NOK: Test nelze spustit, jelikoz nefunguje funkce get_power.")
        return False

    for i in range(10000):
        actual_power = attack.count_hit()
        if actual_power < (0.8 * attack.get_power()) or actual_power > \
                (1.2 * attack.get_power()):
            print("NOK: Byla vracena hodnota utoku %d, ktera je mimo povolene "
                  "rozmezi %d-%d." % (actual_power,
                                      int(0.8 * attack.get_power()),
                                      int(1.2 * attack.get_power())))
            return False

    print("OK")
    return True


def test_get_attack():
    print("************* TEST GET_ATTACK *************")

    attacks = [Attack('Fire breath', 100, 50, 25),
               Attack('Ice breath', 100, 50, 25),
               Attack('Whirlwind', 100, 50, 25)]
    monster = Creature('Drogon', 200, 100, 9, attacks)

    if monster.get_attack(0) is None:
        print("NOK: Chyba pri vraceni utoku. Test nelze spustit, jelikoz"
              "get_attack vraci None.")
        return False

    for i in range(3):
            attack = monster.get_attack(i)
            if attack != attacks[i]:
                print("NOK: Chyba pri vraceni utoku. Byl ocekavan utok:\n"
                      "%s\n ale byl vracen utok:\n%s" % (attacks[i], attack))
                return False

    if monster.get_attack(4) is not None:
        print("NOK: Chyba pri vraceni utoku. Utok na indexu 4 neexistuje a"
              "mela byt vracena hodnota None")
        return False

    print("OK")
    return True


def test_get_random_attack():
    print("************* TEST GET_RANDOM_ATTACK *************")

    attacks = [Attack('Fire breath', 100, 50, 25),
               Attack('Ice breath', 100, 50, 25),
               Attack('Whirlwind', 100, 50, 25)]
    monster = Creature('Drogon', 200, 100, 9, attacks)

    attack = monster.get_random_attack()
    for i in range(1000):
        if attack is None:
            print("NOK: Pri volbe nahodneho utoku byla vracena hodnota None.")
            return False
        attack = monster.get_random_attack()

    counter = 0
    for i in range(1000):
        if monster.get_random_attack() == attack:
            counter += 1

    if counter > 990:
        print("NOK: Chyba pri vraceni nahodneho utoku. Byl ocekavan stale"
              "vracen stejny utok: %s" % (attacks[i], attack))
        return False

    print("OK")
    return True


def test_decrease_health():
    print("************* TEST DECREASE_HEALTH *************")

    monster = Creature('Drogon', 200, 100, 9,
                       [Attack('Fire breath', 100, 50, 25)])

    monster.decrease_health(50)
    if monster.get_health() != 150:
        print("NOK: Po snizeni o 50 zivotu nebyla vracena spravna hodnota "
              "aktualnich zivotu prisery. Byla ocekavana hodnota 150, ale "
              "byla vracena hodnota %d." % monster.get_health())
        return False

    monster.decrease_health(175)
    if monster.get_health() < 0:
        print("NOK: Po snizeni o 175 zivotu nebyla vracena spravna hodnota "
              "aktualnich zivotu prisery. Byla ocekavana hodnota 0, ale "
              "byla vracena hodnota %d." % monster.get_health())
        return False

    print("OK")
    return True


def test_decrease_energy():
    print("************* TEST DECREASE_ENERGY *************")

    monster = Creature('Drogon', 200, 100, 9,
                       [Attack('Fire breath', 100, 50, 25)])

    monster.decrease_energy(25)
    if monster.get_energy() != 75:
        print("NOK: Po snizeni o 25 energie nebyla vracena spravna hodnota "
              "aktualni energie prisery. Byla ocekavana hodnota 75, ale "
              "byla vracena hodnota %d." % monster.get_energy())
        return False

    monster.decrease_energy(175)
    if monster.get_energy() < 0:
        print("NOK: Po snizeni o 175 energie nebyla vracena spravna hodnota "
              "aktualni energie prisery. Byla ocekavana hodnota 0, ale "
              "byla vracena hodnota %d." % monster.get_energy())
        return False

    print("OK")
    return True


def test_rest():
    print("************* TEST REST *************")

    monster = Creature('Drogon', 200, 99, 9,
                       [Attack('Fire breath', 100, 50, 25)])

    monster.decrease_energy(11)
    monster.rest()
    if monster.get_energy() != 97:
        print("NOK: Problem ve funkci rest. Prisera se max_health rovno 99 a "
              "aktualni energii 88 by mela po odpocinku mit 97 energie. Ale "
              "byla vracena hodnota %d." % monster.get_energy())
        return False

    monster.rest()
    monster.rest()
    if monster.get_energy() > 99:
        print("NOK: Problem ve funkci rest. Prisera se max_health rovno 99 "
              "nemuze po odpocinku ziskat vice energie, nez je jeji maximul. "
              "Ale presto byla vracena hodnota %d." % monster.get_energy())
        return False

    print("OK")
    return True


def test_is_attack_makeable():
    print("************* TEST IS_ATTACK_MAKEABLE *************")

    attack = Attack('Fire breath', 100, 50, 40)
    monster = Creature('Drogon', 200, 100, 9, [attack])

    if monster.is_attack_makeable(attack) is not True:
        print("NOK: Neni mozne provest utok o energeticke narocnosti 40, "
              "presto, ze nestvura ma dostatek energie (100).")
        return False

    monster.decrease_energy(75)
    if monster.is_attack_makeable(attack) is True:
        print("NOK: Je mozne provest utok o energeticke narocnosti 40, "
              "presto, ze nestvura nema dostatek energie (25).")
        return False

    print("OK")
    return True


def test_is_dead():
    print("************* TEST IS_DEAD *************")

    attack = Attack('Fire breath', 100, 50, 40)
    monster = Creature('Drogon', 200, 100, 9, [attack])

    if monster.is_dead() is True:
        print("NOK: Prisera byla oznacena za mrtvou, prestoze ma %d zivotu."
              % monster.get_health())
        return False

    monster.decrease_health(199)
    if monster.is_dead() is True:
        print("NOK: Prisera byla oznacena za mrtvou, prestoze ma %d zivotu."
              % monster.get_health())
        return False

    monster.decrease_health(199)
    if monster.is_dead() is not True:
        print("NOK: Prisera nebyla oznacena za mrtvou, prestoze ma %d zivotu."
              % monster.get_health())
        return False

    print("OK")
    return True


def test_get_lowest_attack_energy():
    print("************* TEST GET_LOWEST_ATTACK_ENERGY *************")

    monster = Creature('Drogon', 200, 99, 9,
                       [Attack('Fire breath', 100, 50, 25)])
    if monster.get_lowest_attack_energy() != 25:
        print("NOK: Nebyl korektne vracen nejsnadnejsi utok - vracena byla"
              "hodnota %d, ale ocekavana byla hodnota 25."
              % monster.get_lowest_attack_energy())
        return False

    dragon_attacks = [
        Attack('Fire breath', 50, 40, 25),
        Attack('Kick', 10, 20, 10),
        Attack('Tail slash', 35, 80, 15),
        Attack('Tail twist', 50, 50, 20)
    ]
    monster = Creature('Drogon', 200, 100, 9, dragon_attacks)

    if monster.get_lowest_attack_energy() != 10:
        print("NOK: Nebyl korektne vracen nejsnadnejsi utok - vracena byla"
              "hodnota %d, ale ocekavana byla hodnota 10.")
        return False

    print("OK")
    return True


def test_resolve_hit():
    print("************* TEST RESOLVE_HIT *************")
    attacker = Creature('Drogon', 200, 100, 9,
                        [Attack('Fire breath', 100, 50, 25)])
    defender = Creature('Viserion', 150, 80, 9,
                        [Attack('Fire breath', 100, 50, 25)])

    old_health = defender.get_health()
    old_energy = attacker.get_energy()
    attack = attacker.get_random_attack()
    hit = attacker.resolve_hit(attack, defender)

    if defender.get_health() != old_health - hit:
        print("NOK: Nebyl korektne vracen vyresen utok - branici prisera"
              "mela byt poskozena o %d a mit tedy %d zivotu, ale ma jich %d."
              % (hit, old_health - hit, defender.get_health()))
        return False

    if attacker.get_energy() != old_energy - 25:
        print("NOK: Nebyl korektne vracen vyresen utok - utocici prisera"
              "mela mit energii snizenu o 25 a mit tedy %d energie, ale ma "
              "ji %d." % (old_energy - 25, defender.get_energy()))
        return False

    print("OK")
    return True


def test_choose_creature(creature_a, creature_b):
    print("1. " + str(creature_a))
    print("2. " + str(creature_b))
    return int(input("What creature should be yours?: "))


def test_main():
    dragon_attacks = [
        Attack('Fire breath', 50, 40, 25),
        Attack('Kick', 10, 20, 10),
        Attack('Tail slash', 35, 80, 15),
        Attack('Tail twist', 50, 50, 20)
    ]
    spider_attacks = [
        Attack('Web', 25, 90, 15),
        Attack('Bite', 10, 50, 10),
        Attack('Acid splash', 40, 60, 20),
    ]
    dragon = Creature("Drogon", 15, 20, 10, dragon_attacks)
    green_dragon = Creature("Viserion", 20, 175, 3, spider_attacks)

    mode = int(input("Zadejte mod hry - (1) Single player (2) Multiplayer: "))
    player = test_choose_creature(dragon, green_dragon)

    match = Match([dragon, green_dragon], mode, player - 1)
    match.run()


# Hlavni funkce volana automaticky po spusteni programu.
if __name__ == '__main__':
    initial_tests_correct = True
    initial_tests_correct = test_is_hit()
    initial_tests_correct = test_count_hit()
    initial_tests_correct = test_get_attack()
    initial_tests_correct = test_get_random_attack()
    initial_tests_correct = test_decrease_health()
    initial_tests_correct = test_decrease_energy()
    initial_tests_correct = test_rest()
    initial_tests_correct = test_is_attack_makeable()
    initial_tests_correct = test_is_dead()
    initial_tests_correct = test_get_lowest_attack_energy()
    initial_tests_correct = test_resolve_hit()

    if initial_tests_correct:
        print("***** Spoustim zkusebni hru *****")
        test_main()