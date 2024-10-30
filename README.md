Compliance Checker API
This API checks the content of a specified webpage against a provided compliance policy, identifying any non-compliant sections and reporting them. It leverages OpenAI's API to process text and determine compliance based on natural language understanding.


Request Example : 
curl -X POST http://127.0.0.1:5000/check-compliance \
-H "Content-Type: application/json" \
-d '{
      "target_url": "https://mercury.com",
      "policy_url": "https://stripe.com/docs/treasury/marketing-treasury"
     }'

Response Example : 
{
    "status": "success",
    "findings": [
        "Non-compliance detected in section 3 regarding promotional language.",
        "Section 5 violates policy requirements for product disclaimer."
    ]
}
