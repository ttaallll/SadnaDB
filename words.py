__author__ = 'tal'


def addAllWords(rc, bookLines, bookId):

    currentLine = 0
    for tempLine in bookLines:
        wordsInLine = tempLine.split(' ')

        addWords(rc, wordsInLine, bookId)

        currentLine += 1
        print currentLine


def addWords(rc, words, bookId):

    wordsExists, wordsNotExists = checkIfWordsExists(rc, words)

    cursor = rc["db"].cursor()
    query = 'INSERT INTO sadnadb.words (word) VALUES (%s)'
    cursor.executemany(query, wordsNotExists)

    rc["db"].commit()

    print 'inserted - ' + str(wordsNotExists)




def checkIfWordsExists(rc, words):

    exists = {}
    notExists = []

    if '' in words:
        words.remove('')

    if len(words) == 0:
        return exists, notExists

    lowerWords = []
    for tempWord in words:
        newTempWord = tempWord.replace("'", "\\'")
        lowerWords += [newTempWord.lower()]


    cursor = rc["db"].cursor()
    query = 'SELECT * FROM sadnadb.words WHERE word in ('
    for tempWord in lowerWords[:-1]:
        query += '\'' + tempWord + '\'' + ', '
    query += '\'' + lowerWords[-1] + '\')'
    cursor.execute(query)
    result = cursor.fetchall()

    for tempWordId in result:
        exists[tempWordId[1]] = tempWordId[0]

    for tempWord in lowerWords:
        if tempWord not in exists:
            notExists += [(tempWord,)]

    notExists = set(notExists)

    return exists, notExists