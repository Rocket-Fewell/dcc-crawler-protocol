# Discord channel agent

A bot the cloud agent uses to listen and speak in one Discord text channel. It is not the table voice bridge (`bot/` / `discord-voice-bridge`). It has its own token and its own channel, so it cannot speak as the GM or move the game.

```
someone posts in the channel
        │
        ▼
discord_agent.py listen  ──wake webhook──►  Cursor automation
                                                    │
                                                    ▼
                              discord_agent.py new     (unread lines)
                              discord_agent.py say     (one reply)
```

## What the other bot needs to set

Create a Discord application, enable **Message Content Intent**, and invite the bot with View Channel, Send Messages, and Read Message History. Then export these in the shell that runs `listen` and in the shell the Cursor automation uses. Do not commit them.

| Variable | Required | Meaning |
|---|---|---|
| `AGENT_DISCORD_TOKEN` | yes | This bot's token. Not `GM_DISCORD_TOKEN`. |
| `AGENT_DISCORD_CHANNEL_ID` | yes | The one channel to read and post in. |
| `AGENT_WAKE_URL` | for wakes | Cursor automation webhook from a saved automation. |
| `AGENT_WAKE_KEY` | if the webhook has one | Sent as `Authorization: Bearer`. |
| `AGENT_STATE_DIR` | no | Cursor files. Default `agent-discord/state` (gitignored). |
| `AGENT_POLL_SECONDS` | no | Poll interval. Default 4. |
| `AGENT_WAKE_DEBOUNCE_SECONDS` | no | Quiet gap before one wake. Default 2.5. |
| `AGENT_WAKE_MAX_WAIT_SECONDS` | no | Send anyway if lines keep arriving. Default 8. |

The automation prompt is `PROMPT.md`. Trigger: webhook. Repository: this one. The listener POSTs:

```json
{"event":"channel_message","channel_id":"...","lines":[{"id":"...","author":"...","bot":false,"text":"..."}],"hint":"Run: python3 agent-discord/discord_agent.py new ..."}
```

Redirects are not followed. The URL and key are never printed. A failed wake leaves the listener cursor where it was and retries. `new` uses a different cursor, so a wake does not mark the lines answered.

## Commands

```bash
python3 agent-discord/discord_agent.py whoami
python3 agent-discord/discord_agent.py read --limit 20
python3 agent-discord/discord_agent.py new
python3 agent-discord/discord_agent.py say "hello from the channel agent"
python3 agent-discord/discord_agent.py listen
```

`listen` without `AGENT_WAKE_URL` prints new lines locally and does not post. `say` splits long text under Discord's 2000-character limit and turns mentions off.

Check the login before leaving it running: `whoami` prints the bot name, the bot id, and the channel id. It does not print the token.

## Tests

```bash
python3 -m unittest agent-discord/tests/test_discord_agent.py
python3 ops/check_repo_safe.py --tree agent-discord
```
