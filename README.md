# crypto_watch
A static site generator to display crypto token price charts

It makes use of the Coingecko API.

Firstly the `generate_json.py` script is used to generate the .png figures of the charts, as well as a json with the corresponding info.

Then, the `generate_page.py` script takes the generated json to create the html static page, based on the template in the "references" folder.

There is a bash script (`run_crypto_watch.sh`) that can be scheduled to update the page.
