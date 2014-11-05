import web
import recipeTools
from web import form
import ConfigParser
import databaseTools
import pickle

#read the config file
config = ConfigParser.ConfigParser()
config.read("config.conf")



urls = (
	"/", "index",
	"/admin", "admin",
	"/allRecipes", "allRecipes",
	"/recipe/(.*)", "recipe",
	"/session", "session",
	"/youCanMake", "youCanMake"
	)
render = web.template.render('templates/')
app = web.application(urls, globals())
db = web.database(dbn='mysql', host=config.get("Database", "DBhost"), port=int(config.get("Database", "DBport")), user=config.get("Database", "DBuser"), pw=config.get("Database", "DBpassword"), db=config.get("Database", "DBname"))

def prepRecipeForDisplay(recipe):
	recipe.ingredients = pickle.loads(recipe.ingredients.replace("|","\n"))
	return recipe

class index:
	def GET(self): 
		ingredients = db.select('ingredients')
		return render.selectIngredients(ingredients)

class admin:
	def GET(self):
		recipes = db.select('recipes')
		return render.admin(recipes)

class allRecipes:
	def GET(self):
		allRecipes = db.select('recipes')
		return render.showRecipes(allRecipes)

class recipe:
	def GET(self, name):
		name = name.replace("%20"," ")
		name = name.replace("%27","'")
		theRecipe = db.query("SELECT * FROM recipes WHERE name=\'" + name + "\'")[0]
		theRecipe = prepRecipeForDisplay(theRecipe)
		return render.recipe(theRecipe)

class youCanMake:
	def GET(self):
		raise web.seeother('/')


	def POST(self):
		search_relationship = ("SELECT * FROM recipe_ingredient_relations WHERE ingredient_id={0}")
		search_recipe = ("SELECT * FROM recipes WHERE id={0}")
		ingredientInput = web.input().ingredients
		ingredients = ingredientInput.split("|")
		ingredients = ingredients[:-1]
		ingredients = [x.replace("ingredient-","") for x in ingredients]
		#create a dictionary of recipes containing each ingredient
		#on recipe collision increment that recipe's counter
		#when done compare recipe counter to totalIngredients
		#if counter == totalIngredients you can make the drink
		recipeIngredientCount = {}
		makeableRecipes = []
		for ingredientId in ingredients:
			query = search_relationship.format(databaseTools.sanitize(ingredientId))
			results = db.query(query)
			for relationship in results:
				if relationship.recipe_id in recipeIngredientCount:
					recipeIngredientCount[relationship.recipe_id] = recipeIngredientCount[relationship.recipe_id] + 1
				else:
					recipeIngredientCount[relationship.recipe_id] = 1
		for recipeId, count in recipeIngredientCount.iteritems():
			query = search_recipe.format(databaseTools.sanitize(recipeId))
			result = db.query(query)[0]
			if count >= result.totalIngredients:
				makeableRecipes.append(result)
		return render.showRecipes(makeableRecipes)

class session:
	def GET(self):
		s = web.ctx.session
		s.start()

		try:
			s.click += 1
		except AttributeError:
			s.click = 1

		print 'click: ', s.click
		s.save()



if __name__ == "__main__":
	app.run()