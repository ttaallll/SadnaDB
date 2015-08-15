__author__ = 'tal'


LINES_OF_BULK_WORDS = 3


def addAllWords(rc, bookLines, bookId, startBookChar):

    currentChar = 0
    currentLine = 1
    currentParagraph = 1
    currentWords = []
    for tempLine in bookLines:

        currentWords += tempLine.split(' ')

        if currentLine % LINES_OF_BULK_WORDS == 0:

            currentWords = fixWords(currentWords)
            addWords(rc, currentWords)
            currentWords = []

        addWordsInBooks(currentWords, currentLine, currentParagraph, bookId, startBookChar, startLineChar)

        print currentLine

        currentChar += len(tempLine) + 2
        currentLine += 1
        if tempLine == '':
            currentParagraph += 1


def addWordsInBooks(words, lineNumber, paragraphNumber, bookId, startBookChar, startLineChar):



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
