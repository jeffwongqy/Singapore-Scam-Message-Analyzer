# Singapore Scam Message Analyzer

<img width="780" height="435" alt="Screenshot 2026-09-01 180001" src="https://github.com/user-attachments/assets/45b97377-88c3-4543-bf94-352ec882c032" />

## 1. Introduction 
Scam messages have become an increasing concern in Singapore, with scammers using text messages and online communication to deceive individuals into revealing personal information, making payments, or clicking malicious links. Identifying scam messages can be challenging because scammers often use convincing language and impersonate legitimate organisations such as banks, government agencies, employers, and investment companies.

This project develops an AI-powered Singapore Scam Message Analyzer using LangChain, Ollama and Llama 3.2. The application allows users to enter a suspicious message and automatically classify it into categories such as Banking Scam, Government Scam, Job Scam, Investment Scam, Phishing Scam, Romance Scam, or No Obvious Scam.

A router-based approach is implemented, where the initial classification determines which specialised analysis chain should process the message. Each specialised chain identifies potential warning signs and provides recommendations on what the user should do.

## 2. Aim 
The aim of this project is to develop an AI-powered scam message analysis system that uses a LangChain router to classify and analyse potential Singapore scam messages and provide users with understandable warnings and safety recommendations.

## 3. Objectives
1. Develop an interactive Streamlit application that allows users to enter and analyse suspicious messages.
2. Implement an AI-based classification system using Llama 3.2 to categorise messages into different scam types, including banking, government, job, investment, phishing, and romance scams.
3. Implement a LangChain router mechanism using conditional logic to direct each classified message to the appropriate specialised analysis chain.
4. Identify potential scam warning signs and explain why a message may be suspicious.
5. Provide practical recommendations to help users respond safely to potentially fraudulent messages.
6. Provide a “No Obvious Scam” category for messages where the system does not identify an obvious indication of a scam, while still reminding users to remain cautious when personal information, passwords, OTPs, or money are requested.

## 4. Langchain Router Chain 

### 4.1 User Input
Allows users to enter the input messages for analysis.

```python
user_message = st.text_area("Enter a message:", placeholder = "Example: Your bank account will be suspended. Click this link to verify")
```

### 4.2 Ollama LLM
Configures the local llama3.2 model to perform the linguistic analysis and correction tasks.

```python
llm = ChatOllama(model = "llama3.2", temperature = 0)
```

### 4.3 Router Prompt
Instructs the LLM to classify the user's message into one of the predefined scam categories.

```python
router_prompt = ChatPromptTemplate.from_template(
    """
    You are a Singapore scam message classifier.

    Classify the following message into ONE of these categories:

    - Banking Scam
    - Government Scam
    - Job Scam
    - Investment Scam
    - Phishing Scam
    - Romance Scam
    - No Obvious Scam

    Message:
    {message}

    Return ONLY the category name.
    """  
)
```

### 4.4 Specialised Prompt
Defines separate prompts for Banking, Government, Job, Investment, Phishing, and Romance scams. Each prompt asks the LLM to explain warning signs and recommended actions.

```python
banking_prompt = ChatPromptTemplate.from_template(
    """
    Analyze this message as a Singapore banking scam.

    Message:
    {message}

    Explain:
    - Why it may be a banking scam
    - Warning signs
    - What the user should do

    Keep the answer simple.
    """
)

government_prompt = ChatPromptTemplate.from_template(
    """
    Analyze this message as a Singapore government impersonation scam.

    Message:
    {message}

    Explain:
    - Why it may be a government scam
    - Warning signs
    - What the user should do

    Keep the answer simple.
    """
)

job_prompt = ChatPromptTemplate.from_template(
    """
    Analyze this message as a Singapore job scam.

    Message:
    {message}

    Explain:
    - Why it may be a job scam
    - Warning signs
    - What the user should do

    Keep the answer simple.
    """
)

investment_prompt = ChatPromptTemplate.from_template(
    """
    Analyze this message as a Singapore investment scam.

    Message:
    {message}

    Explain:
    - Why it may be an investment scam
    - Warning signs
    - What the user should do

    Keep the answer simple.
    """
)

phishing_prompt = ChatPromptTemplate.from_template(
    
    """
    Analyze this message as a phishing scam.

    Message:
    {message}

    Explain:
    - Why it may be phishing
    - Warning signs
    - What the user should do

    Keep the answer simple.
    """
)

romance_prompt = ChatPromptTemplate.from_template(
    """
    Analyze this message as a Singapore romance scam.

    Message:
    {message}

    Explain:
    - Why it may be a romance scam
    - Warning signs
    - What the user should do

    Keep the answer simple.
    """
)


```

