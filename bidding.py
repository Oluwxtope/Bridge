from dealing import *
# import check


class Bid:
  '''
  Fields:
     value (Str)
     suit (anyof Str None)
  Requires:
     value is one of "1", "2", "3", "4", "5", "6", "7", 
         "pass", "double", "redouble"
     suit is one of "C", "D", "H", "S", "NT" or None
     If value is non-numeric, then suit must be None
  '''
  
  def __init__(self, bid_value, bid_suit):
    '''
    Initialized a valid Bridge bid.
   
    Effects: Mutates self
  
    __init__: Bid Str (anyof Str None) -> None
    Requires: Conditions from Fields above are met.
    '''
    self.value = bid_value
    self.suit = bid_suit

  def __repr__(self):
    '''
    Returns a representation of a Card object
  
    __repr__: Card -> Str
    '''
    if self.suit == None:
      return "{0.value}".format(self)
    return "{0.value}{0.suit}".format(self)
    
  def __eq__(self, other):
    '''
    Returns True if self and other have equal values and suits 
    and False otherwise
  
    __eq__: Bid Any -> Bool
    '''
    return (isinstance(other, Bid) and self.value == other.value and
            self.suit == other.suit)
  
  def __lt__(self, other):
    '''
    Returns True if both self and other are numeric bids and
    self is a bid that comes before other. False otherwise
  
    __lt__: Bid Any -> Bool
    '''
    ## ♣, ♦, ♥, ♠ and lastly, "no trump" 
    if (isinstance(other, Bid) and self.value.isdigit() and
            other.value.isdigit()):
      if self == other:
        return False
      else:
        ranking = {"C": 1, "D": 2, "H": 3, "S": 4, "NT": 5}
        if self.value == other.value:
          return ranking[self.suit] < ranking[other.suit]
        else:
          return self.value < other.value
    return False
  
  
def valid_bid(bids, new_bid):
  '''
  Returns True if new_bid is allowed in a Bridge
  game given the previous bids in bids. False otherwise
  
  valid_bid: (listof Bid) Bid -> Bool
  Requires: 
     For all k from 0 to len(bids) - 1,
       valid_bid(bids[:k], bids[k]) => True
  
  Examples:
     valid_bid([],Bid("pass", None)) => True
     valid_bid([Bid("pass", None), Bid("pass", None), 
                 Bid("pass", None)], Bid("pass", None)) 
                  => True 
     valid_bid([Bid("1", "C"), Bid("pass", None), 
                 Bid("pass", None), Bid("pass", None)], 
                  Bid("pass", None)) => False
     valid_bid([Bid("7", "NT")], Bid("2", "H")) => False
     valid_bid([Bid("1", "C"), Bid("pass", None)], 
                 Bid("double", None)) => False
     valid_bid([Bid("1", "C"), Bid("pass", None), 
                 Bid("pass", None)], Bid("double", None)) 
                   => True
  '''
  if new_bid.value == "pass":
    if len(bids) >= 3:
      if len(bids) == 3 and bids == [Bid("pass", None), Bid("pass", None), 
                                     Bid("pass", None)]:
        return True
      elif bids[-3:] == [Bid("pass", None), Bid("pass", None), 
                         Bid("pass", None)]:
        return False
      return True
    return True
  elif new_bid.value == 'double':
    if bids == []:
      return False
    else:
      count = 1
      for pos in range(-1, -len(bids) - 1, -1):
        if bids[pos].value == "pass":
          count += 1
        elif bids[pos].value == "double":
          return False
        elif bids[pos].value == "redouble":
          return False
        elif bids[pos].value.isnumeric():
          if count % 2 != 0:
            return True
          else:
            return False
      return False
  elif new_bid.value == "redouble":
    if bids == []:
      return False
    else:
      count = 1
      for pos in range(-1, -len(bids) - 1, -1):
        if bids[pos].value == "pass":
          count += 1
        elif bids[pos].value.isnumeric():
          return False
        elif bids[pos].value == "double":
          if count % 2 != 0:
            return True
          else:
            return False
        elif bids[pos].value == "redouble":
          return False
      return False
  else:
    if bids == []:
      return True
    else:
      for pos in range(-1, -len(bids) - 1, -1):
        if bids[pos].value.isnumeric():
          return bids[pos] < new_bid 
      return True
    
def bidding_complete(bids):
  '''
  Returns True if bids represents a complete contract and False otherwise
  
  bidding_complete: (listof Bid) -> Bool
  Requires: 
     For all k from 0 to len(bids) - 1,
       valid_bid(bids[:k], bids[k]) => True 
  
  Examples:
     bidding_complete([Bid("pass", None), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) => True
     bidding_complete([Bid("1", "C"), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) => True
     bidding_complete([Bid("1", "C"), Bid("3", "NT"), 
                Bid("pass", None), Bid("pass", None)]) => False
  '''
  if bids == [Bid("pass", None), Bid("pass", None), 
              Bid("pass", None), Bid("pass", None)]:
    return True
  elif len(bids) >= 4:
    for pos in range(-1, -4, -1):
      if bids[pos].value != "pass":
        return False
    return True
  return False

  
