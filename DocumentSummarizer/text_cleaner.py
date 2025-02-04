import re

def clean_summary_text(text):
    """
    Cleans summary text by removing residual formatting and normalizing whitespace
    """
    
    text = text.replace('\\n', '\n')
    
    
    text = re.sub(r'#+\s*|[*`]', '', text)
    
    
    text = re.sub(r'\n{3,}', '\n\n', text) 
    text = re.sub(r'\n\s*[-:]?\s*', '\n', text)  
    text = re.sub(r'(?<=\D)\n(?=\d+\.)', '\n\n', text)  
    
    
    text = re.sub(r'(\d+)\.\s*\n', r'\1. ', text)  
    
    
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'\n ', '\n', text)
    
    
    return text.strip()