

from utilities import *
from eco_support import *


"""
SCROLL TO THE BOTTOM FOR A SHORT BUT SIMPLE
GUIDE ON HOW TO ADD AND CREATE YOUR OWN COGS
(basically extensions of the bot)
"""





# FARMING COG






class Farming(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Command to plant crops
    @commands.command(aliases=['crop', 'carrots'])
    async def plant(self, ctx, amount: int=None):
        user_id = ctx.author.id
        user_balance = get_user_balance(user_id)
        
        try:
            if amount is None: # if they didn't enter an amount
                embed = discord.Embed(color=embed_error)
                
                embed.title = "Incorrect usage"
                
                embed.description = f"{ctx.author.mention}, Please enter the amount of crops you want to plant. Usage: `{prefix}plant <amount>`"
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            total_cost = amount * cost_per_carrot # total cost of planting their amount of crops

            embed = discord.Embed(color=discord.Color.green())

            # Check if the user has already planted carrots
            if user_has_plants(user_id):
                embed.title = "Wait a Little Longer"
                
                embed.description = f"{ctx.author.mention}, Your crops take {config.get('carrot_growth_duration')} hours to grow. Try harvesting them using: `{prefix}harvest`."
                
                embed.color = embed_error
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            # Check if the user is trying to plant too many crops
            if amount > max_carrot_planted:
                embed.title = "Too Many crops"
                
                embed.description = f"{ctx.author.mention}, You cannot plant more than {max_carrot_planted} crops."
                
                embed.color = embed_error
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            # Check if the user has enough balance
            if user_balance < total_cost:
                embed.title = "Not Enough Balance"
                
                embed.description = f"{ctx.author.mention}, You need {total_cost} credits to plant {amount} crops"
                
                embed.color = embed_error
                
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                
                await ctx.send(embed=embed)
                return

            # Plant crops
            plant_carrots(user_id, amount)

            # Send success message
            embed.title = "Crops Planted"
            
            embed.description = f"{ctx.author.mention}, You have planted {amount} crops."
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)

            # Update last action time
            update_last_action_time(user_id, "plant")
        except Exception as e:
            print(e)


    @commands.command(aliases=['har'])
    async def harvest(self, ctx):
        user_id = str(ctx.author.id)
        user_plantations = load_user_plants()  # Load planted crops

        try:
            if user_id in user_plantations:
                time_planted, amount_planted = user_plantations[user_id]
                current_time = time.time()
                time_left_seconds = max(0, time_planted + growth_duration - current_time)  # Time left of growth (if any)
                growth_percentage = min(100, ((growth_duration - time_left_seconds) / growth_duration) * 100)  # Calculate growth percentage

                if time_left_seconds <= 0:
                    harvested_amount = amount_planted  # Get how much they can harvest

                    total_profit = harvested_amount * carrot_sell  # Calculate total profit
                    update_user_balance(user_id, total_profit)  # Sell crops and add money
                    del user_plantations[user_id]  # Removing the plantation record

                    embed = discord.Embed(
                        title="Success",
                        description=f"{ctx.author.mention}, You have successfully harvested {harvested_amount} crops and earned ${total_profit}.",
                        color=discord.Colour.green()
                    )
                    embed.set_footer(text=f"Need some help? Do {ctx.prefix}tutorial")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Crop Info",
                        description=f"{ctx.author.mention}, Your crops are not ready yet. They are {int(growth_percentage)}% grown.",
                        color=discord.Colour.orange()
                    )
                    embed.set_footer(text=f"Need some help? Do {ctx.prefix}tutorial")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Error",
                    description=f"{ctx.author.mention}, You don't have any crops planted.",
                    color=embed_error
                )
                embed.set_footer(text=f"Need some help? Do {ctx.prefix}tutorial")
                await ctx.send(embed=embed)

            save_user_plants(user_plantations)  # Save data

        except Exception as e:
            print(e)

            
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Farming Cog Loaded! {Fore.RESET}')
        global user_carrot_plantations
        user_carrot_plantations = load_user_plants() # load plantd crops


def farming_setup(bot):
    bot.add_cog(Farming(bot))






# CRAFTING COG






