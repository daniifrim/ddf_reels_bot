Creating a **Telegram bot** to collect Instagram Reel links and send them to a Coda database is an excellent idea. Here’s a step-by-step guide to set this up:

---

## **Step 1: Create Your Telegram Bot**
To create a Telegram bot, follow these steps:

1. **Talk to BotFather**:
   - Open Telegram and search for `BotFather`.
   - Start a conversation and type `/newbot`.
   - Follow the prompts to name your bot and create a unique username (e.g., `ReelCollectorBot`).

2. **Get the Bot Token**:
   - After creating the bot, BotFather will provide you with an API token (e.g., `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`).
   - Save this token; it will be used for API calls.

---

## **Step 2: Set Up the Bot to Receive Messages**
You’ll use Python and the `pyTelegramBotAPI` library to handle incoming messages.

### Install Required Libraries:
Run the following command to install the library:
```bash
pip install pyTelegramBotAPI
```

### Create the Python Script:
Here’s a basic script to capture Reel links sent to your bot:

```python
import telebot
import requests
import time

# Telegram Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Coda API Details
CODA_API_KEY = "3e92f721-91d1-485e-aab9-b7d50e4fa4da"
DOC_ID = "dNYzN0H9At4"
TABLE_ID = "tun7MrAA"
COLUMN_ID = "c-LFekrYG0se"

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Function to send data to Coda
def send_to_coda(link, sender):
    url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"
    headers = {
        "Authorization": f"Bearer {CODA_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "rows": [
            {
                "cells": [
                    {"column": COLUMN_ID, "value": link},
                    {"column": "AddedBy", "value": sender}
                ]
            }
        ]
    }
    response = requests.post(url, json=body, headers=headers)
    return response.status_code

# Handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    link = message.text.strip()
    sender = message.from_user.username or message.from_user.first_name
    if link.startswith("https://www.instagram.com/reel/"):
        status_code = send_to_coda(link, sender)
        if status_code == 200:
            bot.reply_to(message, "Link saved successfully!")
        else:
            bot.reply_to(message, f"Failed to save link. Status code: {status_code}")
    else:
        bot.reply_to(message, "Please send a valid Instagram Reel link.")

# Polling for new messages
while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
```

### Replace Placeholders:
- Replace `YOUR_BOT_TOKEN` with your Telegram bot token.
- Replace `CODA_API_KEY`, `DOC_ID`, `TABLE_ID`, and `COLUMN_ID` with your Coda API details.

---

## **Step 3: Run Your Bot**
1. Save the script as `telegram_bot.py`.
2. Run the script:
   ```bash
   python telegram_bot.py
   ```
3. Share your bot’s username with your team so they can start sending Reel links.

---

## **Step 4: Test Your Setup**
1. Send an Instagram Reel link (e.g., `https://www.instagram.com/reel/xyz123/`) to your bot on Telegram.
2. Check your Coda database to confirm the link has been added.

---

## **Optional Enhancements**
### Add Sender Information in Coda:
If you want to track who submitted each link:
- Add a column in your Coda table named `AddedBy`.
- Modify the script’s `send_to_coda()` function to include the sender's username or first name.

### Deploy on a Server:
To keep your bot running 24/7:
- Deploy it on a cloud platform like Heroku or AWS.
- Use Flask or FastAPI for webhook-based handling instead of polling.

---

## **Why This Workflow Works**
- **Ease of Use**: Your team can simply send links via Telegram.
- **Centralized Data**: All links are stored in Coda for easy access and processing.
- **Scalability**: You can add features like metadata extraction or analytics later.

Let me know if you need help setting up any part of this workflow!

