import random
import re

class AammssChatBot:
    
    negative_response = ("no","nope","nah","naw","not a chance","sorry")
    exit_commands = ("quit","pause","exit","goodbye","bye","later")


    random_question = (
        "How can I help You?",
        "What type of details do you need?",
        "Will you give some time, I will check it?",
        "What is your order ID?",
        "What is your order date?"
    )

    def __init__(self):
        self.response = {
            'ask_about_product': r'.*\s*product.*',
            'ask_about_price': r'.*price.*',
            'ask_about_shipping': r'.*\s*shipping.*',
        }

    def greet(self):
        self.name = input("what is your name ?\n")
        will_help = input(
            f"Hi {self.name}, I am chatbot. How can I help you?\n")
        if will_help in self.negative_response:
            print("Have a nice day!")
            return 
        self.chat()

    def make_exit(self, reply):
        for command in self.exit_commands:
            if reply == command:
                print("Good-Bye")
                return True

    def chat(self):
        reply = input(random.choice(self.random_question)).lower()
        while not self.make_exit(reply):
            reply = input(self.match_reply(reply))


    def match_reply(self, reply):
      for intent, regex_pattern in self.response.items():
          found_match = re.match(regex_pattern, reply)
          if found_match and intent == 'ask_about_product':
              return self.ask_about_product()
          elif found_match and intent == 'ask_about_price':
              return self.ask_about_price()
          elif found_match and intent == 'ask_about_shipping':
              return self.ask_about_shipping()
          
    def ask_about_product(self):
       responses = ("Our products are of high quality & tested.\n",
                    "You can find more product details on website.\n")
       return random.choice(responses)
      
    def ask_about_price(self):
       responses = ("The prices are based on offers and discounts.\n",
                    "The prices of product may vary.\n")
       return random.choice(responses)
      
    def ask_about_shipping(self):
        responses = ("The shipping is done within 7 working days.\n",
                     "Urgent shipping can be done with some extra charges.\n")
        return random.choice(responses)

    def no_match_intent(self):
        responses = ( "Please tell me more.\n","tell me more!\n",
                     "I see.Can you elaborate\n", "Interesting.can you tell me more ?\n",
                     "I see.How do you think?\n","why?\n",
                     "how do you think I feel when i say that.Why?\n")
        return random.choice(responses)

bot = AammssChatBot()
bot.greet()