import codecs
import json
import sys

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('config/muslim-app-api-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


class UploadJsonFileToFirestore:
    def __init__(self):
        if len(sys.argv[1:]) != 3:
            print(
                f'ERROR: Arguements expected [file=filepath, method=[set or add], collectionname=[firestore collection name]')
            return None

        self.filepath = sys.argv[1:][0]
        self.method = sys.argv[1:][1]
        self.collection_name = sys.argv[1:][2]

    def __str__(self):
        return (f'Uploading {self.filepath} JSON items to firestore!')

    def _load_json_data(self):
        try:
            with codecs.open(self.filepath, 'r', 'utf-8') as f:
                json_data = json.load(f)
            return json_data
        except Exception as e:
            raise e

    def _add(self, item):
        return db.collection(self.collection_name).add(item)

    def _set(self, item):
        return db.collection(self.collection_name).document(str(item['id'])).set(item)

    def upload(self):
        self.json_data = self._load_json_data()

        for idx, item in enumerate(self.json_data):
            json_str = json.dumps(item, indent=4)

            if self.method == 'set':
                self._set(item)
            else:
                self._add(item)

        print('SUCCESS UPLOAD')


if __name__ == '__main__':
    uploadjson = UploadJsonFileToFirestore()
    uploadjson.upload()
