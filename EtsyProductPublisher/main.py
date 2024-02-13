# Program that publishes products based on a folder structure where every folder is a product
# Each folder contains a product.json file and the files that need to be published
# A folder contains:
#   - product.json
#   - up to five rar files
#   - a folder with the images that will be displayed in the product's page
#
# The json file contains:
#   - shop_id
#   - title (string)
#   - description (string)
#   - price
#   - quantity, always 1
#   - personalized message
#   - category
#   - tags (list of strings, 13 elements)
#   - materials (list of strings, 13 elements)
#   - shop section
#
# The script then uploads the product to Etsy and publishes it

import os
import json
import sys