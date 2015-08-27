__author__ = 'pais'


def createGroup(rc, groupName):

    cursor = rc["db"].cursor()
    query = 'INSERT INTO sadnadb.groupWords (name) ' \
            'VALUES (%s)'
    cursor.execute(query, groupName)
    rc["db"].commit()

    query = 'SELECT id FROM sadnadb.groupWords ' \
            'ORDER BY id DESC LIMIT 1'
    cursor.execute(query)
    result = cursor.fetchall()

    return result[0][0]


def getGroup(rc, groupId):

    groupDetails = {}

    cursor = rc["db"].cursor()
    query = 'SELECT * FROM sadnadb.groupWords ' \
            'WHERE id = %s'
    cursor.execute(query, groupId)
    result = cursor.fetchall()

    groupDetails['groupId'] = groupId
    groupDetails['groupName'] = result[0][1]
    groupDetails['date'] = result[0][2]

    ###
    # get the words
    query = 'SELECT w.id, w.word FROM sadnadb.wordsInGroupWords wg, sadnadb.words w ' \
            'WHERE wg.groupWordId = %s AND wg.wordId = w.id'
    cursor.execute(query, groupId)
    result = cursor.fetchall()

    groupDetails['words'] = result

    return groupDetails


def getAllGroups(rc):
    cursor = rc["db"].cursor()
    query = 'SELECT * FROM sadnadb.groupWords ORDER BY id DESC'
    cursor.execute(query)
    result = cursor.fetchall()

    return result


def addWordToGroup(rc, groupId, word, textOrId=True):

    cursor = rc["db"].cursor()

    wordId = None

    if textOrId:
        query = 'SELECT id FROM sadnadb.words ' \
                'WHERE word = %s'
        cursor.execute(query, word)
        result = cursor.fetchall()

        if len(result) == 0:
            query = 'INSERT INTO sadnadb.words (word) ' \
                    'VALUES (%s)'
            cursor.execute(query, word)
            rc["db"].commit()

            query = 'SELECT id FROM sadnadb.words ' \
                    'WHERE word = %s'
            cursor.execute(query, word)
            result = cursor.fetchall()

        wordId = result[0][0]
    else:
        wordId = word

    query = 'INSERT INTO sadnadb.wordsInGroupWords (wordId, groupWordId) ' \
            'VALUES (%s, %s)'
    cursor.execute(query, (wordId, groupId))
    rc["db"].commit()


def removeWordFromGroup(rc, groupId, wordId):
    cursor = rc["db"].cursor()
    query = 'DELETE FROM sadnadb.wordsInGroupWords ' \
            'WHERE groupWordId = %s AND wordId = %s'
    cursor.execute(query, (groupId, wordId))
    rc["db"].commit()
