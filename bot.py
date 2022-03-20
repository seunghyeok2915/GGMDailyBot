from distutils.log import error
from errno import errorcode
from operator import truediv
from pydoc import cli
import discord
import traceback
from discord.ext import commands
import datetime
import os 


client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("!도움말 "))
    return

@client.event
async def on_message(message):
    message_content = message.content 
    badList = ["씨발", "시발", "좆", "개새끼", "발련","새끼","ㅣ발","l발","I발","씨빨","tlqkf","원숭이","병신","꺼져","ㅄ","ㅂㅅ","ㅅㅂ","ㅆㅃ","ㅆㅂ","fuck","Fuck","장애","미친년","미친놈","또라이","쉬불","쒸불","FUCK","개놈","개년","씨바","애미","느금","원숭","싸발","개놈","썅"]
    for i in badList: 
        bad = message_content.find(i) 
        if bad >= 0:
            await message.delete() 
            channel = await message.author.create_dm()
            
    covid19List = ["기침", "두통", "재채기","콧물","아파","어지러움","아픔","콜록"]
    for i in covid19List: 
        covid19 = message_content.find(i) 
        if covid19 >= 0:
            channel = await message.author.create_dm()
            await channel.send("너는 코로나 입니다. 증상 : {}".format(i))
            await message.channel.send("!!!!!!!!코로나 감지!!!!!!!")

    minsooList = ["민수", "일줘"]
    for i in minsooList: 
        minsoo = message_content.find(i) 
        if minsoo >= 0:
            await message.channel.send("야 기획! 일 주라고! 엉?")

    await client.process_commands(message) # 메세지 중 명령어가 있을 경우 처리해주는 코드

@client.command()
async def 도움말(ctx):
    embed = discord.Embed(title="도움말", description=f"명령어들", color=0x62c1cc)
    embed.add_field(name="!정보등록", value=f"형식  :  `{client.command_prefix}정보등록 이메일 비밀번호 팀번호`\n 정보는 OAuth 2.0 토큰을 가져올 때만 사용되며 다른 용도로는 사용되지 않고 저장되지 않습니다.", inline=False)
    embed.add_field(name="!일간", value=f"형식  :  `{client.command_prefix}일간 내용`", inline=False)
    embed.add_field(name="갱스터햄스터", value=f"팀번호  :  `1`", inline=True)
    embed.add_field(name="고금도 찌르호크", value=f"팀번호  :  `2`", inline=True)
    embed.add_field(name="Detroy Duck", value=f"팀번호  :  `3`", inline=True)
    embed.add_field(name="Semicolon", value=f"팀번호  :  `4`", inline=True)
    embed.add_field(name="GGM-Like", value=f"팀번호  :  `5`", inline=True)
    embed.add_field(name="REG", value=f"팀번호  :  `6`", inline=True)
    embed.add_field(name="불협화웅", value=f"팀번호  :  `7`", inline=True)
    embed.add_field(name="핫_페럿", value=f"팀번호  :  `8`", inline=True)
    embed.add_field(name="나쁜놈들", value=f"팀번호  :  `9`", inline=True)
    embed.add_field(name="214", value=f"팀번호  :  `10`", inline=True)
    embed.add_field(name="가보작", value=f"팀번호  :  `11`", inline=True)
    embed.add_field(name="BSS", value=f"팀번호  :  `12`", inline=True)
    embed.add_field(name="네트워크PC", value=f"팀번호  :  `13`", inline=True)
    await ctx.send(embed = embed)
    return

@client.command()
@commands.dm_only()
async def 정보등록(ctx,email=None,password=None,teamNum=None):
    #입력되지 않은 요소가 있을 경우
    if email==None or password==None or teamNum==None:
        embed = discord.Embed(title="정보 등록 실패", description=f"모든 값이 들어오지 않았습니다.\n다시 한번 입력해주시기 바랍니다.\n> 형식  :  `정보등록 이메일 비밀번호 팀번호`\n> 예시 : `정보등록 seung@gmail.com pass123 12`\n> 입력값 : `정보등록 {email} {password} {teamNum}`", color=0x62c1cc)
        await ctx.send(embed = embed)
        return
    output = os.popen(f'E:\바탕화면\SeunghyeokBot\GondrProgram\GondrTestPost.exe SaveToken {email} {password}').read()
    print(output)
    if output == "BAD":
        embed = discord.Embed(title="실패하였습니다.", description=f"아이디 또는 비밀번호가 틀립니다.", color=0x62c1cc)
        await ctx.send(embed = embed)
        return

    embed = discord.Embed(title="정보가 저장되었습니다.", description=f"당신의 토큰 : \n`{output}`\n 팀번호 : `{teamNum}`", color=0x62c1cc)
    f = open(f"E:/바탕화면/SeunghyeokBot/UserInfos/{ctx.author}.txt", 'w')
    data = "{} {}".format(output,teamNum)
    f.write(data)
    f.close()
    await ctx.send(embed = embed)
    return

@client.command()
async def 일간(ctx, *args):

    if len(args) <= 0:
        await ctx.send("내용이 없습니다.")
        return
    try:
        f = open(f"E:/바탕화면/SeunghyeokBot/UserInfos/{ctx.author}.txt", 'r')
        data = f.readline()
        f.close()
        path = f'E:\바탕화면\SeunghyeokBot\GondrProgram\GondrTestPost.exe WriteDaily {data} '
        for item in args:
            path += item
            path += " "
        print(path)
        output = os.popen(path).read()
        embed = discord.Embed(title="메시지", description=f"`{output}`", color=0x62c1cc)
    except FileNotFoundError as e:
        embed = discord.Embed(title="정보등록 에러", description=f"정보등록을 해주세요.", color=0x62c1cc)
    await ctx.send(embed = embed)
    return
    

@client.event
async def on_command_error(ctx, error):
    tb = traceback.format_exception(type(error), error, error.__traceback__)
    err = [line.rstrip() for line in tb]
    errstr = '\n'.join(err)
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send('개인정보 보호를 위해 봇과 개인메시지로 정보등록을 해주시기 바랍니다.')
    else:
        print(errstr)

client.run('OTUzODI1NDMyOTMzOTA0NDY1.YjKNKA.y-dgPftLoUcTnHYAQmx3NWLOheY')