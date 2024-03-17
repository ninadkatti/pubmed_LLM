import os
import requests
from groq import Groq

api_key=os.environ["GROK_API_KEY"]="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" 
client = Groq(api_key=api_key) 

def prepare_abstracts_for_llm(query, num_results):  
    apiUrl = 'https://nirakar09.pythonanywhere.com/'
    params = {'query': query, 'num_results': num_results}
    response = requests.get(apiUrl, params=params)

    if response.status_code == 200:
        data = response.json()

        abstracts = []  
        for result in data.get('results', []):
            abstract = result.get('Abstract', '')  
            abstracts.append(abstract) 

        llm_context = "\n\n".join(abstracts) 
        return llm_context 
    else:
        raise Exception(f"Request failed with status code: {response.status_code}") 


def answer_question_with_abstracts(model="mixtral-8x7b-32768"):
    question = input("What is your question? ")
    query = input("Enter your search keywords: ")
    num_results = int(input("Enter the number of abstracts to search: "))

    abstracts = prepare_abstracts_for_llm(query, num_results)

    groq_prompt = f"""
    Your job is to answer the questions based on the given abstracts, you are a medical helper to the doctor, analysing the sypmtoms and providing preliminary care:

    Abstracts: {abstracts}

    Question: {question} 
    Answer: """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": groq_prompt}],
        model=model
    )

    return response.choices[0].message.content 

if __name__ == "__main__": 
    answer = answer_question_with_abstracts()  
    print(answer)
