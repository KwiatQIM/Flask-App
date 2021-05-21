import dominate as dom
from dominate.tags import *
import re

def create_page():

    # big_methods stores the html for every method that is in the documentation.
    # It holds the Title of the function, its parameters currently.
    big_methods = div()

    # This scans TomoClass, gets the comments and creates the html needed for the Table of Contents
    TomoClass_bullets = ul()
    TomoClass_list = getAllCommentBlocks('DocumentationPage/QuantumTomography/TomoClass.py')
    for comment in TomoClass_list[3:]:
        comment = comment.strip()
        if '(' in comment and ')' in comment:
            cur_title = comment[:comment.index("(")].split(" ")[-1]
            cur_params = comment[:comment.index(")") + 1]

            TomoClass_bullets += li(comment[:comment.index("(")], onclick="displayMethod(this.innerHTML); this.style.fontWeight = 'bold'", id=cur_title+'_li_link')

            cur_div = big_methods.add(div(style="display:none;", cls="MethodInfo", id=cur_title))
            cur_div.add(h1('Tomography.'+cur_title, cls="MethodTitle"))
            cur_div.add(h3('Tomography.'+cur_params, cls="methodSyntax"))
            cur_div.add(p('long desc', cls="methodLongDesc"))


    # This scans TomoFunctions, gets the comments and creates the html needed for the Table of Contents
    TomoFunctions_bullets = ul()
    TomoFunctions_list = getAllCommentBlocks('DocumentationPage/QuantumTomography/TomoFunctions.py')
    for comment in TomoFunctions_list:
        comment = comment.strip()
        if '(' in comment and ')' in comment:
            current_title = comment[:comment.index("(")].split(" ")[-1]
            cur_params = comment[:comment.index(")") + 1]

            TomoFunctions_bullets += li(current_title, onclick="displayMethod(this.innerHTML); this.style.fontWeight = 'bold'", id=current_title+'_li_link')

            cur_div = big_methods.add(div(style="display:none;", cls="MethodInfo", id=cur_title))
            cur_div.add(h1(cur_title, cls="MethodTitle"))
            cur_div.add(h3(cur_params, cls="methodSyntax"))
            cur_div.add(p('long desc', cls="methodLongDesc"))

    # This scans TomoDisplay, gets the comments and creates the html needed for the Table of Contents
    TomoDisplay_bullets = ul()
    TomoDisplay_list = getAllCommentBlocks('DocumentationPage/QuantumTomography/TomoDisplay.py')
    for comment in TomoDisplay_list:
        comment = comment.strip()
        if '(' in comment and ')' in comment:
            current_title = comment[:comment.index("(")].split(" ")[-1]
            cur_params = comment[:comment.index(")") + 1]

            TomoDisplay_bullets += li(current_title, onclick="displayMethod(this.innerHTML); this.style.fontWeight = 'bold'", id=current_title+'_li_link')

            cur_div = big_methods.add(div(style="display:none;", cls="MethodInfo", id=cur_title))
            cur_div.add(h1(cur_title, cls="MethodTitle"))
            cur_div.add(h3(cur_params, cls="methodSyntax"))
            cur_div.add(p('long desc', cls="methodLongDesc"))


def getAllCommentBlocks(filepath):
    # Grab contents of file as string
    with open(filepath) as f:
        txt = f.read()
    # find everything wrapped in triple quotes
    return re.findall(r'"""(.+?)"""', txt,re.DOTALL)

if __name__ == '__main__':
    create_page()