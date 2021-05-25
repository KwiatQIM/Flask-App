import dominate as dom
from dominate.tags import *
import re

def create_page():

    # accessing the documentation page
    doc_page = open('templates/DocumentationPage.html', 'r')
    doc_lines = doc_page.readlines()
    doc_page.close()

    # big_methods stores the html for every method that is in the documentation.
    # It holds the Title of the function, its parameters currently.
    big_methods = div()

    # This scans TomoClass, gets the comments and creates the html needed for the Table of Contents
    TomoClass_bullets = ul()
    TomoClass_list = getAllCommentBlocks('DocumentationPage/QuantumTomography/TomoClass.py')
    TomoClass_count = len(TomoClass_list)

    TomoFunctions_bullets = ul()
    TomoFunctions_list = getAllCommentBlocks('DocumentationPage/QuantumTomography/TomoFunctions.py')
    TomoFunctions_count = len(TomoFunctions_list)

    TomoDisplay_bullets = ul()
    TomoDisplay_list = getAllCommentBlocks('DocumentationPage/QuantumTomography/TomoDisplay.py')
    TomoDisplay_count = len(TomoDisplay_list)

    combined_list = TomoClass_list + TomoFunctions_list + TomoDisplay_list

    for i in range(len(combined_list)):
        comment = combined_list[i].strip()
        if '(' in comment and ')' in comment:
            cur_title = comment[:comment.index("(")].split(" ")[-1]
            cur_params = comment[:comment.index(")") + 1]
            comment_lines = comment.splitlines()

            if 'Desc:' in comment:
                # this accesses the second line of the comment, trims it, and then removes the Desc: from the front
                cur_description = ''
                for line in comment_lines:
                    if cur_description != '':
                        if 'todo' in line.lower() or line == '':
                            break
                        else:
                            cur_description += ' ' + line.strip()
                    if 'Desc:' in line:
                        cur_description += line.strip()[6:]
            else:
                cur_description = 'Description not currently available'

            if i < TomoClass_count:
                TomoClass_bullets += li(comment[:comment.index("(")], onclick="displayMethod(this.innerHTML); this.style.fontWeight = 'bold'", id=cur_title+'_li_link')
                cur_div = big_methods.add(div(style="display:inline;", cls="MethodInfo", id=cur_title))
                cur_div.add(h1('Tomography.' + cur_title, cls="MethodTitle"))
                cur_div.add(h3('Tomography.' + cur_params, cls="methodSyntax"))
                cur_div.add(p(cur_description, cls="methodShortDesc"))
            elif i < TomoClass_count + TomoFunctions_count:
                TomoFunctions_bullets += li(cur_title, onclick="displayMethod(this.innerHTML); this.style.fontWeight = 'bold'", id=cur_title+'_li_link')
                cur_div = big_methods.add(div(style="display:inline;", cls="MethodInfo", id=cur_title))
                cur_div.add(h1(cur_title, cls="MethodTitle"))
                cur_div.add(h3(cur_params, cls="methodSyntax"))
                cur_div.add(p(cur_description, cls="methodShortDesc"))
            else:
                TomoDisplay_bullets += li(cur_title, onclick="displayMethod(this.innerHTML); this.style.fontWeight = 'bold'", id=cur_title + '_li_link')
                cur_div = big_methods.add(div(style="display:inline;", cls="MethodInfo", id=cur_title))
                cur_div.add(h1(cur_title, cls="MethodTitle"))
                cur_div.add(h3(cur_params, cls="methodSyntax"))
                cur_div.add(p(cur_description, cls="methodShortDesc"))

    # This code splits the html for the table of contents into separate lines
    TomoClass_bullets_lines = TomoClass_bullets.render().split('\n')
    TomoFunctions_bullets_lines = TomoFunctions_bullets.render().split('\n')
    TomoDisplay_bullets_lines = TomoDisplay_bullets.render().split('\n')
    big_methods_lines = big_methods.render().split('\n')

    # this block of code identifies the indices that we need to delete and add the necessary lines
    TomoClassind = 0
    TomoFunctionsind = 0
    TomoDisplayind = 0
    OtherFilesind = 0
    big_methods_ind = 0
    close_big_methods_ind = 0
    for i in range(len(doc_lines)):
        if "<!-- TomoClass -->" in doc_lines[i]:
            TomoClassind = i + 1
        if "<!-- TomoFunctions -->" in doc_lines[i]:
            TomoFunctionsind = i + 1
        if "<!-- TomoDisplay -->" in doc_lines[i]:
            TomoDisplayind = i + 1
        if "<!-- Other Files -->" in doc_lines[i]:
            OtherFilesind = i + 1
        if "<!-- Open Methods Div -->" in doc_lines[i]:
            big_methods_ind = i + 1
        if "<!-- Closing the Methods Div -->" in doc_lines[i]:
            close_big_methods_ind = i + 1
            break

    # making sure that all of the necessary indices were found
    # deleting all of the lines from the previous documentation
    # adding the new documentation to the doc_lines variable
    if TomoClassind != 0 and TomoFunctionsind != 0 and TomoDisplayind != 0 and big_methods_ind != 0:
        # deleting
        del doc_lines[TomoClassind:TomoFunctionsind - 1]
        TomoClass_deleted = TomoFunctionsind - 1 - TomoClassind
        TomoFunctionsind -= TomoClass_deleted
        TomoDisplayind -= TomoClass_deleted
        OtherFilesind -= TomoClass_deleted
        big_methods_ind -= TomoClass_deleted
        close_big_methods_ind -= TomoClass_deleted

        # deleting all of the TomoFunctions lines in the Table of Contents
        del doc_lines[TomoFunctionsind:TomoDisplayind - 1]
        TomoFunctions_deleted = TomoDisplayind - 1 - TomoFunctionsind
        TomoDisplayind -= TomoFunctions_deleted
        OtherFilesind -=  TomoFunctions_deleted
        big_methods_ind -= TomoFunctions_deleted
        close_big_methods_ind -= TomoFunctions_deleted

        # deleting all of the TomoDisplay lines in the Table of Contents
        del doc_lines[TomoDisplayind:OtherFilesind - 1]
        TomoDisplay_deleted = OtherFilesind - 1 - TomoDisplayind
        OtherFilesind -= TomoDisplay_deleted
        big_methods_ind -= TomoDisplay_deleted
        close_big_methods_ind -= TomoDisplay_deleted

        # deleting all of the lines for the methods in the html
        del doc_lines[big_methods_ind:close_big_methods_ind - 1]
        big_methods_deleted = close_big_methods_ind - 1 - big_methods_ind
        close_big_methods_ind -= big_methods_deleted

        # adding the new documentation
        for k in range(len(TomoClass_bullets_lines)):
            doc_lines.insert(TomoClassind + k, TomoClass_bullets_lines[k])
        for k in range(len(TomoFunctions_bullets_lines)):
            doc_lines.insert(TomoFunctionsind
                             + len(TomoClass_bullets_lines)
                             + k, TomoFunctions_bullets_lines[k])
        for k in range(len(TomoDisplay_bullets_lines)):
            doc_lines.insert(TomoDisplayind
                             + len(TomoClass_bullets_lines)
                             + len(TomoFunctions_bullets_lines)
                             + k, TomoDisplay_bullets_lines[k])
        for k in range(len(big_methods_lines)):
            doc_lines.insert(big_methods_ind
                             + len(TomoClass_bullets_lines)
                             + len(TomoFunctions_bullets_lines)
                             + len(TomoDisplay_bullets_lines) + k, big_methods_lines[k])
    else:
        print('The necessary lines in Documentation page are not present')

    # adding newlines to the end of elements in doc_lines so that the html is readable
    for i in range(len(doc_lines)):
        if '\n' not in doc_lines[i]:
            doc_lines[i] += '\n'

    # opening the file agin, and overwriting it with the lines from doc_lines, joined together.
    doc_page = open('templates/DocumentationPage.html', 'w')
    doc_page.write(''.join(doc_lines))
    doc_page.close()


def getAllCommentBlocks(filepath):
    # Grab contents of file as string
    with open(filepath) as f:
        txt = f.read()
    # find everything wrapped in triple quotes
    return re.findall(r'"""(.+?)"""', txt,re.DOTALL)

if __name__ == '__main__':
    create_page()