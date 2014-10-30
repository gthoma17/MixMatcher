import web
import recipeTools
from web import form

urls = (
	"/", "mixApp"
	)
render = web.template.render('templates/')
app = web.application(urls, globals())
allRecipes = recipeTools.RecipeBook("menu.csv")
allIngredients = allRecipes.allIngredients() 

class mixApp:
	def GET(self): 
		return render.ingredientSelectPage(allIngredients)



if __name__ == "__main__":
	app.run()