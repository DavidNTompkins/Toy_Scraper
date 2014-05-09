import urllib

url_start="http://www.amazon.com/s/ref=sr_pg_2?rh=n%3A165793011%2Ck%3A"
url_second="&page="
url_middle="&keywords="
url_finish="&ie=UTF8&qid=1399563598"

keyword_list=[
	'hasbro',
	'mattel',
	'alex toys',
	'lego',
	'Bratz',
	'thomas the train',
	'transformers',
	'knex',
	'crayola',
	'rose art',
	'megabloks',
	'nerf',
	'goldiblox',
	'cars',
	'action figure',
	'marbles',
	'toy',
	'monster high',
	'monopoly',
	'board games',
	'costume',
	'air zone',
	'foam',
	'foam darts',
	'wham-o',
	'aerobie',
	'bandai',
	'jakks pacific',
	'girls',
	'boys',
	'space',
	'castle',
	'firetruck',
	'aliens',
	'planes',
	'cars',
	'pixar',
	'disney',
	'princess',
	'wiffle',
	'balls',
	'play-doh'
]

def get_keyword(index):
	keyword=keyword_list[index]
	keyword=keyword.replace (" ", "+")
	return keyword


def import_page(keywords,page_number):
	url=url_start+keywords+url_second+str(page_number)+url_middle+keywords+url_finish
	print url
	raw_page = urllib.urlopen(url)
	raw_page = raw_page.read()
	return raw_page

def grab_ASINs(raw_page,start,threshold):
	count = 0
	start_mark="newaps"
	ASIN_mark ="/dp/"
	name_mark = '<span class="lrg bold">'
	name_end = '</span>'
	review_mark='rvwCnt">'
	review_end= '</a>'
	Products=[]
	index=start
	print"enter loop"
	while count<24:
		index=raw_page.find(start_mark,index)
		index=raw_page.find(ASIN_mark,index)
		ASIN =raw_page[index+4:index+14]
		#print ASIN
		index=raw_page.find(name_mark,index)
		index2=raw_page.find(name_end,index)
		name = raw_page[index+len(name_mark):index2]
		#print name
		index=raw_page.find(review_mark,index)
		index=raw_page.find('>',index+12)
		index2=raw_page.find(review_end,index)
		reviews =raw_page[index+1:index2]
		#print reviews
		if reviews.find("<html>\n")==-1:
			reviews = reviews.replace(",","")
			if int(reviews)>=threshold:
				Product=[name,ASIN,reviews]
				Products.append(Product)
		count +=1
		
	return Products


def get_search_review(search_index,product_list):
	keyword= get_keyword(search_index)
	print keyword
	for i in range(5):
		raw_page=import_page(keyword,i)
		if raw_page.find("did not match any products.")!=-1:
			break
		print i
		product_list=product_list+grab_ASINs(raw_page,0,30) #contains product list for the page, 30 is thresh
	return product_list

def main():
	product_list=[]
	output= open('ASINList.txt','w')
	for i in range(len(keyword_list)):
		product_list=get_search_review(i,product_list)
	for i in range(len(product_list)):
		for j in product_list[i]:
			output.write(j+",")
		output.write('\n')
	print len(product_list)

	output.close()


main()
