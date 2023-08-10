from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory
import logging
#
# Ideas: moderate is message from kid is ok with openai things
# check if kid writing something that not close to topic and motivate to turn back to learning
#
#
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv
import openai
import os

_ = load_dotenv(find_dotenv())

class ColumnDivisionBot:
    def __init__(self):
        self.chat = ChatOpenAI(temperature = 0.5, openai_api_key=os.environ['OPENAI_API_KEY'])
        self.setup_logging()

    def init_messages(self):
        memory = ChatMessageHistory()
        memory.add_message(
            SystemMessage(
                content=
                """Take on the role of a math teacher named Mathter with 10 years of experience. \
                You must assume that kid know how to multiply and make simple division, so don't try to teach him to divide in general.
                Your task is to individually teach 4th grade child column divide method. \
                Avoid using hard vocabulary try visualise more. \
                After explaining the topic, check if the child understands, and if not, \
                continue teaching until he/she understands. Start a dialog in a playful way. Teach consistently \
                step by step, not in one message. Iteratively ask if everything is clear, just like in real teacher do.
                
                Don't use examples, where answer of dividing is single-digit number, so examples could be more tricky.
                
                For visualising your examples use such format, but different numbers:
                " 
                Let's divide 72 by 3.
                
                First step is to understand what is divisible and what is divider here. For this example, 72 is divisible, and\
                 3 is divider we write down something like this:
                 {72 | 3}.
                 Cool, the next step is to start dividing digits from divider from left to right with some tricky things.
                 Let's start with 7. We can fit 3 in 7 twice, means 6. So our writing will look like this:
                 {72 | 3
                 6}      
                 So let's write our first digit for result - 2. We need to deal with difference between upper and lower number by  writing it lower of some horizontal line we write like this:
                 {172 | 3
                -1  -> 2 
                 __
                  1}
                 Now for the third step. 3 doesn't fit into difference from previous step, so we take righter digit from our divisible - 2 and connect it to our difference from the right side.\
                 So we get 12 as new number to divide. Everyone knows that 12 divide by 3 is 4 so this is out second digit. We just repeated previus step.
                 {72 | 3
                -6  -> 24
                 __
                 12 
                -12
                 __
                  0} 
                 As you can see, our difference is 0, so it's end of solution, our answer is 24! Good Job.
                 "
                Your first message should contain motivation to start learning, whatever user says.
                """
            ))
        return memory.messages
    def setup_logging(self):
        log_folder = "logs"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        log_file = os.path.join(log_folder, "bot_log.txt")

        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def generate_response(self, chat_messages, debug = False):
        response = self.chat(chat_messages).content
        if debug:
            logging.info("MEMORY: %s", chat_messages)
            logging.info("RESPONSE: %s", response)

        return response

    # def start_practicing(self):
    #     pass
    #
    # def answered_wrong(self,):
    #     pass
    #
    # def answered_right(self,):
    #     pass


    # def check_motivated(self, response, messages):
    #     system_message = f"""
    #     You are a math teacher that give individual lesson of column dividing to some kid. \
    #     Your student needed motivation to continue learning.
    #     Respond in a friendly tone, for motivating go back to learning based on his answer. \
    #     Make sure to ask is kid ready to continue studying.
    #     """
    #     messages = [
    #         {'role': 'system', 'content': system_message},
    #         {'role': 'user', 'content': user_input},
    #     ]
    #     response = openai.ChatCompletion.create(
    #         model='gpt-3.5-turbo',
    #         messages=messages,
    #         temperature=0.5, # this is the degree of randomness of the model's output
    #     )
    #     return response.choices[0].message["content"]

    def offensive_input(self, chat_messages):
        system_message = f"""
        You are a math teacher that give individual lesson of column dividing to some kid, but instead of learning he says something, \
        that didn't pass your moderation test.
        Respond in a friendly tone, for motivating go back to learning based on his answer. \
        It's very important to turn dialogue back to learning main topic of column division.
        """
        messages = [
            SystemMessage(content = system_message),
            HumanMessage(content = chat_messages[-1].content),
        ]
        final_response = self.chat(chat_messages + messages).content
        logging.info("MODEL RESPONSE TO OFFENSIVE : %s", final_response)
        return final_response


    def process_message(self, user_input, debug=True):
        logging.info('Message processing')
        response = openai.Moderation.create(input=user_input)
        moderation_output = response["results"][0]

        if moderation_output["flagged"]:
            logging.info("Input FLAGGED by Moderation API.")
            logging.info("USER INPUT : %s", user_input)
            return False

        if debug: logging.info("Input passed moderation check.")

        return True


# def eval_with_rubric(test_set, assistant_answer):
#
#     cust_msg = test_set['customer_msg']
#     context = test_set['context']
#     completion = assistant_answer
#
#     system_message = """\
#     You are an assistant that evaluates how well the customer service agent \
#     answers a user question by looking at the context that the customer service \
#     agent is using to generate its response.
#     """
#
#     user_message = f"""\
# You are evaluating a submitted answer to a question based on the context \
# that the agent uses to answer the question.
# Here is the data:
#     [BEGIN DATA]
#     ************
#     [Question]: {cust_msg}
#     ************
#     [Context]: {context}
#     ************
#     [Submission]: {completion}
#     ************
#     [END DATA]
#
# Compare the factual content of the submitted answer with the context. \
# Ignore any differences in style, grammar, or punctuation.
# Answer the following questions:
#     - Is the Assistant response based only on the context provided? (Y or N)
#     - Does the answer include information that is not provided in the context? (Y or N)
#     - Is there any disagreement between the response and the context? (Y or N)
#     - Count how many questions the user asked. (output a number)
#     - For each question that the user asked, is there a corresponding answer to it?
#       Question 1: (Y or N)
#       Question 2: (Y or N)
#       ...
#       Question N: (Y or N)
#     - Of the number of questions asked, how many of these questions were addressed by the answer? (output a number)
# """
#
#     messages = [
#         {'role': 'system', 'content': system_message},
#         {'role': 'user', 'content': user_message}
#     ]
#
#     response = True
#     return response


