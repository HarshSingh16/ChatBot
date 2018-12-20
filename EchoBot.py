#Creating an Echo Bot

#Setting the user and bot templates
user_template="USER : {0}"
bot_template="BOT : {0}"

#Lets begin by first defining a respond() function:
def respond(message):
 bot_message="Yes, I can hear you, you said :" + message
 return bot_message


#Now, lets define a send_message() function that logs a message to the bot
def send_message(message):
 print(user_template.format(message))
 response=respond(message)
 print(bot_template.format(response))


#Running a couple of test commands
send_message("Hello")
send_message("How are you")

#Works Perfectly!
