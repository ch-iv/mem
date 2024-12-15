from pathlib import Path
import subprocess
import sys

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
        while True:
            notes = get_notes_in_dir(NOTES_PATH)
            if len(notes) == 0:
                print("There are no notes")
                return
            for n, note in enumerate(notes):
                print(n, note.content_path.name.removesuffix("".join(MEMNOTE_SUFFIXES)))
            note_to_edit = input("Enter note id: ")
            if not note_to_edit.isnumeric() and (int(note_to_edit) < 0 or int(note_to_edit) > len(notes) - 1):
                continue
            note = notes[int(note_to_edit)]
            edit_note(note)
    else:
        if sys.argv[1].casefold() == "new":
            note_name = input("Name: ")
            note = create_note(note_name)
            edit_note(note)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        pass
