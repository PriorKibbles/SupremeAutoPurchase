#Created by Colin Cowie
import time
import sys
import requests
from bs4 import BeautifulSoup
from splinter import Browser

product_name = "Crew Socks"
product_color = "White"
selectOption = "1"
mainUrl = "http://www.supremenewyork.com/shop/all/accessories"
baseUrl = "http://supremenewyork.com"
checkoutUrl = "https://www.supremenewyork.com/checkout"
namefield = "Colin Cowie"
emailfield = "colincowie@example.com"
phonefield = "3015550876"
addressfield = "1234 Normal st."
zipfield = "54321"
statefield = "IN"
cctypefield = "visa"  # "master" "visa" "american_express"
ccnumfield = "4475123468556632"  # Randomly Generated Data (aka, this isn't mine)
ccmonthfield = "10"  # Randomly Generated Data (aka, this isn't mine)
ccyearfield = "2022"  # Randomly Generated Data (aka, this isn't mine)
cccvcfield = "123"  # Randomly Generated Data (aka, this isn't mine)


def main():
    r = requests.get(mainUrl).text
    #print(r)
    if product_name in r:
        print("Product Found")
        parse(r)
    else:
        print("Product not found.")

def parse(r):
    soup = BeautifulSoup(r, "html.parser")
    for div in soup.find_all('div', { "class" : "inner-article" }):
        product = ""
        color = ""
        link = ""
        for a in div.find_all('a', href=True, text=True):
            link = a['href']
        for a in div.find_all(['h1','p']):
            if(a.name=='h1'):
                product = a.text
            elif(a.name=='p'):
                color = a.text
        checkproduct(link,product,color)



def checkproduct(Link,product_Name,product_Color):
    if(product_name in product_Name and product_color==product_Color):
        prdurl = baseUrl + Link
        print('\nTARGETED PRODUCT FOUND\n')
        print('Product: '+product_Name+'\n')
        print('Color: '+product_Color+'\n')
        print('Link: '+prdurl+'\n')
        print('Moving to next phase of purchase...\n')
        buyprd(prdurl)
    #print('Product:'+product_Name+', Color:'+product_Color+', Link:'+Link)



def buyprd(u):
    browser = Browser('firefox')
    url = u
    browser.visit(url)
    # 10|10.5
    browser.find_option_by_text(selectOption).first.click()
    browser.find_by_name('commit').click()
    if browser.is_text_present('item'):
        print("Added to Cart!")
    else:
        print("Error, most likely out of stock.")
        return
    print("checking out")
    browser.visit(checkoutUrl)
    print("Filling Out Billing Info")
    browser.fill("order[billing_name]", namefield)
    browser.fill("order[email]", emailfield)
    browser.fill("order[tel]", phonefield)

    print("Filling Out Address")
    browser.fill("order[billing_address]", addressfield)
    browser.fill("order[billing_zip]", zipfield)
    browser.select("order[billing_state]", statefield)
    print("Filling Out Credit Card Info")

    browser.select("credit_card[type]", cctypefield)
    browser.fill("credit_card[cnb]", ccnumfield)
    browser.select("credit_card[month]", ccmonthfield)
    browser.select("credit_card[year]", ccyearfield)
    browser.fill("credit_card[vval]", cccvcfield)
    browser.find_by_css('.terms').click()
    print("Submitting Info")
    browser.find_by_name('commit').click()
    sys.exit(0)


i = 1

while (True):
    print("On try number " + str(i))
    main()
    i = i + 1
    time.sleep(2)
