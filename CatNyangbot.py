import discord, asyncio, os
from discord.ext import commands
import sys
import random
import sqlite3
import datetime
import koreanbots
import asyncio, discord, time
from game import *
from user import *
import time
import requests

rmy=random.randint(1000,50000)
a=rmy
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

game=discord.Game("냥냥!")
bot=commands.Bot(command_prefix="C:", status=discord.Status.online, activity=game)

@bot.command(aliases=['안녕하세요','hi','hello'])
async def 안녕(ctx):
    await ctx.send(f'{ctx.author.mention}님 안녕하세요!')

@bot.command(aliases=['주사위'])
async def 주사위게임(ctx):
    result, _color, bot1, bot2, user1, user2, a, b = dice()
    embed = discord.Embed(title = "주사위 게임 결과", description = None, color = _color)
    embed.add_field(name = "CatNyangBot의 숫자 " + bot1 + "+" + bot2, value = ":game_die: " + a, inline = False)
    embed.add_field(name = ctx.author.name+"의 숫자 " + user1 + "+" + user2, value = ":game_die: " + b, inline = False)
    embed.set_footer(text="결과: " + result)
    await ctx.send(embed=embed)

@bot.event
async def on_ready() :
    print(f'봇 활성화! : {bot.user.name}!')
    game=discord.Game("냥냥냥! 명령어 C:")
    await bot.change_presence(status = discord.Status.online, activity = game)

@bot.command(aliases=['도움'])
async def 도움말(ctx):
    embed = discord.Embed(title= "도움말!", description = "__CatNyangbot__\n==도움말!==\n사용가능한 명령어!:", color = 0xffc0cb)
    embed.add_field(name=bot.command_prefix + "도움말", value="도움말을 봅니다", inline=False)
    embed.add_field(name=bot.command_prefix + "주사위", value="주사위를 굴려 봇과 대결합니다", inline=False)
    embed.add_field(name=bot.command_prefix + "회원가입", value="각종 컨텐츠를 즐기기 위한 회원가입을 합니다", inline=False)
    embed.add_field(name=bot.command_prefix + "내정보", value="자신의 정보를 확인합니다", inline=False)
    embed.add_field(name=bot.command_prefix + "정보 [대상]", value="멘션한 [대상]의 정보를 확인합니다", inline=False)
    embed.add_field(name=bot.command_prefix + "송금 [대상] [돈]", value="멘션한 [대상]에게 [돈]을 보냅니다", inline=False)
    embed.add_field(name=bot.command_prefix + "도박 [돈]", value="[돈]을 걸어 도박을 합니다. 올인도 가능합니다 (올인은 4배,배팅은 2배)", inline=False)
    embed.add_field(name=bot.command_prefix + "돈받기 신청", value="[돈]을 받습니다. 1000원에서 50000원사이의 돈을 랜덤지급합니다", inline=False)
    embed.add_field(name=bot.command_prefix + "랭킹", value="유저 레벨 랭킹을 보여줍니다", inline=False)
    embed.add_field(name=bot.command_prefix + "도박랭킹", value="유저 도박 랭킹을 보여줍니다", inline=False)
    embed.set_footer(text = f"{ctx.message.author.name} | Cat Nyang#2483", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = embed)

