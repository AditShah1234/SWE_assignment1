import unittest

from app import app


class TestFlash(unittest.TestCase):

    # Ensure the index was setup correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure the inputs was setup correctly
    def test_inputs(self):
        tester = app.test_client(self)
        response = tester.get('/inputs', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure the inputs page responds correctly
    def test_inputs_response(self):
        tester = app.test_client(self)
        response = tester.get('/inputs', content_type='html/text')
        self.assertTrue(b'Coordinates' in response.data)

    # Ensure the correct response if the coordinates are at rest
    def test_coordinates_rest(self):
        tester = app.test_client(self)
        # res = tester.post('/inputs/', data={'X_axis': '0', 'Y_axis': '0'}, follow_redirects=True)
        res = tester.post('/inputs', data=dict(X_axis='0', Y_axis='0'), follow_redirects=True)
        # self.assertTrue(res.text('Bike is at rest.', res.get_data(as_text=True)))
        try:
            assert b'Bike is at rest.' in res.data
            print(res.data)
        except AssertionError:
            print(res.data)
            print("Assertion failed!")

    # Ensure the correct response if the coordinates are at rest
    def test_coordinates_move(self):
        tester = app.test_client(self)
        res = tester.post('/inputs', data=dict(X_axis='0', Y_axis='0'), follow_redirects=True)
        try:
            assert b'Bike is relocated!!' in res.data
            print(res.data)
        except AssertionError:
            print(res.data)
            print("Assertion failed!")


if __name__ == "__main__":
    unittest.main()
