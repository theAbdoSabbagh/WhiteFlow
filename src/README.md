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
- `0: IDENTIFY`. data: valid, Token, Username, ID, Discriminator
- `1: UPDATE`. data: ... (A config update is pushed)
- `2: INTERRUPT`. data: command_name (The flow is to be interrupted)
- `3: KILL`. data: uuid (kills the account after current command, closes the flow)
- `4: TERMINATE`. data: uuid (instantly kills the account even if there is an ongoing command)