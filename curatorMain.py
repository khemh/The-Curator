import discord
import random
from discord.ext.commands import Bot
import os

BOT_PREFIX = ("c!")
TOKEN = 
client = Bot(command_prefix=BOT_PREFIX)
folder=os.path.dirname(os.path.realpath(__file__)) 
def get_channel_list():
	channelfile = open(os.path.join(folder,'channellist.txt'),"r")
	imageonlychannels = channelfile.read().splitlines()
	channelfile.close()
	return imageonlychannels
imageonlylist = get_channel_list()

@client.event
async def on_ready():

	print(f'Logged in as {client.user}')

@client.command('imageonly')
async def imageonly(message):
	channel = message.channel
	global imageonlylist
	if(imageonlylist):
		if(str(channel.id) in imageonlylist):
			def checkauthor(m2):
				return message.author ==m2.author
			await channel.send("Image only disabled")
			tempchannellist=get_channel_list()
			tempchannellist.remove(str(channel.id))
			channelfile=open("channellist.txt", "w")
			if(len(tempchannellist)==0):
				pass
			else:
				channelfile.writelines(["%s\n" % item  for item in tempchannellist])
			channelfile.close()
			imageonlylist=tempchannellist
			print(imageonlylist)
		else:
			def checkauthor(m2):
				return message.author ==m2.author
			await channel.send("Image only enabled")
			channelid = channel.id
			imageonlylist.append(str(channel.id))
			print(imageonlylist)
			channelfile = open("channellist.txt","a")
			channelfile.writelines(["%s\n" % channelid])
			channelfile.close()
			await message.message.delete()

	#repeated code for lower level if statement
	else:
		def checkauthor(m2):
			return message.author ==m2.author
		await channel.send("Image only enabled")
		channelid = channel.id
		imageonlylist.append(str(channel.id))
		channelfile = open("channellist.txt","w")
		channelfile.writelines(["%s\n" % item  for item in imageonlylist])
		channelfile.close()
		await message.message.delete()
		
		#channelfile = open("channellist.txt","w+")
		#await client.get_channel(imageonlychannels[0]).send("testing saving")
		
@client.event
async def on_message(message):
	await client.process_commands(message)
	channel = message.channel
	global imageonlylist
	if (not message.author.bot):
		if(str(channel.id) in imageonlylist and message.author != client.user):
			if (message.attachments):
				pass
			elif(len(message.content) > 8):
				if(message.content[0:8] == 'https://'):
					pass
				else:
					try:
						await message.delete()
					#message was already deleted
					except discord.errors.NotFound:
						pass
			else:
				try:
					await message.delete()
				#message was already deleted
				except discord.errors.NotFound:
					pass
		

async def list_servers():
	await client.wait_until_ready()
	while not client.is_closed:
		print("Current servers:")
		for server in client.servers:
			print(server.name)
		await asyncio.sleep(600)

try:
	client.loop.create_task(list_servers())
	client.run(TOKEN)
except:
	channelfile = open("channellist.txt","w")
	channelfile.writelines(["%s\n" % item  for item in imageonlylist])
	channelfile.close()