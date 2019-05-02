import random
import enchant
'''
DOWNLOADS NEEDED IN ORDER TO RUN:
pip install pyenchant


Scrabble Project Outline
----------------------

What we did:

-Ask player: Scrabble is a 2-4 player game so when you input 1 then we should repeat the question until they give us 2-4!


What we need to do:

-Draw for first play. The player with the letter closest to "A" plays first. A blank tile beats any letter. Return the letters to the pool and remix.
    -All players draw seven new letters and place them on their racks.
    -If two players tie for first, repeat
-Add function that allows the user to pull up the rules.txt file when needed
-Each word will go through a dictionary library to see if it is part of the english dictionary.
-We need to add the 1-15 y-axis and a-z for the top
-Fix score function to be dictionary

-If we need to tell the players how many tiles are left in the bag?
-Ask players if they want the word right or down

'''

players = {}
num_p = 0
letter_count = 98
alpha = "abcdefghijklmnopqrstuvwxyz"
order_of_the_players = []
dict = enchant.Dict("en_US")
word_placed = False
turns_taken = 0


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


def ask_player():
    '''
        Ask how many players are playing
        then makes a "score board" in dict
        in form of {Player #: score}
        0 < player # <= 4
    '''
    global num_p
    while (num_p < 1 or num_p > 4):
        num_p = int(input("How many players will there be? "))
    for i in range(int(num_p)):
        players.setdefault(i+1,[0,""])

def randomtile(basket_of_letters):
    '''
    12/8/17, Gives a random tile from the basket
    -use random.choice works with strings and lists
    -use the basket and multiple i and i+1 together to get a,2 to 'aa' then random.choice to get a random character
    Problem:
    Remove a tile from basket_of_letters
    

    Input:
    -Basket of letters
    Output:
    -Random character tile
    '''
    global letter_count
    
    newbasket='' #Empty string
    for i in range(len(basket_of_letters)-1):  #Index of each position 
        if type(basket_of_letters[i])==int:    #If the type of value is a int
            pass                               #Pass and move to else
        else: 
            newbasket+=(basket_of_letters[i]*basket_of_letters[i+1]) #Ex. Add the '##' from #,2 to the empty string\
    newtile=random.choice(newbasket)                    #Randomly choose a character from the newbasket
    index=basket_of_letters.index(newtile)              #Index of newtile in original basket 
    basket_of_letters[index+1]=basket_of_letters[index+1]-1       #Change the value of how many of the random letters there are -1.
    
    letter_count=letter_count-1                              #Subtract 1 tile from the letter_count
    
    return newtile  #Return a random tile
    



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


def add_word_across(board,word, row, col,p):

    '''
    Input: board, word, r, c
    Output: board with word on it
    '''
    
    global players                                            #Time to change the score
    
    scoreofword=score(word)
    sumofscore=0
    r = int(row)
    c = int(col)
    
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
        
    #print(p)
    for key in players:
        if key==p:
            (players[key][0])=players[key][0]+sumofscore
    
    #print(players)
    
    print_board(board)
        
def add_word_down(board,word,row,col,p):
    scoreofword=score(word)
    sumofscore=0
    r = int(row)
    c = int(col)
    
    global players                 #Time to change the score
    
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
    #print(score(word))
        
    for key in players:
        if key==p:
            (players[key][0])=players[key][0]+sumofscore
        
    print_board(board)
    
def check_hands(): # checks hands of each player
    global players
    not_empty = []
    for key,value in players.items():
        if len(value[1]) > 0: # if their hand is not empty then add it to a list of players
            not_empty.append(key) 
    return not_empty

def hand_out(): # hands out tiles initial hand 
    for key, value in players.items():
        i = 7
        while (i > 0):
            tile = randomtile(basket_of_letters)
            value[1] += tile
            i = i - 1
            
            
