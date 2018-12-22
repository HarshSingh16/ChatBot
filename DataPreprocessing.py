#importing the libraries
import tensorflow as tf
import numpy as np
import re
import time

#Loading the datasets
lines=open("movie_lines.txt",encoding="utf-8",errors="ignore").read().split("\n")   
conversations=open("movie_conversations.txt",encoding="utf-8",errors="ignore").read().split("\n")   

#Creating a dictionary for lines
id2line={}
for line in lines:
    _line1=line.split(" +++$+++ ")
    if len(_line1)==5:
        id2line[_line1[0]]=_line1[4]

 
#Creating a LIST for conversations   
coversation_ids=[]
for conversation in conversations[:-1]:
    _conversation=conversation.split(" +++$+++ ")[-1][1:-1].replace("'","").replace(" ","")
    coversation_ids.append(_conversation.split(","))
    

#Defining Questions and Answers-mapping questions and answers
questions=[]
answers=[]
for conversation in coversation_ids:
    for i in range(len(conversation)-1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])
    


#Doing the first cleaning
def cleantext(text):
    text=text.lower()
    text=re.sub(r"he's","he is",text)
    text=re.sub(r"she's","she is",text)
    text=re.sub(r"i'm","i am",text)
    text=re.sub(r"that's","that is",text)
    text=re.sub(r"what's","what is",text)
    text=re.sub(r"where's","where is",text)
    text=re.sub(r"\'ll"," will",text)
    text=re.sub(r"\'ve"," have",text)
    text=re.sub(r"\'re"," are",text)
    text=re.sub(r"\'d"," would",text)
    text=re.sub(r"won't"," will not",text)
    text=re.sub(r"can't"," cannot",text)
    text=re.sub(r"[-()\"#/@;:<>{}+=~|.?,]","",text)
    return text


#Cleaning the questions:
Clean_questions=[]
for question in questions:
    Clean_questions.append(cleantext(question))

#Cleaning the answers
Clean_answers=[]
for answer in answers:
    Clean_answers.append(cleantext(answer))


#Creating a dictionary that maps each word to its occurences
word2count={}
for question in Clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word]=1
        else:
            word2count[word]+=1
for answer in Clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word]=1
        else:
            word2count[word]+=1           


#Creating a dictionary that maps each word to a unique integer and also checking if the frequency threshold is met
threshold=20
questionswordstoint={}
wordnumber=0
for word,count in word2count.items():
    if count>=threshold:
        questionswordstoint[word]=wordnumber
        wordnumber+=1
answersswordstoint={}
wordnumber=0
for word,count in word2count.items():
    if count>=threshold:
        answersswordstoint[word]=wordnumber
        wordnumber+=1       
        
    
#Adding the tokens to our dictionaries
tokens=["<PAD>","<EOS>","<SOS>","<OUT>"]
for token in tokens:
    questionswordstoint[token]=len(questionswordstoint)+1
for token in tokens:
    answersswordstoint[token]=len(answersswordstoint)+1


#Creating inverse dictionaries to map integers to words
answersint_to_words={w_i:w for w,w_i in answersswordstoint.items()}


#Adding an EOS token to every answer
for i in range(len(Clean_answers)):
    Clean_answers[i] += " <EOS>"
    

#Another way to add an EOS token to every answer
#new=[]
#for i in Clean_answers:
#   new.append(i+"<EOS>")


#Translating all the questions and answers into a sequence of integers 
# And replacing all the words that were filteres out by token <out>
questions_to_int=[]
for question in Clean_questions:
    int=[]
    for word in question.split():
        if word not in questionswordstoint:
            int.append(questionswordstoint["<OUT>"])
        else:
            int.append(questionswordstoint[word])
    questions_to_int.append(int)
            
        
answers_to_int=[]
for answer in Clean_answers:
    int=[]
    for word in answer.split():
        if word not in answersswordstoint:
            int.append(answersswordstoint["<OUT>"])
        else:
            int.append(answersswordstoint[word])
    answers_to_int.append(int)


#Sorting questions and answers by questions:
sorted_clean_questions=[]
sorted_clean_answers=[]
for value in range(1,25+1):
    for questions in enumerate(questions_to_int):
        if len(questions[1])==value:
            sorted_clean_questions.append(questions_to_int[questions[0]])
            sorted_clean_answers.append(answers_to_int[questions[0]])
