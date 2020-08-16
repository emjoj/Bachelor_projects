from random import randint

column = -1
plan_rows = 0
plan_cols = 0
symbol = ""


def tictactoe(rows, cols, human_starts=True):
    computer_turn = True
    state = []
    check = "not ok"
    global plan_rows, column, symbol, plan_cols
    plan_rows = rows
    plan_cols = cols
    for row in range(rows):
        line = []
        for col in range(cols):
            line.append("  ")
        state.append(line)
    show_state(state)

    while is_won(state) == False:
        while check == "not ok":
            if human_starts == True:
                column = int(input("Zvolte prazdny stlpec na hracom plane"))
                while column < 0 or column >= cols:
                    column = int(input("Zvolte prazdny stlpec na hracom plane"))
                symbol = chr(120)
            elif computer_turn == True:
                column = strategy(state, chr)
                symbol = chr(111)
            check = valid_move(state)

        show_state(state)

        if human_starts == True:
            human_starts = False
            computer_turn = True
        elif computer_turn == True:
            human_starts = True
            computer_turn = False

        check = "not ok"
        win = is_won(state)

        if win == True:
            print("koniec hry, vyhral hrac so symbolom", symbol)
        elif win == "tie":
            print("nikto nevyhral")
    return


def is_won(state):
    amount_columns = 0
    diagonal_ascending = 0
    diagonal_descending = 0
    tie = 0
    for i in range(plan_rows - 1, -1, -1):
        if state[i][column] == symbol + " ":
            amount_columns += 1
            if amount_columns >= 4:
                return True
        else:
            amount_columns = 0

    for row in range(plan_rows):
        amount_rows = 0
        for col in range(plan_cols):
            if state[row][col] == symbol + " ":
                amount_rows += 1
                if amount_rows >= 4:
                    return True
            else:
                amount_rows = 0

    for row in range(plan_rows - 1, -1, -1):
        for col in range(plan_cols):
            if state[row][col] == symbol + " ":
                diagonal_ascending = 1
                diagonal_descending = 1

                for i in range(1, row + 1):
                    if (col + i) < plan_cols:
                        if state[row - i][col + i] == symbol + " ":
                            diagonal_ascending += 1
                            if diagonal_ascending >= 4:
                                return True
                        else:
                            diagonal_ascending = 0

                    if (col - i) > -1:
                        if state[row - i][col - i] == symbol + " ":
                            diagonal_descending += 1
                            if diagonal_descending >= 4:
                                return True
                        else:
                            diagonal_descending = 0

    for i in range(plan_cols):
        if state[0][i] != "  ":
            tie += 1
            if tie == plan_cols:
                return "tie"
    return False


def show_state(state):
    for element in state:
        for i in element:
            print(i, end=" ")
        print()

    for trial in range(plan_cols):
        print("-", end="  ")
    print()
    for number in range(plan_cols):
        if number < 10:
            print(number, end="  ")
        else:
            print(number, end=" ")
    print()


def strategy(state, chr):
    symbol = chr(111)
    computer_column = randint(0, plan_cols - 1)
    return computer_column


def valid_move(state):
    for i in range(plan_rows):
        if state[i][column] == "  ":
            for i in range(plan_rows - 1, -1, -1):
                if state[i][column] == "  ":
                    state[i][column] = symbol + " "
                    return "ok"
        return "not ok"


tictactoe(6, 6, human_starts=True)