def contract(bids):
  '''
  Returns the contract to be played, including any doubling 
  or redoubling that occurred.
  
  contract: (listof Bid) -> (list Bid (anyof Bid None))
  Requires: 
     For all k from 0 to len(bids) - 1,
       valid_bid(bids[:k], bids[k]) => True 
     bidding_complete(bids) => True
  
  Examples:
     contract([Bid("pass", None), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)])
                  => [Bid("pass", None), None]
     contract([Bid("1", "C"), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) 
                  => [Bid("1", "C"), None]
     contract([Bid("1", "C"), Bid("double", None), 
                Bid("pass", None), Bid("pass", None), 
                Bid("pass", None)]) 
                  => [Bid("1", "C"), Bid("double", None)]
     contract([Bid("1", "C"), Bid("double", None), 
                Bid("redouble", None), Bid("pass", None),
                Bid("pass", None),  Bid("pass", None)]) 
                 => [Bid("1", "C"), Bid("redouble", None)]
     contract([Bid("1", "C"), Bid("double", None), 
                Bid("redouble", None), Bid("1", "S"), 
                Bid("pass", None), Bid("pass", None), 
                Bid("pass", None)]) => [Bid("1", "S"), None]
  '''
  if bids == [Bid("pass", None), Bid("pass", None), 
              Bid("pass", None), Bid("pass", None)]:
    return [bids[-1], None]
  else:
    contract = [None, None]
    for pos in range(-1, -(len(bids)) - 1, -1):
      if bids[pos].value == "redouble":
        contract[-1] = bids[pos]
      elif bids[pos].value == "double":
        if contract[-1] == None:
          contract[-1] = bids[pos]
      elif bids[pos].value.isnumeric():
        contract[0] = bids[pos]
        return contract
          



##PROVIDED FUNCTIONS BELOW - DO NOT CHANGE
  
def declarer(starting_team, bids):
  '''
  Returns who the declarer is given the starting_team
  and the bids. Returns None if all passed contract.
  
  declarer: Str (listof Bid) -> (anyof Str None)
  Requires:
     starting_team is one of "North", "East", "South" or "West"
     For all k from 0 to len(bids) - 1,
       valid_bid(bids[:k], bids[k]) => True 
     bidding_complete(bids) => True
     
  Examples:
     declarer("North", [Bid("pass", None), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) => None
     declarer("North", [Bid("1", "C"), Bid("pass", None), 
                Bid("pass", None), Bid("pass", None)]) => "North" 
     declarer("North", [Bid("1", "C"), Bid("2", "C"),
                Bid("3", "C"), Bid("pass", None),
                Bid("pass", None), Bid("pass", None)]) => "North"
  '''
  all_pass = [Bid("pass", None)]*4
  if all_pass == bids:
    return None
  deal_contract = contract(bids)
  players = ["North", "East", "South", "West"]
  winning_team = None
  cur_dir = starting_team
  for i in bids:
    if i == deal_contract[0]:
      winning_team = cur_dir
    cur_dir = players[(players.index(cur_dir) + 1) % len(players)]
    
  winning_team = [winning_team, 
                  players[(players.index(winning_team) + 2) % len(players)]]
  cur_dir = starting_team
  for i in bids:
    if i.suit == deal_contract[0].suit and cur_dir in winning_team:
      return cur_dir
    cur_dir = players[(players.index(cur_dir) + 1) % len(players)]



def bidding_bootstrap(deck = []):
  '''
  Performs a deal and bidding sequence for Bridge.
  Bids should be made of the format #S, pass, double or redouble 
  where # is a number from 1 to 7 and S is a suit C, D, H, S, NT.
  
  bidding_bootstrap: [(listof Nat)] -> (list Player Player Player Player)
  Requires:
     1 <= deck[i] <= 52 for all indices i.
  '''
  SUITS = ['C', 'D', 'H', 'S', 'NT']
  players = deal_bootstrap(deck) #From a10q1
  invalid_response = "Invalid response."
  invalid_bid_response = "Invalid bid."
  bid_prompt = "Please enter a valid bid for {0}: "
  odd_bids = ['pass', 'double', 'redouble']   
  bids = []
  num_players = len(players)
  starting_player = num_players - 1
  while not bidding_complete(bids):
    print("{0}'s hand: ".format(players[starting_player].name))
    display_hand(players[starting_player].hand)
    bid = input(bid_prompt.format(players[starting_player].name))
    
    def good_bid_input(bid):
      '''
      Local helper function to determine a good bid
    
      good_bid_input: Str -> Bool
      '''      
      num = bid[0]
      suit = bid[1:]
      if bid in odd_bids:
        return True
      elif num not in ['1', '2', '3', '4', '5', '6', '7'] or \
        suit not in SUITS:
        return False
      return True
    
    while not good_bid_input(bid):
      print(invalid_response)
      print("{0}'s hand: ".format(players[starting_player].name))
      display_hand(players[starting_player].hand)
      bid = input(bid_prompt.format(players[starting_player].name))  
    if bid in odd_bids:
      bid = Bid(bid, None)
    else:
      num = bid[0]
      suit = bid[1:]      
      bid = Bid(num, suit)
    if not valid_bid(bids, bid):
      print(invalid_bid_response)
    else:
      bids.append(bid)
      starting_player = (starting_player + 1) % num_players
  return [players, bids]
    

