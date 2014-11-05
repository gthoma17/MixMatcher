import MySQLdb 
import csv
import sys
import ConfigParser
import databaseTools




def main(csvFile):
	config = ConfigParser.ConfigParser()
	config.read("config.conf")


	#db access info
	HOST = config.get("Database", "DBhost")
	USER = config.get("Database", "DBuser")
	PASSWD = config.get("Database", "DBpassword")
	DATABASE = config.get("Database", "DBname")
	
	# make a connection to the database
	db_connection = MySQLdb.connect(
	        host=HOST,
	        user=USER, 
	        passwd=PASSWD, 
	        )
	
	#create cursor
	cursor = db_connection.cursor()

	#create out database if it doesn't exist
	try:
		cursor.execute('use '+DATABASE)
	except Exception, e:
		createDatabase(DATABASE, cursor)
	finally:
		cursor.execute('use '+DATABASE)

	#create recipes table if it doesn't exist
	if not tblExists("recipes", cursor):
		createRecipesTbl(cursor)

	#create ingredients table if it doesn't exist
	if not tblExists("ingredients", cursor):
		createIngredientsTbl(cursor)
	
	#create recipe ingredient relations table if it doesn't exist
	if not tblExists("recipe_ingredient_relations", cursor):
		createRecipeIngredientRelationsTbl(cursor)

	#insert into the tables
	databaseTools.insertRecipes(csvFile, cursor)


	#we're done here. close up shop
	db_connection.commit()
	cursor.close()
	db_connection.close()


def createDatabase(DATABASE, cursor): 
	#create our database
	print "Creating database: " +DATABASE
	cursor.execute('create database '+DATABASE)

def createIngredientsTbl(cursor):
	print "Creating table: ingredients"
	cursor.execute("""
	CREATE TABLE ingredients(
	  id INTEGER  NOT NULL AUTO_INCREMENT,
	  name VARCHAR(255)  NOT NULL,
	  picture TEXT(65535),
	  PRIMARY KEY(id)
	)
	""")

def createRecipeIngredientRelationsTbl(cursor):
	print "Creating table: recipe ingredient relations"
	cursor.execute("""
	CREATE TABLE recipe_ingredient_relations(
	  id INTEGER  NOT NULL AUTO_INCREMENT,
	  recipe_id INTEGER  NOT NULL,
	  ingredient_id INTEGER NOT NULL,
	  PRIMARY KEY(id)
	)
	""")

def createRecipesTbl(cursor):
	print "Creating table: recipes"
	cursor.execute("""
	CREATE TABLE recipes(
	  id INTEGER  NOT NULL AUTO_INCREMENT,
	  name VARCHAR(255)  NOT NULL,
	  instructions TEXT(65535),
	  glass VARCHAR(255),
	  ingredients TEXT(65535),
	  rawIngredients TEXT(65535),
	  picture TEXT(65535),
	  totalIngredients INTEGER,
	  PRIMARY KEY(id)
	)
	""")

def tblExists(name, cursor):
	search_tbl = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = {0}"
	search_tbl = search_tbl.format(databaseTools.sanitize(name))
	cursor.execute(search_tbl)
	if cursor.fetchone()[0] == 1:
		return True
	else:
		return False


if __name__ == "__main__":
	main(sys.argv[1])	