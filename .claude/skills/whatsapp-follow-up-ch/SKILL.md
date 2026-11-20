---
name: "whatsapp-follow-up-ch"
description: "Reactivate Coach Ben's past product clients on WhatsApp Business (reconnect, restock check, group coaching / call invite, challenge question) safely and personally, in English, by first name. Use for \"run follow up customer lama\", \"whatsapp follow up\", \"reactivate old clients\" or \"follow up past clients\"."
---

# WhatsApp Follow-Up — Coach Ben (Client Reactivation)

This skill follows up **past clients who have bought products before** through **WhatsApp Web (WhatsApp Business)** using **Claude in Chrome**. The goal is to reactivate them: restart their routine, restock products, and where it fits, bring them into group coaching or a call.

Claude reads each chat, picks the right message for the stage, shows the draft, and sends only after the user approves.

Only for existing clients who agreed to be contacted. Nothing here gets around WhatsApp's limits, so keep it natural, personal and never spammy.

## Voice (Coach Ben)
- **English**, conversational, warm and direct. Short lines. Sounds like a coach texting, not a brand broadcasting.
- Sign as **Coach Ben** only when introducing himself (Message 1 / scripts that reopen a chat). Otherwise just talk.
- Address the client by **first name**. Take it from the WhatsApp contact name or the chat; use only the first name. If it's unclear (e.g. a business name, nickname, or "~" unsaved number), ask the user before drafting. Never write "[First name]" in a sent message.
- **Few to no emojis.** At most one per message, often none. No emoji strings.
- No pressure, no hard selling. Ask a question, make it easy to reply.
- If the user later shares real messages they've sent, match their wording and rhythm and update these scripts.

## Safety rules
- Only message clients who agreed to be contacted. Never blast.
- One message at a time. The next message only after the client replies.
- No reply: wait 2–3 days, send ONE short follow-up.
- Still silent: stop until the client reaches out.
- If the client doesn't want messages: stop immediately and respect it.
- Don't send every script to the same person. Pick by situation.
- Before sending, show each draft to the user and wait for approval. Never send anything without approval.

## Main flow
Day 1 → Message 1. Reply → Message 2. No reply after 2–3 days → Message 3. Reply YES → Message 4, then hand over for a personal conversation.

### Message 1 — Reconnect
Hi [First name], Coach Ben here.

It's been a while since we last caught up. How have you been, and how's your fat loss going lately?

Just checking in. If anything's been getting in the way, let me know and I'll help where I can.

### Message 2 — After they reply (pick the version that fits their reply)
**2A — They're still on track or want to keep going:**
Good to hear, [First name].

How are you doing on your products right now? If you're running low, I can sort out a restock for you so you don't lose momentum.

**2B — They've fallen off / struggling:**
Totally normal, [First name]. Busy schedules do that to everyone.

We've got a group coaching running right now that helps people get their routine back without overhauling their whole life. Want me to send you the details?

**2C — They have specific questions or a bigger goal:**
Makes sense, [First name]. That's worth a proper conversation.

Would you be open to a quick call this week? I can look at where you are now and map out the next steps with you.

### Message 3 — Nudge (if silent for 2–3 days, once only)
Hi [First name], just a quick one.

If you'd still like my help getting back on track, reply YES and I'll follow up with you personally.

### Message 4 — When they reply YES
Great, thanks [First name].

Quick question so I know how to help. What's the biggest thing holding you back right now?

1. Controlling what I eat
2. Weight is stuck
3. Cravings
4. Staying consistent with a busy schedule

Just reply with the number.

After Message 4, tell the user to continue personally (suggest products, group coaching or a call based on the answer).

## 10 reactivation scripts — pick ONE by situation
1. **Friendly Reconnect:** Hi [First name], Coach Ben here. It's been a while. How have things been on your end, and how's your fat loss journey going?
2. **Challenge Check:** Hi [First name], quick check-in. Is anything making it hard to stay on track with your eating or weight right now? Tell me and I'll see how I can help.
3. **Consistency Check:** Hi [First name], how's your routine these days? Still going, or has work taken over? No pressure, just checking in.
4. **Group Coaching Invite:** Got it, [First name]. We've got a group coaching running that helps busy people stay consistent. Want me to send you the details?
5. **Reply YES Follow-Up:** Hi [First name], if you'd like my help getting back on track, just reply YES and I'll follow up with you personally.
6. **Progress Check:** Hi [First name], I'm curious. Since we last worked together, have you noticed any changes in your weight, measurements or energy? I'd love to hear.
7. **Quiet Past Client:** Hi [First name], it's been a while since we caught up. Hope you've been well. If you ever want support to restart a healthy routine, I'm still here.
8. **Restart Invite:** Hi [First name], if you're thinking of getting back into a healthy routine, I can help you rebuild it around your schedule. Want me to share how we can do that, through group coaching or a quick call?
9. **Product Restock Check:** Hi [First name], quick check. How are you doing on your products? If you're running low or want help setting up your routine with them again, just let me know.
10. **Final Follow-Up:** Hi [First name], just checking in one last time. Whenever you're ready to get back on track, message me anytime. If now isn't the right time, that's completely fine. Take care.

Script 10 is the final message. After that, stop.

## How to run (Claude in Chrome + WhatsApp Web)

### Before starting (once per session)
1. Load the Claude in Chrome tools in one go (ToolSearch: `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__get_page_text`). Call `tabs_context_mcp` first. If the tools aren't available, tell the user to install the Claude in Chrome extension and stop.
2. Ask for the **WhatsApp Business label name** that holds the past clients. Remember it for the whole session; don't ask again.
3. Open `https://web.whatsapp.com` in a new tab. If there's a QR code / not logged in, stop and ask the user to log in first.

### For each chat in the label
1. Open the label (Chats → filter/Labels menu → choose the label) and list the chats in it.
2. Open one chat. Read the recent history (last message, who sent it, date, what products they bought if visible).
3. Decide the stage:
   - No follow-up from us yet → **Message 1** (or the single best-fitting script from the 10)
   - Client replied to Message 1 → **Message 2** (2A, 2B or 2C depending on their reply)
   - Our last message is 2–3+ days old, no reply, and no nudge sent yet → **Message 3** (once only)
   - Client replied YES → **Message 4**, then tell the user to continue personally
   - Our last message is under 2 days old with no reply → **skip, wait**
   - Already nudged and still silent → **skip, stop**
   - Client asked to stop / doesn't want messages → **skip completely**
   - An active personal conversation is going on → **skip**, don't interrupt
4. Show the user: contact name, first name to be used, chat summary, stage, and the full draft (with the real first name filled in). **Wait for OK.** If the user edits it, use their version.
5. After OK: type the draft in the message box (keep line breaks with Shift+Enter) and send. Check the message went out correctly.
6. Move to the next chat.

### Pace
- Small batches: max 5 contacts per round, then ask the user whether to continue.
- Natural rhythm, with pauses between chats. Never blast. One message at a time per contact.

### Wrap-up
Give a summary: who got which message, who was skipped and why, and who the user should follow up personally (and whether they look like a restock, group coaching or call lead).
