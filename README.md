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

## ENDPOINT OPERATIONS (v0.0.1)

### CHAT
- `POST /chat` - Send messages to AI
- `GET /chat/:id` - Get a specific chat
- `GET /chat` - List recent chats

### TOOLS
- `GET /tools` - List available tools
- `POST /tools/:tool_id` - Use a specific tool
- `GET /tools/:tool_id` - Get tool details

### MEMORY
- `POST /memory` - Store a key-value pair
- `GET /memory/:key` - Get value by key
- `GET /memory` - List all keys
- `PUT /memory/:key` - Update existing value
- `DELETE /memory/:key` - Delete a key-value pair
- `POST /memory/query` - Search with semantic query

### RESOURCES
- `GET /resources` - List available resources
- `GET /resources/:id` - Get a specific resource
- `GET /resources/search?q=query` - Search resources

### PAY
- `POST /pay` - Create a payment
- `GET /pay/:id` - Get payment status

---

## API EXAMPLES - ALL ENDPOINTS

### CHAT ENDPOINTS

#### POST /chat
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
  "id": "chat_123",
  "message": {
    "role": "assistant", 
    "content": "I don't have real-time weather data. You could check a weather service for current conditions."
  }
}
```

#### GET /chat/:id
```json
// REQUEST
GET /chat/chat_123

// RESPONSE
{
  "id": "chat_123",
  "messages": [
    {"role": "user", "content": "Hello, what's the weather like?"},
    {"role": "assistant", "content": "I don't have real-time weather data. You could check a weather service for current conditions."}
  ],
  "model": "any-model-id",
  "created_at": "2023-05-15T10:30:00Z"
}
```

#### GET /chat
```json
// REQUEST
GET /chat

// RESPONSE
{
  "chats": [
    {
      "id": "chat_123",
      "snippet": "Hello, what's the weather like?",
      "created_at": "2023-05-15T10:30:00Z"
    },
    {
      "id": "chat_456",
      "snippet": "Tell me about Mars",
      "created_at": "2023-05-14T14:20:00Z"
    }
  ]
}
```

### TOOLS ENDPOINTS

#### GET /tools
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

#### POST /tools/:tool_id
```json
// REQUEST
POST /tools/calculator
{
  "expression": "15 * 7"
}

// RESPONSE
{
  "result": 105
}
```

#### GET /tools/:tool_id
```json
// REQUEST
GET /tools/calculator

// RESPONSE
{
  "id": "calculator",
  "description": "Performs mathematical calculations",
  "parameters": {
    "expression": {
      "type": "string",
      "description": "Mathematical expression to evaluate"
    }
  },
  "example": "15 * 7"
}
```

### MEMORY ENDPOINTS

#### POST /memory
```json
// REQUEST
POST /memory
{
  "key": "user_preference",
  "value": {
    "theme": "dark",
    "language": "en"
  }
}

// RESPONSE
{
  "status": "stored"
}
```

#### GET /memory/:key
```json
// REQUEST
GET /memory/user_preference

// RESPONSE
{
  "key": "user_preference",
  "value": {
    "theme": "dark",
    "language": "en"
  },
  "created_at": "2023-05-15T10:30:00Z"
}
```

#### GET /memory
```json
// REQUEST
GET /memory

// RESPONSE
{
  "keys": [
    {
      "key": "user_preference",
      "created_at": "2023-05-15T10:30:00Z"
    },
    {
      "key": "search_history",
      "created_at": "2023-05-14T14:20:00Z"
    }
  ]
}
```

#### PUT /memory/:key
```json
// REQUEST
PUT /memory/user_preference
{
  "value": {
    "theme": "light",
    "language": "en"
  }
}

// RESPONSE
{
  "status": "updated",
  "previous_value": {
    "theme": "dark",
    "language": "en"
  }
}
```

#### DELETE /memory/:key
```json
// REQUEST
DELETE /memory/user_preference

// RESPONSE
{
  "status": "deleted"
}
```

#### POST /memory/query
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

### RESOURCES ENDPOINTS

#### GET /resources
```json
// REQUEST
GET /resources

// RESPONSE
{
  "resources": [
    {
      "id": "mars-101",
      "title": "Mars: The Red Planet",
      "type": "article"
    },
    {
      "id": "document-123",
      "name": "project_plan.pdf",
      "type": "file"
    }
  ]
}
```

#### GET /resources/:id
```json
// REQUEST
GET /resources/mars-101

// RESPONSE
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
```

#### GET /resources/search
```json
// REQUEST
GET /resources/search?q=mars

// RESPONSE
{
  "results": [
    {
      "id": "mars-101",
      "title": "Mars: The Red Planet",
      "type": "article",
      "score": 0.98
    },
    {
      "id": "solar-system",
      "title": "Our Solar System",
      "type": "article",
      "score": 0.75
    }
  ]
}
```

### PAY ENDPOINTS

#### POST /pay
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

#### GET /pay/:id
```json
// REQUEST
GET /pay/tx_987654

// RESPONSE
{
  "transaction_id": "tx_987654",
  "amount": 5.00,
  "currency": "USD",
  "description": "API usage - 1000 tokens",
  "status": "success",
  "created_at": "2023-05-15T10:30:00Z",
  "receipt_url": "https://api.example.com/receipts/tx_987654"
}
``` 
