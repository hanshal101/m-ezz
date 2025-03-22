import asyncio
import grpc
import json
import logging
from concurrent import futures
from typing import Any, AsyncIterator
from grpc.aio import ServicerContext

import proto.chat_pb2 as pb2
import proto.chat_pb2_grpc as pb2_grpc

from config.config import Configuration
from server.server import Server
from llm.llm import LLMClient
from logger.logging import logger

class ChatServicer(pb2_grpc.ChatServiceServicer):
    def __init__(self) -> None:
        self.config = Configuration()
        self.server_config = self.config.load_config("servers_config.json")
        self.llm_client = LLMClient(self.config.llm_api_key)
        self.servers: list[Server] = []
        
    async def initialize_servers(self) -> None:
        """Initialize all MCP servers."""
        self.servers = [
            Server(name, srv_config)
            for name, srv_config in self.server_config["mcpServers"].items()
        ]
        for server in self.servers:
            await server.initialize()

    async def get_human_verification(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> bool:
        """Get human verification for tool execution."""
        print("\nHuman Verification Required:")
        print(f"Tool: {tool_name}")
        print("Arguments:")
        for key, value in arguments.items():
            print(f"  {key}: {value}")
        
        while True:
            response = input("\nApprove execution? (yes/no): ").lower()
            if response in ['yes', 'y']:
                return True
            if response in ['no', 'n']:
                return False
            print("Please answer 'yes' or 'no'")

    async def ProcessQuery(
        self, request: pb2.QueryRequest, context: ServicerContext
    ) -> AsyncIterator[pb2.QueryResponse]:
        """Process a query and stream responses."""
        try:
            if not self.servers:
                await self.initialize_servers()

            all_tools = []
            for server in self.servers:
                tools = await server.list_tools()
                all_tools.extend(tools)

            tools_description = "\n".join([tool.format_for_llm() for tool in all_tools])
            system_message = self._create_system_message(tools_description)
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": request.query}
            ]
            
            llm_response = self.llm_client.get_response(messages)
            yield pb2.QueryResponse(text=f"Assistant: {llm_response}")

            try:
                tool_call = json.loads(llm_response)
                if "tool" in tool_call and "arguments" in tool_call:
                    tool_name = tool_call["tool"]
                    arguments = tool_call["arguments"]

                    if not request.skip_human_verification:
                        verification = pb2.HumanVerification(
                            tool_name=tool_name,
                            arguments=arguments,
                            description="Please verify this tool execution"
                        )
                        yield pb2.QueryResponse(verification=verification)
                        
                        if not await self.get_human_verification(tool_name, arguments):
                            yield pb2.QueryResponse(
                                text="Tool execution cancelled by human operator"
                            )
                            return

                    for server in self.servers:
                        tools = await server.list_tools()
                        if any(tool.name == tool_name for tool in tools):
                            result = await server.execute_tool(tool_name, arguments)
                            yield pb2.QueryResponse(
                                tool=pb2.ToolExecution(
                                    tool_name=tool_name,
                                    result=str(result)
                                )
                            )

                            messages.extend([
                                {"role": "assistant", "content": llm_response},
                                {"role": "system", "content": f"Tool result: {result}"}
                            ])
                            final_response = self.llm_client.get_response(messages)
                            yield pb2.QueryResponse(text=final_response)
                            break

            except json.JSONDecodeError:
                pass
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return

    def _create_system_message(self, tools_description: str) -> str:
        """Create the system message for the LLM."""
        return (
            "You are a helpful assistant with access to these tools:\n\n"
            f"{tools_description}\n"
            "Choose the appropriate tool based on the user's question. "
            "If no tool is needed, reply directly.\n\n"
            "IMPORTANT: When you need to use a tool, respond ONLY with "
            "the exact JSON object format below, nothing else:\n"
            "{\n"
            '    "tool": "tool-name",\n'
            '    "arguments": {\n'
            '        "argument-name": "value"\n'
            "    }\n"
            "}\n\n"
            "After receiving a tool's response:\n"
            "1. Transform the raw data into a natural, conversational response\n"
            "2. Keep responses concise but informative\n"
            "3. Focus on the most relevant information"
        )

async def serve(port: int = 50051) -> None:
    """Start the gRPC server."""
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    
    logger.info(f"Starting server on port {port}")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())