import time
import random
import curses
import json
import os
from curses import wrapper

SCORES_FILE = "scores.json"

# Word lists by difficulty
WORD_LISTS = {
    "easy": ["the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "for", "not", "on", "with",
             "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her"],
    "medium": ["about", "which", "their", "would", "there", "could", "other", "after", "first", "well",
               "water", "very", "through", "just", "where", "most", "know", "good", "something", "think"],
    "hard": ["experience", "development", "government", "environment", "information", "understand",
             "organization", "technology", "performance", "management", "communication", "particularly"]
}

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_score(wpm, accuracy, duration, mode):
    scores = load_scores()
    scores.append({
        "wpm": wpm,
        "accuracy": accuracy,
        "duration": duration,
        "mode": mode,
        "date": time.strftime("%Y-%m-%d %H:%M")
    })
    scores = sorted(scores, key=lambda x: x['wpm'], reverse=True)[:10]
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def generate_text(word_count, difficulty="medium"):
    words = WORD_LISTS[difficulty]
    return " ".join(random.choices(words, k=word_count))

def calculate_wpm(chars, seconds):
    if seconds == 0: return 0
    return round((chars / 5) / (seconds / 60))

def calculate_cpm(chars, seconds):
    if seconds == 0: return 0
    return round(chars / (seconds / 60))

def draw_progress_bar(stdscr, y, x, width, progress):
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    stdscr.addstr(y, x, f"[{bar}] {int(progress*100)}%")

