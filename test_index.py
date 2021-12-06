from index import app
import unittest
import requests
import os


class IndexTest(unittest.TestCase):
    """
    class IndexTest, test the flask api of mindmap app, test index.py
    """

    URL = "http://127.0.0.1:8081/"

    CREATE_DATA = {
        "id": "my-map"
    }
    CREATE_DATA_ERROR_SEP = {
        "id": "my/map"
    }
    CREATE_DATA_ERROR_SCHEMA = {
        "id2": "my-map"
    }
    CREATE_DATA_PATH = "./data/my-map/root"

    ADD_DATA = {
        "path": "i\like\potatoes",
        "text": "Because reasons"
    }
    ADD_ID = "id=my-map"
    ADD_ID_ERROR_SCHEMA = "id2=my-map"
    ADD_ID_ERROR_MISSING_ID = "id="
    ADD_ID_ERROR_ID = "id=my/map"
    ADD_DATA_PATH = './data/my-map/root/i/like'
    ADD_DATA_FILE_PATH = './data/my-map/root/i/like/potatoes'

    READ_PATH = 'path=/i/like/potatoes'
    READ_PATH_ERROR_SCHEMA = 'patth=/i/like/potatoes'
    READ_PATH_ERROR_MISSING_PATH = 'path='

    READ_LEAF_OUTPUT = {"path": "/i/like/potatoes", "text": "Because reasons"}
    READ_MAP_OUTPUT = b"root/\n    i/\n        like/\n            potatoes\n"

    def test_createmap(self):
        """
        test_createmap function, test to create a map dicretory from root
        crul cmd example:
            curl -v -X POST -H "Content-Type: application/json" 
            -d "{\"id\": \"my-map\"}" http://127.0.0.1:8081/createma
        """
        resp = requests.post(self.URL+"createmap", json=self.CREATE_DATA)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(os.path.exists(self.CREATE_DATA_PATH))

    def test_createmap_error_ossep(self):
        """
        test_createmap_error_ossep function, test api no accpet id with os separator
        """
        resp = requests.post(self.URL+"createmap",
                             json=self.CREATE_DATA_ERROR_SEP)
        self.assertEqual(resp.status_code, 400)

    def test_createmap_error_schema(self):
        """
        test_createmap_error_schema fucntion, test api check the ID schema
        """
        resp = requests.post(self.URL+"createmap",
                             json=self.CREATE_DATA_ERROR_SCHEMA)
        self.assertEqual(resp.status_code, 422)

    def test_addleaf(self):
        """
        test_addleaf function, test to add a file from ID root directory
        crul cmd example:
            curl -X POST -H "Content-Type: application/json" 
            -d "{\"path\": \"i\/like\/potatoes\",\"text\": \"Because I like it\"}" 
            http://localhost:0881/addleaf?id=my-map
        """
        resp = requests.post(self.URL+"addleaf?" +
                             self.ADD_ID, json=self.ADD_DATA)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(os.path.exists(self.ADD_DATA_PATH))
        self.assertTrue(os.path.isfile(self.ADD_DATA_FILE_PATH))

    def test_addleaf_error_schema(self):
        """
        test_addleaf_error_schema function, test api return error 
        when ID schema agrs not correct
        """
        resp = requests.post(self.URL+"addleaf?" +
                             self.ADD_ID_ERROR_SCHEMA, json=self.ADD_DATA)
        self.assertEqual(resp.status_code, 422)

    def test_addleaf_error_missing_id(self):
        """
        test_addleaf_error_missing_id function, test api return error 
        when ID data agrs missing
        """
        resp = requests.post(self.URL+"addleaf?" +
                             self.ADD_ID_ERROR_MISSING_ID, json=self.ADD_DATA)
        self.assertEqual(resp.status_code, 422)

    def test_addleaf_error_id(self):
        """
        test_addleaf_error_missing_id function, test api return error 
        when ID data agrs not correct
        """
        resp = requests.post(self.URL+"addleaf?" +
                             self.ADD_ID_ERROR_ID, json=self.ADD_DATA)
        self.assertEqual(resp.status_code, 400)

    def test_readleaf(self):
        """
        test_readleaf function, test to read a file from path directory
        crul cmd example:
            curl -X GET -H "Content-Type: application/json" 
            "http://localhost:8081/readleaf?id=my-map&path=i/like/potatoes"
        """
        resp = requests.get(self.URL+"readleaf?" +
                            self.ADD_ID + '&' + self.READ_PATH)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), self.READ_LEAF_OUTPUT)

    def test_readleaf_error_schema(self):
        """
        test_readleaf_error_schema function, test api return error 
        when path schema agrs not correct
        """
        resp = requests.get(self.URL+"readleaf?" + self.READ_PATH_ERROR_SCHEMA)
        self.assertEqual(resp.status_code, 422)

    def test_readleaf_error_missing_path(self):
        """
        test_readleaf_error_missing_path function, test api return error 
        when path data agrs missing
        """
        resp = requests.get(self.URL+"readleaf?" +
                            self.READ_PATH_ERROR_MISSING_PATH)
        self.assertEqual(resp.status_code, 422)

    def test_readleaf_error_no_args(self):
        """
        test_readleaf_error_no_args function, test api return error 
        when no args
        """
        resp = requests.get(self.URL+"readleaf")
        self.assertEqual(resp.status_code, 422)

    def test_readmap(self):
        """
        test_readmap function, test to read tree root directory from id
        crul cmd example:
            curl -X GET -H "Content-Type: application/json" 
            "http://localhost:8081/readmap?id=my-map
        """
        resp = requests.get(self.URL+"readmap?" + self.ADD_ID)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, self.READ_MAP_OUTPUT)


if __name__ == "__main__":
    tester = IndexTest()
    # tester.test_addleaf()
    # tester.test_readmap()
    unittest.main()
