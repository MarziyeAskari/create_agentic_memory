import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=openai_api_key
)

model = "gpt-4o-mini"

agent_memory = {"human": ""}


def core_memory_save(section: str, memory: str):
    agent_memory[section] += '\n'
    agent_memory[section] += memory


core_memory_save_description = "save information about you" \
                               + "the human or the agent you are chatting with"

core_memory_save_properties = {
    "section": {
        "type": "string",
        "enum": ["human", "agent"],
        "description": "must be either 'human' (save information about human) or "
                       "'agent' (save information about yourself)"
    },
    "memory": {
        "type": "string",
        "description": "Memory save in the section"
    }
}

core_memory_save_metadata = \
    {
        "type": "function",
        "function": {
            "name": "core_memory_save",
            "description": core_memory_save_description,
            "parameters": {
                "type": "object",
                "properties": core_memory_save_properties,
                "required": ["section", "memory"]
            }
        }
    }

system_prompt = "you are a chatbot," \
                + "you have a section of your context called [MEMORY] " \
                + "that contains information relevant to your conversation."

system_prompt_os = system_prompt + (" \n. you must either call a tool (core_memory_save)"
                                    " or write a response to the user."
                                    "Dont take a the same action multiple times! "
                                    "when you learn new information, "
                                    "make sure to always call core_memory_save tool")


def agent_step(user_message, chat_history=[]):
    # prefix messages with system prompt and memory
    messages = [
        # system prompt
        {"role": "system", "content": system_prompt_os},
        # memory
        {
            "role": "system",
            "content": "[MEMORY]\n" + json.dumps(agent_memory)
        },
    ]

    # append the chat history
    messages += chat_history

    # append the most recent message
    messages.append({"role": "user", "content": user_message})

    # agentic loop
    while True:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=[core_memory_save_metadata]
        )
        response = chat_completion.choices[0]

        # update the messages with the agent's response
        messages.append(response.message)

        # if NOT calling a tool (responding to the user), return
        if not response.message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": response.message.content
            })
            return response.message.content

        # if calling a tool, execute the tool
        if response.message.tool_calls:
            # add the tool call response to the message history
            messages.append(
                {"role": "tool", "tool_call_id": response.message.tool_calls[0].id, "name": "core_memory_save",
                 "content": f"Memory updated successfully: {json.dumps(agent_memory)}"})

            # parse the arguments from the LLM function call
            arguments = json.loads(response.message.tool_calls[0].function.arguments)

            # run the function with the specified arguments
            core_memory_save(**arguments)


res = agent_step("my name is mahand")
print(res)