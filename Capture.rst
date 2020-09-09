Service Monitoring Overview
===========================


Capture Flow Basic
==================

Described here is an overview of all the actions that take place when a capture is started -

1. Front End issues a 'start' capture request with following parameters -
   - service name

2. The API is received by FE API Server (Code in this repository). The API Server -
   a. Checks if capture session is already running? If yes, returns an error 403
   b. Creates a session object with name of the following form - resourceName.serviceName.yyyymmddhhmmm
   c. Creates a new UUID and a 'task' key - to be stored in the Redis DB. The presence of this key
      indicates a requested/running task on an agent.
   d. Returns the task-id, session-name to the client. The client is expected to keep polling for this task.

3. Upon receiving a 'success' response to 'start' API, the client should -
   a. 'Connect' to the 'data server' (Web Socket Server) and wait for Task Result.
   b. Send the 'session' name in the 'session' message to the 'data server'.
   c. Start polling for the 'task' result - give up after 30 seconds.

4. Upon receiving the 'success' response of the polling above, client should -
   a. Send a 'start' message to the 'data server'
   b. Continue receiving the data when it receives.
   c. Terminate this when 'stop' is pressed
   d. Unknowns: What if Client forgets to send a 'stop'? Or is 'disconnected'? There should be a way of doing this.

5. Upon receiving next KeepAlive Request from the agent -
   a. Send the agent following information -
      - Start the capture. Along with 'service' name.
      - Endpoint name where to dump the data.
      - Endpoint type (eg. MongoDB) (Enough for 'agent' to construct a 'connect' URL)

6. Upon receiving this information in KeepAlive, the agent -
   a. Starts the capture with the params above (in a 'separate thread')
   b. Responds to API Server via 'status' message about the status of the task above.
   c. Continues sending KeepAlive messages.


7. Data Server upon receiving 'Session' Message -
   a. Maintain a map of 'Sessions' with Connected Clients List - empty initially.
   b. Keep any additional data if required
   c. Wait for a 'start' message to actually 'start' sending the data to the clients. This is fairly straight forward like -
      - Get the document - aka Json - Aka packet from the MongoDB upon new document
      - Collect some of them together - and then send as a batch to the connected clients.
   d. Unknowns: State keeping and state cleanup required and how to authenticate clients?

