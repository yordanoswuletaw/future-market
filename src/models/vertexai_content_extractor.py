import json
from langchain_google_vertexai import VertexAI
from utils.config import settings

class ContentExtractor:
  
    def __call__(self, title, content, *args, **kwds):
        vertexai_llm = VertexAI(
            model_name=settings.GEMINI_MODEL_NAME,  # Use the PaLM 2 text model
            max_output_tokens=200,  # Limit the response length
            temperature=0.7,  # Control creativity
        )
        """Use VertexAI to extract relevant content based on the title."""
        prompt = f"""
            Extract the most relevant content from the following article that relates to the title: {title}
            **Requirements:**  
                1. Return only plain text paragraph with no formatting (no markdown, HTML, etc.)  
                2. Include only exact text passages from the article content  
                3. Exclude any sections not specifically relevant to the title  
            \n\nArticle: {content}
            """
        
        # Generate response using VertexAI
        response = vertexai_llm.invoke(prompt)
        return response.strip()

content_extractor = ContentExtractor()