import dominate as dom
from dominate.tags import *
import re

def create_page():

    doc = dom.document()

    #getting the actual comments
    TomoClass_bullets = ul()
    TomoClass_list = getAllCommentBlocks('DocumentationPage/QuantumTomography/TomoClass.py')
    for comment in TomoClass_list:
        comment = comment.strip()
        if '(' in comment and ')' in comment:

            TomoClass_bullets += li(comment[:comment.index("(")], onclick="displayMethod(this.innerHTML); this.style.fontWeight = 'bold'")

    TomoFunctions_bullets = ul()
    TomoFunctions_list = getAllCommentBlocks('DocumentationPage/QuantumTomography/TomoFunctions.py')
    for comment in TomoFunctions_list:
        comment = comment.strip()
        if '(' in comment and ')' in comment:

            TomoFunctions_bullets += li(comment[:comment.index("(")], onclick="displayMethod(this.innerHTML); this.style.fontWeight = 'bold'")

    TomoDisplay_bullets = ul()
    TomoDisplay_list = getAllCommentBlocks('DocumentationPage/QuantumTomography/TomoDisplay.py')
    for comment in TomoDisplay_list:
        comment = comment.strip()
        if '(' in comment and ')' in comment:

            TomoDisplay_bullets += li(comment[:comment.index("(")], onclick="displayMethod(this.innerHTML); this.style.fontWeight = 'bold'")





def getAllCommentBlocks(filepath):
    # Grab contents of file as string
    with open(filepath) as f:
        txt = f.read()
    # find everything wrapped in triple quotes
    return re.findall(r'"""(.+?)"""', txt,re.DOTALL)

if __name__ == '__main__':
    create_page()