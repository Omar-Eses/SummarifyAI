from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import json

class ChatBotAssistant:
  def __init__(self, uploaded_file, model_name="gpt-3.5-turbo-1106", embedding_model_name="text-embedding-ada-002",summary_length = 3,details_level = "abstract"):
    if(uploaded_file.endswith('pdf')):
      loader = PyPDFLoader(uploaded_file)
    else:
      loader = Docx2txtLoader(uploaded_file)
    self.pages = loader.load()
    self.model_name = model_name
    self.llm = ChatOpenAI(temperature=0, model_name=self.model_name)
    self.allowed = self.isAllowed()
    self.num_of_sent = summary_length
    self.lvl_of_det = details_level
  def isAllowed(self):    
      encoding = tiktoken.encoding_for_model(self.model_name)
      num_tokens = len(encoding.encode("".join([page.page_content for page in self.pages])))
      MAX_TOKEN = 15000
      return num_tokens<MAX_TOKEN

  def generate_summary(self):
    prompt_template = """
  ROLE: To write an abstract or detailed summary of the text at the end between the delimiter ### in a specific number of sentences.

  ***important***
  1) If the user choose (abstract), the summary should be general overview of the text and have shorter sentences.
  2) If the user choose (detailed), the summary should be in details and capture more information about the text and have longer sentences.
  3) You MUST stick with the exact number of sentences, each sentence end with dot.
  4) If there is any persons or organizations names, places or locations or dates keep them on the summary.
  5) DON'T make things up, just summarize based on the text.
  6) Return ONLY the summary, with no extra words on the beginning or ending.

  EXAMPLES:
  1) If the user said use 3 sentences, the summary must be withen 3 sentences, that's meen having 3 dots exactly.
  2) If the user said the write a detailed summary, it MUST be longer than the abstract one, but using the same number of sentences, no more.
  3) If the number_of_sentences is 4, it have to be longer than if the number_of_sentences is 3 and VICE VERSA.

  NOTES:
  * Summarize the given text in the exact number of sentences, and make it abstract or detailed based on the user preferences. 
  * You will get three inputes: 
    1) text: the text you will summarize.
    2) number_of_sentences: the number of sentences the summary MUST be in.
    3) level_of_detail: abstract or detailed.
  * Think about your summary before returning it, is it correct? is it in the same number_of_sentences? is it at the same level_of_detail?


  INPUTS:
  number_of_sentences: {number_of_sentences}.
  level_of_detail: {level_of_detail}
  text: ###{text}###

  SUMMARY:
  """
    prompt = PromptTemplate(template=prompt_template, input_variables=["text","number_of_sentences","level_of_detail"])
    context = "".join([page.page_content for page in self.pages])
    p = prompt.format(text=context, number_of_sentences=self.num_of_sent,level_of_detail=self.lvl_of_det)
    return self.llm.invoke(p).content

  def generate_ner(self):
    prompt_template = """
  ROLE: To extract information of the text at the end between the delimiter ### in a specific format.

  ***important***
  1) Extract the names of the individuals.
  2) Extract the names of the organizations.
  3) Extract the names of the places.
  4) Extract the dates, and time.
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

  INPUTES:
  text: ###{text}###

  Extracted information in JSON format:
  """
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    context = "".join([page.page_content for page in self.pages])
    p = prompt.format(text=context)
    return json.loads(self.llm.invoke(p).content)