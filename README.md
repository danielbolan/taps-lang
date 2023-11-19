# taps-lang

A programming language written via Spotify playlists.

This project was inspired by [spet](https://github.com/h313/spet) but modified to allow for a bit more personal expression.

## Program structure

Taps is a brainfuck-like Turing machine with a circular tape of of 30000 bytes initialized to 0 and a pointer at position 0.

Programs are written as Spotify playlists that are then interpreted as brainfuck instructions.

Titles from the songs in the playlist are tokenized case-insensitively and individually into words separated by spaces, newlines, and punctuation and translated.

Each instruction has several aliases:

- `<` : `back`, `backward`, `last`, `past`, `was`, `were`, `before`, `left`
- `>` : `forward`, `next`, `future`, `will`, `after`, `right`
- `+` : `more`, `plus`, `up`, `with`, `increment`, `on`, `above`
- `-` : `less`, `minus`, `down`, `without`, `decrement`, `off`, `below`
- `.` : `out`, `say`, `speak`, `shout`, `put`, `output`, `!`
- `,` : `in`, `listen`, `hear`, `get`, `input`, `?`
- `[` : `jump`, `go`, `going`, `to`
- `]` : `loop`, `come`, `from`, `return`

All aliases are case-insensitive.

If a song contains the input command (`,`) or any of its aliases, the input will be read from the first character of the next song's title. If the Unicode codepoint takes up more than one byte, only the least-significant byte will be input.

Titles not containing tokens will be ignored and may safely be used for documentation.

## Setup and Running

Before anything, you should go [get yourself a client ID and secret from Spotify.](https://developer.spotify.com/documentation/web-api/concepts/apps)

```bash
git clone https://github.com/danielbolan/tapslang.git
cd tapslang
pip install poetry
poetry intall

# This will prompt you to input your Spotify client ID and secret,
# which will be saved to your keyring.
poetry run setup

# Running a program: both the URL and bare playlist ID should work
poetry run taps https://open.spotify.com/playlist/5OHBydIdhW0KSRy3O0ghcJ
poetry run taps 5OHBydIdhW0KSRy3O0ghcJ --debug
```

## Example Playlists

Just the one so far: [hello_world.taps](https://open.spotify.com/playlist/5OHBydIdhW0KSRy3O0ghcJ)
