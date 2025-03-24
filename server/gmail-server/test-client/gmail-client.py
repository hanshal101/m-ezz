import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
import os
from openai import OpenAI
import sys
import json


load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY (or OPENAI_API_KEY) not found in environment variables.")
        self.openai = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
        self.assistant_message_content = [] 

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])
        
    async def process_query(self, query: str) -> str:
        """Process a query using OpenAI (Groq) and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]
        messages.extend(self.assistant_message_content) # Append previous assistant messages

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        tool_list_openai = [{
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"]
            }
        } for tool in available_tools]

        final_text = []
        tool_calls_needed = True # Flag to control loop for tool calls

        while tool_calls_needed:
            # Initial/Subsequent OpenAI API call
            response = self.openai.chat.completions.create(
                model="llama-3.3-70b-versatile", # or mixtral-8x7b-32768
                max_tokens=1000,
                messages=messages,
                tools=tool_list_openai if available_tools else None, # Send tools only if available
                tool_choice="auto" if available_tools else "none" # Auto tool selection if tools are available
            )

            tool_calls_needed = False # Assume no more tool calls unless explicitly found in response
            response_message = response.choices[0].message

            if response_message.content:
                final_text.append(response_message.content)
                self.assistant_message_content.append({"role": "assistant", "content": response_message.content}) # Store assistant message in history

            tool_calls = response_message.tool_calls
         
            if tool_calls:
                tool_calls_needed = True # Set flag to true as tool calls are present in response
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args_str = tool_call.function.arguments # tool arguments are coming in string format
                    tool_call_id = tool_call.id

                    try:
                        function_args = json.loads(function_args_str) # Parse string to dictionary
                    except json.JSONDecodeError as e:
                        final_text.append(f"Error decoding tool arguments: {e}")
                        function_args = {} # Handle error by using empty dict, or you can handle it differently

                    final_text.append(f"[Calling tool {function_name} with args {function_args}]")

                    # Execute tool call
                    tool_result = await self.session.call_tool(function_name, function_args) # <--- SUSPECT AREA

                    tool_result_content = tool_result.content
                    # Ensure tool_result_content is a string before adding to messages
                    tool_result_content_str = str(tool_result_content)

                    final_text.append(f"[Tool result: {tool_result_content_str}]")

                    # Append assistant message with tool_call to history
                    messages.append({
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": tool_call_id,
                                "type": "function",
                                "function": {
                                    "name": function_name,
                                    "arguments": function_args_str, # Keep arguments as string in message history
                                }
                            }
                        ]
                    })
                    # Append tool result to messages history
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": tool_result_content_str # Use the string version here
                    })


        return "\n".join(final_text)


    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                self.assistant_message_content = [] # Clear assistant message history for new query
                response = await self.process_query(query)
                print("\nAssistant Response:\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
