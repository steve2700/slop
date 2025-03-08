import os
import json
import time
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any
import asyncio

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
def router_agent(query: str) -> Dict[str, str]:
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
                            "enum": ["researcher", "creative", "technical", "summarizer"],
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
def create_agent(role: str, temperature: float = 0.7):
    def agent(query: str) -> str:
        return openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": query}
            ],
            temperature=temperature
        ).choices[0].message.content
    return agent

agents = {
    "researcher": create_agent("You are a research agent providing factual information with sources.", 0.3),
    "creative": create_agent("You are a creative agent generating imaginative content.", 0.9),
    "technical": create_agent("You are a technical agent providing precise, detailed explanations.", 0.2),
    "summarizer": create_agent("You are a summarization agent that creates concise summaries.", 0.3)
}

# ======= SLOP API IMPLEMENTATION =======

# CHAT endpoint - main entry point
@app.route('/chat', methods=['POST'])
async def chat():
    try:
        data = request.json
        messages = data.get('messages', [])
        pattern = data.get('pattern')
        user_query = messages[0]['content'] if messages else ""
        
        response = None

        if pattern:
            if pattern == 'sequential':
                # Research then summarize
                research = await agents["researcher"](user_query)
                response = await agents["summarizer"](research)
            
            elif pattern == 'parallel':
                # Get multiple perspectives simultaneously
                research_task = agents["researcher"](user_query)
                creative_task = agents["creative"](user_query)
                results = await asyncio.gather(research_task, creative_task)
                response = f"Research perspective:\n{results[0]}\n\nCreative perspective:\n{results[1]}"
            
            elif pattern == 'branching':
                route = router_agent(user_query)
                response = await agents[route['agent']](user_query)
        else:
            # Default to original router behavior
            route = router_agent(user_query)
            response = await agents[route['agent']](user_query)
        
        # Store in memory
        session_id = f"session_{int(time.time())}"
        memory[session_id] = {
            "query": user_query,
            "pattern": pattern or "router",
            "response": response
        }
        
        return jsonify({
            "message": {
                "role": "assistant",
                "content": response,
                "metadata": {
                    "session_id": session_id,
                    "pattern": pattern or "router"
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
            {"id": "technical", "description": "Provides technical explanations"},
            {"id": "summarizer", "description": "Creates concise summaries"}
        ],
        "patterns": [
            {"id": "sequential", "description": "Research then summarize"},
            {"id": "parallel", "description": "Multiple perspectives at once"},
            {"id": "branching", "description": "Route to best agent (default)"}
        ]
    })

# RESOURCES endpoint
@app.route('/resources', methods=['GET'])
def get_resources():
    return jsonify({
        "patterns": {
            "sequential": "Chain agents: Research → Summarize",
            "parallel": "Multiple agents work simultaneously",
            "branching": "Route to specialized agents"
        }
    })

# PAY endpoint (simple mock)
@app.route('/pay', methods=['POST'])
def process_payment():
    data = request.json
    tx_id = f"tx_{int(time.time())}"
    memory[tx_id] = {"amount": data.get('amount'), "status": "completed"}
    return jsonify({"transaction_id": tx_id})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    print(f"🤖 SLOP Multi-Agent API running on port {port}")
    app.run(host="0.0.0.0", port=port)

# Example usage:

# Basic query:
# curl -X POST http://localhost:3000/chat \
#   -H "Content-Type: application/json" \
#   -d '{"messages":[{"content":"What are black holes?"}]}'
#
# With pattern:
# curl -X POST http://localhost:3000/chat \
#   -H "Content-Type: application/json" \
#   -d '{"messages":[{"content":"What are black holes?"}], "pattern": "sequential"}'