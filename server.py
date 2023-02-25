import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 8000
server.bind((ip, port))

server.listen()

clients = []
messages = []
questions = [
  "What is 10 + 2? \n a) 2 \n b) 12 \n c) 21 \n d) 9",
  "What is 10-1? \n a) 3 \n b) 8 \n c) 9 \n d) 0",
  "what is 0+1? \n a) 1 \n b) 2 \n c) 3 \n d) 4"
]
answers = ["c","c","a"]
numberOfQ = len(questions)

def getRandomQuestion(conn):
  randomIndex = random.randint(0, len(questions)-1)
  randomQuestion = questions[randomIndex]
  randomAnswer = answers[randomIndex]
  conn.send(randomQuestion.encode("utf-8"))
  return randomIndex, randomQuestion, randomAnswer


def clientThread(conn, addr):
  point = 0
  conn.send("Welcome to the Quizes".encode("utf-8"))
  conn.send("Answer each question with a, b, c, or d.".encode("utf-8"))
  conn.send("best of luck \n\n".encode("utf-8"))
  index, question, answer = getRandomQuestion(conn)

  while True:
    try:
      message = conn.recv(2048).decode("utf-8").split(":")[1]
      if message:
        if message.lower() == answer:
          point += 1
          conn.send(f"Correct! Your point is {point}\n\n".encode("utf-8"))
        else:
          conn.send(f"Incorrect! Your point is still {point}\n\n".encode("utf-8"))
        removeQuestion(index)
        index, question, answer = getRandomQuestion(conn)
      else:
        remove(conn)
    except:
      continue

def removeQuestion(index):
  questions.pop(index)
  answers.pop(index)
        
def remove(conn):
  if conn in clients:
    clients.remove(conn)

while True:
  conn, addr = server.accept()
  conn.send(input("message here").encode("utf-8"))
  mes = conn.recv(2048).decode("utf-8")
  clients.append(conn)
  messages.append(mes)

  message = '{} entered the quiz'.format(mes)
  print(message)

  newThread = Thread(target=clientThread, args=(conn,addr))
  newThread.start()
  