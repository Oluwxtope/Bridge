from playing import *
# import check


def score(bridge_game):
  '''
  Returns the score of a bridge game.
  
  score: Game -> Int
  
  Examples:
     P = [Player("North", []), Player("East", []),  
          Player("South", []), Player("West", [])]  
     G = Game([Bid("3", "NT"), None], "South", 
         "North", 9, P, False, False)
     score(G) => 400
     
     G = Game([Bid("4", "S"), None], "South", 
         "North", 11, P, False, True)
     score(G) => 450
  
     G = Game([Bid("4", "S"), Bid("double", None)], 
              "South", "North", 9, P, True, False)
     score(G) => -200 
  '''
  points = 0
  contract_suit = bridge_game.contract[0].suit
  contract_tricks = int(bridge_game.contract[0].value)
  declarer = bridge_game.declarer
  declarer_tricks = bridge_game.declarer_tricks
  tricks_made = declarer_tricks >= contract_tricks + 6
  mult = {"double": 2, "redouble": 4}
  north_south = ["North", "South"]
  
  if declarer in north_south:
    if bridge_game.ns_vulnerable:
      declarer_vul = True
    else: declarer_vul = False
  else:
    if bridge_game.ew_vulnerable:
      declarer_vul = True
    else:
      declarer_vul = False
  
  if contract_tricks == 6:
    slam = "small"
  elif contract_tricks == 7:
    slam = "grand"
  else:
    slam = None
  
  if tricks_made:
    
    ## contract points
    major = ["S", "H"] #30
    minor = ["D", "C"] #20
    contract_points = 0
    if contract_suit in major:
      contract_points += (30 * contract_tricks)
    elif contract_suit in minor:
      contract_points += 20 * contract_tricks
    else:
      first = True
      trick = contract_tricks
      while trick > 0:
        if first:
          contract_points += 40
          first = False
        else:
          contract_points += 30
        trick -= 1
    
    if bridge_game.contract[-1] != None:
      contract_points *= mult[bridge_game.contract[-1].value]
    
    if contract_points < 100:
      contract_points += 50
    else:
      if declarer_vul:
        contract_points += 500
      else: contract_points += 300
    
    ## overtrick points
    overtrick_points = 0
    overtricks = declarer_tricks - contract_tricks - 6
    if overtricks > 0:
      if bridge_game.contract[-1] == None:
        if contract_suit in minor:
          overtrick_points += (20 * overtricks)
        else: overtrick_points += (30 * overtricks)
      elif bridge_game.contract[-1].value == "double":
        if declarer_vul:
          overtrick_points += 200 * overtricks
        else:
          overtrick_points += 100 * overtricks
      else:
        if declarer_vul:
          overtrick_points += 400 * overtricks
        else:
          overtrick_points += 200 * overtricks
    
    ## Doubled/Redoubled Contract Made Bonus
    double_redouble_bonus = 0
    if bridge_game.contract[-1] != None:
      if bridge_game.contract[-1].value == "double":
        double_redouble_bonus += 50
      else:
        double_redouble_bonus += 100
    
    ## Slam Bonuses
    slam_bonus = 0
    if declarer_vul:
      if slam == "small":
        slam_bonus += 750
      elif slam == "grand":
        slam_bonus += 1500
    else:
      if slam == "small":
        slam_bonus += 500
      elif slam == "grand":
        slam_bonus += 1000

    return contract_points + overtrick_points + double_redouble_bonus + slam_bonus
  ## undertricks
  else:
    points = 0
    undertricks = 6 + contract_tricks - declarer_tricks
    first = True
    second = True
    third = True
    if declarer_vul:
      if bridge_game.contract[-1] == None:
        return points - (undertricks * 100)
      elif bridge_game.contract[-1].value == "double":
        if undertricks == 1:
          return points - 200
        else:
          return points - 200 - (300 * undertricks - 1)
      else:
        if undertricks == 1:
          return points - 400
        else:
          return points - 400 - (600 * undertricks - 1)
    else:
      if bridge_game.contract[-1] == None:
        return points - (undertricks * 50)
      elif bridge_game.contract[-1].value == "double":
        if undertricks == 1:
          return points - 100
        elif undertricks <= 3:
          return points - 100 - (200 * undertricks - 1)
        else:
          return points - 100 - (200 * 2) - (300 * (undertricks - 3))
      else:
        if undertricks == 1:
          return points - 200
        elif undertricks <= 3:
          return points - 200 - (400 * undertricks - 1)
        else:
          return points - 200 - (400 * 2) - (600 * (undertricks - 3))

'''
##Examples for score

P = [Player("North", []), Player("East", []),  Player("South", []), Player("West", [])]  
G = Game([Bid("3", "NT"), None], "South", "North", 9, P, False, False)
check.expect("Example 1", score(G), 400)

G = Game([Bid("4", "S"), None], "South", "North", 11, P, False, True)
check.expect("Example 2", score(G), 450)

G = Game([Bid("4", "S"), Bid("double", None)], "South", "North", 9, P, True, False)
check.expect("Example 3", score(G), -200)
'''

##To see the whole game in action, uncomment this to play!
print(score(play_game_bootstrap()))