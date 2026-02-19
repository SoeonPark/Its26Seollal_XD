#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
윷놀이 (Yut Nori) - Korean Traditional Board Game
2-4 Players Terminal Game
"""

import random
import os
import time
from typing import List, Tuple, Optional, Dict

# ANSI 색상 코드
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # 보드 위치 색상만 사용
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

# 플레이어 동물 아이콘
ANIMAL_EMOJIS = ['🐴', '🐑', '🐱', '🐰', '🐶', '🐷', '🐼', '🦊', '🐻', '🐯', '🦁', '🐮']

class YutNori:
    def __init__(self, num_players: int = 2):
        self.num_players = num_players
        self.player_names = [f"Player {i}" for i in range(num_players)]
        
        # 각 플레이어에게 알파벳 기호 배정 (A, B, C, D)
        self.player_symbols = {i: chr(65 + i) for i in range(num_players)}  # A, B, C, D
        
        # 각 플레이어에게 랜덤 동물 배정 (표시용)
        selected_animals = random.sample(ANIMAL_EMOJIS, num_players)
        self.player_animals = {i: selected_animals[i] for i in range(num_players)}
        
        # 보드 위치 매핑 (좌표 -> 보드 표시)
        self.position_map = {
            0: '00', 1: '01', 2: '02', 3: '03', 4: '04',
            5: '05', 6: '06', 7: '07', 8: '08', 9: '09',
            10: '10', 11: '11', 12: '12', 13: '13', 14: '14',
            15: '15', 16: '16', 17: '17', 18: '18', 19: '19',
            20: 'FIN'  # 도착
        }
        
        # 각 플레이어의 말들 (최대 4개)
        self.player_pieces = {i: [] for i in range(num_players)}
        for i in range(num_players):
            self.player_pieces[i] = [
                {'id': j, 'position': -1, 'finished': False} 
                for j in range(4)
            ]
        
        # 윷 결과
        self.yut_names = ['도', '개', '걸', '윷', '모']
        self.yut_values = [1, 2, 3, 4, 5]
        
        # 특수 위치 (지름길)
        self.shortcuts = {
            5: 20,   # 5번에서 바로 20번(도착)으로
            10: 20,  # 10번에서 바로 20번(도착)으로
        }
        
        self.current_player = 0
        self.game_over = False
        self.recent_moves = []
        
    def clear_screen(self):
        """화면 지우기"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def throw_yut(self) -> Tuple[str, int]:
        """윷 던지기"""
        # 윷 결과: 도(1), 개(2), 걸(3), 윷(4), 모(5)
        # 확률: 도 32.8%, 개 29.7%, 걸 26.6%, 윷 7.8%, 모 3.1%
        rand = random.random() * 100
        
        if rand < 32.8:
            return '도', 1
        elif rand < 62.5:
            return '개', 2
        elif rand < 89.1:
            return '걸', 3
        elif rand < 96.9:
            return '윷', 4
        else:
            return '모', 5
    
    def get_pieces_at_position(self, position: int) -> List[Tuple[int, int]]:
        """특정 위치에 있는 말들 반환 [(player_idx, piece_idx), ...]"""
        pieces = []
        for player_idx in range(self.num_players):
            for piece in self.player_pieces[player_idx]:
                if piece['position'] == position and not piece['finished']:
                    pieces.append((player_idx, piece['id']))
        return pieces
    
    def draw_board(self):
        """보드 그리기"""
        print("=" * 80)
        print("윷놀이 (YUT NORI)")
        print("=" * 80)
        print()
        
        # 각 위치에 있는 말들 수집
        position_pieces: Dict[int, List[Tuple[int, int]]] = {}
        for pos in range(21):
            pieces = self.get_pieces_at_position(pos)
            if pieces:
                position_pieces[pos] = pieces
        
        # 보드 위치별 표시 생성 - 말이 있으면 동물, 없으면 숫자
        def get_pos_display(pos: int, base_color: str = Colors.WHITE) -> str:
            if pos in position_pieces:
                pieces = position_pieces[pos]
                
                # 같은 플레이어의 말들만 있는지 확인
                player_ids = list(set(p[0] for p in pieces))
                
                if len(player_ids) == 1:
                    # 한 플레이어의 말만
                    player_idx = player_ids[0]
                    animal = self.player_animals[player_idx]
                    if len(pieces) == 1:
                        return f"{animal} "
                    else:
                        return f"{animal}{len(pieces)}"
                else:
                    # 여러 플레이어의 말이 섞여 있음
                    animals_str = ""
                    for player_idx in player_ids:
                        animal = self.player_animals[player_idx]
                        count = sum(1 for p in pieces if p[0] == player_idx)
                        if count == 1:
                            animals_str += animal
                        else:
                            animals_str += f"{animal}{count}"
                    return animals_str
            else:
                pos_str = f"{pos:02d}"
                return f"{base_color}{pos_str}{Colors.RESET}"
        
        # 보드 위치별 기본 색상
        corner_color = Colors.RED
        side_color = Colors.BLUE
        start_color = Colors.GREEN
        shortcut_color = Colors.YELLOW
        
        # 외곽 위치 표시
        p10 = get_pos_display(10, corner_color)
        p09 = get_pos_display(9, side_color)
        p08 = get_pos_display(8, side_color)
        p07 = get_pos_display(7, side_color)
        p06 = get_pos_display(6, side_color)
        p05 = get_pos_display(5, shortcut_color)
        p11 = get_pos_display(11, side_color)
        p04 = get_pos_display(4, side_color)
        p12 = get_pos_display(12, side_color)
        p03 = get_pos_display(3, side_color)
        p13 = get_pos_display(13, side_color)
        p02 = get_pos_display(2, side_color)
        p14 = get_pos_display(14, side_color)
        p01 = get_pos_display(1, start_color)
        p15 = get_pos_display(15, corner_color)
        p16 = get_pos_display(16, side_color)
        p17 = get_pos_display(17, side_color)
        p18 = get_pos_display(18, side_color)
        p19 = get_pos_display(19, side_color)
        p00 = get_pos_display(0, start_color)
        
        c_center = "🔴 "  # 중앙
        
        # 보드 그리기
        print(f"  {p10}  {p09}  {p08}  {p07}  {p06}  {p05}")
        print("      ○            ○  ")
        print(f"  {p11}                  {p04}")
        print("         ○      ○  ")
        print(f"  {p12}                  {p03}")
        print(f"            {c_center}      ")
        print(f"  {p13}                  {p02}")
        print("         ○      ○  ")
        print(f"  {p14}                  {p01}")
        print("      ○            ○  ")
        print(f"  {p15}  {p16}  {p17}  {p18}  {p19}  {p00}")
        print()
        
    def display_player_status(self):
        """플레이어 상태 표시"""
        print("PLAYER STATUS:")
        print("-" * 80)
        
        for i in range(self.num_players):
            on_board = sum(1 for p in self.player_pieces[i] if p['position'] >= 0 and not p['finished'])
            finished = sum(1 for p in self.player_pieces[i] if p['finished'])
            waiting = 4 - on_board - finished
            
            animal = self.player_animals[i]
            marker = ">>>" if i == self.current_player else "   "
            
            print(f"{marker} {animal} {self.player_names[i]}: On board: {on_board}, Finished: {finished}, Waiting: {waiting}")
            
            # 보드 위의 말 위치 표시
            for piece in self.player_pieces[i]:
                if piece['position'] >= 0 and not piece['finished']:
                    pos_display = self.position_map[piece['position']]
                    print(f"        - Piece {piece['id']} at position {pos_display}")
        
        print("-" * 80)
        print()
        
    def display_recent_moves(self, moves: List[str]):
        """최근 이동 기록"""
        if not moves:
            return
            
        print("RECENT MOVES:")
        for move in moves[-5:]:  # 최근 5개만
            print(f"  {move}")
        print()
        
    def move_piece(self, player_idx: int, piece_idx: int, steps: int) -> Tuple[bool, str]:
        """말 이동"""
        piece = self.player_pieces[player_idx][piece_idx]
        animal = self.player_animals[player_idx]
        player_name = self.player_names[player_idx]
        
        # 새 말 진입
        if piece['position'] == -1:
            piece['position'] = 0
            msg = f"{animal} {player_name} entered Piece {piece_idx}"
            self.recent_moves.append(msg)
            return True, msg
        
        # 이동
        old_pos = piece['position']
        new_pos = old_pos + steps
        
        # 지름길 체크
        if old_pos in self.shortcuts and new_pos > old_pos:
            new_pos = self.shortcuts[old_pos]
            msg = f"{animal} {player_name} took shortcut from {self.position_map[old_pos]} to {self.position_map[new_pos]}!"
        else:
            msg = f"{animal} {player_name} moved Piece {piece_idx} from {self.position_map[old_pos]} to {self.position_map.get(new_pos, 'FIN')}"
        
        # 도착 체크
        if new_pos >= 20:
            piece['finished'] = True
            piece['position'] = 20
            msg = f"{animal} {player_name}'s Piece {piece_idx} finished!"
            self.recent_moves.append(msg)
            return True, msg
        
        piece['position'] = new_pos
        
        # 상대 말 잡기 체크
        for other_player in range(self.num_players):
            if other_player == player_idx:
                continue
                
            for other_piece in self.player_pieces[other_player]:
                if other_piece['position'] == new_pos and not other_piece['finished']:
                    other_piece['position'] = -1
                    other_animal = self.player_animals[other_player]
                    other_name = self.player_names[other_player]
                    capture_msg = f"Captured {other_animal} {other_name}'s Piece {other_piece['id']}!"
                    msg += f"\n  {capture_msg}"
                    self.recent_moves.append(capture_msg)
        
        self.recent_moves.append(msg)
        return True, msg
    
    def get_movable_pieces(self, player_idx: int, steps: int) -> List[int]:
        """이동 가능한 말 찾기"""
        movable = []
        
        for i, piece in enumerate(self.player_pieces[player_idx]):
            if piece['finished']:
                continue
                
            # 대기 중인 말
            if piece['position'] == -1:
                movable.append(i)
            # 보드 위의 말
            elif piece['position'] + steps <= 20:
                movable.append(i)
        
        return movable
    
    def check_win(self, player_idx: int) -> bool:
        """승리 조건 체크"""
        return all(p['finished'] for p in self.player_pieces[player_idx])
    
    def play_turn(self):
        """한 턴 진행"""
        player_idx = self.current_player
        player_name = self.player_names[player_idx]
        animal = self.player_animals[player_idx]
        
        self.clear_screen()
        self.draw_board()
        self.display_player_status()
        
        print("=" * 80)
        print(f"{animal} {player_name}'s turn (Player {player_idx})")
        print("=" * 80)
        print()
        
        extra_turn = True
        
        while extra_turn:
            extra_turn = False
            
            user_input = input("Press Enter to throw yut sticks (or 'q' to quit)... ").strip().lower()
            if user_input == 'q':
                print("\nGame ended by user.")
                self.game_over = True
                return
            
            yut_name, yut_value = self.throw_yut()
            
            print(f"\n🎲 Result: {yut_name} ({yut_value} spaces)")
            print()
            
            # 윷이나 모는 한번 더
            if yut_name in ['윷', '모']:
                extra_turn = True
                print(f"✨ {yut_name}! You get another turn!")
                print()
            
            # 이동 가능한 말 찾기
            movable = self.get_movable_pieces(player_idx, yut_value)
            
            if not movable:
                print("No pieces can move!")
                move_msg = f"{animal} {player_name} threw {yut_name} but couldn't move"
                self.recent_moves.append(move_msg)
                time.sleep(2)
                continue
            
            # 말 선택
            print("Select a piece to move:")
            for i, piece_idx in enumerate(movable):
                piece = self.player_pieces[player_idx][piece_idx]
                if piece['position'] == -1:
                    print(f"  {i+1}. Piece {piece_idx} (Enter the board)")
                else:
                    pos_display = self.position_map[piece['position']]
                    print(f"  {i+1}. Piece {piece_idx} (at position {pos_display})")
            
            while True:
                try:
                    choice = input(f"\nEnter choice (1-{len(movable)}, or 'q' to quit): ").strip().lower()
                    if choice == 'q':
                        print("\nGame ended by user.")
                        self.game_over = True
                        return
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(movable):
                        selected_piece = movable[choice_idx]
                        break
                    else:
                        print("Invalid choice!")
                except (ValueError, IndexError):
                    print("Invalid input!")
            
            # 말 이동
            success, msg = self.move_piece(player_idx, selected_piece, yut_value)
            print(f"\n{msg}")
            
            # 윷 던진 기록 추가
            throw_msg = f"{animal} {player_name} threw {yut_name} ({yut_value} spaces)"
            self.recent_moves.append(throw_msg)
            
            # 승리 체크
            if self.check_win(player_idx):
                self.clear_screen()
                self.draw_board()
                self.display_player_status()
                print("=" * 80)
                print(f"🎉 {animal} {player_name} WINS! 🎉")
                print("=" * 80)
                self.game_over = True
                return
            
            time.sleep(1.5)
            
            if extra_turn:
                self.clear_screen()
                self.draw_board()
                self.display_player_status()
                self.display_recent_moves(self.recent_moves)
                print(f"{animal} {player_name} gets another turn!")
                print()
        
        # 다음 플레이어로
        self.current_player = (self.current_player + 1) % self.num_players
    
    def play_game(self):
        """게임 실행"""
        self.clear_screen()
        print("=" * 80)
        print("WELCOME TO YUT NORI (윷놀이)!")
        print("=" * 80)
        print()
        print("Game Rules:")
        print("- Each player has 4 pieces")
        print("- Throw yut sticks to move pieces")
        print("- First to get all 4 pieces to finish wins!")
        print("- 도(Do)=1, 개(Gae)=2, 걸(Geol)=3, 윷(Yut)=4, 모(Mo)=5")
        print("- 윷 and 모 give you an extra turn!")
        print("- Land on opponent's piece to send them back!")
        print("- Type 'q' at any time to quit the game")
        print()
        print("Players:")
        for i in range(self.num_players):
            animal = self.player_animals[i]
            print(f"  {animal} {self.player_names[i]}")
        print()
        input("Press Enter to start...")
        
        while not self.game_over:
            self.play_turn()
        
        print("\nThank you for playing Yut Nori!")
        

def main():
    """메인 함수"""
    print("=" * 80)
    print("윷놀이 (YUT NORI) - Korean Traditional Board Game")
    print("=" * 80)
    print()
    
    while True:
        try:
            num_players = int(input("Enter number of players (2-4): "))
            if 2 <= num_players <= 4:
                break
            else:
                print("Please enter a number between 2 and 4!")
        except ValueError:
            print("Invalid input!")
    
    print()
    
    # 플레이어 이름 입력
    player_names = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i} (or press Enter for default): ").strip()
        if not name:
            name = f"Player {i}"
        player_names.append(name)
    
    game = YutNori(num_players)
    game.player_names = player_names
    game.play_game()


if __name__ == "__main__":
    main()