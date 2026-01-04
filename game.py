from dataclasses import dataclass
from typing import Optional
import random


@dataclass
class GameState:
    round_no: int = 0
    user_score: int = 0
    bot_score: int = 0
    user_used_bomb: bool = False
    bot_used_bomb: bool = False
    max_rounds: int = 3


def validate_move(move: str, bomb_used: bool) -> Optional[str]:
    allowed = {"rock", "paper", "scissors", "bomb"}

    if move not in allowed:
        return None

    if move == "bomb" and bomb_used:
        return None

    return move


def resolve_round(user: str, bot: str) -> str:
    if user == bot:
        return "draw"

    if user == "bomb" and bot == "bomb":
        return "draw"
    if user == "bomb":
        return "user"
    if bot == "bomb":
        return "bot"

    wins_against = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }

    return "user" if wins_against[user] == bot else "bot"


def apply_round_result(
    state: GameState,
    winner: Optional[str],
    user_move: str,
    bot_move: str,
):
    state.round_no += 1

    if user_move == "bomb":
        state.user_used_bomb = True
    if bot_move == "bomb":
        state.bot_used_bomb = True

    if winner == "user":
        state.user_score += 1
    elif winner == "bot":
        state.bot_score += 1


class GameReferee:
    def __init__(self):
        self.state = GameState()

    def show_rules(self):
        print(
            "Best of 3 rounds. Moves: rock, paper, scissors, bomb (once per game).\n"
            "Bomb beats everything. Same moves draw. Invalid input wastes the round.\n"
        )

    def bot_move(self) -> str:
        options = ["rock", "paper", "scissors"]
        if not self.state.bot_used_bomb:
            options.append("bomb")
        return random.choice(options)

    def play_round(self, raw_input: str):
        user_input = raw_input.strip().lower()
        bot_choice = self.bot_move()

        user_move = validate_move(user_input, self.state.user_used_bomb)

        if user_move is None:
            print("Invalid move. You lose this round.")
            apply_round_result(self.state, None, user_input, bot_choice)
            return

        winner = resolve_round(user_move, bot_choice)
        apply_round_result(self.state, winner, user_move, bot_choice)

        print(f"Round {self.state.round_no}")
        print(f"You played: {user_move} | Bot played: {bot_choice}")

        if winner == "draw":
            print("Result: Draw")
        elif winner == "user":
            print("Result: You win the round")
        else:
            print("Result: Bot wins the round")

        print(f"Score → You: {self.state.user_score}, Bot: {self.state.bot_score}\n")

    def finish(self):
        print("Game Over")
        if self.state.user_score > self.state.bot_score:
            print("Final Result: You Win")
        elif self.state.bot_score > self.state.user_score:
            print("Final Result: Bot Wins")
        else:
            print("Final Result: Draw")


if __name__ == "__main__":
    referee = GameReferee()
    referee.show_rules()

    while referee.state.round_no < referee.state.max_rounds:
        move = input("Enter your move: ")
        referee.play_round(move)

    referee.finish()