@bot.command()
async def 돈받기(ctx, money):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    win = gamble()
    result = ""
    betting = 0
    _color = 0x000000
    ct=0
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        cur_money = getMoney(ctx.author.name, userRow)
        if money == "신청":
            betting = cur_money
            #if ct == 0:
            if getMoney(ctx.author.name, userRow) == 0:
                if win:
                    result = "성공"
                    _color = 0x00ff56
                    print(result)
                    modifyMoney(ctx.author.name, userRow, int(a))
                    betting = a
                    print(a)
                else:
                    betting = 0
                    result = "실패"
                    _color = 0xFF0000
                    print(result)
                    modifyMoney(ctx.author.name, userRow, int(0))
                    await ctx.send(f"{ctx.author.mention}님 돈받기 요청에 실패했습니다! 다시 시도해보세요!")

                embed = discord.Embed(title="돈받기 결과", description=result, color=_color)
                embed.add_field(name="받은금액", value=betting, inline=False)
                embed.add_field(name="현재 자산", value=getMoney(ctx.author.name, userRow), inline=False)
                await ctx.send(embed=embed)
            else:
                betting = 0
                result = "실패"
                _color = 0xFF0000
                print(result)
                modifyMoney(ctx.author.name, userRow, int(0))
                await ctx.send(f"{ctx.author.mention}님 돈받기 요청에 실패했습니다! 소유 자산이 0원이 아닙니다!")
            #else:
                #betting = 0
                #result = "실패"
                #_color = 0xFF0000
                #print(result)
                #modifyMoney(ctx.author.name, userRow, int(0))
                #await ctx.send(f"{ctx.author.mention}님 돈받기 요청에 실패했습니다! 명령어 쿨타임 중입니다!.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        await ctx.send("돈받기 신청은 회원가입 후 이용 가능합니다!")
print("------------------------------\n")

