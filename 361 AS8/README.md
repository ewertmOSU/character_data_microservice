
    1) The RPC server subscribes to a messaging queue named "rpc_character_queue" and waits for messages to appear

    2) When a message is published to the "rpc_character_queue", the server reads the message body and uses that to lookup a file containing character data and publishes a response message containing that character data in the body

    3) The incoming message contains a "correlation_id", the outgoing message that the server will publish will also use the correlation_id so the client can tell what response messages are associated with which request messages it sent to the server

    4)The incoming message the server is reading from has a "reply_to" field on it containing the name of another queue, the server then publishes an event to that queue with the body containing the character data. The "reply_to" queue is a callback queue that the client is subscribing to waiting for response messages 
