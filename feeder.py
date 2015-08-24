__author__ = 'pais'

from datetime import datetime

from words import addAllWords
from storage import geFromStorage

siteFormats = [
    'gutenberg',
]


def getLastBookFromDB(rc):

    cursor = rc["db"].cursor()
    query = 'SELECT * FROM sadnadb.books ORDER BY id DESC LIMIT 1'
    cursor.execute(query)
    result = cursor.fetchall()

    bookData = None
    if len(result) != 0:
        bookData = result[0]

    return bookData


def getLastNBookFromDB(rc, n):

    cursor = rc["db"].cursor()
    query = 'SELECT * FROM sadnadb.books ORDER BY id DESC LIMIT %s'
    cursor.execute(query, n)
    result = cursor.fetchall()

    bookData = []
    for r in result:
        if len(r) != 0:
            bookData += [r]

    return bookData


def addBookToDB(rc, bookUrl, siteFormat):

    bookText = geFromStorage(bookUrl)

    bookData = {
        'bookUrl': bookUrl,
        'bookText': bookText
    }

    if siteFormat == 'gutenberg':
        parseGutenberg(bookData)

    addNewBook(rc, bookData)


def parseGutenberg(bookData):

    text = bookData['bookText']
    lines = text.split('\r\n')

    metadata1 = {
        'title': '',
        'author': '',
        'releaseDate': '',
        'language': ''
    }
    currentLine = -1
    startBookLine = 0
    startBookChar = 0
    endBookLine = 0
    currentChar = 0

    for tempLine in lines:
        currentLine += 1
        if tempLine.startswith('Title:'):
            metadata1['title'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('Author:'):
            metadata1['author'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('Release Date:'):
            try:
                # metadata1['releaseDate'] = datetime.strptime(tempLine[tempLine.find(':') + 2:].split('[')[0], '%b, %Y ')
                metadata1['releaseDate'] = tempLine[tempLine.find(':') + 2:].split('[')[0]
            except:
                print 'couldn\'t parse release date'
        if tempLine.startswith('Language:'):
            metadata1['language'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('*** START'):
            # we start from here to read the book
            startBookLine = currentLine
            startBookChar = currentChar
        if tempLine.startswith('*** END OF '):
            endBookLine = currentLine
            break

        currentChar += len(tempLine) + 2

    bookLines = lines[startBookLine + 1:endBookLine]

    bookData['metadata'] = metadata1
    bookData['bookLines'] = bookLines
    bookData['startBookChar'] = startBookChar


def addNewBook(rc, bookData):

    metadata = bookData['metadata']
    bookLines = bookData['bookLines']
    bookUrl = bookData['bookUrl']
    startBookChar = bookData['startBookChar']

    bookId = insertBook(rc, metadata, bookUrl)

    addAllWords(rc, bookLines, bookId, startBookChar)






def getLanguageId(rc, languageName):

    languageNameLowerCase = languageName.lower()

    cursor = rc["db"].cursor()

    selectLanguageIdQuery = 'SELECT id FROM sadnadb.languages WHERE name = \'{0}\''.format(languageNameLowerCase)
    cursor.execute(selectLanguageIdQuery)
    result = cursor.fetchall()

    if len(result) == 0:
        createLanguageQuery = 'INSERT INTO sadnadb.languages (name) VALUES (\'{0}\')'.format(languageNameLowerCase)
        cursor.execute(createLanguageQuery)

        cursor.execute(selectLanguageIdQuery)
        result = cursor.fetchall()


    languageId = 0
    for r in result:
        if len(r) != 0:
            languageId = r[0]

    return languageId


def insertBook(rc, metadata, bookUrl):

    cursor = rc["db"].cursor()
    cursor.execute('INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}) VALUES (\'{6}\', \'{7}\', \'{8}\', \'{9}\', \'{10}\')'.format(
        'sadnadb.books',
        'title',
        'author',
        'releaseDate',
        'language',
        'fileLocation',

        metadata['title'],
        metadata['author'],
        metadata['releaseDate'],
        getLanguageId(rc, metadata['language']),
        bookUrl
    ))

    rc["db"].commit()

    selectQuery = 'SELECT id FROM sadnadb.books WHERE fileLocation = %s'
    cursor.execute(selectQuery, bookUrl)
    result = cursor.fetchall()

    bookId = 0
    if len(result) > 0:
        bookId = result[0][0]

    return bookId
