import pandas as pd
import json
import re

df = pd.read_csv('dataaa')
def parse_json_column(column):
    return column.apply(json.loads)
df['use'] = parse_json_column(df['ingredients'])
df['ingredients'] = parse_json_column(df['ingredients'])
df['directions'] = parse_json_column(df['directions'])

df['use'] = df['use'].apply(lambda x: '\n'.join(x).lower())
df['ingredients'] = df['ingredients'].apply(lambda x: '\n'.join(x).lower())
df['directions'] = df['directions'].apply(lambda x: '\n'.join(x).lower())

df['full_recipe'] =  "Use:\n" + df['use'] + "\n\nTitle:\n" + df['title'] + "\n\nIngredients:\n" + df['ingredients'] + "\n\nDirections:\n" + df['directions']
print(df['full_recipe'].head())
print(df['full_recipe'][0])
df['full_recipe'].to_csv('unprocessed.csv', index=False)

number = r'(a|\d+\s*\d+/\d+|\d+/\d+|\d+\.\d+|\d+)'
text_numbers = r'(a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen)'
tens = r'(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)'
large = r'(hundred|thousand)'
common = r'(c[\.]?|cup[s]?|tsp[\.]?|teaspoon[s]?|tbsp[\.]?|tablespoon[s]?|g[\.]?|gram[s]?|kg[\.]?|kilogram[s]?|ml[\.]?|milliliter[s]?|l[\.]?|liter[s]?)'
en = r'(oz[\.]|ounce[s]?|fl[\.]?\s*oz[\.]?|fluid\s*ounce[s]?|fluid\s*oz[\.]?|fl[\.]?\s*ounce[s]?|lb[\.]?|pound[s]?|pt[\.]?|pint[s]?|qt[\.]?|quart[s]?)'
amount = r'(pkt[\.]?|packet[s]?|pack[s]?|pkg[\.]?|package[s]?|can[s]?|tin[s]?|stk[\.]?|stick[s]?|carton[s]?|box[s]?|jar[s]?|bottle[s]?|bag[s]?|pouch[es]?)'
few =r'(catty|catties|bunch[es]?|chunk[s]?|slice[s]?|piece[s]?|clove[s]?|pinch|dash|handful|jigger[s]?|sachet[s]?|tube[s]?)'
unit_pattern = rf'\(({number}|{text_numbers}(?:\s*{large})?|{tens}(?:-{text_numbers})?(?:\s*{large})?)\s*({common}|{en}|{amount}|{few})\)\s*'
df['use'] = [re.sub(unit_pattern, '', ingredient).strip() for ingredient in df['use']]
unit_pattern = rf'\b({number}|{text_numbers}(?:\s*{large})?|{tens}(?:-{text_numbers})?(?:\s*{large})?)\b\s+?'
df['use'] = [re.sub(unit_pattern, '', ingredient).strip() for ingredient in df['use']]
unit_pattern = rf'\b({common}|{en}|{amount}|{few})\s+(\bof\s+)?'
df['use'] = [re.sub(unit_pattern, '', ingredient).strip() for ingredient in df['use']]

df['full_recipe'] =  "Use:\n" + df['use'] + "\n\nTitle:\n" + df['title'] + "\n\nIngredients:\n" + df['ingredients'] + "\n\nDirections:\n" + df['directions']
print(df['full_recipe'].head())
print(df['full_recipe'][0])
df['full_recipe'].to_csv('processed.csv', index=False)