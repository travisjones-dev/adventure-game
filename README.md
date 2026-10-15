# Adventure Game

A text-based, D&D-style dark fantasy adventure in Python, with Claude as the dungeon master. You type what you want to do; Claude narrates what happens. When you pick something up, Claude calls a `pick_up` tool and the game adds the item to a persistent inventory.

I built this to put the Anthropic *Building with the Claude API* course into practice: multi-turn conversation state, system prompts, and tool use.

## How it works

- **Conversation history:** every player input and every Claude response is appended to a `messages` list that is sent on each call, so the story stays consistent from turn to turn.
- **System prompt:** sets Claude up as a dungeon master, establishes the starting room (a stone chamber with a door to the north and a rusty sword on the floor), and keeps replies to 2–4 sentences.
- **Tool use for inventory:** the `pick_up` tool is defined with a JSON schema. When Claude decides the player is picking something up, it stops with `stop_reason == "tool_use"`. The game then updates the inventory (ignoring duplicates), returns a `tool_result`, and makes a second call so Claude can narrate the pickup.

## Running it

Requires Python 3.9+ and an [Anthropic API key](https://console.anthropic.com/).

```bash
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your-key-here" > .env
python adventure.py
```

Type actions like `look around` or `pick up the sword`, and `quit` to exit.
