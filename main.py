import requests
import json
from bs4 import BeautifulSoup
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords




stop_words = stopwords.words('english')



url=input("Enter a link to summarize content inside: ")

def scrap_content(url):
    page=requests.get(url)
    page_content= page.text
    content = BeautifulSoup(page_content, 'html.parser')
    para= content.find_all('p')
    text_list = [p.text for p in para]
    complete_text = ' '.join(text_list)
    return complete_text

def clean_text(text):
    #text = remove_stopWords(text)
    text = ' '.join(text.split())
    text = remove_urls(text)
    text = text.lower()
    return text

def limit_to_2000_words(text):
    words = text.split()
    return ' '.join(words[:2000])

def split_text(text):
    max_chunk_size = 2000
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)



def remove_stopWords(text):
    splittedText=text.split()
    withoutStopWords=[word for word in splittedText if word not in stop_words]
    return ' '.join(withoutStopWords)


    
def get_response(text):
    input_chunks = split_text(text)
    output_chunks = []
    url= "http://localhost:1234/v1/chat/completions"
    headers={
        "content-type": "application/json"
    }
    system_message = {
    "role": "system",
    "content": "### Instruction: You are a helpful assistant. provide a concise summary of the following text with less than 80 words:  "
    }
    messages=[system_message]
    for chunk in input_chunks:
        user_message ={ 
                       "role":"user",
                       "content": f"{chunk} \n###Response:" }        
        messages.append(user_message)
        data={
        "messages":messages,
        "temperature": 0.7, 
        "max_tokens": 400,
        "stream": False
        }
        response = requests.post(url,headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response = response.json()
            summary=response["choices"][0]["message"]["content"]
            output_chunks.append(summary)
        else:
            print(f"Error: {response.status_code}")
    return " ".join(output_chunks)
        
    
    
page_text = scrap_content(url)
cleanedText = clean_text(page_text)
print(f"The cleaned text is : {cleanedText}/n /n /n")
with open('cleanedText.txt', 'w',encoding="utf-8") as f:
    f.write(cleanedText)

summary_answer = get_response(cleanedText)
print(f"The Summary is : {summary_answer}")
with open('summary.txt', 'w',encoding="utf-8") as f:
    f.write(summary_answer)


