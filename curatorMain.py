import discord
import random
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("s!", "!", "s! ")

client = Bot(command_prefix=BOT_PREFIX)

#list of channel ids
def get_channel_list():
	channelfile = open("channellist.txt","r")
	imageonlychannels = channelfile.read().splitlines()
	channelfile.close()
	return imageonlychannels

@client.event
async def on_ready():
	#prints out the bot used to see if its running
	print(f'Logged in as {client.user}')

#set the channel to image only
@client.command('imageonly')
async def imageonly(message):
	channel = message.channel
	imageonlychannels = get_channel_list()
	if(imageonlychannels):
		if(str(channel.id) in imageonlychannels):
			def checkauthor(m2):
				return message.author ==m2.author
			await channel.send("Image only disabled")
			channelfile = open("channellist.txt","r")
			tempchannellist=channelfile.read().splitlines()
			channelfile.close()
			tempchannellist.remove(str(channel.id))
			channelfile=open("channellist.txt", "w")
			if(len(tempchannellist)==0):
				pass
			else:
				channelfile.writelines(["%s\n" % item  for item in tempchannellist])
			channelfile.close()
			imageonlychannels=tempchannellist
			await message.message.delete()
		else:
			def checkauthor(m2):
				return message.author ==m2.author
			await channel.send("Image only enabled")
			channelid = channel.id
			imageonlychannels.append(channelid)
			channelfile = open("channellist.txt","w")
			channelfile.writelines(["%s\n" % item  for item in imageonlychannels])
			channelfile.close()

			await message.message.delete()
			#channelfile = open("channellist.txt","w+")
			#await client.get_channel(imageonlychannels[0]).send("testing saving")
			channelid = channel.id
			imageonlychannels.append(channelid)
			channelfile = open("channellist.txt","w")
			channelfile.writelines(["%s\n" % item  for item in imageonlychannels])
			channelfile.close()
	#repeated code for lower level if statement
	else:
		def checkauthor(m2):
			return message.author ==m2.author
		await channel.send("Image only enabled")
		channelid = channel.id
		imageonlychannels.append(channelid)
		channelfile = open("channellist.txt","w")
		channelfile.writelines(["%s\n" % item  for item in imageonlychannels])
		channelfile.close()
		await message.message.delete()
		#channelfile = open("channellist.txt","w+")
		#await client.get_channel(imageonlychannels[0]).send("testing saving")
		
#check if a message is sent in image only channel and delete it if it is
@client.event
async def on_message(message):
	await client.process_commands(message)
	channel = message.channel
	imageonlychannels = get_channel_list()
	if(str(channel.id) in imageonlychannels and message.author != client.user):
		if (message.attachments):
			pass
		elif(len(message.content) > 8):
			if(message.content[0:8] == 'https://'):
				pass
			else:
				await message.delete()
		else:
			await message.delete()
		


client.run(TOKEN)
#client.close()