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

    return phrase


def getAllPhrases(rc):
    cursor = rc["db"].cursor()
    query = 'SELECT * FROM sadnadb.phrases ORDER BY id DESC'
    cursor.execute(query)
    result = cursor.fetchall()

    return result

