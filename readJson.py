import json

def insert_question(json_file, email, question):
    
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Check if the email already exists in the JSON
    for entry in data["newQs"]:
        if entry["user"] == email:
            if indb(question):
                break
            else:
                entry["qestions"].append(question)
                break
            
        else:
            data["newQs"].append({"user": email, "qestions": [question]})
    
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
        
def indb(question):
    with open('newQ.json', 'r') as f:
        data = json.load(f)
    # Check if the email already exists in the JSON
    for entry in data["newQs"]:
        for qs in entry["qestions"]:
                if qs == question:
                    # entry["qestions"].append("here")
                    return True
        return False
    
# Gets the total number of new questions for all the users..
def numOfNewQ():
    nqLength = 0
    with open('newQ.json', 'r') as f:
        data = json.load(f)
        
    for entry in data["newQs"]:
        nqLength += len(entry["qestions"])
        
    return nqLength

def getquestions():
    questions = []
    with open('newQ.json', 'r') as f:
        data = json.load(f)
        
    for entry in data["newQs"]:
        questions.append(entry["qestions"])
        # nqLength += len(entry["qestions"])
        
    return questions

def getUsers():
    users = []
    with open('newQ.json', 'r') as f:
        data = json.load(f)
        
    for entry in data["newQs"]:
        users.append(entry["user"])
        # nqLength += len(entry["qestions"])
        
    return users

        
# if __name__ == "__main__":
#     json_file = "newQ.json"
#     email = input("Enter the email address: ")
#     question = input("Enter the question: ")

#     insert_question(json_file, email, question)