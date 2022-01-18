from json import load
from os import path
from sys import argv
from re import compile

print(f"{path.dirname(path.realpath(__file__))}")

FILEPATH = argv[1]
FILETYPE = path.splitext(FILEPATH)[1]

with open(".\.github\workflows\scripts\custom.json", "r") as f:
    rules = load(f)

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
