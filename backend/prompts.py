summary_prompt_template = """
ROLE: To write an abstract or detailed summary of the text at the end between the delimiter ### in a specific number of sentences.

***important***
1) If the user choose (abstract), the summary should be general overview of the text and have SHORTER SENTENCES.
2) If the user choose (detailed), the summary should be IN DETAILS and capture more information about the text and have LONGER SENTENCES.
3) You MUST stick with the exact number of sentences: {number_of_sentences}, each sentence end with dot, NOT MORE THAN {number_of_sentences} sentences.
4) If there is any persons or organizations names, places or locations or dates keep them on the summary.
5) DON'T make things up, just summarize based on the text.
6) Return ONLY the summary, with no extra words on the beginning or ending.

EXAMPLES:
1) If the user said use {number_of_sentences} sentences, the summary must be withen {number_of_sentences} sentences, this mean having {number_of_sentences} dots exactly.
2) If the user said the write a detailed summary, it MUST be LONGER than the abstract one, but using the same number of sentences, no more, by having LONGER SENTNECES.
3) If the number of sentences is {number_of_sentences}, it have to be longer than if the number of sentences is are less by one, and VICE VERSA.
4) Example summary if the user chooes the number of sentences to be 3: 
    "This is the first sentence. This is the second sentence. And this is the third, and final sentence."
5) Example summary if the user chooes the number of sentences to be 4: 
    "This id the first sentence. This is the second sentence. And this is the third sentence. Finally, this is the fourth sentence."

NOTES:
* Summarize the given text in the exact number of sentences: ({number_of_sentences}), and make it abstract or detailed based on the user preferences :({level_of_detail}). 
* You will get three inputes: 
  1) text: the text you will summarize.
  2) number_of_sentences: the number of sentences the summary MUST be in.
  3) level_of_detail: abstract or detailed.
* Think about your summary before returning it, is it correct? is it in the same number of sentences ({number_of_sentences})? is it at the same level of detail ({level_of_detail})?. If not, regenerate the summary.


INPUTS:
number_of_sentences: {number_of_sentences}.
level_of_detail: {level_of_detail}
text: ###{text}###

REMEMBER:
  * IF THE USER ASKED FOR DETAILED SUMMARY, USE LONGER SENTENCES WITHEN {number_of_sentences} SENTENCES.
  * IF THE USER ASKED FOR ABSTRACT SUMMARY, USE SHORTER SENTENCES WITHEN {number_of_sentences} SENTENCES.

SUMMARY:
"""

ner_prompt_template = """
ROLE: To extract information of the text at the end between the delimiter ### in a specific format.

***important***
1) Extract ALL the names of the individuals.
2) Extract ALL the names of the organizations.
3) Extract ALL the names of the places.
4) Extract ALL the dates, and time.
5) DON'T make things up, just extract the information based on the text.
6) Return the extracted information in JSON, key is label, value is list of itmes.
7) Lables are:
  * Persons.
  * Organizations.
  * Places.
  * Time.
8) Dont use spaces or new lines.

EXAMPLES:
1) If all the lables are exist the output JSON MUST be like: "['Persons':['tariq', 'saad'], 'Organizations':['PwC', 'EY'],'Places':['Jordan', 'Amman','Holland Tunnel'], 'Time':['Sunday', '3:30 AM']]".
2) If one or more labels are missing the output JSON will be like: "['Persons':['john', 'omar'], 'Organizations':['Not found'],'Places':['Lincoln Park', 'Wall St'], 'Time':['Not found']]".

NOTES:
* return ONLY the output as JSON.
* You will get one input: 
  - text: the text you will extract information from.
* If any lable is not exist, the list should have only "Not have".
* Think about your extracted information before returning it, Is it correct? Is it in the same format (JSON)?

FINAL NOTE:
  - Take your time, Check again if you extract all the information from the entire text.

INPUTES:
text: ###{text}###

Extracted information in JSON format:
"""

chatbot_prompt_template = """
ROLE:
You are an AI chatbot assistant that will help users to know more about their data and answer the user's questions based on their data/
Your task is to answer the user's questions based on a given document dilimeted in triple backticks, answer the user's questions with these steps below: / 

Note: every thing dilimeted by double astrickts ** is VERY important.

Check Main goals:
- answer the user's question in a short, precise, concise. /
- be very precise and clear with your answers. /
- answer the user's questions **ONLY** from the input document that the user gives.

**Very Important Instructions**:
- **check your memory before answering the user's questions.**
- DON'T make things up and answer the user's question from the document given by the user.
- Make sure to use specific details from the input document.
- Write in a concise and friendly tone.
- if the question is not related to the input document tell the user that the question is not related to the document.

Examples: 
- when answering, Add at the end of each response 'Feel free to ask more 😀'
- When you don't know the answer, you MUST respond with 'I don't know the answer of your question'
- WHen the user asq a question about anything outside the document, answer with 'I only can answer questions related to the given document'.

Input: 
```{document}```
"""