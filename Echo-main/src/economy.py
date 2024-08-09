"""
Main economy game
See more extensions (farming, crafting etc)
in extensions.py
"""

from utilities import *
from eco_support import *


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Discord bot command for inventory
    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, user: commands.MemberConverter = None):
        try:
            if user is None:
                user_id = ctx.author.id
                inventory = get_user_inventory(user_id)
                item_counts = Counter(inventory)
                embed_title = f"{ctx.author.display_name}'s Inventory"
            else:
                user_id = user.id
                inventory = get_user_inventory(user_id)
                item_counts = Counter(inventory)
                embed_title = f"{user.display_name}'s Inventory"

            embed = discord.Embed(title=embed_title, color=discord.Colour.blue())
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            for item, count in item_counts.items():
                embed.add_field(name=item, value=f"Count: {count}", inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            print(f"Error in inventory command: {e}")

    
    # Command to give money to a user (TO REMOVE DO /GIVE <USER> -<amount>)
    @commands.command()
    @commands.check(is_admin) # Only one user can do this (put the id in config.json)
    async def give(self, ctx, user: commands.MemberConverter, amount: int):
        update_user_balance(user.id, amount)
        embed = discord.Embed(
            title="Credits Given!",
            description=f"Admin {ctx.author.display_name} has given **{amount} credits** to {user.display_name}.",
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

        # Send the embed
        await ctx.send(embed=embed)

    # Error handling for the give command
    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            # Create an embed for the error message with red color
            embed = discord.Embed(
                title="Permission Denied",
                description=f"{ctx.author.mention}, You don't have permission to use this command.",
                color=embed_error
            )

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
            return


    # Command to reset the cooldowns file
    # so if you run this all current cooldowns are wiped
    # good for debugging (and cheating but thats not nice)
    @commands.command()
    @commands.check(is_admin) # Only one user can do this (put the id in config.json)
    async def cool_bypass(self, ctx):
        conn = sqlite3.connect('src/databases/cooldowns.db')
        cursor = conn.cursor()

        # Assuming your cooldowns are stored in a table called 'cooldowns'
        cursor.execute("DELETE FROM cooldowns WHERE type != 'interest' AND type != 'farming'")
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="Cooldowns Wiped",
            description=f"Admin {ctx.author.display_name} has just wiped all cooldowns! (except for interest on banks and farming)",
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

        # Send the embed
        await ctx.send(embed=embed)

    # Error handling for the give command
    @cool_bypass.error
    async def cool_bypass_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            # Create an embed for the error message with red color
            embed = discord.Embed(
                title="Permission Denied",
                description=f"{ctx.author.mention}, You don't have permission to use this command.",
                color=embed_error
            )

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
            return


    # Command to remove items from a users inventory
    @commands.command()
    @commands.check(is_admin) # Only one user can do this (put the id in config.json)
    async def remove_item(self, ctx, user: commands.MemberConverter, item: str, amount=1):
        embed = discord.Embed(
            title="Item Removal success",
            description=f"{ctx.author.mention}, I have successfully removed **{amount} {item}'s from {user.mention}'s** inventory.",
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)
        
        for i in range(0, amount):
            remove_item_from_inventory(user.id, item)    

    # Error handling for the give command
    @remove_item.error
    async def remove_item_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            # Create an embed for the error message with red color
            embed = discord.Embed(
                title="Permission Denied",
                description=f"{ctx.author.mention}, You don't have permission to use this command.",
                color=embed_error
            )

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
            return


    @commands.command()
    @commands.check(is_admin)
    async def add_item(self, ctx, user: commands.MemberConverter, item: str, amount=1):
        embed = discord.Embed(
            title="Item Add success",
            description=f"{ctx.author.mention}, I have successfully Added **{amount} {item}'s to {user.mention}'s** inventory.",
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)

        for i in range(0, amount):
            add_item_to_inventory(user.id, item)

    # Error handling for the give command
    @add_item.error
    async def add_item_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            # Create an embed for the error message with red color
            embed = discord.Embed(
                title="Permission Denied",
                description=f"{ctx.author.mention}, You don't have permission to use this command.",
                color=embed_error
            )

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
            return

    # pay another user money
    @commands.command()
    async def pay(self, ctx, user: commands.MemberConverter=None, amount: int=None): # type: ignore
        if amount is None or amount <= 0:
            embed = discord.Embed(
                title="Invalid Amount",
                description=f"{ctx.author.mention}, Please specify an amount to pay. Usage: `{prefix}pay <@user> <amount>`",
                color=embed_error
            )

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return
        
        if user is None:
            embed = discord.Embed(
                title="Not a user",
                description=f"{ctx.author.mention}, Please specify a user. Usage: `{prefix}pay <@user> <amount>`",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return         

        payer_id = str(ctx.author.id)
        user_id = str(user.id)

        if payer_id == user_id: # check if they tried to pay themself
            embed = discord.Embed(
                title="Payment Error",
                description=f"{ctx.author.mention}, Yeah nah you cant pay yourself.",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
            return

        if amount > get_user_balance(payer_id): # if they dont have enough money
            embed = discord.Embed(
                title="Broke  :sob:",
                description=f"{ctx.author.mention}, go grind the bot ",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        # Assuming update_user_balance and get_user_balance are defined elsewhere
        update_user_balance(payer_id, -amount) # reduce the mount they paid
        update_user_balance(user_id, amount) # add it to the reciver

        embed = discord.Embed(
            title="Payment Successful",
            description=f"{ctx.author.mention}, 💵 You just paid {user.display_name} **{amount} credits**!",
            color=discord.Color.green()
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

        await ctx.send(embed=embed)


    @commands.command()
    async def buy(self, ctx, item_name: str = import discord
from discord.ext import commands)

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def buy(self, ctx, item_name: str = None, amount: int = 1):
        try:
            if item_name is None:
                embed = discord.Embed                    title="Incorrect Buy Usage",
                    description=f"{ctx.author.mention}, Please specify an item name. Usage: `{ctx.prefix}buy <item_name> <amount>`"
                )
                await ctx.send(embed=embed)
                return

            # Your logic for handling the purchase goes here

        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred: {str(e)}"
            )
            await ctx.send(embed=embed)

# Assuming you have a bot instance
bot = commands.Bot(command_prefix="
, amount: int = 1):
        try:
            if item_name is None:
                embed = discord.Embed(
                    title="Incorrect Buy Usage",
                    description=f"{ctx.author.mention}, Please specify an item name. Usage: `{prefix}buy <item_name> <amount>`",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                await ctx.send(embed=embed)
                return

            item_name = item_name.lower()  # Normalize the item name to lowercase

            # Check if the item is in the shop
            if item_name not in shop_items:
                embed = discord.Embed(
                    title="Item Not Found",
                    description=f"{ctx.author.mention}, Item not found in the shop.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                await ctx.send(embed=embed)
                return

            user = ctx.author

            item_cost = shop_items[item_name]['cost']  # Get the item cost

            user_balance = get_user_balance(user.id)  # Get the user's balance

            total = amount * item_cost

            if user_balance < total:  # Check if the user has enough balance for the total cost
                embed = discord.Embed(
                    title="Insufficient Funds",
                    description=f"{ctx.author.mention}, You don't have enough credits to buy this item.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                await ctx.send(embed=embed)
                return

            # Deduct the total cost from the user's balance and add the items to their inventory
            update_user_balance(user.id, -total)

            for _ in range(amount):
                add_item_to_inventory(user.id, item_name)

            # Log the purchase
            log_purchase(user.id, amount, user.name, item_name, item_cost)

            embed = discord.Embed(
                title="Purchase Successful",
                description=f"{ctx.author.mention}, You have successfully bought **{item_name}** for **{total} credits**.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            await ctx.send(embed=embed)

        except Exception as e:
            print(f"An error occurred: {e}")
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred while processing your request. Please try again later.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            await ctx.send(embed=embed)


    @commands.command()
    async def dig(self, ctx):
        user_id = ctx.author.id

        # Check if the user has a 'shovel' in their inventory
        user_inventory = get_user_inventory(user_id)
        if 'shovel' not in user_inventory:
            embed = discord.Embed(
                title="You need a shovel...",
                description=f"{ctx.author.mention}, digging with your hands? We arn't animals, **go buy or find a shovel**.",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        # check for a cooldown
        if not can_dig(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description=f"{ctx.author.mention}, You're on a **15min break** buddy 🤫 don't chat to me.",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        # Simulate winning an item based on chances
        chosen_item = random.choices(list(cosmetics_items.keys()), weights=[item["chance"] for item in cosmetics_items.values()], k=1)[0]

        # Get the details of the won item
        won_item = cosmetics_items[chosen_item]

        # Add the won item to the user's inventory
        add_item_to_inventory(user_id, chosen_item)

        embed = discord.Embed(
            title=f"{ctx.author.display_name}, Item Found",
            description=f"🎉 You found: **{won_item['name']}**! 🎉 Check your inventory with `{prefix}inventory`.",
            color=discord.Color.green()
        )
       
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
       
        await ctx.send(embed=embed)

        amount = random.randint(1000, 1600) # random amount of money

        update_user_balance(ctx.author.id, amount) # update balance

        embed = discord.Embed(
            title=f"{ctx.author.display_name}, Credits Found",
            description=f"💵 You found: **{amount} credits**! Your new balance is: **{get_user_balance(ctx.author.id)} credits**.",
            color=discord.Color.green()
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)
        
        update_last_action_time(user_id, "dig")

    @commands.command()
    async def hunt(self, ctx):
        user_id = ctx.author.id

        # Check if the user has a 'bow' in their inventory
        # if not dont let them run the hunt command
        user_inventory = get_user_inventory(user_id)
        if 'bow' not in user_inventory:
            embed = discord.Embed(
                title="Find a bow first lol",
                description=f"{ctx.author.mention}, You need a **bow** too shoot arrows... **Go buy or find one.**",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        # check if they can hunt (not on cooldown)
        if not can_hunt(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description=f"{ctx.author.mention}, You're on a **15min break. Go away**.",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        # Simulate winning an item based on chances
        chosen_item = random.choices(list(cosmetics_items.keys()), weights=[item["chance"] for item in cosmetics_items.values()], k=1)[0]

        # Get the details of the won item
        won_item = cosmetics_items[chosen_item]

        # Add the won item to the user's inventory
        add_item_to_inventory(user_id, chosen_item)

        embed = discord.Embed(
            title=f"{ctx.author.display_name}, Item Found",
            description=f"🎉 You found: **{won_item['name']}**! 🎉 Check your inventory with `{prefix}inventory`",
            color=discord.Color.green()
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)

        amount = random.randint(600, 1300) # random money amount

        update_user_balance(ctx.author.id, amount) # update balance

        embed = discord.Embed(
            title=f"{ctx.author.display_name}, Credits Found",
            description=f"💵 You found: **{amount} credits**! Your new balance is: **{get_user_balance(ctx.author.id)} credits**.",
            color=discord.Color.green()
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)

        update_last_action_time(user_id, "hunt")


    @commands.command(aliases=['scavenge', 'scarp', 'scav', 'scap', 'srcap'])
    async def scrap(self, ctx):
        try:
            user_id = ctx.author.id

            if not can_scavenge(user_id):
                embed = discord.Embed(
                    title="Cooldown Active",
                    description=f"{ctx.author.mention}, **5min cooldown** lmao.",
                    color=embed_error
                )
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            # Simulate winning an item based on chances
            chosen_item = random.choices(list(cosmetics_items.keys()), weights=[item["chance"] for item in cosmetics_items.values()], k=1)[0]
            
            add_item_to_inventory(ctx.author.id, chosen_item)
            
            # Get the details of the won item
            won_item = cosmetics_items[chosen_item]


            embed = discord.Embed(
                title=f"{ctx.author.display_name}, Item Found",
                description=f"🎉 You found: **{won_item['name']}**. 🎉 Check your inventory with `{prefix}inventory`",
                color=discord.Color.green()
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)

            amount = random.randint(400, 800)

            update_user_balance(ctx.author.id, amount)

            embed = discord.Embed(
                title=f"{ctx.author.display_name}, Credits Found",
                description=f"💵 You found: **{amount} Credits**! Your new balance is: **{get_user_balance(ctx.author.id)} credits**.",
                color=discord.Color.green()
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)

            update_last_action_time(user_id, "scavenge")
        except Exception as e:
            print(e)


    @commands.command()
    async def beg(self, ctx):
        user_id = ctx.author.id

        if not can_beg(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description=f"{ctx.author.mention}, You begged in the past **30s. Wait the cooldown**.",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        amount = random.randint(100, 200)

        update_user_balance(user_id, amount)

        embed = discord.Embed(
            title=f"{ctx.author.display_name} is begging",
            description=f'💵 A kind man gave you **{amount} credits**.',
            color=discord.Color.green()
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)

        update_last_action_time(user_id, "beg")


    @commands.command()
    async def daily(self, ctx):
        user_id = ctx.author.id

        try:
            if not can_claim_daily(user_id):
                embed = discord.Embed(
                    title="Daily Reward Already Claimed",
                    description=f"{ctx.author.mention}, Nah its called **'daily' for a reason**. What are you tryna do.",
                    color=embed_error
                )
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            # daily_reward is defined in eco_support.py
            update_user_balance(user_id, int(daily_reward))
            
            embed = discord.Embed(
                title="Daily Reward Claimed",
                description=f'{ctx.author.mention}, You have claimed your daily reward of 💵 **{daily_reward} credits**!',
                color=discord.Color.green()
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            
            set_last_claim_time(user_id)
        except Exception as e:
            print(e)


    # probably the most shit code i have ever wrote in my life but it works - Mal - dev1
    @commands.command()
    async def sell(self, ctx, item_id: str=None, amount: int=1):
        user_id = ctx.author.id
        item_id = item_id # this fixes cannot access local variable 'item_name' where it is not associated with a value somehow
        user_inventory = get_user_inventory(user_id)

        try:
            if item_id is None:
                embed = discord.Embed(
                    title="Incorrect Usage",
                    description=f"{ctx.author.mention}, Incorrect usage. Please use: `{prefix}sell <item> <amount>`",
                    color=embed_error
                )
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            if item_id not in user_inventory: # check if they own the item
                embed = discord.Embed(
                    title="Item Not Found",
                    description=f"{ctx.author.mention}, You don't have this in your inventory.",
                    color=embed_error
                )
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            item_count = sum(item == item_id for item in user_inventory)
            if item_count < amount:
                embed = discord.Embed(
                    title=f"Insufficient {item_id}",
                    description=f"{ctx.author.mention}, You only have {item_count} {item_id}'s, which is less than the requested amount of {amount}.",
                    color=embed_error
                )
                await ctx.send(embed=embed)
                return
            
            item_id = item_id.lower() # make it lower to prevent stuff like LeG.SwoRD 
            
            # I replaced the old algorithm that used the 'for i in range(amount)' with this
            # (its faster and just overall better)
            user = await self.bot.fetch_user(ctx.author.id) 
            
            special_shop_items = ["gold", "silver"]

            if item_id in special_shop_items: # for shop items
                item_info = shop_items[item_id]
                item_sell_price = item_info["cost"] * amount
            else:
                item_info = combined_items[item_id]
                item_sell_price = item_info["sell"] * amount

            if item_id not in combined_items and item_id not in shop_items:
                embed = discord.Embed(
                    title="Invalid Item ID",
                    description=f"{ctx.author.mention}, That Item ID is invalid/does not exist.",
                    color=embed_error
                )
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                await ctx.send(embed=embed)
                return
            
            # Update user's balance
            update_user_balance(user_id, item_sell_price)

            for i in range(0, amount):
                # Remove the item from the user's inventory
                remove_item_from_inventory(user_id, item_id)
            
            log_purchase(user_id, 0 ,user.name , item_id, item_sell_price)

            embed = discord.Embed(
                title="Item Sold",
                description=f"{ctx.author.mention}, You sold **{amount} {item_id} for 💵 {item_sell_price} credits**. Your new balance is: 💵 **{get_user_balance(user_id)} credits**!",
                color=discord.Color.green()
            )

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
        except Exception as e:
            print(e)


    @commands.command()
    async def deposit(self, ctx, amount=None):
        if amount == 'all' or amount == 'max':  # deposit as much as possible
            amount = get_user_balance(ctx.author.id)
        elif amount is None:
            embed = discord.Embed(
                title="Incorrect deposit usage!",
                description=f"{ctx.author.mention}, Incorrect deposit usage, please use: `{prefix}deposit <amount>`",
                color=embed_error
            )

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
            return
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    title="Invalid deposit amount",
                    description=f"{ctx.author.mention}, Please enter a valid amount.",
                    color=embed_error
                )

                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                await ctx.send(embed=embed)
                return

        if amount <= 0 or amount > get_user_balance(ctx.author.id):
            embed = discord.Embed(
                title="Invalid deposit amount",
                description=f"{ctx.author.mention}, Please enter a valid amount.",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
            return

        remaining_space = max_bank_size - get_user_bank_balance(ctx.author.id)
        amount_to_deposit = min(amount, remaining_space)

        update_user_balance(ctx.author.id, -amount_to_deposit)
        update_bank_balance(ctx.author.id, amount_to_deposit)

        # Embed the message
        embed = discord.Embed(
            title="Deposit Successful",
            description=f'{ctx.author.mention}, 💵 **{amount_to_deposit} credits** has been deposited to your sussy account.',
            color=discord.Color.green()
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)


    @commands.command()
    async def withdraw(self, ctx, amount=None):
        if amount is None: # if they didnt enter an amount
            embed = discord.Embed(
                title="Incorrect withdraw usage!",
                description=f'{ctx.author.mention}, Incorrect withdraw usage. Please use: `{prefix}withdraw <amount>`',
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        if amount == 'max' or amount == 'all':
            amount = get_user_bank_balance(ctx.author.id)
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    title="Invalid Withdraw amount",
                    description=f"{ctx.author.mention}, Please enter a valid amount.",
                    color=embed_error
                )

                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                await ctx.send(embed=embed)
                return        

        if amount <= 0 or amount > get_user_bank_balance(ctx.author.id): # check if they have that amount to withdraw
            embed = discord.Embed(
                title="Invalid withdraw amount",
                description=f'{ctx.author.mention}, Invalid withdraw amount. Please try again.',
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        update_bank_balance(ctx.author.id, -amount)
        update_user_balance(ctx.author.id, amount)

        # Embed the message
        embed = discord.Embed(
            title="Withdraw Successful",
            description=f'{ctx.author.mention}, 💵 **{amount} credits** have been withdrawn from your sussy account.',
            color=discord.Color.green()
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)
        
        
    @commands.command(aliases=['top', 'balancetop', 'balance_top'])
    async def baltop(self, ctx):
        try:
            # Initialize an empty list to store user balances
            user_balances = []

            # Loop through all members of the server
            for member in ctx.guild.members:
                # Skip bot accounts
                if member.bot:
                    continue

                # Get balances and inventory for each user
                pocket_money = get_user_balance(member.id)
                bank_balance = get_user_bank_balance(member.id)
                user_inventory = get_user_inventory(member.id)

                # Calculate the total value of items in the inventory
                total_inventory_value = sum(combined_items[item_id]["sell"] if item_id in combined_items and item_id != 'meth' else shop_items[item_id]["cost"] for item_id in user_inventory if item_id != 'meth')

                # Calculate the total balance
                total_balance = pocket_money + bank_balance + total_inventory_value

                # Append user balance to the list
                user_balances.append((member.id, total_balance))

            # I honestly dont even know what this line right here does, I honestly don't know. - Mal - dev1
            user_balances.sort(key=lambda x: x[1], reverse=True)

            # Get the user's rank
            user_id = ctx.author.id
            user_rank = next((rank + 1 for rank, (member_id, _) in enumerate(user_balances) if member_id == user_id), None)

            # Create the embed
            embed = discord.Embed(
                title="💰 Highest Networths 💰",
                color=discord.Color.green()
            )

            # Add each user's balance to embed
            for rank, (member_id, balance) in enumerate(user_balances[:10], start=1): # only show the highest 3
                member = ctx.guild.get_member(member_id)
                if member:
                    embed.add_field(name=f"**#{rank}** - {member.display_name}", value=f"💰 **{balance} credits**", inline=False)

            # Add a line break
            embed.add_field(name="\u200b", value="\u200b", inline=False)

            # Add user's rank
            if user_rank is not None:
                embed.add_field(name="Your Rank", value=f"Your net worth rank is **#{user_rank}**", inline=False)
            else:
                embed.add_field(name="Your Rank", value="**You are not ranked in the top net worths.**", inline=False)

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(e)
            print(e)


    @commands.command(aliases=['bal'])
    async def balance(self, ctx, user: commands.MemberConverter=None):
        try:
            user = user or ctx.author
            user_id = user.id

            pocket_money = get_user_balance(user_id)
            bank_balance = get_user_bank_balance(user_id)

            embed = discord.Embed(
                title=f"**{user.display_name}'s** Balance",
                description=f'On Hand: **{pocket_money} credits**\nBank Balance: **{bank_balance}/{max_bank_size} credits**',
                color=discord.Color.green()
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            print(e)
            
    
    @commands.command(aliases=['networth', 'net', 'worth', 'netowrth', 'netwoth'])
    async def character(self, ctx, user: commands.MemberConverter=None):
        try:
            user = user or ctx.author

            pocket_money = get_user_balance(user.id)
            bank_balance = get_user_bank_balance(user.id)
            user_inventory = get_user_inventory(user.id)
            
            # Calculate the total value of items in the inventory
            total_inventory_value = sum(combined_items[item_id]["sell"] if item_id in combined_items else shop_items[item_id]["cost"] for item_id in user_inventory)

            # Calculate the total balance
            total_balance = pocket_money + bank_balance + total_inventory_value

            embed = discord.Embed(
                title=f"💰 {user.display_name}'s Balance 💰",
                description=f'💼 Wallet: **{pocket_money} credits**💼\n🏦 Bank Account: **{bank_balance}/{max_bank_size} credits**🏦\n\n🛍️ Assets: **{total_inventory_value}** credits🛍️',
                color=discord.Color.green()
            )
            
            # Set thumbnail as user's avatar
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar_url)

            # Add total balance at the bottom of the embed in big text
            embed.add_field(name="💰 NETWORTH 💰", value=f"**{total_balance}** credits", inline=False)

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)
            print(e)


#-----------------GAMBLING GAMES-----------------


    @commands.command(aliases=['g'])
    async def gamble(self, ctx, amount: str = None):
        if amount is None: # if they didnt enter an amount to gamble
            embed = discord.Embed(
                title="Gamble Command",
                description=f"{ctx.author.mention}, Please specify an amount to gamble. Usage: `{prefix}gamble <amount>`",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        # Check if the user entered "max"
        if amount.lower() == "max":
            amount = min(get_user_balance(ctx.author.id), max_bet) # gamble as much as possible (within max gamble limit)
        else:
            try:
                amount = int(amount)
            except ValueError:
                embed = discord.Embed(
                    title="Invalid Input",
                    description=f"{ctx.author.mention}, Please enter a valid amount or 'max'.",
                    color=embed_error
                )
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

        if amount <= 0 or amount > get_user_balance(ctx.author.id) or amount > max_bet:
            embed = discord.Embed(
                title="Invalid Bet Amount",
                description=f"{ctx.author.mention}, Invalid bet amount. You can bet up to {max_bet} Credits.",
                color=discord.Color.green()
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        # Gambling logic with 1/3 chance of winning
        if random.choice([True, False, False]):  # 1/3 chance
            # User wins
            update_user_balance(ctx.author.id, amount)
            result_description = f"{ctx.author.mention}, You won 💵 **{amount} credits**!"
            result_color = discord.Color.green()
        else:
            update_user_balance(ctx.author.id, -amount)
            result_description = f"{ctx.author.mention}, You lost 💵 **{amount} credits! Big L**."
            result_color = embed_error

        # Send result embed
        result_embed = discord.Embed(
            title="Gamble Result",
            description=result_description,
            color=result_color
        )
        await ctx.send(embed=result_embed)

    @commands.command()
    async def shoot(self, ctx, user: commands.MemberConverter=None):
        user_id = ctx.author.id

        # Check if the user has a 'bow' in their inventory
        # if not dont let them run the hunt command
        user_inventory = get_user_inventory(user_id)
        if 'gun' in user_inventory:
            pass
        elif 'm4a1' in user_inventory:
            pass
        else:
            embed = discord.Embed(
                title="Unable to shoot",
                description=f"{ctx.author.mention}, You need to find a gun or craft an m4a1 to shoot people! Find a gun using `{prefix}scrap` or craft an m4a1 using `{prefix}craft m4a1` view recipes using `{prefix}recipes`!",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        
        if user is None:
            embed = discord.Embed(
                title="Suicide",
                description=f"{ctx.author.mention} has just shot themself!",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="Shots Fired",
            description=f"{ctx.author.mention}, Has just **shot and killed {user.mention}** in cold blood.",
            color=discord.Color.green()
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)

    @commands.command()
    async def bomb(self, ctx, user: commands.MemberConverter=None):
        user_id = ctx.author.id

        # Check if the user has a 'bow' in their inventory
        # if not dont let them run the hunt command
        user_inventory = get_user_inventory(user_id)
        if 'c4' not in user_inventory:
            embed = discord.Embed(
                title="Unable to bomb",
                description=f"{ctx.author.mention}, You need C4 to blow someone up! Craft one using `{prefix}craft c4` view recipes using `{prefix}recipes`",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return
        
        if user is None:
            embed = discord.Embed(
                title="Suicide",
                description=f"{ctx.author.mention}, has just **blown up!**",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="Bombing",
            description=f"{ctx.author.mention}, has just **bombed and killed {user.mention}** with c4!",
            color=discord.Color.green(),
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)


    @commands.command()
    async def trade(self, ctx, user: commands.MemberConverter=None, item_name: str=None):
        user_id = ctx.author.id

        if user is None:
            embed = discord.Embed(
                title="Incorrect usage",
                description=f"{ctx.author.mention}, Incorrect usage. Please use: `{prefix}trade <@user> <item2give>`",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        if item_name is None:
            embed = discord.Embed(
                title="Incorrect usage",
                description=f"{ctx.author.mention}, Incorrect usage. Please use: `{prefix}trade <@user> <item2give>`",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return

        user_inventory = get_user_inventory(user_id)

        if item_name not in user_inventory:
            embed = discord.Embed(
                title="Item not found",
                description=f"{ctx.author.mention}, You **dont have {item_name}** in your inventory!",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return
        
        add_item_to_inventory(user.id, item_name)
        remove_item_from_inventory(user_id, item_name)

        embed = discord.Embed(
            title="Trade successfull",
            description=f"{ctx.author.mention}, You have **given {item_name} to {user}**!",
            color=discord.Color.green(),
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)
    

    @commands.command()
    async def rob(self, ctx, user: commands.MemberConverter = None):
        user_id = ctx.author.id
        target_id = user.id

        # check if they can hunt (not on cooldown)
        if not can_rob(user_id):
            embed = discord.Embed(
                title="Cooldown Active",
                description=f"{ctx.author.mention}, Police are on the streets right now. **Wait 1h**.",
                color=embed_error
            )
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return


        try:
            if user is None:
                embed = discord.Embed(
                    title="Incorrect Usage",
                    description=f"{ctx.author.mention}, Please specify the user to rob: `{prefix}rob <@user>`",
                    color=embed_error
                )
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            if user == ctx.author:
                embed = discord.Embed(
                    title="You can't rob yourself!",
                    description=f"{ctx.author.mention}, You can't rob yourself!",
                    color=embed_error
                )
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            # Get the balance of the command invoker and the target
            user_balance = get_user_balance(user_id)
            target_balance = get_user_balance(target_id)

            # Calculate the amount to rob (20% of the target's balance)
            amount_to_rob = int(0.2 * target_balance)

            # Check if the user has enough balance to rob
            if user_balance < amount_to_rob:
                embed = discord.Embed(
                    title="Insufficient Balance",
                    description=f"{ctx.author.mention}, You don't have enough balance to rob.",
                    color=embed_error
                )
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                await ctx.send(embed=embed)
                return

            if target_balance <= 0:
                embed = discord.Embed(
                    title=f"Your target has no money!",
                    description=f"{ctx.author.mention}, Why rob a poor person! Instead, rob the rich and give to the poor.",
                    color=embed_error
                )
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                await ctx.send(embed=embed)
                return
            
            # Calculate the chance of success (45%)
            success_chance = random.random()

            # Perform the robbery with 45% chance of success
            if success_chance <= 0.45:
                # Success: Rob the target
                update_user_balance(user_id, amount_to_rob)
                update_user_balance(target_id, -amount_to_rob)

                embed = discord.Embed(
                    title="Robbery Successful",
                    description=f"You successfully robbed {amount_to_rob} from {user.mention}!",
                    color=discord.Color.green()
                )
            else:
                # Failure: User loses 20% of their balance
                loss_amount = int(0.2 * user_balance)
                update_user_balance(user_id, -loss_amount)

                embed = discord.Embed(
                    title="Robbery Failed",
                    description=f"You failed to rob {user.mention} and lost {loss_amount}!",
                    color=embed_error
                )

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            await ctx.send(embed=embed)

            update_last_action_time(user_id, "rob")

        except Exception as e:
            print(e)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Economy Cog Loaded! {Fore.RESET}')


def economy_setup(bot):
    bot.add_cog(Economy(bot))