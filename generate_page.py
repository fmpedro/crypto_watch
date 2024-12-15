import json
from jinja2 import Environment, FileSystemLoader

# Load JSON data from file
with open('./references/tickers_info.json', 'r') as file:
    charts = json.load(file)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('./references/template.html')

# Render the template with data
output = template.render(charts=charts)

# Save the rendered HTML to a file
with open('crypto_watch.html', 'w') as file:
    file.write(output)
print("Generated html static page.")
