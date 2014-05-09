import urllib

first_review_url = "http://www.amazon.com/product-reviews/"
middle_review_url = "/ref=cm_cr_pr_top_link_next_2?ie=UTF8&filterBy=addFiveStar&pageNumber="
last_review_url = "&showViewpoints=0&sortBy=bySubmissionDateDescending"


check_list = {'5-year-old':5,
'Grandchildren ages 2, 3, 4 & 5':2,
'3 1/2yr ol':3.5,
'his 4th birthday':4,
'his 3rd birthday':3,
'3.6 year old boy':3.6,
'3 year old son':3,
'2 year old grandson':2,
'his 5th birthday':5,
'4 yr old ':4,
'four year old':4,
'3 YO':3,
'3 yo son':3,
'4 years old son':4,
'2 1/2 year old son':2.5,
'3 year old and 5 year old boys':3,
'His fourth birthday':4,
'he is 5-6 years old':5.5,
'any 4 year old':4,
'four-year-old':4,
'3 year old':3,
'2 year old':2,
'5 year old ':5,
'3 years old':3,
'4 year old':4,
'6-year old':6,
'4 yr old':4,
'5 yr old':5,
'3 yr old':3,
'(4yr and 3yr)':4,
'5 yo':5,
'3 yr old son':3,
'a 4 year old and a 2 year old':4,
'3.5-year-old':3.5,
'son is almost 5':4.5,
'My 3 y/o':3,
'4 y.o.':4,
'5yr Old':5,
'when he was 2 or 3':2.5,
'three yr old grandson':3,
'3 years old kid':3,
'4 year old grandson':4,
'almost 4 year old':3.75,
'4 year old twins':4,
'nearly 4 years old':3.75,
'a 3 year old':3,
'my 3 and 5 year olds':3,
'kids (2 and 3)':2,
'my son is three':3,
'my 3 year old ':3,
'my two year old':2,
'my 4 year old son':4,
'my grandsons, ages 4 and 5':4,
'he was 3 at the time, now 4 years old':3,
'he is 3 years old':3,
'three year old':3,
'4-year-old':4,
'4 year olds':4,
'3yr old.':3,
'5 year old':5,
'he was closer to 2 1/2':2.5,
'six-year-old daughter and 4 year old son':4,
'when he just turned 3':3,
'4 year old son':4,
'they are 3 and 6.':3,
'5 year old grandson':5,
'got it for him when he was 3':3,
'two boys (7 and 5)':7,
'my three year old':3,
'four year old son':4,
'5 year old and 2 year old':5,
"3 year old son's":3,
'who just turned 3':3,
'3 yr old.,':3,
'4 years old':4,
'my son, 3.5 years old,':3.5,
'and my 2 1/2 now 3 year old':2.5,
'3 year old granddaughter':3,
'3 y.o.':3,
'two year old and five year old':2,
'4-year old':4,
'3-year old ':3,
'3 and 5 yr old boys':3,
'4 1/2 year old':4.5,
"4 year old's":4,
'3 year old step son':3,
'3 year old ':3,
'2year old':2,
'my son is 3':3,
'3 and 5 years old':3,
'my 4 year old':4,
'3.75 yr. old son':3.75,
'(ages 2 & 4)!':2,
'4 year old boy':4,
'3 and 6 year olds':3,
'my grandson who is 4':4,
'3 and 6 year olds playing hard':3,
'my 5 year old grandson':5,
'a 2 1/2 year old':2.5,
'My 3 year old':3,
'my 3 year old grandson':3,
"a 3 year old boy's birthday present":3,
'my six-year-old':6,
'our three-year-old nephew':3,
'4-year old grandson':4,
'my 4 years old':4,
'my 4-year old':4,
'my 5 year old ':5,
'a 4 year old':4,
}


start_mark = '<div class="reviewText">'
finish_mark = '<div style="padding-top: 10px; clear: both; width: 100%;">'

def grab_ASINs():
	ASIN_list=[]
	with open('../data/ASINListClean.txt','r') as ASINList:
		ASINs_raw = ASINList.readlines()
		ASINs_raw = list(set(ASINs_raw))
		for i in ASINs_raw:
			i = i[:(len(i)-2)]
			ASIN_list.append(i.split(','))

	return ASIN_list


def grab_reviews(my_reviews, start_mark, finish_mark):
	start = 0
	finish = 0
	starts = []
	finishes = []
	point = 0
	text =[]

	while point <10: #should be number of reviews on page, diff for final page
		start = my_reviews.find(start_mark,start+1)
		finish = my_reviews.find(finish_mark,finish+1)
		starts.append(start+len(start_mark))
		finishes.append(finish)

		point +=1
	for i in range(len(starts)):
		text.append(my_reviews[starts[i]:finishes[i]])
	return text

def parse_reviews(review_text,check_list,ages):
	age = []
	for i in range(len(review_text)):
		for key in check_list:
			if review_text[i].find(key) >=0:
				age.append(int(check_list[key]))
				break

	return age

def sort_ages(ages):
	ages_count=[0]*18
	ages.sort()
	for i in ages:
		ages_count[i]+=1
	return ages_count


def main(ASIN_list):
	final_output = {}
	#[[name ,ASIN,review_count]]
	ASIN_list= grab_ASINs() 
	for j in ASIN_list:
		ages =[]
		for i in range(28): # should be review_count/10
			review_url = first_review_url+j+middle_review_url+str(i)+last_review_url
			#print "1"
			my_reviews = urllib.urlopen(review_url)
			my_reviews = my_reviews.read()
			review_text = grab_reviews(my_reviews,start_mark,finish_mark)
			ages = ages+ parse_reviews(review_text,check_list,ages)
		break_down = sort_ages(ages)
		final_output[j]=break_down
		print ages
	print final_output
	
	#print float(sum(final_output["B00A8UT562"]))/float(len(final_output["B00A8UT562"]))
	#print float(sum(final_output["B00A8UT55I"]))/float(len(final_output["B00A8UT55I"]))
	#print float(sum(final_output["B00A8UT5TY"]))/float(len(final_output["B00A8UT5TY"]))
	#print float(sum(final_output["B00A8UT558"]))/float(len(final_output["B00A8UT558"]))




