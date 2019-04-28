import socket
import pickle
import numpy as np
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--IP', dest = 'IP', default  = 'localhost', help = 'IP address of server')
parser.add_argument('--port', dest = 'port', default  = 10000, type=int, help = 'port of the server')
parser.add_argument('--player', dest = 'player', default  = 1, type=int, help = 'Player ID number (1 or 2)')
parser.add_argument('--random', dest = 'random', default  = True, type=bool, help = 'Play a random brainless game')

args = parser.parse_args()

# starting data dict
data=dict(A=np.zeros((15,15),dtype=int),
          who_is_next = 5, 
          end_of_game = False, 
          succesful_update = True)


def suggest_random_step(A):
    '''Method for suggesting a brainless next step.'''
    zx,zy=np.where(A==0)
    if len(zx)==0:
        return [0,0]
    i=np.random.randint(len(zx))
    return [zx[i],zy[i]]

while not(data['end_of_game']):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.connect((args.IP, args.port))
        # Send data
        query_from_player = dict(pos=suggest_random_step(data['A']),player=args.player)
        sock.sendall(pickle.dumps(query_from_player))  
        data = pickle.loads(sock.recv(8192))
        sock.close()
    except:
        print('Server disconected.. end of game')
        break

