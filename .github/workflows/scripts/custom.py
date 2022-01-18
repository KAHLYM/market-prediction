import sys
print(f"Running against file: {sys.argv[1]}")
print(f"::warning file={sys.argv[1]},line=1,col=1,endColumn=2::Test warning against {sys.argv[1]}")