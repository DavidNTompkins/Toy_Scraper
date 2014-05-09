def cleanse():
	ASINs = []
	with open('../data/ASINList.txt','r') as ASINList:
		ASINs_raw = ASINList.readlines()
		
		ASINs_raw = list(set(ASINs_raw))
		for i in ASINs_raw:
			i = i[:(len(i)-2)]
			ASINs.append(i.split(','))
	
	with open('../data/ASINListClean.txt','w') as output:
		did_write = True
		for i in range(len(ASINs)):
			for j in ASINs[i]:
				k = 2
				#print i, "i"
				#print k
				#print ASINs[i]
				#print ASINs[i][k]
				try_again = True
				review_count =0
				while try_again and k<15:
					try:
						print k
						print len(ASINs[i][k])
	   					review_count = int(ASINs[i][k])
	   					try_again= False
					except ValueError:
						print ASINs[i][k-1]
						print k
						ASINs[i][k-2] = ASINs[i][k-2]+" "+ ASINs[i].pop(k-1)
						print ASINs[i][k-1]
						
   		 				try_again= True
				
				print review_count
				if int(review_count)>44:
					output.write(j+",")
					did_write = True
				else:
					did_write = False	
			if did_write:	
				output.write('\n')




cleanse()

