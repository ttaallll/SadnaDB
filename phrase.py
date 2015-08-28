__author__ = 'pais'


def createPhrase(rc, name):

    cursor = rc["db"].cursor()
    query = 'INSERT INTO sadnadb.phrases (name) ' \
            'VALUES (%s)'
    cursor.execute(query, name)
    rc["db"].commit()

    query = 'SELECT id FROM sadnadb.phrases ' \
            'ORDER BY id DESC LIMIT 1'
    cursor.execute(query)
    result = cursor.fetchall()
    phraseId = result[0][0]

    ###
    # insert words to wordsInPhrases table
    wordsInPhrase = name.split(' ')

    wordsValue = []
    i = 1
    for temp in wordsInPhrase:
        wordsValue += [(phraseId, i, temp, temp.lower())]
        i += 1

    query = 'INSERT INTO sadnadb.wordsInPhrases ' \
            '(phraseId, orderNumber, wordText, wordTextLower) ' \
            'VALUES (%s, %s, %s, %s)'
    cursor.executemany(query, wordsValue)
    rc["db"].commit()

    return phraseId


def getPhrase(rc, phraseId):

    phrase = {'id': phraseId}

    cursor = rc["db"].cursor()
    query = 'SELECT * FROM sadnadb.phrases ' \
            'WHERE id = %s'
    cursor.execute(query, phraseId)
    result = cursor.fetchall()

    phrase['name'] = result[0][1]
    phrase['date'] = result[0][2]

    ####
    #
    query = 'SELECT * FROM sadnadb.wordsInPhrases ' \
            'WHERE phraseId = %s ' \
            'ORDER BY orderNumber'
    cursor.execute(query, phraseId)
    result = cursor.fetchall()

    phrase['words'] = result

    phrase['appearances'] = getBooksContainPhrases(rc, phraseId, len(phrase['words']))

    return phrase


def getAllPhrases(rc):
    cursor = rc["db"].cursor()
    query = 'SELECT * FROM sadnadb.phrases ORDER BY id DESC'
    cursor.execute(query)
    result = cursor.fetchall()

    return result


def getBooksContainPhrases(rc, phraseId, wordsInPhrase):

    cursor = rc["db"].cursor()
    query = 'select temp1.bookId, b.title, temp1.orderNumber, temp1.lineNumber, temp1.wordNumberInLine, count(temp1.lineNumber) cnt1 ' \
            'from ' \
            '(SELECT wb.bookId bookId, wb.originalWordLower ow, wp.orderNumber orderNumber, wb.lineNumber lineNumber, wb.wordNumberInLine wordNumberInLine ' \
            'FROM sadnadb.wordsInPhrases wp, sadnadb.wordsInBooks wb ' \
            'WHERE phraseId = %s AND wb.originalWordLower = wp.wordTextLower) as temp1,' \
            '(SELECT wb.bookId bookId, wb.originalWordLower ow, wp.orderNumber orderNumber, wb.lineNumber lineNumber, wb.wordNumberInLine wordNumberInLine ' \
            'FROM sadnadb.wordsInPhrases wp, sadnadb.wordsInBooks wb ' \
            'WHERE phraseId = %s AND wb.originalWordLower = wp.wordTextLower) as temp2,' \
            'sadnadb.books as b ' \
            'where temp1.bookId = temp2.bookId ' \
            'and temp1.lineNumber = temp2.lineNumber ' \
            'and (temp1.wordNumberInLine = temp2.wordNumberInLine - 1 OR temp1.wordNumberInLine = temp2.wordNumberInLine + 1) ' \
            'and temp1.bookId = b.id ' \
            'group by temp1.lineNumber, temp1.bookId ' \
            'order by cnt1 desc'
    cursor.execute(query, (phraseId, phraseId))
    result = cursor.fetchall()

    books = {}
    phrasesExists = []
    for r in result:
        if r[5] == (wordsInPhrase - 1) * 2:
            phrasesExists += [r]

            bookId = r[0]
            query = 'SELECT w.id, wb.originalWord, wb.lineNumber, wb.wordNumberInLine ' \
                    'FROM sadnadb.wordsInBooks wb, sadnadb.words w ' \
                    'WHERE wb.lineNumber = %s AND w.id = wb.wordId AND wb.bookId = %s ' \
                    'ORDER BY wb.wordNumberInLine'
            cursor.execute(query, (r[3], bookId))
            result2 = cursor.fetchall()

            words1 = result2

            if bookId not in books:
                books[bookId] = {'lines': []}

            books[bookId]['lines'] += [{'data': words1, 'from': r[4], 'to': r[4] + wordsInPhrase}]
            books[bookId]['title'] = r[1]
            # books[bookId]['count'] += 1

    return books


