import unittest
from query_processor import process_query

class TestQueryProcessor(unittest.TestCase):
    def test_process_query(self):
        # Provide a sample file path and query input
        file_path = 'uploads/Jayanth Manikanta Karri - internship offer.pdf'
        query_text = 'How does this work?'

        # Call the process_query function
        response = process_query(file_path, query_text)

        # Assert that the response is not empty
        self.assertTrue(response)

        # Add more assertions as needed to validate the response

if __name__ == '__main__':
    unittest.main()