def order_players(): #order the players
    list_of_first_letters = []
    listofletters=[] #Empty list for letters
    letters_drawn = []
    for key, value in players.items():
        go = True
        while (go):
            first_let = randomtile(basket_of_letters)
            if (first_let in letters_drawn): # checks if letter has been drawn yet
                index = basket_of_letters.index(first_let)+1
                print(first_let)
                print(basket_of_letters.index(first_let))
                print("hello")
                basket_of_letters[index+1] += 1 #re add the count in basket_of letters_
            else:
                letters_drawn.append(first_let)
                list_of_first_letters.append(first_let) # adds drawn letter
                listofletters.append(first_let)
                
                list_of_first_letters.append(key) # adds player # it belongs to
                print("Player " + str(key) + " your first letter is " + first_let)
                go = False
        # so after this you have to check which one is closer to the letter a
        #print(list_of_first_letters.sort())                    Can't sort letters and numbers when they are together
 
    
    x=closest_to_a(listofletters,list_of_first_letters) #Use function closest_to_a to find first player
    for p in x:
        order_of_the_players.append(p)
    print("The order of the players is: "+ str(x)+ "\n")
    #y=(listofletters[x])                                   #Char closest to a
    #=list_of_first_letters.index(y)                        #Find where the letter closest to a is in the list_of_first_letters
  

def closest_to_a(listofletters,list_of_first_letters):
    '''
    Input: List of letters because ().sort does not work for numbers and letters in a list 
    Output: Index of the letter that is closest to a
    Problems: Does not give second or third or fourth closest to a
                However whoever is the first player u can remove their letter from listofletters so u can find the second player, third, etc
    '''
    l=[]
    x=[]
    c=[]
    for item in (listofletters):
        if item=='#':                         #Whoever gets blank gets to go first
            return '#'
        l.append(abs(ord('a')-ord(item)))      #finds the difference of each letter from a
    l.sort()                                              #Sort the list from lowest to highest
                                                #chr(#) to turn back to character
    for item in l:
        x.append((chr(item+97)))                   #Turn the numbers back to letters
    for item in (listofletters):
        if item=='#':
            c=['#']+c    
    for item in x:                                                                       
        c.append(list_of_first_letters[((list_of_first_letters.index(item))+1)])
        #Append the players who go first to last
    return c                     #Returns order of players from first to last
    

def exchange(tile, player_num):
    '''
    Exchanges a players player
    Input: Tile you want to exchange
    Output: Random tile
    '''
    global letter_count
    index=basket_of_letters.index(tile)              #Index of player's tile in basket_of_letters 
    basket_of_letters[index+1]=basket_of_letters[index+1]+1       #Change the value of how many of the random letters there are -1.
    letter_count=letter_count+1                                        #Since you are adding a letter back to the bad so add one
    p = players[player_num]
    oldstr = p[1]
    pos = oldstr.index(tile)
    newstr = oldstr[:pos] + oldstr[pos+1:]
    p[1] = newstr
    newtile = randomtile(basket_of_letters)
    p[1] = p[1] + newtile                #Return a new random tile to the player
    
    return newtile

def placeword(word,row,pos,align,p):
    '''
    Input: A word that you want on the board
    Output: Board itself with word on it, and your total points and how many points your word scored
    '''
    global board
    global players
    if align=='across':
        add_word_across(board,word,row,pos,p)
    if align=='down':
        add_word_down(board,word,row,pos,p)
        
    
    
def does_contains(w, hand):
    for let in w:
        if (let not in hand):
            return False
    if (dict.check(w)):
        return True
    else:
        return False

