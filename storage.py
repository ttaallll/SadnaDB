__author__ = 'pais'

import lib.cloudstorage as gcs
from google.appengine.api import app_identity

from datetime import datetime
import os


def uploadToStorage(bookName, bookText):

    bucket_name = os.environ.get('BUCKET_NAME',
                                 app_identity.get_default_gcs_bucket_name())

    bucket = '/' + bucket_name

    filename = bucket + '/books/' + str(datetime.now()) + '/' + bookName

    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/plain',
                        retry_params=write_retry_params,
                        options={'x-goog-acl': 'public-read'})

    gcs_file.write(bookText)
    gcs_file.close()

    return filename


def geFromStorage(bookUrl):

    gcs_file = gcs.open(bookUrl)

    data = gcs_file.read()
    gcs_file.close()

    return data
