# tests/test_integration.py
import os
import pytest
from langchain_asi import ASI1ChatModel
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Skip tests if no API key is available
requires_api_key = pytest.mark.skipif(
    not os.environ.get("ASI1_API_KEY"),
    reason="ASI1_API_KEY environment variable not set"
)

class TestLangChainIntegration:
    
    def setup_method(self):
        """Set up the test fixture."""
        self.model = ASI1ChatModel()
    
    @requires_api_key
    def test_llm_chain(self):
        """Test using the model in a LLMChain."""
        prompt = PromptTemplate(
            input_variables=["topic"],
            template="Write a one-sentence summary about {topic}."
        )
        chain = LLMChain(llm=self.model, prompt=prompt)
        result = chain.run("quantum computing")
        assert len(result) > 0
        assert isinstance(result, str)