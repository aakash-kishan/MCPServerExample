import asyncio


from dotenv import load_dotenv
from langchain_groq import ChatGroq

from mcp_use import MCPClient, MCPAgent
import os

from requests import Response
from urllib3 import response

async def run_memory_chat():

    load_dotenv()
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    config_file = "browser_mcp.json"

    print("Starting chat..........")

    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",  # ✅ Supported model
    temperature=0.7
    )

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
    )

    print("\n IINTERACIVEEE MCP CHATTT-------->")
    print("======== TYPE 'exit' to EXIT-------->")
    print("========= TYPE 'clear' TO CLEAR-------->")

    print("=========================================\n ")

    try:


        while True:

            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                print("ENDING CONVERSATION..............")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.....")
                continue

            print("\nAssistant: ",end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")
    
    finally:

        if client and client.sessions:
            await client.close_all_sessions()



if __name__ == "__main__":
    asyncio.run(run_memory_chat())