def main():
    alpha="abcdefghijklmnopqrstuvwxyz#"
    
    ask_player()
    order_players()
    hand_out()
    not_empty = check_hands()

    global board

    global turns_taken

    global basket_of_letters

    while(letter_count > 0 or len(not_empty) > 0): # condition to keep playing
        for p in order_of_the_players:
            if (p in not_empty): # can exchange, place, pass
                turn = players[p]
                word = ""
                turns_taken += 1
                if (len(word) <= 0):
                    print("Player " + str(p) + ": The current letters you have in your hand are: " + turn[1])
                    word = input("What do you want to do? You can place a word, exchange, or pass? (type 'place', 'exchange', 'pass') \n BE CAREFUL OF WHAT YOU CHOSE OR YOU CANNOT UNCHOOSE IT, IF YOU DON'T KNOW HOW TO SPELL YOU'RE TURN GETS SKIPPED ") 
                    word = word.lower()
                    if (word == "place"):
                        entered_word = ""
                        row = ""
                        num_row = 0
                        column = ""
                        num_column = 0
                        align = ""
                        while (len(entered_word) <= 0): 
                            entered_word = input("What word do you want to place? ")
                            if (does_contains(entered_word, turn[1])):    
                                if (isinstance(entered_word, str)):
                                    entered_word.lower()
                                else:
                                    entered_word = ""
                            else:
                                print("You can't make this word")
                                entered_word = ""
                        while (num_row <= 0):
                            row = input("Which row number do you want it? ")
                            if (isinstance(row, str)):
                                if (int(row) >= 0 or int(row) <= 16):
                                    num_row = int(row)
                                else:
                                    num_row = 0
                        while (len(column) <= 0):
                            column = input("Which letter column do u want it? ")
                            if (isinstance(column, str)):
                                if (len(column) == 1):
                                    column.lower()
                                else:
                                    column = ""
                            else:
                                column = ""     
                        while (len(align) <= 0):
                            align = input("Do you want the word across or down? ")
                            if (isinstance(align, str)):
                                align.lower()
                                if (align != 'across' and align != 'down'):
                                    align = ""
                            else:
                                align = ""
                        pos=(alpha.index(column)+1)                     #Index of the column in alpha (abcd...)
                        placeword(entered_word,row, pos, align,p)            #Call function placeword to put word on board
                        
                        #p is the whoever is the player's turn
                        
                        for key in players:                                      #Remove word from hand then adds back new tiles
                            if key==p:
                                for letter in entered_word:
                                    #print(letter)
                                    removeletter=players[key][1].replace(letter, "")
                                    index=players[key][1].index(letter)              #Index of letter in string
                                    players[key][1]=players[key][1][:index]+players[key][1][(index+1):]   #Remove that letter from the string
                                    
                                    players[key][1]=players[key][1]+randomtile(basket_of_letters)      #Adds random tile back to the hand
                                    
                                    #s = s[:pos] + s[(pos+1):]  Example to remove letter from string                                
                        
                        break                     
                    elif (word == "exchange"):
                        chose = "" # asks for chosen
                        while (len(chose) <= 0):
                            chose = input("Player " + str(p) + ": What tile do you want to exchange? ")
                            chose.lower()
                            if (chose in turn[1]):
                                newtile = exchange(chose, p)
                                print("Player " + str(p) + ": you got a letter: " + newtile)
                                print("Player " + str(p) + ": your hand is: " + turn[1])
                                another = ""
                                while (len(another) <= 0):
                                    another = input("Is there another word you want to exchange? (Enter 'yes' or 'no') ")
                                    another.lower()
                                    if (another =="yes"):
                                        chose = ""
                                    elif (another == "no"):
                                        pass
                                    else:
                                        another = ""
                            else:
                                chose = ""
                                print("That is not a valid letter!")
                    elif (word == "pass"):
                        pass
                    else:
                        word = ""
            print("\n")
    print("The game is finished!")
    scores = [] 
    for key, value in players.items():
        scores.append(value[1])
    max = scores[0]
    max_p = 0
    for i in range(len(scores)):
        if (scores[i] > max):
            max = scores[i]
            max_p = i
    print("The winner is: Player " + str(i) + "!")

board=make_scrabble_board()
print_board(board)
main()