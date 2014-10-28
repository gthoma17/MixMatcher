import sys
import csv
import re

def extractRecipes( text ):
  fIn  = open(sys.argv[1], 'rt')
  fOut = open("menu.csv", 'wb')
  try:
      allRecipe = fIn.read()
      writer = csv.writer(fOut)

      writer.writerow( ('Name', 'Instructions', 'Glass', 'Ingredients') )
      #print "iterating " + str(allRecipe.count("<H2>")-1) + " times"
      recipePointer = 0

      for i in range(allRecipe.count("<H2>")-1):
        #print i

        recipeStart = allRecipe.index("<H2>", recipePointer)
        recipeEnd = allRecipe.index("<H2>", recipeStart+1)
        thisRecipe = allRecipe[recipeStart:recipeEnd]
        
        #print "this recipe: " + thisRecipe
        #print "recipeStart: " + str(recipeStart) + " recipeEnd: " + str(recipeEnd) + " recipePointer: " + str(recipePointer) + " recipeLength: " + str(len(thisRecipe))
                
        nameStart = thisRecipe.index("A NAME=")+8
        nameEnd = thisRecipe.index("\">", nameStart)
        thisName = thisRecipe[nameStart:nameEnd]
                 
        #print thisName

        instructionsStart = thisRecipe.index("<P>")+3
        instructionsEnd = thisRecipe.index("</P>", instructionsStart)
        thisInstructions = thisRecipe[instructionsStart:instructionsEnd]
        thisInstructions = thisInstructions.replace('\n',' ')
        thisInstructions = re.sub(r"<.*>", " ", thisInstructions)

        #print thisInstructions


        if '<I>' not in thisRecipe:
          thisGlass = "N/A"
        else: 
          glassStart = thisRecipe.index("<I>")+3
          glassEnd = thisRecipe.index("</I>")
          thisGlass = thisRecipe[glassStart:glassEnd]

        #print thisGlass

        if "<!BR>" in thisRecipe:
          thisRecipe = thisRecipe.replace("<!BR>","<BR>")
        ingredientsStart = thisRecipe.index("<BR>")
        ingredientsEnd = thisRecipe.index("<P>")-1
        thisIngredients = thisRecipe[ingredientsStart:ingredientsEnd]
        thisIngredients = thisIngredients.replace('<BR>','')
        thisIngredients = thisIngredients.replace('\n',',')


        #print thisIngredients

        row = [thisName, thisInstructions, thisGlass]
        row.extend(thisIngredients.split(","))

        #print row

        writer.writerow(row)
        recipePointer = recipeStart + 1

  finally:
      fOut.close()
      fIn.close()




def main():
    extractRecipes(sys.argv[1])

if __name__ == "__main__":
    main()