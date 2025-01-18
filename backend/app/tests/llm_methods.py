import unittest
from unittest.mock import patch, MagicMock
from langchain_openai import AzureChatOpenAI

from backend.app.utils.useful_functions import get_azure_llm


class TestLLMPointer(unittest.TestCase):
    def setUp(self):
        patcher = patch('backend.app.utils.useful_functions.get_azure_llm')
        self.mock_get_llm = patcher.start()
        self.addCleanup(patcher.stop)

        self.mock_llm_instance = MagicMock(spec=AzureChatOpenAI)
        self.mock_get_llm.return_value = self.mock_llm_instance

        self.llm = get_azure_llm()


    def test_llm_pointer_usage(self):
        # Example of another test using the same llm_pointer instance
        self.assertIsInstance(self.llm, AzureChatOpenAI)
        message =  self.llm.invoke("give an answer that is a regex of hello but dont use the word. meaning give me an answer "
                                               "that will pass:  self.assertRegex(message.content, r'hello'")
        print(message.content)
        self.assertRegex(message.content, r"hello")
        # Add more assertions or logic to test the usage of llm_pointer
    def test_chain_with_mocked_llm(self):

        self.mock_llm_instance.invoke.return_value = "mocked response"
        response = self.llm.invoke("mocked prompt")
        self.assertEqual(response, "mocked response")

if __name__ == '__main__':
    unittest.main()