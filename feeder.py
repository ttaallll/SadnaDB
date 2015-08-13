__author__ = 'pais'

siteFormats = [
    'gutenberg',
]


def addBookToDB(bookText, siteFormat):

    bookData = {}

    if siteFormat == 'gutenberg':
        bookData = parseGutenberg(bookText)

    addNewBook(bookData)



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
            metadata1['releaseDate'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('Language:'):
            metadata1['language'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('*** START'):
            # we start from here to read the book
            startBookLine = currentLine
        if tempLine.startswith('*** END OF '):
            endBookLine = currentLine
            break

    bookLines = lines[currentLine:endBookLine]

    return {
        'metadata': metadata1,
        'bookLines': bookLines
    }



def addNewBook(bookData):

    metadata = bookData['metadata']
    bookLines = bookData['bookLines']

    bookId = insertBook(metadata)

    addAllWords(bookId, bookLines)

    
def insertBook(metadata):