### 4.5 No-Scam Prompt
Handles messages that do not appear to belong to the scam categories and reminds users to remain cautious.

```python
normal_prompt = ChatPromptTemplate.from_template(
    """
    Analyze this message.

    Message:
    {message}

    Explain why there is no obvious indication of a scam.
    Also mention that users should still be cautious if the message
    requests money, passwords, OTPs, or personal information.
    """
)
```

### 4.6 Create Langchain Chains
Combines each prompt with the Llama 3.2 model and output parser to create individual processing chains.

```python
router_chain = router_prompt | llm | StrOutputParser()
banking_chain = banking_prompt | llm | StrOutputParser()
government_chain = government_prompt | llm | StrOutputParser()
job_chain = job_prompt | llm | StrOutputParser()
investment_chain = investment_prompt | llm | StrOutputParser()
phishing_chain = phishing_prompt | llm | StrOutputParser()
romance_chain = romance_prompt | llm | StrOutputParser()
normal_chain = normal_prompt | llm | StrOutputParser()
```

### 4.7 Router Function 
Receives the user's message, sends it to the router chain for classification, and uses if/elif conditions to select the appropriate specialised chain.

```python
def router(message):
    category = router_chain.invoke({
        "message": message
    }).strip()

    category_lower = category.lower()

    if "banking" in category_lower:
        response = banking_chain.invoke({
            "message": message
        })

    elif "government" in category_lower:
        response = government_chain.invoke({
            "message": message
        })

    elif "job" in category_lower:
        response = job_chain.invoke({
            "message": message
        })
    
    elif "investment" in category_lower:
        response = investment_chain.invoke({
            "message": message
        })

    elif "phishing" in category_lower:
        response = phishing_chain.invoke({
            "message": message
        })

    elif "romance" in category_lower:
        response = romance_chain.invoke({
            "message": message
        })

    else:
        response = normal_chain.invoke({
            "message": message
        })
    
    return category, response
```

### 4.8 Analyze Button
Runs the analysis when the user clicks “Analyze Message”, then displays the detected scam category and detailed analysis.

### 4.10 Empty Input Handling 
Checks whether the user entered a message. If the text box is empty, it displays a warning asking the user to enter a message.

```python
if st.button("Analyze Message"):
    if user_message.strip():
        with st.spinner("Analyzing ..."):
            category, response = router(user_message)
            
            st.subheader("Scam Category")
            st.info(category)
            
            st.subheader("Analysis")
            st.write(response)
        
    else:
        st.warning("Please enter a message!")

```

## 5. Testing for Common Scam 
### 5.1 Banking
ALERT: Your account has been temporarily locked due to suspicious login attempts from overseas. To restore access and verify your identity, please click immediately: https://dbs-secure-verify.com

### 5.2 Government
GOV.SG: You have an outstanding CPF payout of $880 pending collection. Please submit your details via our secure portal before 23:59 today to avoid forfeiture: https://cpf-gov-sg-claims.net

### 5.3 Job 
HR Recruitment: Earn $100-$300 daily reviewing movie trailers or liking YouTube videos from home! No experience needed. Contact our manager on WhatsApp at +1-555-0199 to start right away.

### 5.4 Investment 
IP Trading Group: Our AI crypto bot just secured a 45% return for members today! Guaranteed profits with zero risk. Join our exclusive Telegram channel to copy trades: https://t.me

### 5.5 Phishing 
SingPost: Your package could not be delivered due to an incomplete address. Pay the $1.50 customs fee to reschedule delivery now: https://singpost-tracking-update.com

### 5.6 Romance 
Hey Sarah, are we still meeting for lunch at Marina Bay Sands today? Wait, is this not David? So sorry for the wrong number, but since we started chatting, how is your week going?


## 6. Demo Working Implementation 
<img width="1912" height="962" alt="p1" src="https://github.com/user-attachments/assets/3b69b991-a71b-43eb-a0bd-f772aad0de64" />

<img width="1910" height="962" alt="p2" src="https://github.com/user-attachments/assets/bcea9684-e4d8-4022-8d90-36762a1dc35f" />

