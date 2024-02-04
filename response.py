import random, json, torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from arthOps import perform_opertion

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)
    
FILE = "data2.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
bot_name = "Zylla"

def getRespons(sentence):
    qes = sentence
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)
    
    ouput = model(X)
    _, predicted = torch.max(ouput, dim=1)
    tag = tags[predicted.item()]
    
    probs = torch.softmax(ouput, dim=1)
    prob = probs[0][predicted.item()]
    
    
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                if tag == "Digits":
                    return perform_opertion(qes)
                ran = random.choice(intent['responses'])
                print(str(prob.item()))
                print(tag)
                return ran
                
    elif prob.item() > 0.56 and prob.item() <= 0.7:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                if tag == "Digits":
                    return perform_opertion(qes)
                #potentially unaccurate responds.....
                ran = f" {random.choice(intent['responses'])}"
                print(str(prob.item()))
                print(tag)
                return ran
        
    else:
        with open("newQ.csv","a") as f:
            newQ = f
            newQ.writelines(","+qes)
            newQ.close()
            print(str(prob.item()))
        return f"I do not understand could you rephrase"
        
