import re

EXTRACT_PATTERNS = {
    "bbc food": {
        "title": [
            {
                "findallFirst": "<h1 class=\"gel-trafalgar content-title__text\".*?>(.+?)</h1>"
            }
        ],
        "servings": [
            {
                "findallFirst": "<p class=\"recipe-metadata__serving\".*?>(.+?)</p>"
            },
            {
                "sub": ("[^0-9]", ""),
            }
        ]
    },
    "british": {
        "title": [
            {
                "findallFirst": "<h1 itemprop=\"name\">(.+?)</h1>"

            }
        ],
        "servings": [
            {
                "findallFirst": "<span class=\"header-attribute-text\">(.+?)</span>"
            },
            {
                "sub": ("[^0-9]", ""),
            }
        ]
    },
    "italian": {
        "title": [
            {
                "findallFirst": "<h1 itemprop=\"name\">(.+?)</h1>"

            }
        ],
        "servings": [
            {
                "findallFirst": "<span class=\"header-attribute-text\">(.+?)</span>"
            },
            {
                "sub": ("[^0-9]", ""),
            }
        ]
    },
    "delish": {
        "title": [
            {
                "findallFirst": "<h1 class=\"content-hed recipe-hed\">(.+?)</h1>"

            }
        ],
        "servings": [
            {
                "findallFirst": "<span class=\"yields-amount\">(.+?)</span>"
            },
            {
                "sub": ("[^0-9]", ""),
            }
        ]
    },
    "good_food": {
        "title": [
            {
                "findallFirst": "<h1 class=\"heading-1\">(.+?)</h1>"

            }
        ],
        "servings": [
            {
                "findall3": "<div class=\"icon-with-text__children\">(.+?)</div>"
            },
            {
                "sub": ("[^0-9]", ""),
            }
        ]
    },
    "jamie": {
        "title": [
            {
                "findallFirst": "<h3 class=\"h1 single-recipe-title\">(.+?)</h3>"

            }
        ],
        "servings": [
            {
                "findallFirst": "<div class=\"recipe-detail serves\">(.+?)</div>"
            },
            {
                "sub": ("[^0-9]", ""),
            }
        ]
    },
    "seriouseats": {
        "title": [
            {
                "findallFirst": "<h1 class=\"heading__title\">(.+?)</h1>"

            }
        ],
        "servings": [
            {
                "findall3": "<span class=\"meta-text__data\">(.+?)</span>"
            },
            {
                "sub": ("[^0-9]", ""),
            }
        ]
    },
    "simply": {
        "title": [
            {
                "findallFirst": "<h1 class=\"heading__title\">(.+?)</h1>"

            }
        ],
        "servings": [
            {
                "findall3": "<span class=\"meta-text__data\">(.+?)</span>"
            },
            {
                "sub": ("[^0-9]", ""),
            }
        ]
    },
    "spoon": {
        "title": [
            {
                "findallFirst": "<h1 itemprop=\"name\">(.+?)</h1>"

            }
        ],
        "servings": [
            {
                "findallFirst": "<input style=float:left type=number size=2 id=spoonacular-serving-stepper value=(.+?)>"
            },
            {
                "sub": ("[^0-9]", ""),
            }
        ]
    }
}

def applyCustomRegex(regexType, regexPattern, text):
    try:
        if regexType == "findall":
            t = re.findall(regexPattern, text)
            return t
        elif regexType == "findallFirst":
            t = re.findall(regexPattern, text)[0]
            return t
        elif regexType == "findall3":
            t = re.findall(regexPattern, text)[2]
            return t
        elif regexType == "sub":
            pattern = regexPattern[0]
            replaceWith = regexPattern[1]
            if replaceWith == "":
                t = re.sub(pattern, "",text)
            else:
                t = re.sub(pattern, replaceWith,text)
            return t
    except:
        return ""

def getTitleFromSiteContent(title_patterns, site_content):
    content = site_content
    for step in title_patterns:
        for key, value in step.items():
            content = applyCustomRegex(key, value, content)
    return content

def getServingsFromSiteContent(servings_patterns, site_content):
    content = site_content
    for step in servings_patterns:
        for key, value in step.items():
            content = applyCustomRegex(key, value, content)
    return content

