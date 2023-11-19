import sys
import urllib

import tapslang.spotify
import tapslang.bf

# Compiles a playlist into a brainfuck program.

# Songs are tokenized into words separated by spaces or punctuation.

# Any input commands (",") will read the first character
# from the next song in the playlist.

_PUNCTUATION = '<>+-.,[]()"!@#$%^&*?~`:;'
_SYNONYMS = {
    "<": "back,backward,last,past,was,were,before,left".split(","),
    ">": "forward,next,future,will,after,right".split(","),
    "+": "more,plus,up,with,increment,on,above".split(","),
    "-": "less,minus,down,without,decrement,off,below".split(","),
    ".": "out,say,speak,shout,put,output,!".split(","),
    ",": "in,listen,hear,get,input,?".split(","),
    "[": "jump,go,going,to".split(","),
    "]": "loop,come,from,return".split(","),
}

_TRANSLATION_TABLE = {}
for k, v in _SYNONYMS.items():
    _TRANSLATION_TABLE[k] = k
    for syn in v:
        _TRANSLATION_TABLE[syn] = k


def tokenize_playlist(s):
    s = s.strip()
    tokens = []
    buffer = ""
    for c in s:
        if c in [" ", "\n"]:
            if buffer:
                tokens.append(buffer)
            buffer = ""
            continue
        if c in _PUNCTUATION:
            if buffer:
                tokens.append(buffer)
            tokens.append(c)
            buffer = ""
            continue
        buffer += c
    if buffer:
        tokens.append(buffer)
    return tokens


def run_playlist(playlist_id, debug=False):
    songs = tapslang.spotify.get_songs(playlist_id)
    tokenlist = [tokenize_playlist(s) for s in songs]
    bf_program = ""
    for i, s in enumerate(tokenlist):
        newtokens = ""
        for token in s:
            if token.lower() not in _TRANSLATION_TABLE:
                continue
            c = _TRANSLATION_TABLE[token.lower()]
            if c == ",":
                newtokens += tokenlist[i + 1][0][0]
            else:
                newtokens += c
        if debug:
            print(s)
            print(newtokens, "\n")
        bf_program += newtokens

    if debug:
        print(bf_program, "\n")

    i = tapslang.bf.Interpreter()
    i.run(bf_program)


def main():
    playlist_id = sys.argv[1]
    if playlist_id[:5] == "https":
        url = urllib.parse.urlparse(playlist_id)
        playlist_id = url.path.split("/")[-1]

    debug = len(sys.argv) > 2 and sys.argv[2] == "--debug"

    run_playlist(playlist_id, debug=debug)


if __name__ == "__main__":
    sys.argv = ["tapslang.taps", "5OHBydIdhW0KSRy3O0ghcJ", "--debug"]
    main()
