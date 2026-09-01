import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.title("🚨 Singapore Scam Message Analyzer")
st.write("AI-powered detection and analysis of potential scam messages")

user_message = st.text_area("Enter a message:", placeholder = "Example: Your bank account will be suspended. Click this link to verify")

llm = ChatOllama(model = "llama3.2", temperature = 0)

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

router_chain = router_prompt | llm | StrOutputParser()
banking_chain = banking_prompt | llm | StrOutputParser()
government_chain = government_prompt | llm | StrOutputParser()
job_chain = job_prompt | llm | StrOutputParser()
investment_chain = investment_prompt | llm | StrOutputParser()
phishing_chain = phishing_prompt | llm | StrOutputParser()
romance_chain = romance_prompt | llm | StrOutputParser()
normal_chain = normal_prompt | llm | StrOutputParser()

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