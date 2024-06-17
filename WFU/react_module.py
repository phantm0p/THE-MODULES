import random
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext import Application

# List of reactions
reactions = [
    "( ͡° ͜ʖ ͡°)", "( . •́ _ʖ •̀ .)", "( ಠ ͜ʖ ಠ)", "( ͡ ͜ʖ ͡ )", "(ʘ ͜ʖ ʘ)",
    "ヾ(´〇`)ﾉ♪♪♪", "ヽ(o´∀`)ﾉ♪♬", "♪♬((d⌒ω⌒b))♬♪", "└(＾＾)┐", "(￣▽￣)/♫•*¨*•.¸¸♪",
    # ... (add the remaining reactions here)
]

async def react(update: Update, context: CallbackContext):
    message = update.effective_message
    react = random.choice(reactions)
    if message.reply_to_message:
        await message.reply_to_message.reply_text(react)
    else:
        await message.reply_text(react)

def register_react_handler(application: Application):
    react_handler = CommandHandler("react", react)
    application.add_handler(react_handler)

__command_list__ = ["react"]
__handlers__ = [react]
