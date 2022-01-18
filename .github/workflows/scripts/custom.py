from os import path
from sys import argv
from re import compile

FILEPATH = argv[1]
FILETYPE = path.splitext(FILEPATH)[1]

rules = {
    ".py": [
        {
            "severity": "warning",
            "regex": "import",
            "title": "test warning",
            "message": "oh hi there buddy"
        }
    ]
}

if FILETYPE not in rules:
    print(f"No rules associated with this filetype")
    exit()

with open(FILEPATH, "r") as f:
    for index, line in enumerate(f):
        for rule in rules[FILETYPE]:
            SEVERITY = rule["level"]
            REGEX    = rule["regex"]
            TITLE    = rule["title"]
            MESSAGE  = rule["message"]

            regex = compile(REGEX)
            if regex.search(line):
                print(f"::{SEVERITY} file={FILEPATH},line={index},title={TITLE}::{MESSAGE}")
