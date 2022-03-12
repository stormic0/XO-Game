class Player:
    def __init__(self, name):
        self.name = name
        self.winner = False


class XO:
    def __init__(self, size):
        self.size = size
        self.valid_range = range(size)
        self.end = False
        self.players = {}
        self.positions = []
        self.orders = []
        self.turn = 0

    def start(self):
        self._positions_initializer()

        player_count = int(input('How many players? '))

        for player_index in range(player_count):
            name = input(f'Please enter player {player_index+1} name: ')
            self.players[player_index] = Player(name)

        self.orders = [i for i in range(player_count)]

    def action(self):
        if not self.end:
            self._get_position()
            self._check_row()
            self._check_column()
            self._check_diagonal_and_no_winner()
            self._turn_handler()
            self._broadcast_game()

    def winner_announcement(self):
        winner = filter(lambda x: x.winner, self.players.values())
        if winner:
            print(f'{next(winner).name} won the game!')
        else:
            print('No winner!')

    def _check_row(self):
        for row in self.positions:
            if len(row) == row.count(row[0]) and row[0] is not None:
                self.players[row[0]].winner = True
                self.end = True
                break

    def _check_column(self):
        positions_copy = self.positions.copy()

        self.positions = []
        for j in range(self.size):
            self.positions.append([row[j] for row in positions_copy])

        self._check_row()

        self.positions = positions_copy

    def _check_diagonal_and_no_winner(self):
        val00_index = self.positions[0][0] if self.positions[0][0] else False
        val00 = []

        val0n_index = self.positions[0][self.size-1] if self.positions[0][self.size-1] else False
        val0n = []

        no_none = True

        for i in range(self.size):
            for j in range(self.size):
                if i == j:
                    if val00 is not None and val00 is not False and self.positions[i][j] == val00_index:
                        val00.append(self.positions[i][j])
                    else:
                        val00 = False

                if i == self.size - 1 - j:
                    if val0n is not None and val0n is not False and self.positions[i][j] == val0n_index:
                        val0n.append(self.positions[i][j])
                    else:
                        val0n = False

                if no_none and self.positions[i][j] is None:
                    no_none = False

        if val00:
            if len(val00) == self.size:
                self.players[val00[0]].winner = True
                self.end = True

        if val0n:
            if len(val0n) == self.size:
                self.players[val0n[0]].winner = True
                self.end = True

        if no_none:
            self.end = True

    def _broadcast_game(self):
        for row in self.positions:
            print(row)

    def _get_position(self):
        print(f'{self.players[self.turn].name} turn:')

        while 1:
            i, j = map(int, input().split(' '))

            if i in self.valid_range and j in self.valid_range:
                if self.positions[i][j] is None:
                    self.positions[i][j] = self.turn
                    break
                else:
                    print('This position is already taken! please choose another one!')
            else:
                print('Please choose a valid index!')

    def _turn_handler(self):
        if len(self.orders) - 1 == self.turn:
            self.turn = 0
        else:
            self.turn += 1

    def _positions_initializer(self):
        self.positions = [[None for i in range(self.size)] for j in range(self.size)]


def run():
    input_size = int(input('Please enter the size number: '))

    game = XO(input_size)
    game.start()

    while 1:
        game.action()

        if game.end:
            game.winner_announcement()
            restart = input('Do you want to play again? [y/n]').lower()
            if restart == 'n':
                break
            else:
                change_size = input('Do you want to change game size? [y/n]').lower()
                if change_size != 'n':
                    input_size = int(input('Please enter the size number: '))

                game.__init__(input_size)
                game.start()


if __name__ == '__main__':
    run()
