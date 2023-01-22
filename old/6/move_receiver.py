from queue import Queue
# from subprocess import PIPE, Popen
# import time
import threading
import chess
from stockfish import Stockfish

class MoveReiceiver(threading.Thread):

    def __init__(self, work_queue: Queue, socketio):
        super().__init__()
        self.work_queue = work_queue
        self.socketio = socketio
        self.daemon = True
        self.last_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.current_process = Stockfish("./Test_Stockfish/stockfish-ubuntu-20.04-x86-64")
        self.current_process.set_depth(5)#How deep the AI looks
        self.current_process.set_skill_level(10)#Highest rank stockfish
    
    def get_fen(self, work):
        move_list = work.split("_")
        move_list = [ x for x in move_list if '.' not in x]
        board = chess.Board()
        for m in move_list:
            board.push_san(m)
        self.socketio.emit('new_fen', {'fen': board.fen()})

        self.start_engine(board.fen())
    
    def start_engine(self, moves):
        process = self.current_process
        process.set_fen_position(moves)
        self.socketio.emit('analysis', {'analysis' : process.get_top_moves(5)})
     
    def run(self):
        while True:
            work = self.work_queue.get()
            try:
                moves = work['moves']
                self.get_fen(moves)
            except Exception as error:
                print("MoveReceiver", error)


# def encode_str(msg):
#     return msg.encode('utf-8')

# def decode_str(msg):
#     return msg.decode('utf-8')

# class EngineWriter(threading.Thread):

#     def __init__(self, process_stdin, command_queue):
#         super().__init__()
#         self.process_stdin = process_stdin
#         self.command_queue = command_queue
#         self.daemon = True
    
#     def run(self):
#         while True:
#             work = self.command_queue
#             self.process_stdin.write(encode_str(f"{work}"))
#             self.process_stdin.flush()

# class EngineReader(threading.Thread):

#     def __init__(self, process, socketio):
#         super().__init__()
#         self.process = process
#         self.daemon = True
#         self.socketio = socketio
    
#     def run(self):
#         while self.process.poll() is None:
#             output = self.process.stdout.readline()
#             output_str = decode_str(output)
#             output_str= output_str.replace('\r','')
#             output_str= output_str.replace('\n','')
#             if "score cp " in output_str and "multipv" in output_str:
#                 self.socketio.emit("analysis", output_str)

# class MoveReiceiver(threading.Thread):

#     def __init__(self, work_queue: Queue, socketio):
#         super().__init__()
#         self.work_queue = work_queue
#         self.socketio = socketio
#         self.daemon = True
#         self.last_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        # self.command_queue = Queue()
        # self.start_engine()

    # def start_engine(self):

    #     self.current_process = Popen(
    #         ["./Test_Stockfish/stockfish-ubuntu-20.04-x86-64"],
    #         stdout=PIPE,
    #         stdin=PIPE,
    #         bufsize=0, 
    #         shell=True
    #     )

        # self.current_process = Stockfish("./stockfish-ubuntu-20.04-x86-64")
        # self.current_process.set_depth(20)#How deep the AI looks
        # self.current_process.set_skill_level(20)#Highest rank stockfish
        
        # self.wr = EngineReader(self.current_process.stdin, self.command_queue)
        # self.er = EngineWriter(self.current_process, self.socketio)

        # self.wr.start()
        # self.er.start()

        # self.command_queue.put("uci\n")
        # self.command_queue.put("isready\n")
        # self.command_queue.put("setoption name MultiPV value 5\n")

    
    # def get_fen(self, work):
    #     move_list = work.split("_")
    #     move_list = [ x for x in move_list if '.' not in x]
    #     board = chess.Board()
    #     for m in move_list:
    #         board.push_san(m)
    #     self.socketio.emit('new_fen', {'fen': board.fen()})

        # if self.last_fen == board.fen():
        #     return
        # self.last_fen = board.fen()
        # self.go_infite()

    # def go_infite(self):
    #     try:
    #         self.command_queue.put(f"stop\n")
    #         self.command_queue.put(f"stop\n")
    #         self.command_queue.put(f"isready\n")
    #         self.command_queue.put(f"ucinewgame\n")
    #         time.sleep(0.2)
    #         self.command_queue.put(f"position fen {self.last_fen}\n")
    #         self.command_queue.put(f"go infinite\n")
    #     except Exception as error:
    #         print("go_infinite error:", error)
    
    # def run(self):
    #     while True:
    #         work = self.work_queue.get()
    #         try:
    #             moves = work['moves']
    #             self.get_fen(moves)
    #         except Exception as error:
    #             print("MoveReceiver", error)
