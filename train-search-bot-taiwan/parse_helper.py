import re

def is_command_format(commands):
    regex = re.compile('^\/(\w{1,4})\s(.+){1,2}')
    return bool(regex.search(commands))
def parse_commands(commands):
    regex = re.compile('^\/(\w{1,4})\s(.+){1,2}')
    match = regex.search(commands)
    if (bool(match)):
        from_and_to = commands.split(" ")
        from_and_to[0] = from_and_to[0].replace('/', '')
        from_and_to = match_fuzzy_keywords(from_and_to)
        print(from_and_to)
    return from_and_to

def match_fuzzy_keywords(data):
    regex = re.compile('^[台]{1}.+')
    for i in range(len(data)):
        if(bool(regex.search(data[i]))):
            print(data[i])
            data[i] = data[i].replace('台', '臺')
            print('after: {}'.format(data[i]))
    return data
