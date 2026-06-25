def determine_tennis_winner(points):
    """
    Determines the winner of a tennis match based on the given sequence of points.
    
    Args:
        points: List of strings ("A" or "B") representing who won each point
    
    Returns:
        Dictionary with winner, final score, and game details
    """
    games_A = 0
    games_B = 0
    point_index = 0
    tiebreak_played = False
    tiebreak_score = None

    def play_game(points, start_index):
        score_A = 0
        score_B = 0
        idx = start_index
        while idx < len(points):
            winner = points[idx]
            idx += 1

            if winner == 'A':
                score_A += 1
            else:
                score_B += 1

            if score_A >= 3 and score_B >= 3:
                diff = score_A - score_B
                if diff >= 2:
                    return 'A', idx
                elif diff <= -2:
                    return 'B', idx
            else:
                if score_A >= 4:
                    return 'A', idx
                elif score_B >= 4:
                    return 'B', idx

        return None, idx

    def play_tiebreak(points, start_index):
        score_A = 0
        score_B = 0
        idx = start_index

        while idx < len(points):
            winner = points[idx]
            idx += 1

            if winner == 'A':
                score_A += 1
            else:
                score_B += 1

            if score_A >= 7 or score_B >= 7:
                diff = score_A - score_B
                if diff >= 2:
                    return 'A', idx, score_A, score_B
                elif diff <= -2:
                    return 'B', idx, score_A, score_B

        return None, idx, score_A, score_B

    def check_set_winner(games_A, games_B):
        if games_A >= 6 and games_A - games_B >= 2:
            return 'A'
        elif games_B >= 6 and games_B - games_A >= 2:
            return 'B'
        return None

    while point_index < len(points):
        # Check for tiebreak BEFORE playing the next game
        if games_A == 6 and games_B == 6:
            tb_winner, point_index, tb_A, tb_B = play_tiebreak(points, point_index)
            tiebreak_played = True
            tiebreak_score = (tb_A, tb_B)
            if tb_winner == 'A':
                games_A += 1
            elif tb_winner == 'B':
                games_B += 1
            break

        game_winner, point_index = play_game(points, point_index)
        if game_winner == 'A':
            games_A += 1
        elif game_winner == 'B':
            games_B += 1

        set_winner = check_set_winner(games_A, games_B)
        if set_winner:
            break

    match_winner = 'A' if games_A > games_B else 'B'

    result = {
        'winner': match_winner,
        'final_score': f"{games_A}-{games_B}",
        'games_A': games_A,
        'games_B': games_B,
        'tiebreak_played': tiebreak_played,
    }

    if tiebreak_played and tiebreak_score:
        result['tiebreak_score'] = f"{tiebreak_score[0]}-{tiebreak_score[1]}"

    return result


def format_result(result):
    print("=" * 40)
    print(f"  MATCH WINNER: Player {result['winner']}")
    print("=" * 40)
    print(f"  Final Score : {result['final_score']}")
    if result['tiebreak_played']:
        print(f"  Tiebreak    : {result['tiebreak_score']}")
    print("=" * 40)


# ─── Test Cases ───────────────────────────────────────────────────────────────

if __name__ == "__main__":

    def game_points(winner, loser):
        return [winner, winner, winner, winner]

    def deuce_game(winner, loser):
        return [winner, loser, winner, loser, winner, loser, winner, winner]

    # ── Test 1: Player A wins 6-0 ────────────────────────────────────────────
    print("\nTest 1: Player A wins 6-0")
    pts = []
    for _ in range(6):
        pts += game_points('A', 'B')
    print(pts)
    result = determine_tennis_winner(pts)
    format_result(result)
    assert result['winner'] == 'A'
    assert result['final_score'] == '6-0'

    # ── Test 2: Player B wins 0-6 ────────────────────────────────────────────
    print("\nTest 2: Player B wins 0-6")
    pts = []
    for _ in range(6):
        pts += game_points('B', 'A')
    print(pts)
    result = determine_tennis_winner(pts)
    format_result(result)
    assert result['winner'] == 'B'
    assert result['final_score'] == '0-6'

    # ── Test 3: Player A wins 7-5 ────────────────────────────────────────────
    print("\nTest 3: Player A wins 7-5")
    pts = []
    for _ in range(5):
        pts += game_points('A', 'B')
    for _ in range(5):
        pts += game_points('B', 'A')
    pts += game_points('A', 'B')
    pts += game_points('A', 'B')
    print(pts)
    result = determine_tennis_winner(pts)
    format_result(result)
    assert result['winner'] == 'A'
    assert result['final_score'] == '7-5'

    # ── Test 4: Tiebreak – A wins 7-6(3) ─────────────────────────────────────
    print("\nTest 4: Tiebreak – A wins 7-6(3)")
    pts = []
    for _ in range(6):
        pts += game_points('A', 'B')
        pts += game_points('B', 'A')
    pts += ['A', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'A']
    print(pts)
    result = determine_tennis_winner(pts)
    format_result(result)
    assert result['winner'] == 'A', f"Expected A, got {result['winner']}"
    assert result['final_score'] == '7-6', f"Expected 7-6, got {result['final_score']}"
    assert result['tiebreak_played'] is True
    assert result['tiebreak_score'] == '7-3', f"Expected 7-3, got {result['tiebreak_score']}"

    # ── Test 5: Deuce games – A wins 6-4 ─────────────────────────────────────
    print("\nTest 5: Deuce games – A wins 6-4")
    pts = []
    for _ in range(4):
        pts += deuce_game('A', 'B')
    for _ in range(4):
        pts += deuce_game('B', 'A')
    pts += deuce_game('A', 'B')
    pts += deuce_game('A', 'B')
    print(pts)
    result = determine_tennis_winner(pts)
    format_result(result)
    assert result['winner'] == 'A'
    assert result['final_score'] == '6-4'

    # ── Test 6: Tiebreak – B wins extended 8-6 ───────────────────────────────
    print("\nTest 6: Tiebreak – B wins extended tiebreak 8-6")
    pts = []
    for _ in range(5):
        pts += game_points('A', 'B')
    for _ in range(5):
        pts += game_points('B', 'A')
    pts += game_points('A', 'B')
    pts += game_points('B', 'A')
    # Tiebreak goes to 6-6 then B wins 8-6
    pts += ['A', 'B'] * 6   # 6-6
    pts += ['B', 'B']       # B wins 8-6
    print(pts)
    result = determine_tennis_winner(pts)
    format_result(result)
    assert result['winner'] == 'B'
    assert result['final_score'] == '6-7', f"Expected 6-7, got {result['final_score']}"
    assert result['tiebreak_played'] is True
    assert result['tiebreak_score'] == '6-8', f"Expected 6-8, got {result['tiebreak_score']}"

    print("\nAll tests passed!")