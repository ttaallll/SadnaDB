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

    stats['avglengthWord'] = result[0][0]

    ###
    # average number of words in a line
    query = 'select avg(temp1.c1) from ' \
            '(SELECT COUNT(wb.lineNumber) c1, wb.lineNumber, wb.bookId ' \
            'FROM sadnadb.wordsInBooks wb ' \
            'GROUP BY wb.lineNumber, wb.bookId) temp1'
    cursor.execute(query)
    result = cursor.fetchall()

    stats['avglengthLine'] = result[0][0]

    ###
    # average number of chars in a line
    query = 'select avg(temp1.s1) from ' \
            '(SELECT SUM(LENGTH(w.word)) s1, wb.lineNumber, wb.bookId ' \
            'FROM sadnadb.wordsInBooks wb, sadnadb.words w ' \
            'WHERE w.id = wb.wordId ' \
            'GROUP BY wb.lineNumber, wb.bookId) temp1'
    cursor.execute(query)
    result = cursor.fetchall()

    stats['avglengthChars'] = result[0][0]

    return stats


