__author__ = 'pais'


def getStatistics(rc):

    stats = {}

    cursor = rc["db"].cursor()

    query = 'SELECT w.id, w.word, COUNT(w.id) c ' \
            'FROM sadnadb.words w, sadnadb.wordsInBooks wb ' \
            'WHERE w.id = wb.wordId ' \
            'GROUP BY w.id ' \
            'ORDER BY c DESC LIMIT 1000'
    cursor.execute(query)
    result = cursor.fetchall()

    stats['words'] = result

    ###
    # average length of words
    query = 'SELECT AVG(LENGTH(word))' \
            'FROM sadnadb.words'
    cursor.execute(query)
    result = cursor.fetchall()

    stats['avglength'] = result[0][0]

    return stats


