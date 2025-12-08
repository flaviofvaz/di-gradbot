from backend.src.llm import OpenAiLlm
import asyncio


async def main():
    llm = OpenAiLlm()
    msg = await llm.complete("hello! how are doing today? can you tell me what reinforcement learning is?")
    print(msg)

if __name__ == "__main__":
    asyncio.run(main())
