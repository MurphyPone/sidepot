from collections import defaultdict

def compute_payouts(players, boards):
    """
    players: list of dicts with fields:
        - 'name': str
        - 'bet': int (amount committed to pot)
        - 'hands': list of hand strengths (one per board, higher is better)
    boards: int (number of boards)
    
    returns: dict {player_name: payout}
    """
    
    # Step 1: build side pots
    bets = sorted(set(p['bet'] for p in players))
    pots = []
    prev = 0
    for b in bets:
        contributors = [p for p in players if p['bet'] >= b]
        amount = (b - prev) * len(contributors)
        pots.append({
            'amount': amount,
            'contributors': [p['name'] for p in contributors]
        })
        prev = b
    
    # Step 2: divide each pot across boards
    for pot in pots:
        pot['per_board'] = pot['amount'] / boards
    
    # Initialize payouts
    payouts = defaultdict(int)
    
    # Step 3: award pots board by board
    for board in range(boards):
        for pot in pots:
            contenders = [p for p in players if p['name'] in pot['contributors']]
            # get best score for this board
            max_score = max(p['hands'][board] for p in contenders)
            winners = [p for p in contenders if p['hands'][board] == max_score]
            
            print(pot['per_board'] / len(winners))
            share = pot['per_board'] / len(winners)
            
            for w in winners:
                payouts[w['name']] += share
    
    # Convert to integers (handling fractions cleanly)
    # If chips must be whole numbers, distribute remainders fairly
    payouts = {k: float(v) for k, v in payouts.items()}
    return payouts


players = [
    {'name': 'Alice', 'bet': 50, 'hands': [10, 12]},  # two boards
    {'name': 'Bob',   'bet': 100, 'hands': [11, 9]},
    {'name': 'Carol', 'bet': 200, 'hands': [8, 14]},
]

payouts = compute_payouts(players, boards=2)
print(payouts)