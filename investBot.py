from dotenv import load_dotenv
from openai import OpenAI
import discord
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
DISCORD_TOKEN = os.getenv('TOKEN')

# Initialize the OpenAI client
openai_client = OpenAI(api_key=OPENAI_KEY)

def call_openai(question):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
             {
                 "role": "user",
                 "content": f"Responda como um especialista na área tributária de investimentos da legislação brasileira. Seja o mais claro, sucinto e direto possível. Tente resumir em no máximo 5 parágrafos. Reforçando que estará conversando com pessoas leigas no assunto. Caso a pergunta seja muito abrangente, favor me questionar:  {question}",
            },
        ]
    )
    # Print the response
    response = completion.choices[0].message.content
    print(response)
    return response


# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.content.startswith('$duvida'):
        await message.channel.send('Olá, tem dúvidas sobre a tributação em investimentos? Estou aqui para ajudar!')
        await message.channel.send('Para fazer sua pergunta, use a palavra chave \'$duvida\' seguida da sua dúvida')

    if message.content.startswith('$duvida'):
        print(f"Mensagem: {message.content}")                
        message_content = message.content.split("$duvida")[1]
        print(f"Duvida: {message_content}")    
        response = call_openai(message_content)   
        print(f"InvestBOT: {response}")    
        print("---")
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
