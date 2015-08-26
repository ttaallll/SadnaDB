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

    groupDetails['groupName'] = result[0][1]
    groupDetails['date'] = result[0][2]

    return groupDetails
