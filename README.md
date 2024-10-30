Compliance Checker API
This API checks the content of a specified webpage against a provided compliance policy, identifying any non-compliant sections and reporting them. It leverages OpenAI's API to process text and determine compliance based on natural language understanding.

Table of Contents
Features
Requirements
Installation
Usage
API Endpoints
Response File Output
Notes
License
Features
Scrapes text from any public webpage URL.
Summarizes the compliance policy to reduce token usage.
Checks webpage content in chunks for compliance.
Saves the compliance findings in a JSON file.
Requirements
Python 3.7+
Flask
BeautifulSoup4
Requests
OpenAI Python SDK
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/compliance-checker-api.git
cd compliance-checker-api
Set up a virtual environment (recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate    # On Windows, use venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the OpenAI API Key:

OpenAI’s API key is required to use this API. You can set the API key directly in the code or set it as an environment variable:
bash
Copy code
export OPENAI_API_KEY="your_openai_api_key"
Usage
To start the Flask server, run:

bash
Copy code
python compliance_checker.py
The server will start locally at http://127.0.0.1:5000/.

API Endpoints
Check Compliance
Endpoint: /check-compliance
Method: POST
Description: Takes a target webpage URL and a policy URL, checks the webpage content for compliance against the policy, and returns findings.

Request Example:

bash
Copy code
curl -X POST http://127.0.0.1:5000/check-compliance \
-H "Content-Type: application/json" \
-d '{
      "target_url": "https://mercury.com",
      "policy_url": "https://stripe.com/docs/treasury/marketing-treasury"
     }'
Response Example:

json
Copy code
{
    "status": "success",
    "findings": [
        "Non-compliance detected in section 3 regarding promotional language.",
        "Section 5 violates policy requirements for product disclaimer."
    ]
}
Response File Output
The findings from each API call are saved in a JSON file named compliance_findings.json in the project directory. This file will contain a list of non-compliant sections along with reasons for non-compliance, if any.

Example JSON Output:

json
Copy code
{
    "findings": [
        "Non-compliance detected in section 3 regarding promotional language.",
        "Section 5 violates policy requirements for product disclaimer."
    ]
}
Notes
Ensure the OPENAI_API_KEY is valid and active.
OpenAI’s token limits are applied per request. To manage large webpages, the content is broken into smaller chunks to fit within these limits.
compliance_findings.json will be overwritten each time the endpoint is called.
