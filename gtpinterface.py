import sys

class GTPInterface(object):
    def __init__(self, agent):
        self.agent = agent

        commands = {"name": self.gtp_name,
                    "genmove": self.gtp_genmove,
                    "quit": self.gtp_quit,
                    "showboard": self.gtp_show,
                    "play": self.gtp_play,
                    "list_commands": self.gtp_list_commands,
                    "clear_board": self.gtp_clear,
                    "boardsize": self.gtp_boardsize,
                    "close": self.gtp_close}

        self.commands = commands

    def send_command(self, command):
        p = command.split()
        func_key = p[0]
        args = p[1:]

        # ignore unknow commands
        if func_key not in self.commands:
            return True, ""

        # call that function with parameters
        return self.commands[func_key](args)

    def gtp_name(self, args=None):
        return True, self.agent.name

    def gtp_list_commands(self, args=None):
        return True, self.commands.keys()

    def gtp_quit(self, args=None):
        if hasattr(self.agent, 'sess'):
            self.agent.sess.close()
        sys.exit()

    def gtp_clear(self, args=None):
        self.agent.reinitialize()
        return True, ""

    def gtp_play(self, args):
        # play black/white a1
        assert (len(args) == 2)
        player=args[0].lower()
        if not (player[0]=='b' or player[0]=='w'):
            return False, 'Player should be black or white'
        raw_move=args[1].strip()
        assert ord('a') <= ord(raw_move[0]) <= ord('a')+self.agent.boardsize
        assert 1 <= int(raw_move[1:]) <= self.agent.boardsize
        print(raw_move);
        ret=self.agent.play_move(player, raw_move) 

        #if not ret:
        #    return False, 'invalid input'

        return True, ""

    def gtp_genmove(self, args):
        """
        automatically detect who is to play
        """
        assert (args[0][0] == 'b' or args[0][0] == 'w')
        player=args[0]
        raw_move = self.agent.generate_move(player)
        _,board = self.gtp_show(args);
        print(board);
        return True, raw_move

    def gtp_boardsize(self, args=None):
        boardsize=int(args[0])
        assert (3<= boardsize <= 19)
        self.agent.set_boardsize(boardsize)
        return True, ""

    def gtp_show(self, args=None):
        int_game_state=[]
        j1=0
        j2=0
        for i in range(len(self.agent.black_int_moves)+len(self.agent.white_int_moves)):
            if i%2==0:
                int_move=self.agent.black_int_moves[j1] 
                j1 += 1
            else:
                int_move=self.agent.white_int_moves[j2]
                j2 += 1
            int_game_state.append(int_move)
        return True, state_to_str(int_game_state, self.agent.boardsize)

    def gtp_close(self, args=None):
        try:
            self.agent.sess.close()
        except AttributeError:
            pass
        return True, ""


def state_to_str(int_move_seq, boardsize):
    g=int_move_seq
    size=boardsize
    white = 'W'
    black = 'B'
    empty = '.'
    ret = '\n'
    coord_size = len(str(size))
    offset = 1
    ret+=' '*(offset+1)
    board=[None]*size
    for i in range(size):
        board[i]=[empty]*size

    for k, i in enumerate(g):
        x,y=i//size, i%size
        board[x][y]=black if k%2==0 else white

    PLAYERS = {"white": white, "black": black}
    for x in range(size):
        ret += chr(ord('A') + x) + ' ' * offset * 2
    ret += '\n'
    for y in range(size):
        ret += str(y + 1) + ' ' * (offset * 2 + coord_size - len(str(y + 1)))
        for x in range(size):
            if (board[x][y] == PLAYERS["white"]):
                ret += white
            elif (board[x][y] == PLAYERS["black"]):
                ret += black
            else:
                ret += empty
            ret += ' ' * offset * 2
        ret += white + "\n" + ' ' * offset * (y + 1)
    ret += ' ' * (offset * 2 + 1) + (black + ' ' * offset * 2) * size

    return ret

