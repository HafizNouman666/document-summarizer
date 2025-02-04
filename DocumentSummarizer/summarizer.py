from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
#from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from text_cleaner import clean_summary_text
import re

class Summarizer:
    def __init__(self, model="gemini-1.5-flash", temperature=0.3, max_tokens=1000):
        #self.llm = OllamaLLM(model=model, temperature=temperature, max_tokens=max_tokens)
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, max_tokens=1000)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
        self._initialize_prompts()
        
    def _initialize_prompts(self):
        self.map_prompt_template = PromptTemplate(
            input_variables=['text'],
            template="Please summarize the following text:{text}Summary:"
        )
        self.combine_prompt_template = PromptTemplate(
            input_variables=['text'],
            template="Provide a final summary of the entire document . "
                     "{text}"
        )
    
    def summarize(self, text):
        chunks = self.text_splitter.create_documents([text])
        chain = load_summarize_chain(
            llm=self.llm,
            chain_type='map_reduce',
            map_prompt=self.map_prompt_template,
            combine_prompt=self.combine_prompt_template,
            verbose=False
        )
        raw_summary = chain.run(chunks)
        cleaned = clean_summary_text(raw_summary)
        return re.sub(r'\n{2,}', '', cleaned)