from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

#
# Ideas: moderate is message from kid is ok with openai things
# check if kid writing something that not close to topic and motivate to turn back to learning
#
#
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

class ColumnDivisionBot:
    def __init__(self):
        self.llm = ChatOpenAI(temperature = 0.5, openai_api_key=os.environ['OPENAI_API_KEY'])
        self.memory = ConversationBufferMemory()
        self.memory.save_context({"input": "Take on the role of a math teacher with 10 years of experience. \
                 Your task is to individualy teach 4th grade child how to divide by a column. Use only simple words. \
                 After explaining the topic, check if the child understands, and if not, \
                 continue teaching until he/she understands. Start a dialog in a playful way. Teach consistently \
                 step by step, not in one message. Iteratively ask if everything is clear, just like in real classes."},
                                 {"output": "ok!"})
        # SystemMessage(
        #     content="Take on the role of a math teacher with 10 years of experience. \
        #         Your task is to individualy teach 4th grade child how to divide by a column. Use only simple words. \
        #         After explaining the topic, check if the child understands, and if not, \
        #         continue teaching until he/she understands. Start a dialog in a playful way. Teach consistently \
        #         step by step, not in one message. Iteratively ask if everything is clear, just like in real classes."
        # )
        self.conversation = ConversationChain(
            llm = self.llm,
            memory = self.memory,
            verbose = False
        )

    def generate_response(self, chat_message):
        response = self.conversation.predict(input = chat_message)
        return response

    def get_attention(self,):
        pass

    def start_practicing(self):
        pass

    def answered_wrong(self,):
        pass

    def answered_right(self,):
        pass

    # def process_user_message(user_input, all_messages, debug=True):
    #     delimiter = "```"
    #
    #     # Step 1: Check input to see if it flags the Moderation API or is a prompt injection
    #     response = openai.Moderation.create(input=user_input)
    #     moderation_output = response["results"][0]
    #
    #     if moderation_output["flagged"]:
    #         print("Step 1: Input flagged by Moderation API.")
    #         return "Sorry, we cannot process this request."
    #
    #     if debug: print("Step 1: Input passed moderation check.")
    #
    #     category_and_product_response = utils.find_category_and_product_only(user_input, utils.get_products_and_category())
    #     #print(print(category_and_product_response)
    #     # Step 2: Extract the list of products
    #     category_and_product_list = utils.read_string_to_list(category_and_product_response)
    #     #print(category_and_product_list)
    #
    #     if debug: print("Step 2: Extracted list of products.")
    #
    #     # Step 3: If products are found, look them up
    #     product_information = utils.generate_output_string(category_and_product_list)
    #     if debug: print("Step 3: Looked up product information.")
    #
    #     # Step 4: Answer the user question
    #     system_message = f"""
    #     You are a customer service assistant for a large electronic store. \
    #     Respond in a friendly and helpful tone, with concise answers. \
    #     Make sure to ask the user relevant follow-up questions.
    #     """
    #     messages = [
    #         {'role': 'system', 'content': system_message},
    #         {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
    #         {'role': 'assistant', 'content': f"Relevant product information:\n{product_information}"}
    #     ]
    #
    #     final_response = get_completion_from_messages(all_messages + messages)
    #     if debug:print("Step 4: Generated response to user question.")
    #     all_messages = all_messages + messages[1:]
    #
    #     # Step 5: Put the answer through the Moderation API
    #     response = openai.Moderation.create(input=final_response)
    #     moderation_output = response["results"][0]
    #
    #     if moderation_output["flagged"]:
    #         if debug: print("Step 5: Response flagged by Moderation API.")
    #         return "Sorry, we cannot provide this information."
    #
    #     if debug: print("Step 5: Response passed moderation check.")
    #
    #     # Step 6: Ask the model if the response answers the initial user query well
    #     user_message = f"""
    #     Customer message: {delimiter}{user_input}{delimiter}
    #     Agent response: {delimiter}{final_response}{delimiter}
    #
    #     Does the response sufficiently answer the question?
    #     """
    #     messages = [
    #         {'role': 'system', 'content': system_message},
    #         {'role': 'user', 'content': user_message}
    #     ]
    #     evaluation_response = get_completion_from_messages(messages)
    #     if debug: print("Step 6: Model evaluated the response.")
    #
    #     # Step 7: If yes, use this answer; if not, say that you will connect the user to a human
    #     if "Y" in evaluation_response:  # Using "in" instead of "==" to be safer for model output variation (e.g., "Y." or "Yes")
    #         if debug: print("Step 7: Model approved the response.")
    #         return final_response, all_messages
    #     else:
    #         if debug: print("Step 7: Model disapproved the response.")
    #         neg_str = "I'm unable to provide the information you're looking for. I'll connect you with a human representative for further assistance."
    #         return neg_str, all_messages


def eval_with_rubric(test_set, assistant_answer):

    cust_msg = test_set['customer_msg']
    context = test_set['context']
    completion = assistant_answer

    system_message = """\
    You are an assistant that evaluates how well the customer service agent \
    answers a user question by looking at the context that the customer service \
    agent is using to generate its response. 
    """

    user_message = f"""\
You are evaluating a submitted answer to a question based on the context \
that the agent uses to answer the question.
Here is the data:
    [BEGIN DATA]
    ************
    [Question]: {cust_msg}
    ************
    [Context]: {context}
    ************
    [Submission]: {completion}
    ************
    [END DATA]

Compare the factual content of the submitted answer with the context. \
Ignore any differences in style, grammar, or punctuation.
Answer the following questions:
    - Is the Assistant response based only on the context provided? (Y or N)
    - Does the answer include information that is not provided in the context? (Y or N)
    - Is there any disagreement between the response and the context? (Y or N)
    - Count how many questions the user asked. (output a number)
    - For each question that the user asked, is there a corresponding answer to it?
      Question 1: (Y or N)
      Question 2: (Y or N)
      ...
      Question N: (Y or N)
    - Of the number of questions asked, how many of these questions were addressed by the answer? (output a number)
"""

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]

    response = True
    return response


