import dominate as dom
from dominate.tags import *
import re

def create_page():
    TomoClassfunctions = []
    TomoFunctionsfunctions = []
    TomoDisplayfunctions = []
    functions = []
    titles = []
    function_parameters = []
    descriptions = []
    param_bools = []
    return_bools = []
    param_dicts = []
    return_dicts = []
    count = 0


    # accessing the documentation page
    doc_page = open('templates/DocumentationPage.html', 'r')
    doc_lines = doc_page.readlines()
    doc_page.close()

    # big_methods stores the html for every method that is in the documentation.
    # It holds the Title of the function, its parameters currently.
    big_methods = div()

    # This scans the three files and creates the unordered lists that will be filled with the functions
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

    # This loops through the big list of comments and adds the html to big_methods and the bullet lists for the three files
    for i in range(len(combined_list)):
        comment = combined_list[i].strip()
        if '(' in comment and ')' in comment:
            count += 1
            function_title = comment[:comment.index("(")].split(" ")[-1]
            functions.append(function_title)


            cur_title = 'Tomography.' + function_title if i < TomoClass_count else function_title
            titles.append(cur_title)

            cur_params = 'Tomography.' + comment[:comment.index(")") + 1] if i < TomoClass_count else comment[:comment.index(")") + 1]
            function_parameters.append(cur_params)

            # style={% if disp == 'tomography' %}"display:inline;" {% else %} "display:none;" {% endif %}
            display = "{% if disp == '" + function_title.lower() + "' %}'display:inline;' {% else %} 'display:none;' {% endif %} "

            cur_description = getDescription(comment)
            descriptions.append(cur_description)

            if 'Parameters' in comment and '----------' in comment:
                param_bools.append(True)
            else:
                param_bools.append(False)

            if 'Returns' in comment and '-------' in comment:
                return_bools.append(True)
            else:
                return_bools.append(False)

            paramReturn = True if '-------' in comment or '----------' in comment else False
            if paramReturn:
                parameters, returnValues = get_paramReturns(comment)
            else:
                parameters, returnValues = {}, {}
            param_dicts.append(parameters)
            return_dicts.append(returnValues)


            # adding the function to the bulleted list
            if i < TomoClass_count:
                TomoClassfunctions.append(function_title)
                TomoClass_bullets += li(a(function_title, href="{{ url_for('displayDocumentationPage',display='" + function_title.lower() + "') }}"), __pretty=False)
            elif i < TomoClass_count + TomoFunctions_count:
                TomoFunctionsfunctions.append(function_title)
                TomoFunctions_bullets += li(a(function_title, href="{{ url_for('displayDocumentationPage',display='" + function_title.lower() + "') }}"), __pretty=False)
            else:
                TomoDisplayfunctions.append(function_title)
                TomoDisplay_bullets += li(a(function_title, href="{{ url_for('displayDocumentationPage',display='" + function_title.lower() + "') }}"), __pretty=False)

            cur_div = big_methods.add(div(style=display, cls="MethodInfo", id=cur_title))
            cur_div.add(h1(cur_title, cls="MethodTitle"))
            cur_div.add(h3(cur_params, cls="MethodInfo"))
            cur_div.add(p(cur_description, cls="methodShortDesc"))

            # finding the comments that have Parameters or Return Values
            if paramReturn:

                if '----------' in comment:
                    tab = cur_div.add(table(cls="paramReturn"))
                    inner = tab.add(tr())
                    head = inner.add(td(cls="header"))
                    head.add(h6("Parameters:"))
                    param_list = inner.add(td(cls="list"))
                    unordered_param_list = param_list.add(ul())
                    comment_noParams = comment[comment.index('----------')+11:]
                    for param, desc in parameters.items():
                        list_ele = unordered_param_list.add(li())
                        list_ele.add(h4(param))
                        list_ele.add(p(desc))
                if '-------' in comment_noParams:
                    tab = cur_div.add(table(cls="paramReturn"))
                    inner = tab.add(tr())
                    head = inner.add(td(cls="header"))
                    head.add(h6("Returns:"))
                    param_list = inner.add(td(cls="list"))
                    unordered_param_list = param_list.add(ul())
                    for returnval, desc in returnValues.items():
                        list_ele = unordered_param_list.add(li())
                        list_ele.add(h4(returnval))
                        list_ele.add(p(desc))

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
    # deleting the lines and adding from the end first so that the indices aren't messed up
    if TomoClassind != 0 and TomoFunctionsind != 0 and TomoDisplayind != 0 and big_methods_ind != 0:
        # doing the methods list first
        del doc_lines[big_methods_ind:close_big_methods_ind - 1]
        for k in range(len(big_methods_lines)):
            doc_lines.insert(big_methods_ind + k, big_methods_lines[k])

        # deleting old and adding new TomoDisplay
        del doc_lines[TomoDisplayind:OtherFilesind - 1]
        for k in range(len(TomoDisplay_bullets_lines)):
            doc_lines.insert(TomoDisplayind + k, TomoDisplay_bullets_lines[k])

        # deleting old and adding new TomoFunctions
        del doc_lines[TomoFunctionsind:TomoDisplayind - 1]
        for k in range(len(TomoFunctions_bullets_lines)):
            doc_lines.insert(TomoFunctionsind + k, TomoFunctions_bullets_lines[k])

        # deleting old and adding new TomoClass
        del doc_lines[TomoClassind:TomoFunctionsind - 1]
        for k in range(len(TomoClass_bullets_lines)):
            doc_lines.insert(TomoClassind + k, TomoClass_bullets_lines[k])
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

    return TomoClassfunctions, TomoFunctionsfunctions, TomoDisplayfunctions, functions, titles, \
           function_parameters, descriptions, param_bools, return_bools, param_dicts, return_dicts, count

