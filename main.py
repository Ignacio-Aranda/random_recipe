import requests, json, random, webbrowser

APP_KEY = "phAPP_KEY"
APP_ID = "phAPP_ID"

def RandomCountry_Dish():
 
    with open('Consola/dishes.json', 'r') as json_File:
        country_dish_file = json.load(json_File)
    
    random_country = random.randint(0,len(country_dish_file)-1)
    return (country_dish_file[random_country]["country"], 
            country_dish_file[random_country]["CountriesNationalDishes"])

def consultaWeb(dish):
    api_url = f"https://api.edamam.com/api/recipes/v2?type=public&q={dish}&app_id={APP_ID}&app_key=%20{APP_KEY}"
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        return (True, response)
    else:
        return (False, response)
    
def replaceSpaces(phrase):
    return phrase.replace(" ", '%20')

country, dish = RandomCountry_Dish()
print(f"Pais: {country}\nPlato: {dish}")
dish = replaceSpaces(dish)
country = replaceSpaces(country)

country_dish = f"{country}{dish}"
estado, respuesta = consultaWeb(dish)

if (estado):
    data = respuesta.json()
    recipes = data.get('hits')
    if len(recipes) != 0:
        recipeSelected = False
        while not recipeSelected:
            identificador = 1
            for recipe in recipes:
                print(f"{identificador}. {recipe['recipe']['label']}")
                identificador+=1

            indexSelectedRecipe = (int)(input(f"Qué receta quieres cocinar hoy?? (1-{len(recipes)})"))   
            indexSelectedRecipe-=1
            selectedRecipe = recipes[indexSelectedRecipe]['recipe']
            print(f"\nHa seleccionado la receta: {selectedRecipe['label']}")
            print("\nLos ingredientes son: ")
            for ingredient in selectedRecipe['ingredientLines']:
                print(ingredient)
            opcionElegida = False
            while not opcionElegida:
                opcion = input("\nQuieres cocinar esta receta, o prefieres elegir otra? (Y/N)") 
                if opcion.capitalize() == 'Y':
                    recipeSelected = True
                    opcionElegida = True
                elif opcion.capitalize() == 'N':
                    opcionElegida = True
                else:
                    print("\nEsa opcion no existe. Vuelve a intentarlo")

        print(selectedRecipe['url'])
        webbrowser.open(selectedRecipe['url'])

    else:
        print("No hay recetas con este nombre")
