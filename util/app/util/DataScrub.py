from re import sub

def IllegalFilenameCharacters(str):
    str = sub(r'[^\w\s-]', '', str)
    return sub(r'[-\s]+', '', str)