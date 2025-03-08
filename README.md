# SLOP: Because AI shouldn't be complicated

## 1. CORE BELIEFS
- Everything is an HTTP request
- Every tool is an API endpoint
- Every AI is accessible
- Every developer is welcome

## 2. MINIMUM VIABLE ENDPOINTS
- `POST /chat` // Talk to AI
- `POST /tools` // Use tools
- `POST /memory` // Remember stuff
- `GET /resources` // Get knowledge/files/data
- `POST /pay` // Handle money (optional)

## 3. CONNECTIONS
- WebSocket for real-time
- SSE for streaming
- HTTP for everything else

---

## THE SLOP PROMISE:

### 1. OPEN
- Free to use
- Open source
- No vendor lock
- Community driven

### 2. SIMPLE
- REST based
- JSON only
- Standard HTTP
- Zero dependencies

### 3. FLEXIBLE
- Any AI model
- Any tool
- Any platform

---

## API PATTERN EXAMPLES

### POST /chat
Talk to AI models.

```json
// REQUEST
POST /chat
{
  "messages": [
    {"role": "user", "content": "Hello, what's the weather like?"}
  ],
  "model": "any-model-id"
}

// RESPONSE
{
  "message": {
    "role": "assistant", 
    "content": "I don't have real-time weather data. You could check a weather service for current conditions."
  }
}
```

### POST /tools
Use tools through API endpoints.

```json
// REQUEST
POST /tools
{
  "tool": "calculator",
  "input": {
    "expression": "15 * 7"
  }
}

// RESPONSE
{
  "result": 105
}
```

List available tools:
```json
// REQUEST
GET /tools

// RESPONSE
{
  "tools": [
    {
      "id": "calculator",
      "description": "Performs mathematical calculations",
      "parameters": {
        "expression": "string"
      }
    },
    {
      "id": "weather",
      "description": "Gets current weather",
      "parameters": {
        "location": "string"
      }
    }
  ]
}
```

### POST /memory
Store and retrieve information.

```json
// STORE REQUEST
POST /memory
{
  "key": "user_preference",
  "value": {
    "theme": "dark",
    "language": "en"
  }
}

// STORE RESPONSE
{
  "status": "stored"
}

// RETRIEVE REQUEST
GET /memory?key=user_preference

// RETRIEVE RESPONSE
{
  "key": "user_preference",
  "value": {
    "theme": "dark",
    "language": "en"
  }
}
```

Semantic query:
```json
// REQUEST
POST /memory/query
{
  "query": "What theme settings do I have?",
  "limit": 1
}

// RESPONSE
{
  "results": [
    {
      "key": "user_preference",
      "value": {
        "theme": "dark",
        "language": "en"
      },
      "score": 0.92
    }
  ]
}
```

### GET /resources
Access knowledge, files, and data.

```json
// REQUEST
GET /resources?type=knowledge&query=mars

// RESPONSE
{
  "resources": [
    {
      "id": "mars-101",
      "title": "Mars: The Red Planet",
      "type": "article",
      "content": "Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System...",
      "metadata": {
        "source": "astronomy-db",
        "last_updated": "2023-05-10"
      }
    }
  ]
}
```

File resource:
```json
// REQUEST
GET /resources?type=file&id=document-123

// RESPONSE
{
  "id": "document-123",
  "name": "project_plan.pdf",
  "content_type": "application/pdf",
  "url": "https://api.example.com/files/document-123",
  "size": 1502394
}
```

### POST /pay
Handle payments (optional).

```json
// REQUEST
POST /pay
{
  "amount": 5.00,
  "currency": "USD",
  "description": "API usage - 1000 tokens",
  "payment_method": "card_token_123"
}

// RESPONSE
{
  "transaction_id": "tx_987654",
  "status": "success",
  "receipt_url": "https://api.example.com/receipts/tx_987654"
}
``` 
