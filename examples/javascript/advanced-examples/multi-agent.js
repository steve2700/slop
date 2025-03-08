// simple-agent-slop.js
import { OpenAI } from "openai";
import express from "express";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Memory storage
const memory = {};

// ======= SIMPLE AGENT SYSTEM =======

// Router Agent - decides which specialized agent to use
async function routerAgent(query) {
  const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: "You are a router that categorizes queries and selects the best specialized agent to handle them." },
      { role: "user", content: `Classify this query and select ONE agent: "${query}"` }
    ],
    functions: [{
      name: "route_query",
      description: "Route the query to the appropriate agent",
      parameters: {
        type: "object",
        properties: {
          agent: {
            type: "string",
            enum: ["researcher", "creative", "technical"],
            description: "The agent best suited to handle this query"
          },
          reason: {
            type: "string",
            description: "Brief reason for this routing decision"
          }
        },
        required: ["agent", "reason"]
      }
    }],
    function_call: { name: "route_query" }
  });
  
  const args = JSON.parse(completion.choices[0].message.function_call.arguments);
  console.log(`🔀 Routing to: ${args.agent} (${args.reason})`);
  return args;
}

// Specialized Agents
const agents = {
  researcher: async (query) => {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        { role: "system", content: "You are a research agent providing factual information with sources." },
        { role: "user", content: query }
      ]
    });
    return completion.choices[0].message.content;
  },
  
  creative: async (query) => {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        { role: "system", content: "You are a creative agent generating imaginative content." },
        { role: "user", content: query }
      ],
      temperature: 0.9
    });
    return completion.choices[0].message.content;
  },
  
  technical: async (query) => {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        { role: "system", content: "You are a technical agent providing precise, detailed explanations." },
        { role: "user", content: query }
      ],
      temperature: 0.2
    });
    return completion.choices[0].message.content;
  }
};

// ======= SLOP API IMPLEMENTATION =======

// CHAT endpoint - main entry point
app.post('/chat', async (req, res) => {
  try {
    const { messages } = req.body;
    const userQuery = messages[0].content;
    
    // 1. Route the query to the appropriate agent
    const route = await routerAgent(userQuery);
    
    // 2. Process with the selected agent
    const response = await agents[route.agent](userQuery);
    
    // 3. Store in memory
    const sessionId = `session_${Date.now()}`;
    memory[sessionId] = {
      query: userQuery,
      agent: route.agent,
      reason: route.reason,
      response
    };
    
    res.json({
      message: {
        role: "assistant",
        content: response,
        metadata: {
          agent: route.agent,
          session_id: sessionId
        }
      }
    });
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ error: error.message });
  }
});

// MEMORY endpoints
app.post('/memory', (req, res) => {
  const { key, value } = req.body;
  memory[key] = value;
  res.json({ status: 'stored' });
});

app.get('/memory/:key', (req, res) => {
  const { key } = req.params;
  res.json({ value: memory[key] || null });
});

// TOOLS endpoint
app.get('/tools', (req, res) => {
  res.json({
    tools: [
      { id: "researcher", description: "Finds factual information" },
      { id: "creative", description: "Generates imaginative content" },
      { id: "technical", description: "Provides technical explanations" }
    ]
  });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🤖 Simple Agent SLOP API running on port ${PORT}`);
});

// EXAMPLE USAGE
// curl -X POST http://localhost:3000/chat \
// -H "Content-Type: application/json" \
// -d '{"messages":[{"content":"What are black holes?"}]}'
