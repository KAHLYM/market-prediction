from os import path
from re import compile
from sys import argv

FILEPATH = argv[1]
FILETYPE = path.splitext(FILEPATH)[1]

rules = {
    ".scss": [
        {
            "message": "Prefer global SCSS variable font-size",
            "regex": "font-size: [^$].*",
            "severity": "warning",
        }
    ]
}

if FILETYPE not in rules:
    exit()

with open(FILEPATH, "r") as f:
    for index, line in enumerate(f, 1):
        for rule in rules[FILETYPE]:
            SEVERITY = rule["severity"]
            REGEX    = rule["regex"]
            TITLE    = rule["title"]
            MESSAGE  = rule["message"]

            regex = compile(REGEX)
            if regex.search(line):
                print(f"::{SEVERITY} file={FILEPATH},line={index},title={FILEPATH}#{index}::{MESSAGE}")
