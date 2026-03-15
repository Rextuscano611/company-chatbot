import os
import csv
import re
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Embedding model (same used during ingestion)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

retriever = vectorstore.as_retriever()

# LLM
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo"
)

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data["message"]
    message_lower = user_message.lower()

    # -------- EXTRACT EMAIL --------
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', user_message)

    # -------- EXTRACT WEBSITE --------
    website_match = re.search(r'(https?://[^\s]+|www\.[^\s]+)', user_message)

    # -------- EXTRACT NAME --------
    name_match = re.search(r'Name\s*[:\-]\s*([A-Za-z]+)', user_message, re.IGNORECASE)
    

    if email_match:

        email = email_match.group()
        website = website_match.group() if website_match else ""
        name = name_match.group(1).strip() if name_match else ""

        # Create CSV with header if it doesn't exist
        file_exists = os.path.isfile("leads.csv")

        with open("leads.csv", "a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Name", "Email", "Website"])

            writer.writerow([name, email, website])

        return jsonify({
            "response": "Thank you! Our team will contact you soon 🚀"
        })

    # -------- LEAD INTENT DETECTION --------
    lead_keywords = [
        "consultation",
        "meeting",
        "contact",
        "talk to sales",
        "seo service",
        "hire",
        "pricing"
    ]

    if any(word in message_lower for word in lead_keywords):

        return jsonify({
            "response": "Great! I'd love to connect you with our team.<br><br>Please share the following details:<br><br>Name:<br>Email:<br>Company / Website:"
        })

    # -------- NORMAL CHATBOT FLOW --------
    docs = vectorstore.similarity_search(user_message)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are Maya, an AI assistant for SEO Labs.

Use the following context to answer the question.

{context}

Question: {user_message}
"""

    response = llm.invoke(prompt)

    return jsonify({"response": response.content})


if __name__ == "__main__":
    app.run(debug=True)