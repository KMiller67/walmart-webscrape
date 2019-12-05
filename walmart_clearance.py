from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# List for holding web page urls
wal_urls = []

# Loops through all pages of electronics clearance items and adds them to wal_urls list
for i in range(1,26):
	wal_urls.append('https://www.walmart.com/browse/0?cat_id=3944&facet=special_offers%3AClearance&page=' + str(i) + '&redirect=true#searchProductResult')

# Establishes a file name for CSV file and begins writing the file to store web scraped data
filename = "Walmart_Clearance.csv"
f = open(filename, "w")

# Establish headers for columns in CSV file
headers = "Product Name, Price, Old Price, Discount, Discount %\n"

f.write(headers)

# Loop through each web page for web scraping
for page in wal_urls:

	# opening up connection, grabbing the page
	uClient = uReq(page)
	page_html = uClient.read()
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	# Selecting only the product containers within HTML since we don't need other information on the web page
	containers = page_soup.findAll("div", {"class": "search-result-gridview-item-wrapper"})

	# Loop through item containers on the current web page
	for container in containers:

		# Finds where the title is contained within the product container and stores it in a variable
		title_container = container.findAll("a",{"class": "product-title-link line-clamp line-clamp-2"})
		product_name = title_container[0]["title"]

		# Finds each 'piece' of the current price of the product and stores them in variables
		# Each 'piece' is considered a string
		pchar_container = container.findAll("span", {"class": "price-characteristic"})
		pmark_container = container.findAll("span", {"class": "price-mark"})
		pmant_container = container.findAll("span", {"class": "price-mantissa"})

		# Commas are replaced if an item is over $1,000 to avoid issues when writing CSV file
		pcharacteristic = pchar_container[0].string.replace(",", "")
		pmark = pmark_container[0].string
		pmantissa = pmant_container[0].string

		# Combine the string variables and convert result into a float
		price = float(pcharacteristic + pmark + pmantissa)

		# Some items list the previous price before the clearance discount is applied
		# Checks to see if an old price is listed and lists 'N/A' if an old price isn't shown
		if container.findAll("span",{"class": "price display-inline-block arrange-fit price price-secondary"}) == []:
			old_price = "N/A"
		else:
			# Old price 'pieces' are found within the same search as the current price, so those are referenced if they exist
			# Commas are replaced if an item was over $1,000 to avoid issues when writing CSV file
			opcharacteristic = pchar_container[1].string.replace(",", "")
			opmark = pmark_container[1].string
			opmantissa = pmant_container[1].string

			# Combine the string variables and convert result into a float
			old_price = float(opcharacteristic + opmark + opmantissa)

		# Calculates the size of the discount if an old price is listed for the item
		try:
			discount = old_price - price
		except TypeError:
			discount = "N/A"
		else:
			discount = old_price - price

		# Calculates the percentage discount if an old price is listed for the item
		try:
			disc_percentage = discount/old_price
		except TypeError:
			disc_percentage = "N/A"
		else:
			disc_percentage = discount/old_price

		# Print web scraped data to make sure it's running correctly
		print("product_name: " + product_name)
		print("price: " + str(price))
		print("old_price: " + str(old_price))

		# Add the data and calculations into CSV file
		# Commas in product name are replaced with | to avoid issues when adding data to CSV file
		# Many items on Walmart website had unique characters similar to existing ones which break the script,
		# which were addressed by copying the unique character from the website (since it can't be added by a normal keyboard)
		# and replacing it with the appropriate 'normal' character
		f.write(product_name.replace(",", "|").replace('″', '"').replace("！", "!").replace("＆", "&").replace("（", "(" ).replace("）", ")").replace("【", "[").replace("】", "]").replace("，", "|")
				+ "," + str(price) + "," + str(old_price) + "," + str(discount) + "," + str(disc_percentage) + "\n")

f.close()