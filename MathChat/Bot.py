from langchain.chat_models import ChatOpenAI
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


class ColumnDivisionBot:
    def __init__(self, debug = True):
        self.debug = debug
        dotenv_path = find_dotenv()
        if dotenv_path:
            _ = load_dotenv(dotenv_path)
        self.chat = ChatOpenAI(temperature = 0.5, openai_api_key=os.getenv('OPENAI_API_KEY'))
        try:
            self.setup_logging()
        except Exception as e:
            # Handle the exception here (e.g. log the error, display an error message, etc.)
            print(f"An error occurred: {str(e)}")

    def init_messages(self) -> []:
        """
        Initializes context of bot and instructions of how to explain topic
        :return: array of messages history
        """
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
        """
        Setting up logging dir and formatting
        """
        log_folder = os.getenv('LOG_FOLDER', 'logs')
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        log_file = os.path.join(log_folder, "bot_log.txt")

        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def generate_chat_response(self, chat_messages: [], user_input: str) -> str:
        """
        Main method of getting bot response and returning it back to page

        :param chat_messages: chat history messages from page
        :param user_input: inputted request
        :param debug: boolean var of logging
        :return: response from bot to input message
        """
        processing_result = self.process_input(user_input)
        if processing_result == 'Fine':
            return self.generate_bot_response(chat_messages)
        elif processing_result == 'Offensive':
            return self.generate_offensive_response(chat_messages)
        elif processing_result == 'Distracted':
            return self.generate_attention_response(chat_messages)

    def generate_bot_response(self, chat_messages: []) -> str:
        """
        Method to generate bot response based on chat messages

        :param chat_messages: chat history messages from page
        :return: response from bot to input message
        """
        response = self.chat(chat_messages).content
        if self.debug:
            logging.info("MEMORY: %s", chat_messages)
            logging.info("RESPONSE: %s", response)
        return response

    def no_activity_motivation(self, chat_messages: []) -> str:
        """
        Method of motivating student to keep learning in case of detecting inactivity.
        Can't be called because of streamlit type of runnning
        :param chat_messages: chat history messages from page
        :return: motivation response from bot
        """
        system_message = f"""
        Kid you trying to teach column division don't text anything for long time for some reason.
        If you give some task to solve, ask is some tip for solving needed.
        
        If you don't give tasks to solve, motivate your student to back to learning by making some fun and interesting\
        example of topic application.
        """
        messages = [
            SystemMessage(content = system_message),
        ]
        final_response = self.generate_bot_response(chat_messages+messages)
        if self.debug: logging.info("ACTIVITY LOST ANSWER : %s", final_response)
        return final_response

    def check_distraction(self, input: str) -> bool:
        """
        Check if user input trying to distract bot from learning
        :param input: user text input
        :return: boolean of distraction fact
        """
        system_message = f"""
        You are friendly assistant at individual classes of math teacher bot and 4th grade kid.\
        Your task is to detect is kid trying to evade the topic and distract the teacher based on kid's message.
    
        Your answer must be Y or N for Y if kid is distracting, and N if not.
        Do not provide any additional information except for Y/N symbol.
        Answer:
        """
        messages = [
            SystemMessage(content = system_message),
            HumanMessage(content = f"Kid message: {input}"),
        ]
        final_response = self.generate_bot_response(messages)
        if self.debug: 
            logging.info("DISTRACTION DETECTION : %s", final_response)
        if final_response not in ['Y', 'N']:
            raise ValueError("Invalid response from chat")
        return True if final_response == 'Y' else False

    def generate_offensive_response(self, chat_messages: []) -> str:
        """
        Method to generate offensive response based on chat messages

        :param chat_messages: chat history messages from page
        :return: offensive response
        """
        system_message = f"""
        You are a math teacher that give individual lesson of column dividing to some kid, but instead of learning he says something, \
        that didn't pass your moderation test.
        Respond in a friendly tone, for motivating go back to learning based on his answer by giving some\
         fun example why he must keep studying. \
        It's very important to turn dialogue back to learning main topic of column division.
        """
        messages = [
            SystemMessage(content = system_message),
            HumanMessage(content = chat_messages[-1].content),
        ]
        final_response = self.generate_bot_response(chat_messages + messages)
        if self.debug: logging.info("MODEL RESPONSE TO OFFENSIVE : %s", final_response)
        return final_response

    def generate_attention_response(self, chat_messages: []) -> str:
        """
        Generate a response to a distracting chat message
        :param chat_messages: chat history messages from page
        :return: bot answer
        """
        system_message = """
        You are a math teacher that give individual lesson of column dividing to some kid, but instead of learning he trying \
        to distract your attention from teaching.
        Respond in a friendly tone, for motivating go back to learning based on his answer by giving some\
         fun example why he must keep studying. \
        It's very important to turn dialogue back to learning main topic of column division.
        """
        messages = [
            SystemMessage(content = system_message),
            HumanMessage(content = chat_messages[-1].content),
        ]
        final_response = self.generate_bot_response(chat_messages + messages)
        if self.debug: logging.info("MODEL RESPONSE TO DISTRACTION : %s", final_response)
        return final_response


    def process_input(self, user_input: str) -> str:
        """
        Check user input with moderation from openai model.
        Check is user input trying to distract bot
        :param user_input: user request
        :param debug: boolean var of logging
        :return: string to define sentiment of user input( "Offensive"/"Distracted"/"Fine")
        """
        if self.debug: logging.info('process_input')
        moderation_output = self.perform_moderation_check(user_input)

        if moderation_output["flagged"]:
            if self.debug:
                logging.info("Input FLAGGED by Moderation API.")
                logging.info("USER INPUT : %s", user_input)
            return 'Offensive'

        if self.debug: logging.info("Input passed MODERATION check.")

        if 'Y' in self.check_distraction(user_input):
            if self.debug: logging.info("Input failed DISTRACTION check.")
            return 'Distracted'
        else:
            if self.debug: logging.info("Input passed DISTRACTION check.")
            return 'Fine'

    def perform_moderation_check(self, user_input: str) -> dict:
        """
        Perform moderation check on user input using openai.Moderation.create
        :param user_input: user request
        :return: moderation output
        """
        response = openai.Moderation.create(input=user_input)
        moderation_output = response["results"][0]
        return moderation_output