def typing_test(stdscr, duration, word_count, difficulty, mode="time"):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    target_text = generate_text(word_count, difficulty)
    typed_text = []
    start_time = None
    backspaces = 0
    mistakes = 0

    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Timer logic
        if start_time:
            elapsed = time.time() - start_time
            if mode == "time":
                time_left = max(0, duration - elapsed)
                if time_left <= 0:
                    break
                progress = elapsed / duration
            else: # word mode
                time_left = elapsed
                progress = len(typed_text) / len(target_text)
                if len(typed_text) >= len(target_text):
                    break
        else:
            elapsed = 0
            time_left = duration if mode == "time" else 0
            progress = 0

        # Calculate stats
        wpm = calculate_wpm(len(typed_text), elapsed)
        raw_wpm = calculate_wpm(len(typed_text), elapsed)
        cpm = calculate_cpm(len(typed_text), elapsed)
        correct = sum(1 for t, y in zip(target_text, typed_text) if t == y)
        accuracy = round(correct / max(1, len(typed_text)) * 100, 1)

        # Draw UI
        stdscr.addstr(0, 2, "⚡ TYPING SPEED TESTER ⚡", curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(1, 2, "─" * (w-4))

        if mode == "time":
            stdscr.addstr(2, 2, f"Time: {int(time_left)}s")
        else:
            stdscr.addstr(2, 2, f"Time: {int(time_left)}s | Words: {len(''.join(typed_text).split())}/{word_count}")

        stdscr.addstr(2, 30, f"WPM: {wpm} | Raw: {raw_wpm} | CPM: {cpm}", curses.color_pair(3))
        stdscr.addstr(3, 2, f"Accuracy: {accuracy}% | Mistakes: {mistakes} | Backspaces: {backspaces}")

        draw_progress_bar(stdscr, 4, 2, w-4, progress)

        stdscr.addstr(6, 2, "Text:", curses.A_BOLD)

        # Display text with wrapping
        max_width = w - 4
        lines = [target_text[i:i+max_width] for i in range(0, len(target_text), max_width)]
        for idx, line in enumerate(lines[:8]): # Show max 8 lines
            stdscr.addstr(7+idx, 2, line)

        # Display typed text with colors
        typed_str = "".join(typed_text)
        for i, char in enumerate(typed_str):
            y = 7 + (i // max_width)
            x = 2 + (i % max_width)
            if y >= h-2: break

            if i < len(target_text):
                if char == target_text[i]:
                    stdscr.addstr(y, x, char, curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, target_text[i], curses.color_pair(2) | curses.A_UNDERLINE)
                    if char!= target_text[i]:
                        mistakes += 1
            else:
                stdscr.addstr(y, x, char, curses.color_pair(2))

        # Draw cursor
        if len(typed_str) < len(target_text):
            cy = 7 + (len(typed_str) // max_width)
            cx = 2 + (len(typed_str) % max_width)
            if cy < h-1:
                stdscr.addstr(cy, cx, target_text[len(typed_str)] if len(typed_str) < len(target_text) else " ",
                            curses.A_REVERSE)

        stdscr.addstr(h-2, 2, "TAB: Restart | ESC: Quit", curses.color_pair(4))
        stdscr.refresh()

        # Input handling
        try:
            key = stdscr.getch()
        except:
            key = -1

        if key!= -1:
            if start_time is None and 32 <= key <= 126:
                start_time = time.time()

            if key == 27: # ESC
                return None
            elif key == 9: # TAB - restart
                return "restart"
            elif key in (8, 127, curses.KEY_BACKSPACE):
                if typed_text:
                    typed_text.pop()
                    backspaces += 1
            elif 32 <= key <= 126:
                typed_text.append(chr(key))

        time.sleep(0.01)

    # Results screen
    final_elapsed = elapsed if elapsed > 0 else duration
    final_wpm = calculate_wpm(len(typed_text), final_elapsed)
    final_accuracy = round(correct / max(1, len(typed_text)) * 100, 1)

    save_score(final_wpm, final_accuracy, int(final_elapsed), f"{mode}-{difficulty}")
    return {"wpm": final_wpm, "accuracy": final_accuracy, "cpm": cpm, "mistakes": mistakes,
            "backspaces": backspaces, "time": int(final_elapsed)}

def show_menu(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    options = [
        "1. Timed Test - 15s",
        "2. Timed Test - 30s",
        "3. Timed Test - 60s",
        "4. Timed Test - 120s",
        "5. Word Test - 25 words",
        "6. Word Test - 50 words",
        "7. View Leaderboard",
        "8. Change Difficulty",
        "9. Quit"
    ]

    difficulty = "medium"
    selected = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(1, w//2-12, "TYPING SPEED TESTER", curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(2, w//2-15, f"Difficulty: {difficulty.upper()}", curses.color_pair(1))
        stdscr.addstr(3, 0, "═" * w)

        for idx, option in enumerate(options):
            y = 5 + idx
            if idx == selected:
                stdscr.addstr(y, w//2-15, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(y, w//2-13, option)

        stdscr.addstr(h-2, 2, "UP/DOWN: Navigate | ENTER: Select | ESC: Quit")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key == 10: # Enter
            if selected == 0: return typing_test(stdscr, 15, 50, difficulty, "time")
            elif selected == 1: return typing_test(stdscr, 30, 100, difficulty, "time")
            elif selected == 2: return typing_test(stdscr, 60, 200, difficulty, "time")
            elif selected == 3: return typing_test(stdscr, 120, 400, difficulty, "time")
            elif selected == 4: return typing_test(stdscr, 999, 25, difficulty, "words")
            elif selected == 5: return typing_test(stdscr, 999, 50, difficulty, "words")
            elif selected == 6: show_leaderboard(stdscr)
            elif selected == 7: difficulty = change_difficulty(stdscr, difficulty)
            elif selected == 8: break
        elif key == 27:
            break

def change_difficulty(stdscr, current):
    options = ["easy", "medium", "hard"]
    idx = options.index(current)
    stdscr.clear()
    stdscr.addstr(0, 0, "Select Difficulty: 1-Easy 2-Medium 3-Hard")
    key = stdscr.getch()
    if key == ord('1'): return "easy"
    elif key == ord('2'): return "medium"
    elif key == ord('3'): return "hard"
    return current

def show_leaderboard(stdscr):
    scores = load_scores()
    stdscr.clear()
    stdscr.addstr(0, 2, "🏆 LEADERBOARD - Top 10 🏆", curses.A_BOLD)
    stdscr.addstr(1, 2, "─" * 60)

    if not scores:
        stdscr.addstr(3, 2, "No scores yet. Play a game!")
    else:
        stdscr.addstr(3, 2, f"{'Rank':<6}{'WPM':<8}{'Accuracy':<12}{'Mode':<15}{'Date'}")
        for i, s in enumerate(scores, 1):
            stdscr.addstr(4+i, 2, f"{i:<6}{s['wpm']:<8}{s['accuracy']:<12}{s['mode']:<15}{s['date']}")

    stdscr.addstr(16, 2, "Press any key to return...")
    stdscr.getch()

def main(stdscr):
    while True:
        result = show_menu(stdscr)
        if result == "restart":
            continue
        elif result is None:
            break
        elif isinstance(result, dict):
            stdscr.clear()
            stdscr.addstr(0, 2, "🎯 RESULTS 🎯", curses.A_BOLD)
            stdscr.addstr(2, 2, f"WPM: {result['wpm']}")
            stdscr.addstr(3, 2, f"Accuracy: {result['accuracy']}%")
            stdscr.addstr(4, 2, f"CPM: {result['cpm']}")
            stdscr.addstr(5, 2, f"Mistakes: {result['mistakes']}")
            stdscr.addstr(6, 2, f"Time: {result['time']}s")
            stdscr.addstr(8, 2, "Press any key for menu...")
            stdscr.getch()

if __name__ == "__main__":
    wrapper(main)