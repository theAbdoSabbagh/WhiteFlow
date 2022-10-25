### Developer Docs
- The local websocket server follows a json-like structure for each message
- Each message contains an op code, a registered event name and whatever data

### WS Message format.
```json
{
    "op": "0",
    "data": {...}
}
```

### The OP Codes
because I don't remember what I use at any given time
- `0`- Event: `IDENTIFY`, data: valid, Token, Username, ID, Discriminator
- `1`- Event: `UPDATE`, data: ... (A config update is pushed)
- `2`- Event: `INTERRUPT`, data: ... (The flow is to be interrupted)