def getAllCommentBlocks(filepath):
    # Grab contents of file as string
    with open(filepath) as f:
        txt = f.read()
    # find everything wrapped in triple quotes
    return re.findall(r'"""(.+?)"""', txt,re.DOTALL)

'''
getDescription(lines)
    This function is given a list of lines from a comment, and returns the Description listed after 'Desc:' in comment
'''
def getDescription(comment):
    lines = comment.splitlines()
    description = ''
    if 'Desc:' in comment:
        for line in lines:
            if description != '':
                if 'todo' in line.lower() or line == '':
                    break
                else:
                    description += ' ' + line.strip()
            if 'Desc:' in line:
                description += line.strip()[6:]
    else:
        description = 'Description not currently available'
    return description


'''
get_paramReturns(lines)
    This function is given a list of lines from a comment, and returns two dictionaries
    
    parameters:
        keys: list of the parameters to the passed function and their types
        values: descriptions for each parameter
    returnValues:
        keys: the value returned and its type
        values: descriptions for each return value
'''
def get_paramReturns(comment):
    lines = comment.splitlines()
    parameters = {}
    returnValues = {}
    dict_switch = ''
    cur_key = ''
    cur_val = ''
    for line in lines:
        if ' : ' in line:
            if cur_key != '' and cur_val != '' and dict_switch == 'Parameters':
                parameters[cur_key] = cur_val
            elif cur_key != '' and cur_val != '' and dict_switch == 'ReturnValues':
                returnValues[cur_key] = cur_val
            cur_key = line
            cur_val = ''
        elif '----------' in line or '-------' in line or 'Returns' in line or 'Parameters' in line:
            if '----------' in line or 'Parameters' in line:
                dict_switch = 'Parameters'
            if ('-------' in line and '----------' not in line) or 'Returns' in line:
                if cur_key != '' and cur_val != '' and dict_switch == 'Parameters':
                    parameters[cur_key] = cur_val
                cur_val = ''
                dict_switch = 'ReturnValues'

        elif line == lines[-1]:
            cur_val = cur_val + ' ' + line
            if cur_key != '' and cur_val != '' and dict_switch == 'Parameters':
                parameters[cur_key] = cur_val
            elif cur_key != '' and cur_val != '' and dict_switch == 'ReturnValues':
                returnValues[cur_key] = cur_val

        else:
            cur_val = cur_val + ' ' + line
    return parameters, returnValues


if __name__ == '__main__':
    create_page()
