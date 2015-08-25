__author__ = 'pais'


def getBookMetaData(rc, bookId):

    cursor = rc["db"].cursor()

    selectQuery = 'SELECT * FROM sadnadb.books ' \
                  'WHERE id = %s'
    cursor.execute(selectQuery, bookId)
    result = cursor.fetchall()

    metaData = {}
    for r in result:
        if len(r) != 0:
            metaData = {'id': r[0], 'title': r[1], 'author': r[2], 'releaseDate': r[3], 'language': r[4],
                        'fileLocation': r[5]}

    return metaData


def getBook(rc, bookId):

    cursor = rc["db"].cursor()

    # get all words in the book
    selectQuery = 'SELECT w.id, w.word, count(w.id) FROM sadnadb.words w, sadnadb.wordsInBooks wb ' \
                  'WHERE wb.bookId = %s and wb.wordId = w.id ' \
                  'GROUP BY w.id'
    cursor.execute(selectQuery, bookId)
    result = cursor.fetchall()

    words = []
    for r in result:
        if len(r) != 0:
            words += [{'id': r[0], 'text': r[1], 'count': r[2]}]

    #####
    # get metaData of the book
    metaData = getBookMetaData(rc, bookId)

    return {'words': words, 'metaData': metaData}


def getLanguageNameById(rc, languageId):
    cursor = rc["db"].cursor()

    selectQuery = 'SELECT name FROM sadnadb.languages WHERE id = %s'
    cursor.execute(selectQuery, languageId)
    result = cursor.fetchall()

    language = 0
    for r in result:
        if len(r) != 0:
            language = r[0]

    return language


def getBookForTemplate(rc, bookId):

    book = getBook(rc, bookId)

    words = []
    for tempWord in book['words']:
        words += [{'text': tempWord['text'].decode('utf-8'),
                   'href': '/word?id=' + str(tempWord['id']),
                   'count': tempWord['count']
                   }]

    metaData = book['metaData']
    metaData['language'] = getLanguageNameById(rc, book['metaData']['language']).title()

    return {'words': words, 'metaData': metaData}