'''
## Examples for __eq__
c = Bid("1", "C")
d = Bid("1", "D")
e = Bid("1", "C")
f = Bid("pass", None)
g = Bid("2", "C")
check.expect("Test unequal", c == d, False)
check.expect("Test equal", c == e, True)
check.expect("Test against pass", c == f, False)

## Examples for __lt__
check.expect("Test lt true", c < d, True)
check.expect("Test lt false", c < e, False)
check.expect("Test lt pass", c < f, False)
check.expect("Test lt pass", c < g, True)

## Examples for Valid Bid

check.expect("Test on empty", valid_bid([],Bid("pass", None)), True)
check.expect("Test on empty double", valid_bid([],Bid("double", None)), False)
check.expect("Test on empty redouble", 
             valid_bid([],Bid("redouble", None)), False)
check.expect("Test all pass", 
             valid_bid([Bid("pass", None), Bid("pass", None), 
                        Bid("pass", None)], Bid("pass", None)), True)
check.expect("Test passes after bid",
             valid_bid([Bid("1", "C"), Bid("pass", None), 
                        Bid("pass", None), Bid("pass", None)], 
                        Bid("pass", None)), False)
check.expect("Test bid after max", valid_bid([Bid("7", "NT")],
                                              Bid("2", "H")), False)

check.expect("Test invalid double", 
             valid_bid([Bid("1", "C"), Bid("pass", None)], 
                       Bid("double", None)), False)
check.expect("Test valid double", 
valid_bid([Bid("1", "C"), Bid("pass", None), Bid("pass", None)], 
          Bid("double", None)), True)

## Examples contract


check.expect("Test all pass", 
             contract([Bid("pass", None), Bid("pass", None), 
                       Bid("pass", None), Bid("pass", None)]),
            [Bid("pass", None), None])


check.expect("Test simple contract", 
             contract([Bid("1", "C"), Bid("pass", None), 
           Bid("pass", None), Bid("pass", None)]) ,
             [Bid("1", "C"), None])

check.expect("Test simple doubled", 
             contract([Bid("1", "C"), Bid("double", None), 
                       Bid("pass", None), Bid("pass", None), 
                       Bid("pass", None)]) ,
             [Bid("1", "C"), Bid("double", None)])

check.expect("Test simple redoubled", 
             contract([Bid("1", "C"), Bid("double", None), 
                       Bid("redouble", None), Bid("pass", None),
                       Bid("pass", None),  Bid("pass", None)]) ,
             [Bid("1", "C"), Bid("redouble", None)])

check.expect("Test simple redoubled rebid", 
             contract([Bid("1", "C"), Bid("double", None), 
                       Bid("redouble", None), Bid("1", "S"), 
                       Bid("pass", None), Bid("pass", None), 
                       Bid("pass", None)]),
             [Bid("1", "S"), None])
             
## Examples Declarer

check.expect("Test all pass", 
             declarer("North",
                      [Bid("pass", None), Bid("pass", None), 
                       Bid("pass", None), Bid("pass", None)]),
             None)

check.expect("Test Simple 1C", 
declarer("North", [Bid("1", "C"), Bid("pass", None), 
           Bid("pass", None), Bid("pass", None)]), "North")

check.expect("Test Simple 3C", 
declarer("North", [Bid("1", "C"), Bid("2", "C"),
           Bid("3", "C"), Bid("pass", None),
           Bid("pass", None), Bid("pass", None)]), "North")
           

## Examples bidding_complete

check.expect("Example empty", bidding_complete([]), False)
check.expect("Example all-pass",
             bidding_complete([Bid("pass", None), Bid("pass", None), 
                               Bid("pass", None), Bid("pass", None)]), True)
check.expect("Example bid three pass", 
             bidding_complete([Bid("1", "C"), Bid("pass", None), 
                               Bid("pass", None), Bid("pass", None)]), True)
check.expect("Example incomplete", 
             bidding_complete([Bid("1", "C"), Bid("3", "NT"), 
                        Bid("pass", None), Bid("pass", None)]), False)
'''