class Crafting(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.command()
    async def recipes(self, ctx):
        """
        Displays crafting recipes.

        Parameters:
            ctx (commands.Context): The context of the command.

        Returns:
            None
        """
        try:
            embed = discord.Embed(title="Crafting Recipes", description="The 🎉 emoji means you have the materials to craft that item!", color=discord.Colour.green())

            user_id = ctx.author.id
            user_inventory = get_user_inventory(user_id)

            for recipe_id, recipe_details in crafting_recipes.items():
                missing_items = {}
                for ingredient, count in recipe_details.items():
                    if ingredient != 'result' and (user_inventory.count(ingredient) < count):
                        missing_items[ingredient] = count - user_inventory.count(ingredient)

                if not missing_items:  # If there are no missing items for this recipe
                    result_sell_price = craftables.get(recipe_id, {}).get('sell', 'unknown price')
                    recipe_text = ', '.join([f"{count}x {combined_items[item]['name']}" for item, count in recipe_details.items() if item != 'result'])
                    embed.add_field(name=f"{recipe_id} 🎉", value=f"**Sell price: {result_sell_price}**\n{recipe_text}", inline=False)
                else:
                    recipe_text = ', '.join([f"{count}x {combined_items[item]['name']}" for item, count in recipe_details.items() if item != 'result'])
                    embed.add_field(name=f"{recipe_id}", value=f"**Sell price: {craftables.get(recipe_id, {}).get('sell', 'unknown price')}**\n{recipe_text}", inline=False)

            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)
            print(e)


    @commands.command()
    async def craft(self, ctx, item_name: str=None):
        """
        Craft an item using the specified recipe.

        Parameters:
            ctx (commands.Context): The context of the command.
            item_name (str): The name of the item to craft.

        Returns:
            None
        """
        user_id = ctx.author.id

        try:
            # Check if item_name is empty
            if item_name is None:
                embed = discord.Embed(title="Incorrect Usage", description=f"Correct usage: `{ctx.prefix}craft <item>`", color=embed_error)

                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                await ctx.send(embed=embed)
                return

            item_name = item_name.lower()

            if item_name in crafting_recipes:
                recipe = crafting_recipes[item_name]
                inventory = get_user_inventory(user_id)
                missing_items = {}

                # Check for each item in the recipe
                for ingredient, count in recipe.items():
                    if ingredient != 'result' and (inventory.count(ingredient) < count):
                        missing_items[ingredient] = count - inventory.count(ingredient)

                # If missing items
                if missing_items:
                    missing_items_text = ', '.join([f"{count}x {item}" for item, count in missing_items.items()])

                    embed = discord.Embed(title="Missing Items", description=f"You are missing {missing_items_text} for crafting {item_name}.", color=embed_error)

                    embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                    await ctx.send(embed=embed)
                else:
                    # Remove used items from inventory and add crafted item
                    for ingredient, count in recipe.items():
                        if ingredient != 'result':
                            for _ in range(count):
                                remove_item_from_inventory(user_id, ingredient)

                    add_item_to_inventory(user_id, recipe['result'])

                    embed = discord.Embed(title="Crafting Successful", description=f"You have crafted {recipe['result']}.", color=discord.Color.green())

                    embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", description="This item cannot be crafted or does not exist.", color=embed_error)
                embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Crafting Cog Loaded! {Fore.RESET}')


def crafting_setup(bot):
    bot.add_cog(Crafting(bot))





# HEISTS COG





class Heists(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Heists Cog Loaded! {Fore.RESET}')


def Heists_setup(bot):
    bot.add_cog(Heists(bot))





# JOBS COG
# IN DEVELOPMENT, NOT ADDED YET





class JobButton(Button):
    def __init__(self, job_name, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.job_name = job_name

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        self.view.cog.user_jobs[user_id] = self.job_name
        await interaction.response.send_message(f"{interaction.user.mention}, you have selected the job: {self.job_name}!", ephemeral=True)

class JobView(View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog
        for job_name, job_info in cog.jobs.items():
            self.add_item(JobButton(job_name, label=job_name.capitalize()))

class Jobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jobs = {
            "freelancer": {"salary": (50, 100), "description": "Work on various tasks for clients."},
            "gamer": {"salary": (20, 80), "description": "Play games and earn money by streaming or winning tournaments."},
            "chef": {"salary": (30, 70), "description": "Cook and sell delicious meals."},
        }
        self.user_jobs = {}  # This will store user jobs {user_id: job_name}

    @commands.command(aliases=['job', 'jobs', 'list_jobs'])
    async def select_job(self, ctx):
        embed = discord.Embed(title="Select a Job", description="Click a button to choose your job:", color=discord.Color.blue())
        
        job_list = "\n".join([f"**{job.capitalize()}**: {info['description']}\nSalary: {info['salary']}" for job, info in self.jobs.items()])
        
        embed.add_field(name="Available Jobs", value=job_list)
        
        await ctx.send(embed=embed, view=JobView(self))

    @commands.command()
    async def collect_salary(self, ctx):
        job_name = self.user_jobs.get(ctx.author.id)
        
        if not job_name:
            embed = discord.Embed(
                title="Job salary collected",
                description=f"{ctx.author.mention}, you don't have a job! Use `!job` to select one.",
                color=discord.Color.green()
            )           
            
            embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
            
            await ctx.send(embed=embed)
            return
        
        job = self.jobs[job_name]
        salary = random.randint(*job['salary'])
        
        update_user_balance(ctx.author.id, salary)
        
        embed = discord.Embed(
            title="Job salary collected",
            description=f"{ctx.author.mention}, you collected **{salary} credits** from your job as a {job_name}.",
            color=discord.Color.green()
        )
        
        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")
        
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Jobs Cog Loaded! {Fore.RESET}')


def setup(bot):
    bot.add_cog(Jobs(bot))





# SPECIAL EVENTS COG





class Events(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Events Cog Loaded! {Fore.RESET}')


def Events_setup(bot):
    bot.add_cog(Events(bot))





# PROPERTIES COG





class Properties(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Properties Cog Loaded! {Fore.RESET}')


def Properties_setup(bot):
    bot.add_cog(Properties(bot))





# MONEY PRINTING COG





class Printing(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Money Printing Cog Loaded! {Fore.RESET}')


def Printing_setup(bot):
    bot.add_cog(Printing(bot))




# EXAMPLE COG (add your own extensions)
# Go back to main.py and import your cog
# then add it to the 'setup_bot' function

"""
class Example(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def example(self, ctx):
        embed = discord.Embed(
            title="Example",
            description=f"{ctx.author.mention}, This is an example command! ",
            color=embed_colour,
        )

        embed.set_footer(text=f"Need some help? Do {prefix}tutorial")

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Example Cog Loaded! {Fore.RESET}')

def example_setup(bot):
    bot.add_cog(Example(bot))
"""