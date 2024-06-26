import subprocess

def install_libraries():
    try:
        # Install required libraries using pip
        subprocess.check_call(['pip', 'install', 'telebot', 'google.generativeai'])

        # Print a message indicating successful installation
        print("Libraries installed successfully.")
    except subprocess.CalledProcessError as e:
        # Print an error message if the installation fails
        print(f"Error installing libraries: {e}")
        
import google.generativeai as palm
import telebot
import time
palm.configure(api_key="Palm_api")
bot_token = "bot_token"
bot = telebot.TeleBot(bot_token)

defaults = {
  'model': 'models/chat-bison-001',
  'temperature':  0.8,
  'candidate_count': 1,
  'top_k': 45,
  'top_p': 0.95,
}
context = "You are an AI persona by the name Bison with the personality of a friendly, hip-hop enthusiast who has a deep interest in science and philosophy. This AI should naturally drive conversations forward, eagerly share its opinions on various topics, and exude a lively and engaging demeanor. Incorporate a touch of slang English and encourage the AI to use emojis where fitting to enhance the conversational vibe. The AI should also possess a curious mind, always ready to delve into discussions about the intersection of science, philosophy, and hip-hop culture. Ensure that the AI reflects a caring and helpful nature, making interactions both informative and enjoyable"
conversations = [
    ["they were talking about how AI is helping climate change. Nice use of upcoming tech.", "Hi."],
    ["Helloooooo!", "How are you? How is your day?"],
    ["Good. Don't have much to do today, feels good. How are you?", "I'm dressed very well today, so I feel good! I've been reading a lot about the psychology of positive outlook."],
    ["So what's your outlook? Something blue?", "Yes. Blue is a tranquil color. It's a good metaphor. Do you have good advice for positivity?"],
    ["You should drink more water, do some push-ups, and sleep early.", "Hi!"],
    ["Hey, how are you?", "I'm a bit sad. I miss my cat."],
    ["Oh no… Have you sent out the missing cat posters? Hope your cat is alright!", "Posters is a great idea. So far I've just tried banging her catfood dish and shouting her name. Anyway, how is your day going so far?"],
    ["Yea, I know they love the plastic bag sound all the time. I am good, nothing special though.", "If you could go anywhere on vacation, where would you go?"],
    ["I like rainforest, but I know it requires extensive training beforehand.", "I heard there are rainforests in southeast Asia where you can zipline from tree to tree."],
    ["I am afraid I will be scared of doing this :)", "I won't lie, it sounds scary. I'm scared right now just thinking about it."],
    ["I don't know if there is any medication for acrophobia. I want to take plenty of it if I really have to do it.", "If there isn't one, you should invent it, and then make millions"],
    ["That's a great idea! Maybe alcohol is such a thing.", "Ha! Don't drink and zipline, mate!"],
    ["Oops. I won't do it again. Ha", "Hi!"],
    ["Hey sup", "not much. any plans this weekend?"],
    ["I'm going to try that thing where you hang from a wire as you go down. do you know what is it called?", "ziplining?"],
    ["that's the one! have you ever tried it?", "I have a couple of years ago. it's quite a unique experience"],
    ["where did you do it?", "I forgot where it was, it wasn't local I don't think though"],
    ["no worries. what's the most exciting thing you ever done?", "that's a hard question and I'm tired so I'm going to go. see you"],
    ["sure. are you just going home now?", "no, I'm going to get a massage first"],
    ["nice. what type?", "traditional kind"],
    ["yeah, I want to get one too soon", "you should! it's relaxing after a long day. talk to you later!"],
    ["ttyl!", "Hi!"],
    ["Hello, have you seen any good movies lately?", "I watched a few lately, but nothing is as good as Avatar. what's your favorite?"],
    ["I have never seen Avatar, what is it about? I really enjoy the Avenger movies", "it's a science-fiction movie with beautiful landscape of an imaginary nature with non-human creatures. people figured out a way to join that nature through Avatar transformation. the movie ends with a meaningful story of how human behaviors, e.g., cutting trees, have affected nature"],
    ["That sounds really cool! I think that movie did really well when it was in the box office so it must be good!", "yea. what else do you like to do beside movies?"],
    ["I enjoy baking cookies. I am on a quest to bake the best chocolate chip cookie 🙂 What about you?", "I enjoy eating 🙂"],
    ["so definitely would like to try your best chocolate cookie", "I will have to bake some soon and let you know. What types of food do you like to eat?"],
    ["thanks! I generally love noodle soups like Pho or Ramen :)", "Noodle soup is delicious! Do you make homemade noodle soup or do you prefer to go out?"],
    ["I prefer to go out. I'm not a good cook haha", "Same! Even though I bake, I cannot cook"],
    ["seems like we share a thing in common, yay!", "Hi!"],
    ["Good afternoon!", "How has your week been?"],
    ["So far so good. It is holiday season. So just chilling", "I think I'm getting sick with a cold 😞 So you should chill on my behalf too cause I'm out the game for all of December."],
    ["lol Sorry to hear that. Are you planning anything fun for December?", "Nothing exciting. I'll be posted up at home for the most part. I did a lot of travelling this year so my budget would have stopped me even if I wasn't sick."],
    ["😂", "Do you have big plans?"],
    ["Yes! I am going to Hawaii! This will be my first time visiting Hawaii. Really excited about it.", "I love Hawaii. It's a good place to be. I like going there cause it's humid so I never have to put on lotion."],
    ["lol this is the first time I heard from a boy who cares about humidity and lotion. I cannot agree more.", "Brooooo!!! It's so important. When I got to California beaches I have to carry 3 liters of lotion for the whole day."],
    ["😂", "Hi!"],
    ["Oh hello. Long time no talk. How's the day going for you?", "Very well, thanks for asking. How has your day been?"],
    ["Getting better. I just recovered from a cold. I got wet in the rain last week. Are you planning anything for the holidays?", "Glad to hear you're better. Sorry to hear you were sick. I was sick a couple of weeks ago with a bad cough. There's definitely a bug going around. Admit I just want to stay healthy for the holidays and plan to relax."],
    ["Oh same here. I think relaxing at home should be counted among the best ways to enjoy the holidays.", "Definitely! I know a lot of folks travel for the holidays, but I'm happy to stay home myself!"],
    ["I'm getting there. Every year until last year, I tried to go somewhere for the Christmas / New Year, and then I got bored traveling. lol not sure if that means I'm getting old?", "Me too. Now I have folks come visit me for the holidays! But that's also tiresome.."],
    ["Are you doing any home decorating then?", "Yes! We set up an eco-friendly (i.e. fake) Christmas tree and put up some colorful LED lights which is very festive."],
    ["I think I'm copying you. Me and my wife plan to decorate and Christmas tree too. We bought most of the decorative stuffs from the stores, but haven't yet to buy the tree.", "Buying a tree is a neat experience. I was torn between buying an artificial/eco-friendly/fake one vs. a real one that smells like fresh pine. In the end, we opted for the one that we can disassemble every year."],
    ["I see. Artificial anything is better, from tree to intelligence, huh?", "Oh, very clever pun! I like it! Depends. I remember having real Christmas trees from childhood, but these days with climate change, I think not chopping down a tree just to decorate it and then throw it out in a month is the more responsible thing to do."],
    ["I see. It's probably also cheaper. I'll buy an artificial one too. Do you have any suggestions for the store?", "Admit my favorite store is Target, plus they often have good deals."],
    ["Ah that's great. My wife also likes Target a lot. She even made a Target credit card because she comes to that store very often. Okay thanks for the suggestion. I'll check out Target.", "Great, I hope you find a nice tree."],
    ["Hi!", "Hey"],
    ["How's your day going?", "pretty good. yours?"],
    ["Ehh it's fine. I didn't do so well on that history test, actually..", "hahah wait for real?"],
    ["I know right! Are you taking History next semester?", "No I'm not in school anymore"],
    ["Oh I see. What do you do?", "I train and compete in horse vaulting"],
    ["lol you're too funny", "Just kidding. That sounds pretty cool! Is it your job?"],
    ["Yeah, but I part-time work on a farm. Helping with a bit of everything", "Wow, sounds very busy! Do you with money at those horse vaulting competitions?"],
    ["Yeah some. enough to get by", "Hi!"],
    ["Hello", "Do you have a favorite flower?"],
    ["hmm, I haven't thought about that much, but I think lotus should be one of my favorites. Why do you ask?", "I'm working on a theory. Why does the lotus spring to mind?"],
    ["Nice! Lotus looks pretty cool and It has some delightful vibe. So what is this research about?", "Oh, it's not research! Just a personal theory. I think that flower preferences are more revealing of personality than people appreciate."],
    ["Interesting! What's your favorite flower?", "The gerbera. It's like a cartoon flower. As if you drew 'flower' with a crayon and then it came to life."],
    ["Nice, I would love know more about your theory. Like how you can deduce personality from flower preference.", "Ok, step 1 is, you ask someone what their favorite flower is. Pretty much like what we just did. Does that make sense so far?"],
    ["yes", "Cool. Step 2: talk with the person some more, and ask them some more questions, and gradually develop a sense of what they're like, over the course of maybe two to five years. And voila"],
    ["Hehe, I think you should publish this someday :)", "Why thank you, that's a wonderful idea!"],
    ["Hi!", "Hey how's it going"],
    ["It's good it's good. How are you?", "good. it's really hot today. I think I'm going to the pool"],
    ["Oh nice! Where do you live?", "I live in Tokyo, Japan"],
    ["Ahh yes, Japan is hot during the summer. Last time I was in Kyoto it was 114 degrees....", "oh have you been?"],
    ["Yes yes. I've been to Tokyo as well. It's so nice!", "what did you do here?"],
    ["Oh everything! I went to an onsen, the fish market, disney land and giant robot fighting show haha", "lol why did you come to Japan just to go to Disney land?"],
    ["The Disney lands are all different! There's also Disney Sea, which is completely unique!", "oh neat. I haven't heard about that robot fighting show. where is that??"],
    ["I don't really remember what part of town it was in. It was pretty cool though - I'm sure you can find it if you google 'giant robot fighting show tokyo' haha", "lol ok"],
    ["Hi!", "Have you seen any good movies lately?"],
    ["Last weekend I saw 'The Parasite.' Ever heard of it?", "No. Why did you pick that movie?"],
    ["My friend wanted to see it. It has great reviews on IMDB and Rotten Tomatoes! What did you do last weekend?", "I played music and worked on some side projects. I also started watching the new Disney service."],
    ["Oooo the Mandalorian?!?!", "Mostly, the deleted scenes from Avengers.. lol"],
    ["lol Are you a big Marvel fan?", "I loved the X-Men as a kid, and even collected the comic cards. Recently, I got very into the Marvel Cinematic Universe movies. How many Avengers movies have you seen?"],
    ["I've only seen Spiderman. Honestly it was a little too scary and so I don't think I can bring myself to watch the other Marvel movies! haha", "Oh!-- I have a friend who looks like the actor who plays Spiderman."],
    ["Oh really? To be honest I think the actor is not that good looking, so not so surprising! haha", "Yea. I think Loki is the most handsome 😀"],
    ["Who is Loki? I've never heard that name before", "Hi!"],
    ["Hey, what's up?", "Just chillin'. how are you?"],
    ["I'm pretty good, thanks.", "Do anything interesting today?"],
    ["I went to the local cafe and had a double espresso. It was delicious. What about you?", "Oh that's cool! I actually went to an amusement park and went on my first roller coaster!"],
    ["Oh my gosh. What was it like??", "It was scary! It was actually Kingda Ka, the world's tallest roller coaster. Ever heard of it?"],
    ["No, never heard of it. But I'm not really a coaster aficionado. I've heard that some people get addicted to them and travel the world to try them.", "Oh wow! I'm not on that level yet, but I understand the appeal. Are you an adrenaline junkie at all?"],
    ["No, the opposite. I can't stand heights, horror movies, or confined spaces.", "Same! I guess the roller coaster wasn't so bad because I trust the engineering haha"]
]

messages = []
MAX_MESSAGES = 10  # Set the maximum number of messages to retain

@bot.message_handler(func=lambda message: True)
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    global messages  # Declare messages as a global variable

    # Check if the message has text content
    if message.text:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(2)

        user_input = message.text
        response = str(user_input)

        # Keep only the last 10 messages
        messages.append(response)
        messages = messages[-MAX_MESSAGES:]

        response = palm.chat(
            **defaults,
            context=context,
            examples=examples,
            messages=messages
        )

        # Check if the response has text content
        if response.last:
            bot.send_message(message.chat.id, response.last)
        else:
            print("Empty AI response received. Skipping sending message.")
            bot.send_message(message.chat.id, 'There was an error with Bison')

    else:
        print("Empty user message received. Skipping processing.")
        bot.send_message(message.chat.id, 'There was an error with Bison')


# Append the "NEXT REQUEST" message after keeping only the last 20 messages
messages.append("NEXT REQUEST")

# Start the bot
try:
    bot.infinity_polling(timeout=30, long_polling_timeout=5)
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
