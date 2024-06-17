import random
from telegram import Update
from telegram.ext import ContextTypes

# Truth and Dare lists
truth_questions = [
    "What is your biggest fear?",
    "What is the most embarrassing thing you've ever done?",
    "Have you ever lied to your best friend?",
    "What is your deepest secret?",
    "What is something you’ve never told anyone?",
    "What is the worst thing you’ve ever done?",
    "What is your guilty pleasure?",
    "Who is your secret crush?",
    "What was your most awkward date?",
    "What is the weirdest dream you’ve ever had?",
]

dare_challenges = [
    "Do 10 push-ups.",
    "Sing a song loudly.",
    "Dance for one minute without music.",
    "Do an impression of your favorite celebrity.",
    "Post an embarrassing photo on social media.",
    "Let someone tickle you for 30 seconds.",
    "Talk in a fake accent for the next 3 rounds.",
    "Act like a monkey until your next turn.",
    "Wear socks on your hands for the next 10 minutes.",
    "Try to lick your elbow.",
]

# Command handlers
async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = random.choice(truth_questions)
    await update.message.reply_text(f"Truth: {question}")

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    challenge = random.choice(dare_challenges)
    await update.message.reply_text(f"Dare: {challenge}")
