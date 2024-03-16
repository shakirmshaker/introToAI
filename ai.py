import tkinter as tk
from functools import partial

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
        p = pit - 1
        stones = playerDown[p] 
        goal = 6
        bonus = goal - p - stones
    else:
        p = pit
        stones = playerUp[p] 
        goal = 0
        bonus = goal + p - stones
    
    if stones == 0:
        canvas.create_text(150, 210, text="There are no stones here. Pick another pit", font=("Arial", 10), fill='#B22222')
        return

    move(p, stones,current_player)
    update_board()

    if check_winner():
        canvas.create_text(150, 200, text=f"Winner: {get_winner()}", font=("Arial", 12), fill='#32CD32')
    else:
        if (bonus % 13 == 0):
            canvas.create_text(150, 230, text=f"Bonus Move! Play again player : {current_player}", font=("Arial", 10), fill='#4169E1')
            if current_player=='up':
                ai_move()
        else:
            current_player = 'up' if current_player == 'down' else 'down'
            canvas.create_text(150, 190, text=f"Playing now: {current_player}", font=("Arial", 10))
            if current_player == 'up':
                ai_move()  # AI makes its move automatically

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
            if(playerUp[pit]==1 and playerDown[pit]>0):
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


# AI functions
def ai_move():
    best_score = float('-inf')
    best_move = None
    for pit in range(1, 7):
        if playerUp[pit] != 0:
            new_playerUp = playerUp[:]
            new_playerDown = playerDown[:]
            new_playerUp, new_playerDown, bonus = ai_make_move(pit, new_playerUp, new_playerDown)
            score = minimax(new_playerUp, new_playerDown, 3, False)
            if score > best_score:
                best_score = score
                best_move = pit
                if bonus:
                    break  # Break if bonus move is found

    # If best_move is still None, choose the first available move
    if best_move is None:
        for pit in range(1, 7):
            if playerUp[pit] != 0:
                best_move = pit
                break

    # Perform the selected move
    print("ai clicks ", best_move)
    button_click(best_move)




def ai_make_move(pit, playerUp, playerDown):
    stones = playerUp[pit]
    if stones == 0:
        return playerUp, playerDown, False  # No bonus move

    playerUp[pit] = 0
    stones_left = stones
    current_pit = pit

    while stones_left > 0:
        current_pit = (current_pit + 1) % 14
        if current_pit == 0:
            current_pit += 1
        if current_pit < 6:
            playerUp[current_pit] += 1
            stones_left -= 1

    # Check if the last stone ends in the AI player's mancala
    if current_pit == 0:
        return playerUp, playerDown, True  # Bonus move for AI

    # Check if bonus move for the opponent is possible
    if current_pit != 6 and playerUp[current_pit] == 1 and playerDown[current_pit] != 0:
        playerUp[0] += playerDown[current_pit - 1] + playerUp[current_pit]
        playerDown[current_pit - 1] = 0
        playerUp[current_pit] = 0

    return playerUp, playerDown, False




def minimax(playerUp, playerDown, depth, maximizing_player):
    if depth == 0 or check_winner():
        return evaluate(playerUp, playerDown)

    if maximizing_player:
        max_eval = float('-inf')
        for pit in range(1, 7):
            if playerUp[pit] != 0:
                new_playerUp = playerUp[:]
                new_playerDown = playerDown[:]
                new_playerUp, new_playerDown, bonus = ai_make_move(pit, new_playerUp, new_playerDown)
                eval = minimax(new_playerUp, new_playerDown, depth - 1, bonus and maximizing_player)
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for pit in range(1, 7):
            if playerDown[pit] != 0:
                new_playerUp = playerUp[:]
                new_playerDown = playerDown[:]
                new_playerUp, new_playerDown, bonus = ai_make_move(pit, new_playerUp, new_playerDown)
                eval = minimax(new_playerUp, new_playerDown, depth - 1, bonus or not maximizing_player)
                min_eval = min(min_eval, eval)
        return min_eval


#strategy 1:incentivise choosing boards with more capture opportunites for yourself.
'''
def evaluate(playerUp, playerDown):
    # Get the number of stones in each player's mancala
    mancala_up = playerUp[0]
    mancala_down = playerDown[-1]

    # Calculate the difference in scores
    score_difference = mancala_up - mancala_down

    # Evaluate the potential for future moves (bonus move)
    bonus_up = 1 if playerUp[0] > 0 else 0
    bonus_down = 1 if playerDown[-1] > 0 else 0

    # Consider the balance of stones between players
    stones_balance = sum(playerUp) - sum(playerDown)

    # Consider the strategic importance of each pit
    strategic_importance_up = sum([(idx + 1) * stones for idx, stones in enumerate(playerUp[1:])])
    strategic_importance_down = sum([(idx + 1) * stones for idx, stones in enumerate(playerDown[::-1][1:])])

    # Calculate the difference in strategic importance between players
    strategic_difference = strategic_importance_up - strategic_importance_down

    # Additional factors
    # Adjust weights according to their importance
    mancala_weight = 1
    bonus_weight = 0.5
    balance_weight = 0.3
    strategic_weight = 0.2

    # Combine factors with adjusted weights
    evaluation = (mancala_weight * score_difference) + \
                 (bonus_weight * (bonus_up - bonus_down)) + \
                 (balance_weight * stones_balance) + \
                 (strategic_weight * strategic_difference)

    return evaluation
'''

#strategy 2
def evaluate(playerUp, playerDown):
    # Check if there's a move to pick up opponent's stones
    pick_up_score = 0
    for pit in range(1, 7):
        if playerUp[pit] == 1 and playerDown[pit] != 0:
            # Prioritize picking up opponent's stones based on the number of stones that can be picked up
            pick_up_score = playerDown[pit]

    if pick_up_score > 0:
        return pick_up_score

    # Calculate the difference in stones between players
    stones_up = sum(playerUp[1:])
    stones_down = sum(playerDown[:-1])

    # Evaluate the risk of getting picked up
    pick_up_risk = sum([stones for stones in playerUp[1:] if stones >= 2])

    # Evaluate the stones distribution to opponent's pits
    stones_to_opponent_pits = sum(playerDown[:3])

    # Evaluate the stones distribution to player's mancala
    stones_in_mancala = playerUp[0]

    # Evaluate the vulnerability of player's pits
    vulnerable_pits = sum([stones for stones in playerUp[1:4]])

    # Additional factors
    # Adjust weights according to their importance
    pick_up_weight = 0.4
    pick_up_risk_weight = 0.3
    stones_to_opponent_pits_weight = 0.1
    stones_in_mancala_weight = 0.1
    vulnerable_pits_weight = 0.1

    # Combine factors with adjusted weights
    evaluation = (pick_up_weight * pick_up_score) - \
                 (pick_up_risk_weight * pick_up_risk) - \
                 (stones_to_opponent_pits_weight * stones_to_opponent_pits) + \
                 (stones_in_mancala_weight * stones_in_mancala) - \
                 (vulnerable_pits_weight * vulnerable_pits)

    return evaluation





# Initialize UI
root = tk.Tk()
root.title("Kalaha Game")

canvas = tk.Canvas(root, width=300, height=260)
canvas.pack()

current_player = 'down'

for i in range(1, 7):
    button = tk.Button(root, text=str(i), command=partial(button_click, i))
    button.place(x=50 + 30 * i - 10, y=115)

update_board()

root.mainloop()
