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

ingredientForm = form.Form(form.Dropdown("Ingredients", []))

class mixApp:
	def GET(self): 
		ingredient_Form = ingredientForm()
		ingredient_Form.Ingredients.args = allIngredients
		return render.ingredientSelectPage(allIngredients)



if __name__ == "__main__":
	app.run()