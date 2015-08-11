__author__ = 'pais'

siteFormats = [
    'gutenberg',
]


def addBookToDB(bookText, siteFormat):

    if siteFormat == 'gutenberg':
        parseGutenberg(bookText)



def parseGutenberg(text):
    lines = text.split('\r\n')

    metadata1 = {}
    currentLine = -1
    startBookLine = 0
    endBookLine = 0
    for tempLine in lines:
        currentLine += 1
        if tempLine.startswith('Title:'):
            metadata1['title'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('Author:'):
            metadata1['author'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('Release Date:'):
            metadata1['releaseData'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('Language:'):
            metadata1['language'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('*** START'):
            # we start from here to read the book
            startBookLine = currentLine
        if tempLine.startswith('*** END OF '):
            endBookLine = currentLine
            break

    bookLines = lines[currentLine:endBookLine]
    print metadata1
    print startBookLine
    print endBookLine
    print len(lines)