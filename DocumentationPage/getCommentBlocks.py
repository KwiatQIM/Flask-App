import re

# Returns a list of comment blocks for a given a file
def getAllCommentBlocks(filepath):
    # Grab contents of file as string
    with open(filepath) as f:
        txt = f.read()
    # find everything wrapped in triple quotes
    return re.findall(r'"""(.+?)"""', txt,re.DOTALL)

if __name__ == "__main__":

    file = 'QuantumTomography/TomoClass.py'

    comments = getAllCommentBlocks(file)
    for string in comments:
        print(string)
        print("\n------------------------------------------------------\n")