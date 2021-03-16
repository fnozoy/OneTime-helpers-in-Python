###Web Scrapping https://www.youtube.com/watch?v=CHUxmVVH2AQ
###Author: Fabio Nozoy
###Date: 19-feb-2021
###deleta profile no RACF
###c:\> python -m venv env
###c:\> env\Scripts\activate
###c:\> pip install selenium
###baixa chromedriver na pasta do projeto
###executa: %pastadoprojeto%\> pyton deleteRacfProfiles.py
###a entrada é um csv cuja primeira coluna é o profile e a primeira linha é o header

import time
import selenium
from selenium import webdriver
itms = ' '
file_name = ' '
tentatives = 10
url='https://www.racf.ford.com'	

def delete_profiles():
	show_intro()	
	itms = get_itms()
	file_name = get_csv_filename()

	process(itms, file_name, tentatives, url)
	return
	
def process(itms, file_name, tentatives, url):	
	### tip to improve RACFbot
	### ctrl+shift+C ==> click on element ==> get xpath on console with right button
		
	print ('Opening chrome')	
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("detach", True)
	browser = webdriver.Chrome(desired_capabilities=chrome_options.to_capabilities())
	print ('Reaching URL')
	browser.get(url)
	
	if open_new_request(browser, tentatives):
		#open_new_request worked okay
		if enter_itms(browser, tentatives,itms): 
			#enter_itms worked okay
			execute(browser, file_name, tentatives)
			goodbye()
		else:
			print('something unexpected occured in the MAIN DELETE PROFILE process, talk to me in python and teach me to be better...')
			quit()			
			
def execute(browser, file_name, tentatives):
	save_profile=''
	first_line = True
	first_time_profile_dropdown = True
	ab1 = open('out_'+file_name, 'w')
	import csv 
	with open(file_name, 'r') as eb1:
		arq = csv.reader(eb1, delimiter=',')
		print('File {} opened'.format(file_name))
		for reg in arq:
					
			if first_line:
				print('Discarding header: ', reg[0])
				first_line = False
				ab1.write(reg[0]+'\n')
				continue
				
			for i in range(tentatives):
				try:
					### click Add Action button (1st time button is different then other times)
					browser.find_element_by_xpath('//*[@id="newRequestForm:j_id_bz"]/span').click()
					break
				except:
					### click Add Action button (1st time button is different then other times)
					try:
						browser.find_element_by_xpath('//*[@id="newRequestForm:j_id_b5"]').click()
						time.sleep(3)
						break
					except:
						print('Waiting for button Add Action - Retry in 1 second')
						time.sleep(1)
			if i >= tentatives - 1:
				ab1.write('{},fail\n'.format(save_profile))
				browser.find_element_by_xpath('//*[@id="actionDlgForm:j_id_gq"]').click()
				for i in range(tentatives):
					try:
						### click Add Action button (1st time button is different then other times)
						browser.find_element_by_xpath('//*[@id="newRequestForm:j_id_bz"]/span').click()
						break
					except:
						### click Add Action button (1st time button is different then other times)
						try:
							browser.find_element_by_xpath('//*[@id="newRequestForm:j_id_b5"]').click()
							time.sleep(3)
							break
						except:
							print('Waiting for button Add Action - Retry in 1 second')
							time.sleep(1)
			else:
				if save_profile != '':
					ab1.write('{},success\n'.format(save_profile))

			print(reg)		
			### choose FAC-E
			for i in range(tentatives):
				try:
					browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/form/table[2]/tbody/tr/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[6]/div/div[2]/span').click()
					### choose delete profile
					browser.find_element_by_xpath('//*[@id="actionDlgForm:j_id_d6"]/option[10]').click()			
					### first time choosing delete profile the DIV needs to AJAX
					if first_time_profile_dropdown:
						time.sleep(2)
						first_time_profile_dropdown = False
					### type datasetprofile
					browser.find_element_by_xpath('//*[@id="actionDlgForm:j_id_db:0:j_id_df"]').send_keys(reg[0])
					### press validate
					browser.find_element_by_xpath('//*[@id="actionDlgForm:j_id_go"]/span').click()
					save_profile = reg[0]
					break
				except:
					print('Waiting for DIV to stablish')
					time.sleep(1)

			if i >= tentatives - 1:
				print('something unexpected occured while trying to ENTER PROFILE, talk to me in python and teach me to be better...')
				print('bye')
				quit()
	ab1.close()

def show_intro():
	print('Okay. You choose to delete some RACF profiles')
	print('Feed me with a csv file.')
	print('  First row must be header')
	print('  First column must be racf profiles')	 
	print('keep in mind... I will only type profiles for you')
	print('RACF has its own algorithm... so, feed me properly')
	print(' ')
	print('Okay lets start')
	print(' ')
	
def get_itms():
	itms_number = input('What is the ITMS number? ')
	try:
		itms_number = int(itms_number)
		return itms_number
	except:
		print ('I was expecting a number and you entered:{}. I dont know what to do... sorry'.format(itms_number))
		print ('bye')
		quit()
		
def get_csv_filename():
	print ('Now, give me the csv file. Remember first row must be header, first column must be racf profiles')
	file_name = input('Enter the file name: ')
	if len(file_name) <= 0:
		print ('You entered {}, and I was expecting a name... I dont know what to do... sorry'.format(file_name))
		print ('bye')
		quit()
	return file_name

def open_new_request(browser, tentatives):
	### on www.racf.ford.com choose new request
	works = False
	for i in range(tentatives):
		try:
			browser.find_element_by_xpath('//*[@id="form1:j_id_1d:pG1_content"]/div/div[1]/a[1]').click()
			print ('Opening new request')
			works = True
			break
		except:
			print('Waiting to click on new request ')
			time.sleep(1)
	if works:
		return True

def enter_itms(browser, tentatives, itms):	
	works = False
	for i in range(tentatives):
		try:
			### no campo itms request escolhe SIGA e add action
			browser.find_element_by_xpath('//*[@id="newRequestForm:requesterItms"]').send_keys(itms)
			browser.find_element_by_xpath('//*[@id="newRequestForm:targetItms"]').send_keys(itms)					
			works = True	
			break
		except:
			print('Waiting to enter the ITMS#')
			time.sleep(1)
	if works:
		return True
		

def goodbye():
	print('************************************************************************************')
	print('*                                                                                  *')
	print('*                      I have finished my job                                      *')
	print('*          Now you must REVISE the request, save and submit                        *')
	print('*                                                                                  *')
	print('*         OR you may just close RACF page and NOTHING happens                      *')
	print('*                                                                                  *')
	print('*                        Have a nice day                                           *')
	print('*                                                                                  *')
	print('************************************************************************************')
