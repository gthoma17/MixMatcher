import web
import recipeTools
from web import form
import ConfigParser

#read the config file
config = ConfigParser.ConfigParser()
config.read("config.conf")



urls = (
	"/", "index",
	"/admin", "admin",
	"/allRecipes", "allRecipes",
	"/recipe/(.*)", "recipe",
	"/session", "session"
	)
render = web.template.render('templates/')
app = web.application(urls, globals())
db = web.database(dbn='mysql', host=config.get("Database", "DBhost"), port=int(config.get("Database", "DBport")), user=config.get("Database", "DBuser"), pw=config.get("Database", "DBpassword"), db=config.get("Database", "DBname"))


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
		recipes = db.select('recipes')
		return render.allRecipes(recipes)

class recipe:
	def GET(self, name):
		name = name.replace("%20"," ")
		name = name.replace("%27","'")
		theRecipe = db.query("SELECT * FROM recipes WHERE name=\'" + name + "\'")[0]
		return render.recipe(theRecipe)
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