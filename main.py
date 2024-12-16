from pathlib import Path
import subprocess
import sys
import curses

MEMNOTE_SUFFIXES: list[str] = [".memnote", ".txt"]
EDITOR_CMD = "nvim"
NOTES_PATH = Path.home() / ".local" / "share" / "mem"
NOTES_PATH.mkdir(exist_ok=True)

class Note:
    def __init__(self, content_path):
        self.content_path: Path = content_path

def get_notes_in_dir(path: Path) -> list[Note]:
    assert path.exists()
    assert path.is_dir()

    notes: list[Note] = []
    for sub_dir in path.iterdir():
        if sub_dir.is_file() and sub_dir.suffixes == MEMNOTE_SUFFIXES:
            notes.append(Note(sub_dir))
    return notes


def edit_note(note: Note):
    subprocess.call([EDITOR_CMD, note.content_path.absolute()])

def create_note(name: str) -> Note:
    path = NOTES_PATH / Path(name + "".join(MEMNOTE_SUFFIXES))
    return Note(path)

def main() -> None:
    if len(sys.argv) < 2:
        stdscr = curses.initscr()
        stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()

        list_start_y = 1
        list_cursor_y = list_start_y
        while True:
            height, width = stdscr.getmaxyx()
            stdscr.addstr(0, 0, "Mem".center(width), curses.A_BOLD)
            stdscr.move(list_cursor_y, 0)

            notes = get_notes_in_dir(NOTES_PATH)
            for i, note in enumerate(notes):
                note_name = note.content_path.name.removesuffix("".join(MEMNOTE_SUFFIXES))
                stdscr.addstr(i + list_start_y, 0, note_name.ljust(width),
                              curses.A_STANDOUT if list_cursor_y - list_start_y == i else 0)

            stdscr.refresh()
            char = stdscr.getch()
            if char == curses.KEY_DOWN:
                list_cursor_y = max(list_start_y, min(list_cursor_y + 1, len(notes)))
            elif char == curses.KEY_UP:
                list_cursor_y = max(list_start_y, min(list_cursor_y - 1, len(notes)))
            elif char == 10:  # enter key
                note_idx = list_cursor_y - list_start_y
                # http://tldp.org/HOWTO/NCURSES-Programming-HOWTO/misc.html
                curses.def_prog_mode()
                curses.endwin()

                edit_note(notes[note_idx])

                curses.reset_prog_mode()
                stdscr.refresh()
    else:
        if sys.argv[1].casefold() == "new":
            note_name = input("Name: ")
            note = create_note(note_name)
            edit_note(note)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            curses.nocbreak()
            curses.echo()
            curses.endwin()
        except curses.error:
            pass
