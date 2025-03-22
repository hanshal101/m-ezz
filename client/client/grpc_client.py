import asyncio
import grpc
import json
from typing import Optional
import proto.chat_pb2_grpc as pb2_grpc
import proto.chat_pb2 as pb2

class ChatClient:
    def __init__(self) -> None:
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[pb2_grpc.ChatServiceStub] = None

    async def connect(self, server_address: str = 'localhost:50051') -> None:
        """Connect to the gRPC server."""
        self.channel = grpc.aio.insecure_channel(server_address)
        self.stub = pb2_grpc.ChatServiceStub(self.channel)

    async def chat_stream(self, query: str) -> None:
        """Stream chat responses from the server."""
        if not self.stub:
            raise RuntimeError("Not connected to server")

        initial_request = pb2.QueryRequest(
            query=query,
            skip_human_verification=True
        )

        try:
            initial_response = None
            tool_data = None
            
            async for response in self.stub.ProcessQuery(initial_request):
                if response.HasField('text'):
                    initial_response = response.text
                    print(f"\n{initial_response}")
                    
                    try:
                        tool_data = json.loads(initial_response.replace("Assistant: ", ""))
                        if not (isinstance(tool_data, dict) and "tool" in tool_data and "arguments" in tool_data):
                            tool_data = None
                    except json.JSONDecodeError:
                        tool_data = None
                    break

            if tool_data:
                skip_verification = input("\nSkip human verification? (y/n): ").lower() == 'y'
                
                execution_request = pb2.QueryRequest(
                    query=query,
                    skip_human_verification=skip_verification
                )
                
                async for exec_response in self.stub.ProcessQuery(execution_request):
                    if exec_response.HasField('verification'):
                        print("\nHuman verification required:")
                        print(f"Tool: {exec_response.verification.tool_name}")
                        print("Arguments:")
                        for key, value in exec_response.verification.arguments.items():
                            print(f"  {key}: {value}")
                    elif exec_response.HasField('tool'):
                        print(f"\nExecuting tool: {exec_response.tool.tool_name}")
                        print(f"Result: {exec_response.tool.result}")
                    elif exec_response.HasField('text'):
                        if not exec_response.text.startswith("Assistant: {"):
                            print(f"\n{exec_response.text}")

        except grpc.RpcError as e:
            print(f"RPC error: {e.code()}: {e.details()}")

    async def cleanup(self) -> None:
        """Clean up client resources."""
        if self.channel:
            await self.channel.close()

async def main() -> None:
    """Run the gRPC client."""
    client = ChatClient()
    try:
        await client.connect()
        print("\nConnected to MCP gRPC server")
        print("Type 'quit' or 'exit' to end the session")
        
        while True:
            query = input("\nYou: ").strip()
            if query.lower() in ['quit', 'exit']:
                break
            
            await client.chat_stream(query)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.cleanup()

if __name__ == '__main__':
    asyncio.run(main())