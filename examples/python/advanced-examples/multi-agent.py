# simple_agent_slop.py
import os
import json
import time
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Memory storage
memory = {}

# ======= SIMPLE AGENT SYSTEM =======

# Router Agent - decides which specialized agent to use
def router_agent(query):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a router that categorizes queries and selects the best specialized agent to handle them."},
            {"role": "user", "content": f'Classify this query and select ONE agent: "{query}"'}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "route_query",
                "description": "Route the query to the appropriate agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent": {
                            "type": "string",
                            "enum": ["researcher", "creative", "technical"],
                            "description": "The agent best suited to handle this query"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Brief reason for this routing decision"
                        }
                    },
                    "required": ["agent", "reason"]
                }
            }
        }],
        tool_choice={"type": "function", "function": {"name": "route_query"}}
    )
    
    tool_call = completion.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    print(f"🔀 Routing to: {args['agent']} ({args['reason']})")
    return args

# Specialized Agents
agents = {
    "researcher": lambda query: openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a research agent providing factual information with sources."},
            {"role": "user", "content": query}
        ]
    ).choices[0].message.content,
    
    "creative": lambda query: openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative agent generating imaginative content."},
            {"role": "user", "content": query}
        ],
        temperature=0.9
    ).choices[0].message.content,
    
    "technical": lambda query: openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a technical agent providing precise, detailed explanations."},
            {"role": "user", "content": query}
        ],
        temperature=0.2
    ).choices[0].message.content
}

# ======= SLOP API IMPLEMENTATION =======

# CHAT endpoint - main entry point
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        messages = data.get('messages', [])
        user_query = messages[0]['content'] if messages else ""
        
        # 1. Route the query to the appropriate agent
        route = router_agent(user_query)
        
        # 2. Process with the selected agent
        response = agents[route['agent']](user_query)
        
        # 3. Store in memory
        session_id = f"session_{int(time.time())}"
        memory[session_id] = {
            "query": user_query,
            "agent": route['agent'],
            "reason": route['reason'],
            "response": response
        }
        
        return jsonify({
            "message": {
                "role": "assistant",
                "content": response,
                "metadata": {
                    "agent": route['agent'],
                    "session_id": session_id
                }
            }
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# MEMORY endpoints
@app.route('/memory', methods=['POST'])
def store_memory():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    memory[key] = value
    return jsonify({"status": "stored"})

@app.route('/memory/<key>', methods=['GET'])
def get_memory(key):
    return jsonify({"value": memory.get(key)})

# TOOLS endpoint
@app.route('/tools', methods=['GET'])
def list_tools():
    return jsonify({
        "tools": [
            {"id": "researcher", "description": "Finds factual information"},
            {"id": "creative", "description": "Generates imaginative content"},
            {"id": "technical", "description": "Provides technical explanations"}
        ]
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    print(f"🤖 Simple Agent SLOP API running on port {port}")
    app.run(host="0.0.0.0", port=port)

# EXAMPLE USAGE
#    curl -X POST http://localhost:3000/chat \
#      -H "Content-Type: application/json" \
#      -d '{"messages":[{"content":"What are black holes?"}]}'