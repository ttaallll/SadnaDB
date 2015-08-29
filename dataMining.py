__author__ = 'pais'


def getDataMining(rc):

    dataMining = {'commonWordsInSameLine': {'books': {}}}

    cursor = rc["db"].cursor()
    query = 'select b.id, b.title, w1.id, w1.word, w2.id, w2.word, dm.apperanceCount, dm.dateCreated ' \
            'from sadnadb.dataMining dm, sadnadb.books b, sadnadb.words w1, sadnadb.words w2 ' \
            'where b.id = dm.bookId and w1.id = dm.wordId1 and w2.id = dm.wordId2 ' \
            'ORDER BY dm.apperanceCount DESC LIMIT 2000'
    cursor.execute(query)
    result = cursor.fetchall()

    tempBooks = {}

    for r in result:
        if r[0] not in tempBooks:
            tempBooks[r[0]] = []
        tempBooks[r[0]] += [r]

    # remove duplicates
    for tempBook in tempBooks:
        bookData = []
        i = 0
        while i < len(tempBooks[tempBook]):
            bookData += [tempBooks[tempBook][i]]
            i += 2

        dataMining['commonWordsInSameLine']['books'][tempBook] = bookData

    return dataMining


def runDataMining(rc, bookId):

    cursor = rc["db"].cursor()
    query = 'insert into sadnadb.dataMining (bookId, apperanceCount, wordId1, wordId2)' \
            'select wb1.bookId, count(wb1.wordId), wb1.wordId, wb2.wordId ' \
            'from ' \
            '(select * from sadnadb.wordsInBooks twb1 where twb1.bookId = %s) wb1, ' \
            '(select * from sadnadb.wordsInBooks twb2 where twb2.bookId = %s) wb2 ' \
            'where wb1.lineNumber = wb2.lineNumber ' \
            'and wb1.wordId != wb2.wordId ' \
            'group by wb1.wordId, wb2.wordId'
    cursor.execute(query, (bookId, bookId))
    rc["db"].commit()
