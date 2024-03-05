import tkinter as tk
from functools import partial
from termcolor import colored

playerUp = [0, 4, 4, 4, 4, 4, 4]
playerDown = [4, 4, 4, 4, 4, 4, 0]

def update_board():
    
    canvas.delete("all")
    canvas.create_text(150, 30, text="Kalaha Game", font=("Arial", 18))
    canvas.create_text(150, 60, text="First player: down", font=("Arial", 10))
    

    for i in range(1, 7):
        canvas.create_text(50 + 30 * i, 100, text=str(playerUp[i]), font=("Arial", 14), fill="#a95687")
        canvas.create_text(50 + 30 * i, 160, text=str(playerDown[i-1]), font=("Arial", 14), fill="#559e83")

    canvas.create_text(260, 130, text=str(playerDown[6]), font=("Arial", 14), fill="#559e83")
    canvas.create_text(50, 130, text=str(playerUp[0]), font=("Arial", 14), fill="#a95687")

def button_click(pit):
    global current_player
    if current_player == 'down':
        p = pit -1
        stones = playerDown[p] 
        goal = 6
        bonus = goal - p - stones
        
    else:
        p = pit
        stones = playerUp[p] 
        goal = 0
        bonus = goal + p - stones
    
    if stones == 0:
        canvas.create_text(150, 210, text="There are no stones here. Pick another pit", font=("Arial", 10),fill='#B22222')
        return

        
    move(p, stones, current_player)
    update_board()

    if check_winner():
        canvas.create_text(150, 200, text=f"Winner: {get_winner()}", font=("Arial",12),fill='#32CD32')
    else:
        if (bonus % 13==0):
            print('Bonus move!')
            canvas.create_text(150, 230, text=f"Bonus Move! Play again player : {current_player}", font=("Arial", 10),fill='#4169E1')
        else:
            current_player = 'up' if current_player == 'down' else 'down'
            canvas.create_text(150, 190, text=f"Playing now: {current_player}", font=("Arial", 10))

def check_winner():
    return sum(playerUp[1:]) == 0 or sum(playerDown[:-1]) == 0

def get_winner():
    upper_player = playerUp[0] + sum(playerUp[1:])
    down_player = playerDown[-1] + sum(playerDown[:-1])
    return "Player up" if upper_player > down_player else "Player down"

def move(p, stones, player):
    print(stones)
    if player == 'down':
        playerDown[p] = 0
        stones_left = stones - (6-p)
        for stone in range(stones):
            pit = p+stone+1
            playerDown[pit]= playerDown[pit] +1
            #print(p+stone+1)
            if(pit==6):
                break
        if(stones_left>0):
            up_moves(stones_left,player)
        elif (pit!=6):
            print('can I pick up?')
            #check if ou can pick up opponent's stones
            if(playerDown[pit]==1 and playerUp[pit]!=0):
                print('I can')
                #print('pick up from opponent')
                playerDown[6]=playerDown[6] + playerDown[pit] + playerUp[pit+1]
                playerDown[pit]=0
                playerUp[pit+1]=0
    else:
        print('initial pit ',p)
        print('stones in pit ',stones)
        playerUp[p] = 0
        stones_left = stones - p
        #pit = p
        for stone in range(stones):
            pit = (p - stone - 1)
            print('next pit ',pit)
            playerUp[pit]= playerUp[pit] +1
            if(pit==0):
                break
        if(stones_left>0):
            down_moves(stones_left,player)
        elif (pit!=0):
            print('can I pick up?')
            #check if you can pick up opponent's stones
            if(playerUp[pit]==1 and playerDown[pit]!=0):
                print('I can')
                #print('pick up from opponent')
                playerUp[0]=playerUp[0] + playerDown[pit-1] + playerUp[pit]
                playerDown[pit-1]=0
                playerUp[pit]=0
            

def up_moves(stones, player):
    pit = 6
    while stones > 0:
        if player == 'down' and pit == 0:
            break
        playerUp[pit] += 1
        pit -= 1
        stones -= 1
    if stones > 0:
        down_moves(stones, player)

def down_moves(stones, player):
    pit = 0
    while stones > 0:
        if player == 'up' and pit == 6:
            break
        playerDown[pit] += 1
        pit += 1
        stones -= 1
    if stones > 0:
        up_moves(stones, player)

# Initialize UI
root = tk.Tk()
root.title("Kalaha Game")

canvas = tk.Canvas(root, width=300, height=260)
canvas.pack()

current_player = 'down'



for i in range(1, 7):
    button = tk.Button(root, text=str(i), command=partial(button_click, i))
    #button.pack(side=tk.LEFT)
    button.place(x=50 + 30 * i - 10, y=115)
    


update_board()

root.mainloop()