def getIngredientsFromSiteContent(site_content,website):
    pattern_remove = "<[^>]*>"
    pattern = ""
    sub_pattrn = ""
    if website == "bbc food".upper():
        pattern = "<ul class=\"recipe-ingredients__list\".*?>(.+?)</ul>"
        sub_pattrn = "</li>"
    elif website == "british".upper() or website == "italian".upper():
        pattern = "<li class=\"IngredientsList__IngredientItem\" itemprop=\"recipeIngredient\">(.+?)</li>"
        sub_pattrn = "</li>"
    elif website == "delish".upper():
        pattern = "<div class=\"ingredient-item\">(.+?)</div>"
        sub_pattrn = "</div>"
    elif website == "good_food".upper():
        pattern = "<li class=\"pb-xxs pt-xxs list-item list-item--separator\">(.+?)</li>"
        sub_pattrn = "</div>"
    elif website == "jamie".upper(): 
        pattern = "<div class=\"col-md-12 ingredient-wrapper\">(.+?)</div>"
        sub_pattrn = "</li>"
    elif website == "simply".upper():
        pattern = "<ul class=\"structured-ingredients__list text-passage\">(.+?)</ul>"
        sub_pattrn = "</li>"
    elif website == "seriouseats".upper():
        pattern = "<ul id=\"ingredient-list_1-0\" class=\"comp ingredient-list simple-list simple-list--circle \">(.+?)</ul>"
        sub_pattrn = "</li>"
    elif website == "spoon".upper():
        try:
            pattern = "<div class=spoonacular-name>(.+?)</div>"
            pattern_remove = "<[^>]*>"
            ingredient_names = list()
            x = re.findall(pattern, site_content)
            for y in x:
                y = re.sub("</div>","\n",y)
                ingredient_names.extend([x.strip() for x in re.sub(pattern_remove,"",y).split("\n") if x != ""])
            pattern = "<div class=spoonacular-ingredient>(.+?)</div>"
            pattern_remove = "<[^>]*>"
            ingredient_value = list()
            x = re.findall(pattern, site_content)
            for y in x:
                y = re.sub("</div>","\n",y)
                ingredient_value.extend([x.strip() for x in re.sub(pattern_remove,"",y).split("\n") if x != ""])
            return [ingredient_value[i].strip() + " " + ingredient_names[i].strip()  for i in range(len(ingredient_value))]
        except:
            return []
    try :
        x = re.findall(pattern, site_content)
        ingredients = list()
        for y in x:
            y = re.sub(sub_pattrn,"\n",y)
            ingredients.extend([x.strip() for x in re.sub(pattern_remove,"",y).split("\n") if x != ""])
        return ingredients
    except:
        return []


def getStepsFromSiteContent(site_content,website):    
    pattern_remove = "<[^>]*>"
    pattern = ""
    sub_pattrn = ""
    if website == "bbc food".upper():
        pattern = "<ol class=\"recipe-method__list\".*?>(.+?)</ol>"
        sub_pattrn = "</li>"
    elif website == "british".upper() or website == "italian".upper():
        pattern = "<div class=\"MethodList__StepText\" itemprop=\"recipeInstructions\">\s*(.+?)</div>"
        sub_pattrn = "</li>"
    elif website == "delish".upper():
        pattern = "<div class=\"direction-lists\">\s*(.+?)</div>"
        sub_pattrn = "</li>"
    elif website == "good_food".upper():
        pattern = "<li class=\"pb-xs pt-xs list-item\">(.+?)</div>"
        sub_pattrn = "</li>"
    elif website == "jamie".upper():
        pattern = "<ol class=\"recipeSteps\">(.+?)</div>"
        sub_pattrn = "</li>"
    elif website == "seriouseats".upper() or website == "simply".upper():
        pattern = "<OL id=\"mntl-sc-block_3-0\" class=\"comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup\">(.*)</OL>"
        sub_pattrn = "</p>"
    elif website == "spoon".upper():
        pattern = "<div class=\"recipeInstructions\" itemprop=\"recipeInstructions\">(.+?)</div>"
        sub_pattrn = "</li>"
    steps = list()
    try:
        x = re.findall(pattern, site_content)
        for y in x:
            y = re.sub(sub_pattrn,"\n",y)
            steps.extend([x.strip() for x in re.sub(pattern_remove,"",y).split("\n") if x != ""])
        return steps
    except:
        return []