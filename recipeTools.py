import sys
import csv
import re

class Recipe(object):
  	def __init__(self, name, instructions, glass, ingredients):
		self.name = name
		self.glass = glass
		self.instructions = instructions
		self.ingredients = ingredients
	
	
		self.sanitizedIngredients = []
		for ingredient in ingredients:
			thisIngredient = ""
			if "measure" in ingredient:
				ingredientStart = ingredient.find(" ",ingredient.find("measure"))+1
				thisIngredient = ingredient[ingredientStart:]
				#print thisIngredient
			elif "tablespoon" in ingredient:
				ingredientStart = ingredient.find(" ",ingredient.find("tablespoon"))+1
				thisIngredient = ingredient[ingredientStart:]
				#print thisIngredient
			elif "teaspoon" in ingredient:
				ingredientStart = ingredient.find(" ",ingredient.find("teaspoon"))+1
				thisIngredient = ingredient[ingredientStart:]
				#print thisIngredient
			elif "dash" in ingredient:
				ingredientStart = ingredient.find(" ",ingredient.find("dash"))+1
				thisIngredient = ingredient[ingredientStart:]
				#print thisIngredient
			elif "drops of" in ingredient:
				ingredientStart = ingredient.find(" ",ingredient.find("drops of"))+1
				thisIngredient = ingredient[ingredientStart:]
				#print thisIngredient
			else:
				thisIngredient = ingredient
				thisIngredient = re.sub(r"[0-9]", "", thisIngredient)
				thisIngredient = re.sub(r"/", "", thisIngredient)
	
	
			thisIngredient = thisIngredient.lstrip()
			thisIngredient = thisIngredient.rstrip()
			if "" != thisIngredient:
				self.sanitizedIngredients.append(thisIngredient.upper())
	def canBeMade(self, yourIngredients, pref="bool"):
		youNeed = [x for x in self.sanitizedIngredients if x not in yourIngredients]
		if "bool" == pref:	
			if len(youNeed) != 0:
				#print "You cannot make a " + self.name + ", you don't have " + str(youNeed)
				return False
			else:
				return True
		else:
			return youNeed



class RecipeBook(object):
	def __init__(self, inFile):
		f = open(inFile, 'rt')
		f.readline() # skip the first line
		self.recipeList = []
		try:
			reader = csv.reader(f)
			for row in reader:
				self.recipeList.append(Recipe(row[0], row[1], row[2], row[3:len(row)]))
		finally:
			f.close()

	def allIngredients(self):
		#make a list of all ingredients
		allIngredients = []
		for recipe in self.recipeList:
			for ingredient in recipe.sanitizedIngredients:
				if ingredient not in allIngredients:
					allIngredients.append(ingredient)
		return allIngredients

	def whatCanYouMake(self, stock):
		thingsYouCanMake = []
		for recipe in self.recipeList:
			if recipe.canBeMade(stock.ingredients):
				thingsYouCanMake.append(recipe.name)
		return thingsYouCanMake

	def whatCanYouNotMake(self, stock):
		thingsYouCanNotMake = []
		for recipe in self.recipeList:
			if not recipe.canBeMade(stock.ingredients):
				thingsYouCanNotMake.append(recipe.name)
		return thingsYouCanNotMake

	def whatYouShouldBuy(self, stock):
		thingsYouNeed = []
		youShouldBuy = []
		for recipe in self.recipeList:
			thingsYouNeed.extend(recipe.canBeMade(stock.ingredients,"list"))
		for i in range(10):
			buyNext = max(set(thingsYouNeed), key=thingsYouNeed.count)	
			thingsYouNeed = [x for x in thingsYouNeed if x != buyNext]
			youShouldBuy.append(buyNext)
		return youShouldBuy

	def export(self, fileName):
		fOut = open(fileName+".csv", 'wb')
		writer = csv.writer(fOut)
		writer.writerow( ('Name', 'Instructions', 'Glass', 'Ingredients', 'sanitizedIngredients') )
		for recipe in self.recipeList:
			writer.writerow( (recipe.name, recipe.instructions, recipe.glass, recipe.ingredients, recipe.sanitizedIngredients) )



class Inventory(object):
	def __init__(self, ingredients):
		self.ingredients = ingredients



def main():
	allRecipes = RecipeBook(sys.argv[1])
	allRecipes.export("allStuff")



if __name__ == "__main__":
	main()