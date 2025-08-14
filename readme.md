# **Agentic Memory**

Agentic Memory is a Python-based chatbot framework that integrates **OpenAI function calling** with a **custom memory system**, allowing the agent to store and recall information about the user or itself across multiple interactions.

---

## **Features**
- ✅ **OpenAI GPT Integration** – Uses `gpt-4o-mini` for fast, high-quality responses.  
- ✅ **Memory Persistence** – Stores user and agent information in structured sections (`human`, `agent`).  
- ✅ **Function Calling Support** – Utilizes OpenAI’s tools API to call a custom `core_memory_save` function whenever new information is learned.  
- ✅ **Agentic Behavior** – The system instructs the model to use memory before responding to the user.  
- ✅ **Extendable** – Easy to integrate with persistent storage, multi-turn conversations, and additional tools.

---

## **How It Works**
1. **System Prompt & Memory Injection**  
   The chatbot is initialized with a system prompt that includes the `[MEMORY]` section containing all stored information.

2. **Dynamic Memory Updates**  
   When the user provides new information (e.g., `"my name is Mahand"`), the model calls the `core_memory_save` tool.

3. **Function Execution**  
   The `core_memory_save` function updates the `agent_memory` dictionary under the correct section (`human` or `agent`).

4. **Loop & Response**  
   The agent continues until it produces a normal response (not a tool call), then returns it to the user.

---

