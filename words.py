__author__ = 'tal'


LINES_OF_BULK_WORDS = 3


def addAllWords(rc, bookLines, bookId, startBookChar):

    currentChar = 0 + startBookChar
    currentLine = 1
    currentParagraph = 1
    currentWords = []
    currentWordsCount = 1
    for tempLine in bookLines:

        currentWords += tempLine.split(' ')
        currentWordsThisLine = tempLine.split(' ')

        if len(currentWords) == 1 and currentWords[0] == '':
            currentWords = []

        if len(currentWordsThisLine) == 1 and currentWordsThisLine[0] == '':
            currentWordsThisLine = []

        if currentLine % LINES_OF_BULK_WORDS == 0:

            currentWords = fixWords(currentWords)
            addWords(rc, currentWords)
            currentWords = []

        addWordsInBooks(rc, currentWordsThisLine, currentLine, currentParagraph, bookId, currentChar, currentWordsCount)

        print currentLine

        currentWordsCount += len(currentWordsThisLine)
        currentChar += len(tempLine) + 2
        currentLine += 1
        if tempLine == '':
            currentParagraph += 1


def addWordsInBooks(rc, words, lineNumber, paragraphNumber, bookId, startLineChar, startLineWordsCount):

    for tempWord in words:
        newTempWord = tempWord.replace("'", "\\'")

        chars_to_remove = ['.', '!', '?', ',', ':', ';']
        newTempWord = newTempWord.translate(None, ''.join(chars_to_remove))
        newTempWord = newTempWord.lower()

        if len(newTempWord) == 0:
            continue

        cursor = rc["db"].cursor()
        query = 'SELECT id FROM sadnadb.words WHERE word = %s'
        cursor.execute(query, newTempWord)
        result = cursor.fetchall()

        wordId = 0
        if len(result) > 0:
            wordId = result[0][0]


        cursor = rc["db"].cursor()
        query = 'INSERT INTO sadnadb.wordsInBooks (' \
                ' wordId,' \
                ' bookId,' \
                ' lineNumber,' \
                ' wordNumber,' \
                ' characterLocation,' \
                ' sentenceNumber,' \
                ' paragraphNumber)' \
                ' VALUES (%s, %s, %s, %s, %s, %s, %s)' % (wordId, bookId, lineNumber, startLineWordsCount, startLineChar, 0, paragraphNumber)
        cursor.execute(query)
        rc["db"].commit()

        startLineWordsCount += 1
        startLineChar += len(tempWord) + 1


def fixWords(words):
    if '' in words:
        words.remove('')

    if len(words) == 0:
        return []

    lowerWords = []
    for tempWord in words:
        newTempWord = tempWord.replace("'", "\\'")

        chars_to_remove = ['.', '!', '?', ',', ':', ';']
        newTempWord = newTempWord.translate(None, ''.join(chars_to_remove))

        if len(newTempWord) == 0:
            continue

        lowerWords += [newTempWord.lower()]

    return lowerWords


def addWords(rc, words):

    if len(words) == 0:
        return

    words = list(set(words))

    wordsExists, wordsNotExists = checkIfWordsExists(rc, words)

    # insert to table words the not existed
    cursor = rc["db"].cursor()
    query = 'INSERT INTO sadnadb.words (word) VALUES (%s)'
    cursor.executemany(query, wordsNotExists)
    rc["db"].commit()

    print 'inserted - ' + str(wordsNotExists)


def checkIfWordsExists(rc, words):

    exists = {}
    notExists = []

    cursor = rc["db"].cursor()
    query = 'SELECT * FROM sadnadb.words WHERE word in ('
    for tempWord in words[:-1]:
        query += '\'' + tempWord + '\'' + ', '
    query += '\'' + words[-1] + '\')'
    cursor.execute(query)
    result = cursor.fetchall()

    for tempWordId in result:
        exists[tempWordId[1]] = tempWordId[0]

    for tempWord in words:
        if tempWord not in exists:
            notExists += [(tempWord,)]

    return exists, notExists
