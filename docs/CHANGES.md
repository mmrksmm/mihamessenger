# From v1 to v2: what changed and why

The first version of MIHA Messenger (2025) was my last  Ren'Py project excluding the CS50x one. The game worked and had all
the core ideas: chats as the main mechanic, affection points, multiple endings and a rigged choice.
The code, though, grew one scene at a time and was hard to maintain. Version 2 keeps the game design and
rebuilds everything around it.

## Structure

| | v1 | v2 |
|---|---|---|
| Story code | one 2,239-line `script.rpy` | `script.rpy` (skeleton) + `story/` with one file per character |
| Character definitions | 17 `define`s, several duplicated under different aliases (`соф`/`Соф`, `яна`/`Яна`, `дев`/`Дев`...) | one `Contact` record per character, with characters built from it |
| Affection | 7 loose variables (`ri`, `er`, `ya`, `de`, `so`, `sg`, `gr`) plus 12 more flags | one dictionary `affection` and the helpers `like()` / `has_max_affection()` |
| Endings | 12 separate `persistent.*` flags | one `persistent.endings` set + an `Ending` registry with titles and hints |
| Chat selection | three copy-pasted 7-option menus (`d1`, `d25`, `d35`) with a counter `n` | one `free_chats` loop + a `chat_picker` screen generated from the data |
| UI | screenshots of a real messenger used as backgrounds, image-based menus | the whole messenger is drawn in code; menus use styles from one theme file |
| Assets | sprites and CGs from other games, real photos, copyrighted music, a commercial font | own simple placeholder art and UI images; free font (Nunito, OFL) |

## Content

The original dialogue was full of in-jokes, slang and references that only made sense to my friends.
For this public version every line was rewritten to keep the same characters, structure and choices,
with neutral wording.

## New in v2

- Endings gallery in the main menu, with hints for locked endings
- Secret endings unlock from progress instead of being reset after one viewing
- Messages appear as chat bubbles, notifications show inside the chat, thoughts show as an overlay