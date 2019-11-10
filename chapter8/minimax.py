from __future__ import annotations
from board import Piece, Board, Move


# 元のプレイヤーの裁量結果となる手を探す
def minimax(board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8) -> float:
    # 基底部：停止位置または最大深さ
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # 再帰部：利得最大または相手の利得最小を狙う
    if maximizing:
        best_eval: float = float("-inf") # 任意の極小値
        for move in board.legal_moves:
            result: float = minimax(board.move(move), False, original_player, max_depth - 1)
            best_eval = max(result, best_eval)
        return best_eval
    else: # 最小化
        worst_eval: float = float("inf")
        for move in board.legal_moves:
            result = minimax(board.move(move), True, original_player, max_depth - 1)
            worst_eval = min(result, worst_eval)
        return worst_eval


# 現在の位置でmax_depthまでの最良の手を探す
def find_best_move(board: Board, max_depth: int = 8) -> Move:
    best_eval: float = float("-inf")
    best_move: Move = Move(-1)
    for move in board.legal_moves:
        result: float = alphabeta(board.move(move), False, board.turn, max_depth)
        if result > best_eval:
            best_eval = result
            best_move = move
    return best_move


def alphabeta(board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8,
    alpha: float = float("-inf"), beta: float = float("inf")) -> float:
    # 基底部：停止位置または最大深さ
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # 再帰部：利得最大または相手の利得最小
    if maximizing:
        for move in board.legal_moves:
            result: float = alphabeta(board.move(move), False, original_player, max_depth - 1, alpha, beta)
            alpha = max(result, alpha)
            if beta <= alpha:
                break
        return alpha
    else: # 最小化
        for move in board.legal_moves:
            result = alphabeta(board.move(move), True, original_player, max_depth - 1, alpha, beta)
            beta = min(result, beta)
            if beta <= alpha:
                break
        return beta