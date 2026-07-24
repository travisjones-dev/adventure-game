from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic()

#Instructions/Context for Claude model
system_prompt = """You are a dungeon master narrating a dark fantasy text adventure.
The player starts in a dimly lit stone room. There is a wooden door to the north and a rusty sword on the floor.
Keep respones short (2-4 sentences). Be descriptive but concise.
"""

messages = []

inventory = []

print("=== ADVENTURE GAME ===")
print("Type 'quit' to exit\n")
print("You wake up on a cold stone floor...\n")

#Pick up item tool
tools = [
    {
        "name": "pick_up",
        "description": "Pick up an item and store it in the player's inventory",
        "input_schema": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "The name of the item to pick up"
                }
            },
            "required": ["item"]
        }
    }
]


#Main program function - while loop handles the conversation
while True:
    user_input = input("You: ")

    #Allows the user at anytime to quit
    if user_input == "quit":
        break
    
    #Appends the user_input to the messages list for claude to maintain context
    messages.append({
        "role": "user", "content": user_input
    })

    #1st API call
    response = client.messages.create(
        max_tokens = 1000,
        model = "claude-opus-4-5",
        system = system_prompt,
        messages = messages,
        tools = tools
    )

    #Appends claudes response to the messages list, maintaining that context
    messages.append({
        "role": "assistant", "content": response.content
    })

    #Handles when tools are called, makes it so claude responds with the newly added item into the inventory list - more of a dev confirmation 
    if response.stop_reason == "tool_use":
        item_name = response.content[0].input['item']

        if item_name in inventory:
            result_message = f"You already have the {item_name} in your inventory."
            print(inventory)

        else: 
            inventory.append(item_name)
            result_message = f"You picked up the {item_name} and added it to your inventory."
            print(inventory)

            #Adds the tool use and newly added inventory item context, allows claude to see the inventory
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": response.content[0].id,
                    "content": f"You picked up the {item_name}  and added it to your inventory."
                }
            ]

        })

        #2nd API call - requesting claude to narrate the pick up of an item
        narration = client.messages.create(
            max_tokens = 1000,
            model = "claude-sonnet-4-6",
            system = system_prompt,
            messages=messages,
            tools=tools 
        )

        print(narration.content[0].text)

        #This handles the normal non-tool call responses from user.
    else:
        print(response.content[0].text)