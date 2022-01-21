from os import path
from re import compile
from sys import argv

FILEPATH = argv[1]
FILETYPE = path.splitext(FILEPATH)[1]

rules = {
    ".scss": {
        "font-family": {
            "message": "Prefer global SCSS variable",
            "regex": "font-family: (?!var\(\-\-font\-family).*",
            "severity": "warning",
        },
        "font-size": {
            "message": "Prefer global SCSS variable",
            "regex": "font-size: (?!var\(\-\-font\-size).*",
            "severity": "warning",
        },
        "font-weight": {
            "message": "Prefer global SCSS variable",
            "regex": "font-weight: (?!var\(\-\-font\-weight).*",
            "severity": "warning",
        },
    }
}

if not path.isfile(FILEPATH):
    exit()

if FILETYPE not in rules:
    exit()

with open(FILEPATH, "r") as f:
    for index, line in enumerate(f, 1):
        for rule_name, rule in rules[FILETYPE].items():
            SEVERITY = rule["severity"]
            REGEX    = rule["regex"]
            MESSAGE  = rule["message"]

            regex = compile(REGEX)
            if regex.search(line):
                print(f"::{SEVERITY} file={FILEPATH},line={index},title={FILEPATH}#{index}::{MESSAGE} ({rule_name})")
