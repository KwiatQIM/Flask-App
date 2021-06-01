import re

""" 
the see also is formatted like this:

See Also
 ------ 

and other properties is formatted like this:

Other Properties
 -------------- 
 
"""

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
    see_also = []
    count = 0

    # This scans the three files and creates the unordered lists that will be filled with the functions
    TomoClass_list = getAllCommentBlocks('resources/Quantum-Tomography/src/QuantumTomography/TomoClass.py')
    TomoClass_count = len(TomoClass_list)

    TomoFunctions_list = getAllCommentBlocks('resources/Quantum-Tomography/src/QuantumTomography/TomoFunctions.py')
    TomoFunctions_count = len(TomoFunctions_list)

    TomoDisplay_list = getAllCommentBlocks('resources/Quantum-Tomography/src/QuantumTomography/TomoDisplay.py')
    TomoDisplay_count = len(TomoDisplay_list)

    combined_list = TomoClass_list + TomoFunctions_list + TomoDisplay_list

    # This loops through the big list of comments and adds the html to big_methods and the bullet lists for the three files
    for i in range(len(combined_list)):
        comment = combined_list[i].strip()
        comment_lines = comment.splitlines()
        if '(' in comment and ')' in comment and 'class Tomography()' not in comment:
            count += 1
            function_title = comment[:comment.index("(")].split(" ")[-1]
            functions.append(function_title)


            cur_title = 'Tomography.' + function_title if i < TomoClass_count else function_title
            titles.append(cur_title)

            cur_params = 'Tomography.' + comment[:comment.index(")") + 1] if i < TomoClass_count else comment[:comment.index(")") + 1]
            function_parameters.append(cur_params)

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

            cur_see_also = get_see_also(comment)
            see_also.append(cur_see_also)


            # adding the function to the bulleted list
            if i < TomoClass_count:
                TomoClassfunctions.append(function_title)
            elif i < TomoClass_count + TomoFunctions_count:
                TomoFunctionsfunctions.append(function_title)
            else:
                TomoDisplayfunctions.append(function_title)

    return TomoClassfunctions, TomoFunctionsfunctions, TomoDisplayfunctions, functions, titles, \
           function_parameters, descriptions, param_bools, return_bools, param_dicts, return_dicts, see_also, count

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

def get_see_also(comment):
    comment_lines = comment.splitlines()
    functions = []
    see_also_bool = False

    if ' ------ ' in comment:
        functions = []
    else:
        functions = '0'

    for line in comment_lines:
        if see_also_bool:
            functions = line.split(';')
        if ' ------ ' in line:
            see_also_bool = True
    return functions

if __name__ == '__main__':
    create_page()