Citations:
[1] https://pplx-res.cloudinary.com/image/upload/v1741349265/user_uploads/OJQBySwUPOmZwZy/1000083951.jpg
[2] https://pplx-res.cloudinary.com/image/upload/v1741349590/user_uploads/ZGyEBpowtBLBCyn/Screenshot_20250307_131249_Tasker.jpg
[3] https://www.reddit.com/r/learnpython/comments/di4cbn/telegram_bot_tutorial/
[4] https://flowxo.com/how-to-create-a-bot-for-telegram-short-and-simple-guide-for-beginners/
[5] https://onlizer.com/coda/telegram_bot
[6] https://zapier.com/apps/coda/integrations/telegram/1581202/send-messages-in-telegram-for-new-rows-in-coda
[7] https://github.com/sabber-slt/telegram-real-time
[8] https://www.toptal.com/python/telegram-bot-tutorial-python
[9] https://latenode.com/es/pt-br-br-br-br/integrations/telegram-bot-api/coda
[10] https://stackoverflow.com/questions/76396068/how-to-get-user-id-of-the-sender-who-sent-the-message-in-a-telegram-channel
[11] https://core.telegram.org/bots/api
[12] https://www.reddit.com/r/OpenWebUI/comments/1dtysxe/how_to_connect_a_telegram_bot/
[13] https://www.reddit.com/r/unRAID/comments/fvx8d0/tutorial_get_unraid_notifications_via_telegram/
[14] https://www.reddit.com/r/zlibrary/comments/10mi9i2/now_you_can_have_your_own_telegram_bot_no_more/
[15] https://www.reddit.com/r/TelegramBots/comments/o3l61g/i_made_a_bot_that_can_transform_almost_any_link/
[16] https://www.reddit.com/r/learnpython/comments/15ma4dh/telegram_bot_call_updates_manually/
[17] https://www.reddit.com/r/node/comments/e6uwx5/learn_how_to_build_a_telegram_bot_with_node_and/
[18] https://www.reddit.com/r/Oobabooga/comments/175v2b7/an_idiots_guide_to_the_telegram_bot_extension/
[19] https://www.reddit.com/r/zlibrary/comments/10mlgqv/guide_personal_telegram_bot_complete_guide/
[20] https://www.reddit.com/r/TelegramBots/comments/1dxmivc/help_in_getting_started/
[21] https://www.reddit.com/r/TelegramBots/comments/1e7dyh1/i_created_a_telegram_bot_that_generates_summaries/
[22] https://www.reddit.com/r/Telegram/comments/9is64m/using_a_telegram_bot_as_a_chatfront/
[23] https://www.reddit.com/r/Overseerr/comments/10lsvzj/telegram_setup/
[24] https://www.reddit.com/r/Telegram/comments/3b1pwl/create_your_own_telegram_bot_stepbystep/
[25] https://www.reddit.com/r/django/comments/118wkdq/a_stepbystep_tutorial_for_building_a/
[26] https://stackoverflow.com/questions/41684692/how-to-create-link-in-telegram-bot
[27] https://www.youtube.com/watch?v=CbEYuLCGFDU
[28] https://www.youtube.com/watch?v=vZtm1wuA2yc
[29] http://help.invitemember.com/en/articles/5265372-your-telegram-bot-links
[30] https://stackoverflow.com/questions/38565952/how-to-receive-messages-in-group-chats-using-telegram-bot-api
[31] https://code.esube.com.et/telegram-bot-development-complete-guide-for-beginners
[32] https://core.telegram.org/bots/tutorial
[33] https://www.youtube.com/watch?v=EpQx3jJ1q3Q
[34] https://www.directual.com/lesson-library/how-to-create-a-telegram-bot
[35] https://core.telegram.org/bots/features
[36] https://www.youtube.com/watch?v=WHnhL15uyO0
[37] https://www.youtube.com/watch?v=aupKH_J1xc0
[38] https://rubenlagus.github.io/TelegramBotsDocumentation/getting-started.html
[39] https://www.reddit.com/user/AI_Scout_Official/submitted/
[40] https://www.reddit.com/r/learnpython/comments/sfpwxr/how_can_i_automatically_run_my_python_script_in_a/
[41] https://www.reddit.com/r/clickup/comments/k0fhyl/what_are_most_flexible_clickup_alternatives/
[42] https://www.reddit.com/r/web_design/comments/lbf0og/project_management_what_do_you_use/
[43] https://www.reddit.com/r/productivity/comments/101h6ch/what_productivity_tools_are_you_using_in_2023/
[44] https://www.reddit.com/r/chromeos/comments/12dfase/underappreciated_progressive_web_apps_pwa_thread/
[45] https://www.reddit.com/r/MachineLearning/comments/bx0apm/d_how_do_you_manage_your_machine_learning/
[46] https://www.reddit.com/r/learnprogramming/comments/iax5ec/what_coursebootcamp_can_i_take_that_would_make_me/
[47] https://www.reddit.com/r/bash/comments/t6u8xd/i_made_a_collection_of_readytouse_loading/
[48] https://www.reddit.com/r/automation/comments/1ifx67k/automate_tiktok_posts_to_all_social_channels/?tl=it
[49] https://www.reddit.com/r/webdev/comments/xvjjol/can_you_become_a_web_developer_without_a_cs_degree/
[50] https://www.reddit.com/r/malaysia/comments/1dbqykl/calling_for_all_software_engineer_in_malaysia/
[51] https://www.reddit.com/user/CompetitiveChoice732/
[52] https://www.reddit.com/r/AutomateUser/comments/le2fkj/what_do_you_use_automate_for/?tl=it
[53] https://latenode.com/integrations/coda/telegram-bot-api
[54] https://community.coda.io/t/telegram-bot-pack-available-to-install/40354
[55] https://www.make.com/en/templates/2514-send-telegram-messages-for-new-rows-in-a-coda-table
[56] https://n8n.io/integrations/coda/and/telegram/
[57] https://onlizer.com/coda
[58] https://4spotconsulting.com/automate-telegram-messages-with-coda-a-step-by-step-guide/
[59] https://latenode.com/integrations/telegram-bot-api?4b77e0b0_page=6&820bb7f0_page=9
[60] https://latenode.com/integrations/telegram-bot-api/coda
[61] https://coda.io/packs/telegram-bot-10228
[62] https://www.make.com/en/integrations/coda/telegram
[63] https://www.appypie.io/integrate/apps/telegram-bot/integrations/coda
[64] https://www.reddit.com/r/Telegram/comments/wy7efx/a_way_to_see_who_sends_messages_in_groups/
[65] https://www.reddit.com/r/changedetectionio/comments/ztcos5/telegram_bot_with_userid/
[66] https://www.reddit.com/r/TelegramBots/comments/17kjx4w/automated_message_using_bot/
[67] https://www.reddit.com/r/Telegram/comments/rckcmu/how_do_you_find_out_an_identity_of_an_anonymous/
[68] https://www.reddit.com/r/Telegram/comments/1c7f5bu/how_to_telegram_web_apps_recognise_a_user_and/
[69] https://www.reddit.com/r/Notion/comments/piawnn/ive_made_a_free_opensource_selfhosted_singleuser/
[70] https://www.reddit.com/r/Python/comments/8ivt42/is_it_possible_to_read_or_copy_telegram_messages/
[71] https://www.reddit.com/r/OSINT/comments/kvb5jd/telegram_bot_to_find_which_groups_the_person_is/
[72] https://www.reddit.com/r/Python/comments/amhuty/i_made_a_telegram_bot_you_can_send_messages_to/
[73] https://www.reddit.com/r/Telegram/comments/ksy01k/privacy_concern_forwarding_messages/
[74] https://www.reddit.com/r/Telegram/comments/1f2p61w/how_to_find_another_users_id/
[75] https://www.reddit.com/r/TelegramBots/comments/1c8ng6b/anyone_knows_a_free_bot_for_scheduling_messages/
[76] https://www.reddit.com/r/TelegramBots/comments/rmsv82/send_bulk_messages_with_telegram_api/
[77] https://www.reddit.com/r/Telegram/comments/r21kte/question_how_to_search_for_messages_sent_by_an/
[78] https://github.com/python-telegram-bot/python-telegram-bot/discussions/2295
[79] https://stackoverflow.com/questions/70987716/how-to-insert-data-into-a-database-from-a-telegram-bot
[80] https://onlizer.com/notify/telegram_bot/smart_sender
[81] https://github.com/yagop/node-telegram-bot-api/issues/1104
[82] https://www.youtube.com/watch?v=kobnfPJLqsY
[83] https://community.make.com/t/telegram-send-message-to-an-username/11930
[84] https://vikesh.me/blog/telegram-bot-database/
[85] https://github.com/yagop/node-telegram-bot-api/issues/444
[86] https://community.sinch.com/t5/Telegram/Can-I-send-a-message-to-Telegram-user-with-their-Telegram-ID-or/ta-p/10235
[87] https://severalnines.com/blog/mobile-alerts-notifications-your-database-using-telegram/
[88] https://onlizer.com/notify/whatsapp/telegram_bot
[89] https://community.make.com/t/sending-messages-in-telegram-from-a-user-not-a-bot/49105
[90] https://www.reddit.com/r/learnpython/comments/j7drpv/create_a_whatsapptelegram_bot_which_sends_a/
[91] https://www.reddit.com/r/Telegram/comments/1itv0ls/nocode_tutorial_to_make_ai_agent_telegram_bots/
[92] https://www.reddit.com/r/learnprogramming/comments/12swbq4/how_to_create_a_telegram_notification_bot_when_ui/
[93] https://www.reddit.com/r/Julia/comments/ign33f/tutorial_sending_messages_to_telegram_using/
[94] https://www.reddit.com/r/TelegramBots/comments/oy6hys/beginner_guide_for_telegram_bots_programming/
[95] https://flowfuse.com/node-red/notification/telegram/
[96] https://telegram.ebda3at-moparmj.com/Telegram/MakeBottelegram/index-en.html
[97] https://steemit.com/utopian-io/@abhi3700/telegram-bot-tutorial-01-introduction-or-get-chats-or-send-messages
[98] https://apidog.com/blog/beginners-guide-to-telegram-bot-api/
[99] https://www.reddit.com/r/SideProject/comments/1alyrhc/what_are_you_building_right_now/
[100] https://www.reddit.com/r/Notion/comments/c3awp2/any_way_to_link_notion_into_telegram/
[101] https://www.reddit.com/r/productivity/comments/evjtlz/build_the_ultimate_personal_knowledge_management/
[102] https://www.reddit.com/r/SaaS/comments/1ftvnsb/whats_your_tech_stack_for_building_your_saas/
[103] https://www.reddit.com/r/Airtable/comments/v6uuqs/do_you_think_airtables_pricing_strurue_is_be_a/
[104] https://www.reddit.com/r/Notion/comments/13zwghq/if_you_left_notion_where_did_you_go/
[105] https://albato.com/connect/coda-with-telegram
[106] https://www.pabbly.com/connect/integrations/coda/telegram-bot/
[107] https://www.reddit.com/r/Telegram/comments/km752u/telegram_sent_a_message_that_i_didnt/
[108] https://www.reddit.com/r/Telegram/comments/js7sta/can_someone_find_my_contact_through_bots/
[109] https://www.reddit.com/r/learnprogramming/comments/7q21ba/i_made_a_telegram_bot_and_i_want_it_to_make/
[110] https://www.reddit.com/r/Telegram/comments/jldv6c/is_there_a_way_i_can_know_who_is_forwarding/
[111] https://www.reddit.com/r/Telegram/comments/kt9n7h/new_to_telegram_how_to_display_who_sent_me_a/
[112] https://www.reddit.com/r/n8n/comments/1isach8/automating_email_responses_via_telegram_in_n8n/
[113] https://docs.python-telegram-bot.org/en/v21.9/telegram.user.html
[114] https://latenode.com/integrations/telegram-bot-api/database
[115] https://www.youtube.com/watch?v=jkSI-floXs8

---
Answer from Perplexity: pplx.ai/share