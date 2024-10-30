import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def get_page_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join([element.get_text() for element in soup.find_all(['p', 'li', 'span', 'div'])])
    return text

import openai

def summarize_policy(policy_content):
    summary_response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "Summarize the key compliance requirements from this policy."},
            {"role": "user", "content": policy_content}
        ],
        max_tokens=500  # Limit summary size
    )
    return summary_response.choices[0].message.content.strip()

def chunk_text(text, max_tokens=1500):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        # Estimate token count (roughly 4 characters per token for English text)
        if len(' '.join(current_chunk)) / 4 > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def check_compliance(target_content, compliance_policy):
    summarized_policy = summarize_policy(compliance_policy)
    content_chunks = chunk_text(target_content)
    findings = []

    for chunk in content_chunks:
        prompt = f"""
        Given the summarized compliance policy:
        {summarized_policy}

        Check the following content for any non-compliance:
        {chunk}

        Report any specific non-compliant sections and reasons.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are a compliance checker assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800  # Limit response size per chunk
        )
        
        findings.append(response.choices[0].message.content.strip())

    return findings


@app.route('/check-compliance', methods=['POST'])
def check_compliance_endpoint():
    try:
        data = request.json
        target_url = data['target_url']
        policy_url = data['policy_url']

        compliance_policy = get_page_content(policy_url)
        target_content = get_page_content(target_url)

        findings = check_compliance(target_content, compliance_policy)

        with open("compliance_findings.json", "w") as f:
            import json
            json.dump({'findings': findings}, f, indent=4)

        return jsonify({
            'status': 'success',
            'findings': findings
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
