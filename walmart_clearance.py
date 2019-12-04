from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

wal_url = []

for i in range(1,26):
	wal_url.append('https://www.walmart.com/browse/0?cat_id=3944&facet=special_offers%3AClearance&page=' + str(i) + '&redirect=true#searchProductResult')

filename = "Walmart_Clearance.csv"
f = open(filename, "w")

headers = "Product Name, Price, Old Price, Discount, Discount %\n"

f.write(headers)

for page in wal_url:

	# opening up connection, grabbing the page
	uClient = uReq(page)
	page_html = uClient.read()
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll("div", {"class": "search-result-gridview-item-wrapper"})

	for container in containers:

		title_container = container.findAll("a",{"class": "product-title-link line-clamp line-clamp-2"})
		product_name = title_container[0]["title"]

		pchar_container = container.findAll("span", {"class": "price-characteristic"})
		pmark_container = container.findAll("span", {"class": "price-mark"})
		pmant_container = container.findAll("span", {"class": "price-mantissa"})

		pcharacteristic = pchar_container[0].string
		pmark = pmark_container[0].string
		pmantissa = pmant_container[0].string

		price = float(pcharacteristic + pmark + pmantissa)
	
		if container.findAll("span",{"class": "price display-inline-block arrange-fit price price-secondary"}) == []:
			old_price = "N/A"
		else:
			old_price_container = container.findAll("span",{"class": "price display-inline-block arrange-fit price price-secondary"})
			opcharacteristic = pchar_container[1].string
			opmark = pmark_container[1].string
			opmantissa = pmant_container[1].string

			old_price = float(opcharacteristic + opmark + opmantissa)

		try:
			discount = old_price - price
		except TypeError:
			discount = "N/A"
		else:
			discount = old_price - price

		try:
			disc_percentage = discount/old_price
		except TypeError:
			disc_percentage = "N/A"
		else:
			disc_percentage = discount/old_price
	
		print("product_name: " + product_name)
		print("price: " + str(price))
		print("old_price: " + str(old_price))

		f.write(product_name.replace(",", "|").replace('″', '"').replace("！", "!").replace("＆", "&").replace("（", "(" ).replace("）", ")").replace("【", "[").replace("】", "]").replace("，", "|")
				+ "," + str(price) + "," + str(old_price) + "," + str(discount) + "," + str(disc_percentage) + "\n")

f.close()