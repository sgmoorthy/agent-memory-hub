import os
import time

import openai

from agent_memory_hub import MemoryClient

# NOTE: sustainable implementations should use environment variables for keys
# export OPENAI_API_KEY="sk-..."


def run_openai_agent_with_memory():
    """
    Demonstrates how to inject retrieved memories into an OpenAI ChatCompletion call.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable to run this example.")
        return

    client = openai.OpenAI(api_key=api_key)

    # 1. Initialize the Memory Client
    # We use a specific agent_id to persist memory across different runs
    agent_id = "openai_helper_agent"
    session_id = f"session_{int(time.time())}"
    
    print(f"Initializing Memory Client for Agent: {agent_id}, Session: {session_id}")
    memory = MemoryClient(
        agent_id=agent_id,
        session_id=session_id
    )

    # 2. Simulate storing some previous context (e.g., from a past conversation)
    # in a real app, this would happen over time.
    print("Storing context from previous interactions...")
    memory.write(
        "User prefers concise Python code examples.", 
        metadata={"topic": "coding_style"}
    )
    memory.write(
        "User is interested in reinforcement learning.", 
        metadata={"topic": "interests"}
    )

    # 3. Recall relevant memories
    # In a real scenario, you might do semantic search here. 
    # For now, we fetch recent inputs.
    print("Recalling memories...")
    recent_memories = memory.recall(limit=5)
    
    # Format memories for the system prompt
    memory_context = "\n".join([f"- {m['content']}" for m in recent_memories])
    
    system_prompt = f"""You are a helpful AI assistant.
    
    Here is what you know about the user from previous interactions:
    {memory_context}
    
    Use this information to personalize your responses.
    """

    user_query = "Can you show me how to implement a Q-learning agent?"

    print(f"\nUser Query: {user_query}")
    print("-" * 40)

    # 4. Call OpenAI with the memory-enriched system prompt
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=150
        )
        
        answer = response.choices[0].message.content
        print("Agent Response:")
        print(answer)
        
        # 5. Store this new interaction in memory for the future
        memory.write(
            f"User asked about Q-learning. Agent provided example: {answer[:50]}..."
        )
        print("\nStored new interaction in memory.")

    except Exception as e:
        print(f"Error calling OpenAI: {e}")

if __name__ == "__main__":
    run_openai_agent_with_memory()
