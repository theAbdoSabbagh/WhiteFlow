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