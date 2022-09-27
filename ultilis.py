import re
def convert_title(input_string):
    input_string = input_string.split(' ')
    result = []
    for k in input_string:
        temp = re.search('[a-zA-Z]', k)
        if temp != None and k != 'chapter' and k != 'Chapter':
            result.append(k)
    result = ' '.join(result)
    return result