from queue import Queue
from subprocess import PIPE, Popen, STDOUT
import time
import threading
import chess
import chess.svg
import re
from os import linesep

temp_board = chess.Board()


class EngineWriter(threading.Thread):
    def __init__(self, process, command_queue):
        super().__init__()
        self.process_stdin = process.stdin
        self.command_queue = command_queue
        self.daemon = True
    
    def run(self):
        while True:
            work = self.command_queue.get()
            self.process_stdin.write(f"{work}")
            print(work)
            self.process_stdin.flush()


class EngineReader(threading.Thread):
    def __init__(self, process, socketio):
        super().__init__()
        self.process = process
        self.daemon = True
        self.socketio = socketio
    
    def run(self):
        while self.process.poll() is None:
            output_str = self.process.stdout.readline()
            output_str= output_str.replace('\r','')
            output_str= output_str.replace('\n','')
            if "score cp " in output_str and "multipv" in output_str:
                # self.socketio.emit("analysis", {'analysis': output_str})
                analysis = re.search(' pv (.+?)$', output_str).group(1)
                self.socketio.emit("analysis", {'analysis': analysis})
                temp = temp_board
                san = analysis[0:4]
                self.socketio.emit("board", chess.svg.board(temp,lastmove=chess.Move.from_uci(san), flipped=True, size=600))
                # self.socketio.emit("board", chess.svg.board(temp,lastmove=chess.Move.from_uci(san), size=600))
                

class MoveReiceiver(threading.Thread):
    def __init__(self, work_queue: Queue, socketio):
        super().__init__()
        self.work_queue = work_queue
        self.socketio = socketio
        self.daemon = True
        self.last_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.command_queue = Queue()
        self.start_engine()

    def start_engine(self):
        self.current_process = Popen(
            "./Test_Stockfish/stockfish-ubuntu-20.04-x86-64",
            universal_newlines=True,
            stdout=PIPE,
            stdin=PIPE,
            stderr=STDOUT,
            bufsize=0, 
            shell=True
        )
        
        self.wr = EngineWriter(self.current_process, self.command_queue)
        self.er = EngineReader(self.current_process, self.socketio)

        self.wr.start()
        self.er.start()

        self.command_queue.put("uci\n")
        self.command_queue.put("isready\n")
        self.command_queue.put("setoption name MultiPV value 1\n")
        self.command_queue.put("setoption name Threads value 2\n")
        self.command_queue.put("setoption name Hash value 256\n")
        self.command_queue.put("setoption name Skill Level value 20\n")
        self.command_queue.put("go depth 8\n")
    
    def get_fen(self, work):
        work = work.replace("<div class=\"move-info-icon\" data-tooltip=\"En passant is a special pawn move by which a pawn captures another pawn that has advanced two squares.\"><span class=\"icon-font-chess circle-info\"></span></div>","")
        move_list = work.split("_")
        move_list = [ x for x in move_list if '.' not in x]
        board = chess.Board()
        for m in move_list:
            board.push_san(m)
        self.socketio.emit('new_fen', {'fen': board.fen()})

        if self.last_fen == board.fen():
            return
        self.last_fen = board.fen()
        global temp_board
        temp_board = board
        self.go_infite()

    def go_infite(self):
        try:
            self.command_queue.put(f"stop\n")
            self.command_queue.put(f"stop\n")
            self.command_queue.put(f"stop\n")
            self.command_queue.put(f"isready\n")
            self.command_queue.put(f"ucinewgame\n")
            time.sleep(0.2)
            self.command_queue.put(f"position fen {self.last_fen}\n")
            self.command_queue.put(f"go infinite\n")
        except Exception as error:
            print("go_infinite error:", error)
                

    def run(self):
        while True:
            work = self.work_queue.get()
            try:
                moves = work['moves']
                self.get_fen(moves)
            except Exception as error:
                print("MoveReceiver", error)