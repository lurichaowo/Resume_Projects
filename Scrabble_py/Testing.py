import enchant
import random
players = {}
num_p = 0
letter_count = 98
alpha = "abcdefghijklmnopqrstuvwxyz"
order_of_the_players = []
dict = enchant.Dict("en_US")


letter_score = {"aeioulnrst":"1", 
                "dg":"2", 
                "bcmp":"3", 
                "fhvwy":"4",
                "k":"5",
                "jx":"8",
                "qz":"10"}

basket_of_letters = ["a", 9, "b", 2, "c", 2, "d", 4, "e", 12, 
                    "f", 2, "g", 3, "h", 2, "i", 9, "j", 1,
                    "k", 1, "l", 4, "m", 2, "n", 6, "o", 8,
                    "p", 2, "q", 1, "r", 6, "s", 4, "t", 6, 
                    "u", 4, "v", 2, "w", 2, "x", 1, "y", 2, 
                    "z", 1]
                    
# '#'=Blank
TRIPLE_WORD_SCORE = ((0,0), (7, 0), (14,0), (0, 7), (14, 7), (0, 14), (7, 14), (14,14))
DOUBLE_WORD_SCORE = ((1,1), (2,2), (3,3), (4,4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4), (13,13), (12, 12), (11,11), (10,10), (7,7))
TRIPLE_LETTER_SCORE = ((1,5), (1, 9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13, 5), (13,9))
DOUBLE_LETTER_SCORE = ((0, 3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8, 12), (11,0), (11,7), (11,14), (12,6), (12,8), (14, 3), (14, 11))



def make_scrabble_board():
    '''
    Makes scrabble board
    12/7 9:45 pm UPDATE made it os board has numbers and letters on side
    '''
    board=[]
    
    for i in range(16):
        line=[] # each line of the board
        if (i != 0): # prints numbers on y axis of board
            if (i < 10): # helps align the single and double digit numbers ie 9 vs 10
                hello = str(i) + " " 
                line.append(hello)
            else:
                line.append(str(i))
        for j in range(16): 
            if (i ==0 and j ==0): # (0,0) is a " "
                line.append('  ')
            elif (i == 0 and  j < 17): #add letters to x axis
                line.append(alpha[j-1])
            elif (j < 15): #makes rest of board
                line.append('_')
        board.append(line)

    # adds the cap and lower letter to board vvv
    for r,c in TRIPLE_WORD_SCORE:
        board[r+1][c+1] = 'T' 

    for r,c in DOUBLE_WORD_SCORE:
        board[r+1][c+1] = 'D'

    for r,c in TRIPLE_LETTER_SCORE:
        board[r+1][c+1]='t'

    for r,c in DOUBLE_LETTER_SCORE:
        board[r+1][c+1] = 'd'
    return board


def print_board(b):  #Organizes the lines so it looks like a board
    for line in b:
        print (' '.join(line))

def score(w):
  '''
  Input: letter
  Output: Score of letter
  '''
  sum1=0
  for ch in w:
    if ch=='#':
        sum1+=0
    if ch.lower() in 'aeioulnrst':
      sum1+=1
    if ch.lower() in 'dg':
      sum1+=2
    if ch.lower() in 'bcmp':
      sum1+=3
    if ch.lower() in 'fhvwy':
      sum1+=4
    if ch.lower() in 'k':
      sum1+=5
    if ch.lower() in 'jx':
      sum1+=8
    if ch.lower() in 'qz':
      sum1+=10
  return sum1

def add_word_across(board,word,r,c):
    '''
    Input: board, word, r, c
    Output: board with word on it
    '''
    scoreofword=score(word)
    sumofscore=0
    print(word,r,c)
    
    for count, letter in enumerate(word): #Tell me the position of each letter in the word & the letter itself
        if board[r][c+count]=='T': #3*score of word
            sumofscore+=score(word)*3
            
        if board[r][c+count]=='D':#2*score of word
            sumofscore+=score(word)*2
            
        if board[r][c+count]=='t': #3*score of letter
            sumofscore+=score(word[count])*3
            
        if board[r][c+count]=='d': #2*score of letter
            sumofscore+=score(word[count])*2
            
        if board[r][c+count]=='_': #If square is _
            sumofscore+=score(word[count])
            
        board[r][c+count]=word[count]
        
    print(sumofscore)
    
    #print(score(word))
    print(print_board(board))

def add_word_down(board,word,r,c):
    scoreofword=score(word)
    sumofscore=0
    
    '''
    Input: board, word, r, c
    Output: board with word on it
    ''' 
    for count, letter in enumerate(word): #Tell me the position of each letter in the word & the letter itself
        if board[r+count][c]=='T': #3*score of word
            sumofscore+=score(word)*3
            
        if board[r+count][c]=='D':#2*score of word
            sumofscore+=score(word)*2
            
        if board[r+count][c]=='t': #3*score of letter
            sumofscore+=score(word[count])*3
            
        if board[r+count][c]=='d': #2*score of letter
            sumofscore+=score(word[count])*2
            
        if board[r+count][c]=='_': #If square is _
            sumofscore+=score(word[count])
        board[r+count][c]=word[count]

    print(sumofscore)
    
    #print(score(word))
    print(print_board(board))

def placeword(word,row,pos,align):
    '''
    Input: A word that you want on the board
    Output: Board itself with word on it, and your total points and how many points your word scored
    '''
    global board
    if align=='across':
        add_word_across(board,word,row,pos)
    if align=='down':
        add_word_down(board,word,row,pos)

board=make_scrabble_board()
#print_board(board)

#(add_word_across(board,'pay',8,6))

#placeword('pay',8,6,'across')
#placeword('ace',8,6,'across')

players={1: [0, 'uasaioe'], 2: [0, 'tzretpu']}
#for key, value in players.items():
#    print(value[1])

players={1: [0, 'aiofoea'], 2: [0, 'stragda']}
a=2
p=2
for key in players:
    if key==p:
        print(players[key][1])
        players[key][1]='test'

#change score

print(players[key][1])
print(players[key][1][:2])
                                
players[key][1]=players[key][1][:1]+players[key][1][(1+1):]
print(players)
print(players[key])
print(players[key][0])
