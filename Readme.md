## Setup Instructions

1. **Clone the project**
2. **Create and activate a virtual environment** (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows

```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```
4. **Create a .env file and inside it put your API Key**

```bash
API_KEY=your-gemini-api-key-here
```

**How to Get Gemini API Key (FREE)**
1. **Visit: Google AI Studio**
2. **Click on "Get API Key"**
3. **Follow the instructions and generate a free API key**
4. **Copy and paste it into your .env file**



**To run the Chatbot**

```bash
python cli_chat.py
```

**Note**
**feedback.txt will contain your review and rating.**

**chat_history.txt will save all conversations you had.**

