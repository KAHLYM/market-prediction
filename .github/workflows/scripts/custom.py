from os import path
from sys import argv
from re import compile

FILEPATH = argv[1]
FILETYPE = path.splitext(FILEPATH)[1]

rules = {
    "py": [
        {
            "level": "warning",
            "regex": "import",
            "title": "test warning",
            "message": "oh hi there buddy"
        }
    ]
}

if FILETYPE not in rules:
    print(f"No rules associated with this filetype")
    exit()

LEVEL   = rules[FILETYPE]["level"]
REGEX   = rules[FILETYPE]["regex"]
TITLE   = rules[FILETYPE]["title"]
MESSAGE = rules[FILETYPE]["message"]

regex = compile(REGEX)
with open(FILEPATH, "r") as f:
    for index, line in enumerate(f):
        if regex.search(line):
            print(f"::{LEVEL} file={FILEPATH},line={index},title={TITLE}::{MESSAGE}")
