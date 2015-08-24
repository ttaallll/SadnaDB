__author__ = 'tal'


LINES_OF_BULK_WORDS = 3
chars_to_remove = ['.', '!', '?', ',',
                   ':', ';', '"', '\'',
                   '\\', '_', '[', ']',
                   '(', ')', '{', '}',
                   '/', '*', '&', '^',
                   '%', '$', '#', '@']


def addAllWords(rc, bookLines, bookId, startBookChar):

    print 'num of lines - ' + str(len(bookLines))

    currentChar = 0 + startBookChar
    currentLine = 1
    currentParagraph = 1
    currentWords = []
    currentWordsCount = 1

    wordsInBooksToInsert = []

    # add words
    for tempLine in bookLines:
        currentWords += tempLine.split(' ')

        if len(currentWords) == 1 and currentWords[0] == '':
            currentWords = []

        if currentLine % LINES_OF_BULK_WORDS == 0:
            currentWords = fixWords(currentWords)
            addWords(rc, currentWords)
            currentWords = []

        currentLine += 1

        print currentLine

    if len(currentWords) != 0:
        currentWords = fixWords(currentWords)
        addWords(rc, currentWords)
        currentWords = []

    #####
    # add words in books

    currentLine = 1

    for tempLine in bookLines:

        currentWords += tempLine.split(' ')
        currentWordsThisLine = tempLine.split(' ')

        if len(currentWordsThisLine) == 1 and currentWordsThisLine[0] == '':
            currentWordsThisLine = []

        if currentLine % LINES_OF_BULK_WORDS == 0:
            insertWordsInBooks(rc, wordsInBooksToInsert)
            wordsInBooksToInsert = []

        tempWordsInBooksToInsert, realWordsCount = createQueryValuesWordsInBooks(rc, currentWordsThisLine, currentLine, currentParagraph, bookId, currentChar, currentWordsCount)

        wordsInBooksToInsert += tempWordsInBooksToInsert

        print currentLine

        currentWordsCount += realWordsCount
        currentChar += len(tempLine) + 2
        currentLine += 1
        if tempLine == '':
            currentParagraph += 1

    if len(wordsInBooksToInsert) != 0:
        insertWordsInBooks(rc, wordsInBooksToInsert)
        wordsInBooksToInsert = []


def createQueryValuesWordsInBooks(rc, words, lineNumber, paragraphNumber, bookId, startLineChar, startLineWordsCount):

    realWordsCount = 0
    currentWordCount = startLineWordsCount
    currentChar = startLineChar

    wordsToInsert = []

    fixedWords = fixWords(words)

    exists, notExists = checkIfWordsExists(rc, fixedWords)

    for tempWord in words:
        # newTempWord = tempWord.replace("'", "\\'")
        newTempWord = tempWord

        newTempWord = newTempWord.translate(None, ''.join(chars_to_remove))
        newTempWord = newTempWord.lower()

        if len(newTempWord) == 0:
            currentChar += 1
            continue

        # wordsToInsert += [{
        #     'wordId': exists[newTempWord],
        #     'bookId': bookId,
        #     'lineNumber': lineNumber,
        #     'wordNumber': currentWordCount,
        #     'characterLocation': currentChar,
        #     'sentenceNumber': 0,
        #     'paragraphNumber': paragraphNumber
        # }]

        wordsToInsert += [(
            exists[newTempWord],
            bookId,
            lineNumber,
            currentWordCount,
            currentChar,
            0,
            paragraphNumber
        )]

        realWordsCount += 1
        currentWordCount += 1
        currentChar += len(tempWord) + 1

    return wordsToInsert, realWordsCount


def fixWords(words):
    if '' in words:
        words.remove('')

    if len(words) == 0:
        return []

    lowerWords = []
    for tempWord in words:
        # newTempWord = tempWord.replace("'", "\\'")
        newTempWord = tempWord

        newTempWord = newTempWord.translate(None, ''.join(chars_to_remove))

        if len(newTempWord) == 0:
            continue

        lowerWords += [newTempWord.lower()]

    if '' in lowerWords:
        lowerWords.remove('')

    return lowerWords


def addWords(rc, words):

    words = list(set(words))

    if len(words) == 0:
        return

    wordsExists, wordsNotExists = checkIfWordsExists(rc, words)

    # insert to table words the not existed
    cursor = rc["db"].cursor()
    query = 'INSERT INTO sadnadb.words (word) VALUES (%s)'
    cursor.executemany(query, wordsNotExists)
    rc["db"].commit()

    print 'inserted - ' + str(wordsNotExists)


def insertWordsInBooks(rc, wordsInBooks):

    if len(wordsInBooks) == 0:
        return

    # insert to table words the not existed
    cursor = rc["db"].cursor()
    query = 'INSERT INTO sadnadb.wordsInBooks (' \
            ' wordId,' \
            ' bookId,' \
            ' lineNumber,' \
            ' wordNumber,' \
            ' characterLocation,' \
            ' sentenceNumber,' \
            ' paragraphNumber)' \
            ' VALUES (%s, %s, %s, %s, %s, %s, %s)'
    cursor.executemany(query, wordsInBooks)
    rc["db"].commit()

    print 'insert words in books - ' + str(len(wordsInBooks)) + ' ' + str([x[0] for x in wordsInBooks])


def checkIfWordsExists(rc, words):

    exists = {}
    notExists = []

    if len(words) == 0:
        return exists, notExists

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
