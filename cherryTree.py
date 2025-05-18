import curses
import random
import time

TREE_ART = [
    "      _______ ",
    "     / 🌸    \ ",
    "    (      🌸 ) ",
    "    ( 🌸       ) ",
    "     \     🌸/ ",
    "       \   /   ",
    "        | |",
    "        | |",
    "        | |"
]

PETALS = ["🌸", ".", "*"]
WIDTH = 20  # width of the widest TREE_ART line (used for petal spawn)
HEIGHT = 10  # falling space below the tree


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()

    # Init color pairs
    curses.init_pair(1, 205, -1)  # Pink
    curses.init_pair(2, 94, -1)   # Brown
    PINK = curses.color_pair(1)
    BROWN = curses.color_pair(2)

    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    petal_positions = []

    while True:
        stdscr.erase()
        max_y, max_x = stdscr.getmaxyx()

        tree_width = max(len(line.lstrip()) for line in TREE_ART)
        x_offset = (max_x - tree_width) // 2 - 3

        if max_y < len(TREE_ART) + HEIGHT or max_x < tree_width:
            stdscr.addstr(0, 0, "Terminal too small (min ~25x20)")
            stdscr.refresh()
            time.sleep(0.5)
            continue

        # Draw tree, centered
        for row, line in enumerate(TREE_ART):
            for col, ch in enumerate(line):
                draw_x = x_offset + col
                if 0 <= draw_x < max_x - 1 and row < max_y:
                    if ch in ("\\", "/", "(", ")", "_", "🌸"):
                        stdscr.addstr(row, draw_x, ch, PINK)
                    elif ch == "|":
                        stdscr.addstr(row, draw_x, ch, BROWN)
                    else:
                        stdscr.addstr(row, draw_x, ch)

        # Add new petals
        new_petals = [(random.randint(0, WIDTH - 1), 0) for _ in range(random.randint(1, 2))]
        petal_positions.extend(new_petals)

        updated_petals = []
        for x, y in petal_positions:
            screen_y = len(TREE_ART) + y
            draw_x = x_offset + x
            if 0 <= draw_x < max_x - 1 and 0 <= screen_y < max_y:
                stdscr.addstr(screen_y, draw_x, random.choice(PETALS), PINK)
                updated_petals.append((x, y + 1))

        petal_positions = updated_petals

        stdscr.refresh()
        time.sleep(0.1)

        if stdscr.getch() == ord('q'):
            break


if __name__ == "__main__":
    curses.wrapper(main)

