# 🎮 Yut Nori (윷놀이) - Python Terminal Game

Classic Korean traditional board game, **Yut Nori**, brought to your terminal!

한국의 전통 놀이인 **윷놀이**를 터미널 환경에서 즐겨보세요!

설날을 맞이하여, 코딩을 사랑하는 분들이 별도의 도구 없이도 터미널만 있다면 가족, 친구와 함께 전통 놀이를 즐길 수 있도록 파이썬으로 구현해 보았습니다.

---

## 🇰🇷 Celebrating Seollal (Korean Lunar New Year) 🏮

**Seollal** is one of the most significant traditional holidays in Korea, marking the first day of the lunar calendar. It's a time when families gather from across the country to pay respects to their ancestors, enjoy traditional foods like *Tteokguk* (rice cake soup), and share blessings for the new year.

> **Why Yut Nori?** > Traditionally, after the morning ceremonies, families play **Yut Nori** to bond and celebrate together. It’s a game of strategy, luck, and excitement that transcends generations. By bringing this game to the terminal, I hope to bridge the gap between ancient tradition and modern coding culture!

---

## English

### 📝 Project Description

This is a Python-based terminal game that implements the core mechanics of **Yut Nori**. It supports 2 to 4 players, features a visual ASCII board, and uses cute animal emojis to represent players.

### ✨ Key Features

* **Multiplayer Support:** Play with 2 to 4 players.
* **Visual Board:** Real-time updates of piece positions on a terminal-based board.
* **Emoji Markers:** Each player is assigned a unique animal emoji (🐴, 🐑, 🐱, etc.).
* **Core Rules Implemented:**
* **Yut stick logic:** Do, Gae, Geol, Yut, Mo.
* **Extra turns:** Awarded for throwing 'Yut' or 'Mo', or capturing an opponent's piece.
* **Shortcuts:** Strategic movement through positions 05 and 10 for a faster finish.
* **Victory System:** Winner announcement when all 4 pieces safely reach the goal.



### 🕹️ How to Run

1. Ensure you have **Python 3.x** installed.
2. Clone the repository: `git clone https://github.com/your-repo/yut-nori.git`
3. Run the script:
```bash
python yut_nori.py
```



### 📏 Game Rules

* **Moves:**
* **Do (도):** 1 space
* **Gae (개):** 2 spaces
* **Geol (걸):** 3 spaces
* **Yut (윷):** 4 spaces + Extra Throw
* **Mo (모):** 5 spaces + Extra Throw


* **Capture:** Landing on an opponent's space sends their piece back to the start and gives you an **extra throw**.
* **Winning:** The first player to get all **4 pieces** past the finish line wins!

---

## 한국어

### 📝 프로젝트 설명

한국의 전통 보드게임인 **윷놀이**를 파이썬으로 구현한 터미널 게임입니다. 2~4인용 플레이를 지원하며, ASCII 보드와 귀여운 동물 이모지를 통해 게임 상황을 시각적으로 확인할 수 있습니다.

### ✨ 주요 기능

* **다인용 플레이:** 2명에서 4명까지 함께 플레이 가능.
* **시각적 보드:** 터미널 창에 실시간으로 업데이트되는 윷판 표시.
* **동물 이모지:** 각 플레이어에게 고유한 캐릭터(🐴, 🐑, 🐱 등) 부여.
* **핵심 규칙 구현:**
* **윷 던지기:** 도, 개, 걸, 윷, 모 완벽 구현.
* **추가 기회:** '윷'이나 '모'가 나왔을 때, 혹은 상대방 말을 잡았을 때 보너스 턴.
* **지름길:** 5번, 10번 지점의 지름길 로직을 통한 전략적 플레이.
* **승리 시스템:** 4개의 말이 모두 먼저 골인하는 플레이어 승리.



### 🕹️ 실행 방법

1. **Python 3.x** 버전이 설치되어 있어야 합니다.
2. 터미널에서 다음 명령어를 입력합니다:
```bash
python yut_nori.py
```



### 📏 게임 규칙 (구현 내용)

* **이동:** 도(1칸), 개(2칸), 걸(3칸), 윷(4칸+추가), 모(5칸+추가).
* **잡기:** 상대방 말이 있는 위치에 도착하면 말을 잡아 시작점으로 되돌리고 **한 번 더** 던집니다.
* **지름길:** 5번 또는 10번 위치에 정확히 멈추면 지름길로 진입할 수 있습니다.
* **승리:** 가장 먼저 4개의 말을 모두 골인시키면 우승!

---

## 🛠️ Requirements

* Python 3.6+
* Terminal with UTF-8 support (for emoji display)

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=https://opensource.org/licenses/MIT).

---

## ✉️ Contact

If there are any issues or things you'd like to ask, please feel free to contact me!

* **Email:** [soeonpark03@gmail.com](mailto:soeonpark03@gmail.com)

**Enjoy the game and Happy Seollal!** 🧧
