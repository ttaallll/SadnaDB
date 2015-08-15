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


def addBookToDB(rc, bookUrl, siteFormat):

    bookText = geFromStorage(bookUrl)

    bookData = {}

    if siteFormat == 'gutenberg':
        bookData = parseGutenberg(bookText)

    addNewBook(rc, bookData)


def parseGutenberg(text):
    lines = text.split('\r\n')

    metadata1 = {
        'title': '',
        'author': '',
        'releaseDate': '',
        'language': ''
    }
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
            metadata1['releaseDate'] = datetime.strptime(tempLine[tempLine.find(':') + 2:].split('[')[0], '%b, %Y ')
        if tempLine.startswith('Language:'):
            metadata1['language'] = tempLine[tempLine.find(':') + 2:]
        if tempLine.startswith('*** START'):
            # we start from here to read the book
            startBookLine = currentLine
        if tempLine.startswith('*** END OF '):
            endBookLine = currentLine
            break

    bookLines = lines[startBookLine + 1:endBookLine]

    return {
        'metadata': metadata1,
        'bookLines': bookLines
    }


def addNewBook(rc, bookData):

    metadata = bookData['metadata']
    bookLines = bookData['bookLines']

    bookId = insertBook(rc, metadata)

    addAllWords(rc, bookLines, bookId)






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


def insertBook(rc, metadata):

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
        'tempPath'
    ))

    result = cursor.fetchall()

    return result