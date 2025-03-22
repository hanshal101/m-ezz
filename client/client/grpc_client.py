import asyncio
import grpc
from ..protos import chat_service_pb2 as pb2
from ..protos import chat_service_pb2_grpc as pb2_grpc

async def chat_stream(stub: pb2_grpc.ChatServiceStub, query: str, skip_verification: bool = False) -> None:
    """Stream chat responses from the server."""
    request = pb2.QueryRequest(
        query=query,
        skip_human_verification=skip_verification
    )
    
    try:
        async for response in stub.ProcessQuery(request):
            if response.HasField('text'):
                print(response.text)
            elif response.HasField('tool'):
                print(f"\nExecuting tool: {response.tool.tool_name}")
                print(f"Result: {response.tool.result}")
            elif response.HasField('verification'):
                print("\nHuman verification required:")
                print(f"Tool: {response.verification.tool_name}")
                print("Arguments:")
                for key, value in response.verification.arguments.items():
                    print(f"  {key}: {value}")
    except grpc.RpcError as e:
        print(f"RPC error: {e.code()}: {e.details()}")

async def main() -> None:
    """Run the gRPC client."""
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.ChatServiceStub(channel)
        
        while True:
            query = input("\nYou: ").strip()
            if query.lower() in ['quit', 'exit']:
                break
                
            skip_verification = input("Skip human verification? (y/n): ").lower() == 'y'
            await chat_stream(stub, query, skip_verification)

if __name__ == '__main__':
    asyncio.run(main())