@bot.command()
async def 도박(ctx, money):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    win = gamble()
    result = ""
    betting = 0
    _color = 0x000000
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        cur_money = getMoney(ctx.author.name, userRow)
        if money == "올인":
            betting = cur_money
            if win:
                result = "성공"
                _color = 0x00ff56
                print(result)

                modifyMoney(ctx.author.name, userRow, int(3 * betting))

            else:
                result = "실패"
                _color = 0xFF0000
                print(result)

                modifyMoney(ctx.author.name, userRow, -int(betting))
                addLoss(ctx.author.name, userRow, int(betting))

            embed = discord.Embed(title="도박 결과", description=result, color=_color)
            embed.add_field(name="배팅금액", value=betting, inline=False)
            embed.add_field(name="현재 자산", value=getMoney(ctx.author.name, userRow), inline=False)

            await ctx.send(embed=embed)

        elif int(money) >= 10:
            if cur_money >= int(money):
                betting = int(money)
                print("배팅금액: ", betting)
                print("")

                if win:
                    result = "성공"
                    _color = 0x00ff56
                    print(result)

                    modifyMoney(ctx.author.name, userRow, int(2 * betting))

                else:
                    result = "실패"
                    _color = 0xFF0000
                    print(result)

                    modifyMoney(ctx.author.name, userRow, -int(betting))
                    addLoss(ctx.author.name, userRow, int(betting))

                embed = discord.Embed(title="도박 결과", description=result, color=_color)
                embed.add_field(name="배팅금액", value=betting, inline=False)
                embed.add_field(name="현재 자산", value=getMoney(ctx.author.name, userRow), inline=False)

                await ctx.send(embed=embed)

            else:
                print("돈이 부족합니다.")
                print("배팅금액: ", money, " | 현재자산: ", cur_money)
                await ctx.send("돈이 부족합니다. 현재자산: " + str(cur_money))
        else:
            print("배팅금액", money, "가 10보다 작습니다.")
            await ctx.send("10원 이상만 배팅 가능합니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        await ctx.send("도박은 회원가입 후 이용 가능합니다.")

    print("------------------------------\n")

@bot.command()
async def 랭킹(ctx):
    rank = ranking()
    embed = discord.Embed(title = "레벨 랭킹", description = None, color = 0x4A44FF)

    for i in range(0,len(rank)):
        if i%2 == 0:
            name = rank[i]
            lvl = rank[i+1]
            embed.add_field(name = str(int(i/2+1))+"위 "+name, value ="레벨: "+str(lvl), inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def 도박랭킹(ctx):
    await ctx.send("아직 미완성인 명령어입니다!")

@bot.command()
async def 회원가입(ctx):
    print("회원가입이 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        print("------------------------------\n")
        await ctx.send("이미 가입하셨습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("")

        Signup(ctx.author.name, ctx.author.id)

        print("회원가입이 완료되었습니다.")
        print("------------------------------\n")
        await ctx.send("회원가입이 완료되었습니다.")

@bot.command()
async def 탈퇴(ctx):
    print("탈퇴가 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        DeleteAccount(userRow)
        print("탈퇴가 완료되었습니다.")
        print("------------------------------\n")

        await ctx.send("탈퇴가 완료되었습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")

        await ctx.send("등록되지 않은 사용자입니다.")

@bot.command()
async def 내정보(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)

    if not userExistance:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 자신의 정보를 확인할 수 있습니다.")
    else:
        level, exp, money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        expToUP = level*level + 6*level
        boxes = int(exp/expToUP*20)
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "순위", value = str(rank) + "/" + str(userNum))
        embed.add_field(name = "XP: " + str(exp) + "/" + str(expToUP), value = boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.add_field(name = "보유 자산", value = money, inline = False)
        embed.add_field(name = "도박으로 날린 돈", value = loss, inline = False)

        await ctx.send(embed=embed)

@bot.command()
async def 정보(ctx, user: discord.User):
    userExistance, userRow = checkUser(user.name, user.id)

    if not userExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name  + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        level, exp, money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = user.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "경험치", value = str(exp) + "/" + str(level*level + 6*level))
        embed.add_field(name = "순위", value = str(rank) + "/" + str(userNum))
        embed.add_field(name = "보유 자산", value = money, inline = False)
        embed.add_field(name = "도박으로 날린 돈", value = loss, inline = False)

        await ctx.send(embed=embed)


@bot.command()
async def 송금(ctx, user: discord.User, money):
    print("송금이 가능한지 확인합니다.")
    senderExistance, senderRow = checkUser(ctx.author.name, ctx.author.id)
    receiverExistance, receiverRow = checkUser(user.name, user.id)

    if not senderExistance:
        print("DB에서", ctx.author.name, "을 찾을수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 송금이 가능합니다.")
    elif not receiverExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        print("송금하려는 돈: ", money)

        s_money = getMoney(ctx.author.name, senderRow)
        r_money = getMoney(user.name, receiverRow)

        if s_money >= int(money) and int(money) != 0:
            print("돈이 충분하므로 송금을 진행합니다.")
            print("")

            remit(ctx.author.name, senderRow, user.name, receiverRow, money)

            print("송금이 완료되었습니다. 결과를 전송합니다.")

            embed = discord.Embed(title="송금 완료", description="송금된 돈: " + money, color=0x77ff00)
            embed.add_field(name="보낸 사람: " + ctx.author.name,
                            value="현재 자산: " + str(getMoney(ctx.author.name, senderRow)))
            embed.add_field(name="→", value=":moneybag:")
            embed.add_field(name="받은 사람: " + user.name, value="현재 자산: " + str(getMoney(user.name, receiverRow)))

            await ctx.send(embed=embed)
        elif int(money) == 0:
            await ctx.send("0원을 보낼 필요는 없죠")
        else:
            print("돈이 충분하지 않습니다.")
            print("송금하려는 돈: ", money)
            print("현재 자산: ", s_money)
            await ctx.send("돈이 충분하지 않습니다. 현재 자산: " + str(s_money))

        print("------------------------------\n")

@bot.command()
async def reset(ctx):
    resetData()

@bot.command()
async def add(ctx, money):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    addMoney(row, int(money))
    print("money")

@bot.command()
async def exp(ctx, exp):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    addExp(row, int(exp))
    print("exp")

@bot.command()
async def lvl(ctx, lvl):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    adjustlvl(row, int(lvl))
    print("lvl")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "!reset":
        await bot.process_commands(message)
        return
    else:
        userExistance, userRow = checkUser(message.author.name, message.author.id)
        channel = message.channel
        if userExistance:
            levelUp, lvl = levelupCheck(userRow)
            if levelUp:
                print(message.author, "가 레벨업 했습니다")
                print("")
                embed = discord.Embed(title = "레벨업", description = None, color = 0x00A260)
                embed.set_footer(text = message.author.name + "이 " + str(lvl) + "레벨 달성!")
                await channel.send(embed=embed)
            else:
                modifyExp(userRow, 1)
                print("------------------------------\n")

        await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다. C:도움말 을 입력하여 명령어를 확인하세요.")

bot.run("OTE0MTY4NTM0NTg0Njg0NTQ1.YaJHyw.U56TsZ0ijcWWB1PD19pvPIsa2Xk")