from os import path
from sys import argv
from re import compile

FILEPATH = argv[1]
FILETYPE = path.splitext(FILEPATH)[1]

rules = {
    ".py": [
        {
            "level": "warning",
            "regex": "import",
            "title": "test warning",
            "message": "oh hi there buddy"
        }
    ]
}

print(f"FILEPATH: {FILEPATH}")
print(f"FILETYPE: {FILETYPE}")

if FILETYPE not in rules:
    print(f"No rules associated with this filetype")
    exit()

print(f"::warning file=README.md,line=1,title=TestTitle::TestMessage")

with open(FILEPATH, "r") as f:
    for index, line in enumerate(f):
        for rule in rules[FILETYPE]:
            LEVEL   = rule["level"]
            REGEX   = rule["regex"]
            TITLE   = rule["title"]
            MESSAGE = rule["message"]

            regex = compile(REGEX)
            if regex.search(line):
                print(f"::{LEVEL} file={FILEPATH},line={index},title={TITLE}::{MESSAGE}")
