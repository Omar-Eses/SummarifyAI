from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from prompts import *
import openai
import json
import os 
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.environ['OPENAI_API_KEY']


class ChatBotAssistant:
  def __init__(self, uploaded_file, model_name="gpt-3.5-turbo-1106", embedding_model_name="text-embedding-ada-002",summary_length = 3,details_level = "abstract"):
    # Read the file
    if(uploaded_file.endswith('pdf')):
      loader = PyPDFLoader(uploaded_file)
    else:
      loader = Docx2txtLoader(uploaded_file)

    self.pages = loader.load()

    # Define LLM
    self.model_name = model_name
    self.llm = ChatOpenAI(temperature=0.0, model_name=self.model_name)

    # Check number of tokens
    self.allowed = self.isAllowed()

    # Summary settings
    self.num_of_sent = summary_length
    self.lvl_of_det = details_level

    # Combine string
    self.context = "".join([page.page_content for page in self.pages])

    # Summary prompt
    self.summary_prompt = PromptTemplate(template=summary_prompt_template, input_variables=["text","number_of_sentences","level_of_detail"])

    # named entity recognition prompt
    self.ner_prompt = PromptTemplate(template=ner_prompt_template, input_variables=["text"])

    # Chat Messages
    self.system_msg_prompt = SystemMessagePromptTemplate.from_template(chatbot_prompt_template).format(document=self.pages)
    self.human_msg_prompt = HumanMessagePromptTemplate.from_template("{question}")
    self.chat_prompt = ChatPromptTemplate(messages=[self.system_msg_prompt,MessagesPlaceholder(variable_name="chat_history"),self.human_msg_prompt,])

    # Creating Memory 
    self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create the LLM chain
    self.conversation = LLMChain(llm=self.llm, prompt=self.chat_prompt, memory=self.memory)

  def isAllowed(self):    
      encoding = tiktoken.encoding_for_model(self.model_name)
      num_tokens = len(encoding.encode("".join([page.page_content for page in self.pages])))
      MAX_TOKEN = 15000
      return num_tokens<MAX_TOKEN

  def generate_summary(self):
    return self.llm.invoke(self.summary_prompt.format(text=self.context, number_of_sentences=self.num_of_sent,level_of_detail=self.lvl_of_det)).content

  def generate_named_entity_recognition(self):
    return json.loads(self.llm.invoke(self.ner_prompt.format(text=self.context)).content)

  def chat_bot(self,question):
    return self.conversation({"question": question})['text']