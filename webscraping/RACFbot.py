###Author: Fabio Nozoy
###Date: 21-feb-2021
###This RPA was created to solve MY problem... It does not intent to be a robust and all proof tool...
###
###problem to solve: delete dataset profiles on www.racf.ford.com is one by one 
###                  it takes hours when it's necessary to decomission an application due to large amount of profiles
###                  delete RACF groups also take long... 
###
###install selenium
###c:\> pip install selenium
###
###download chromedriver to project execution folder
###
###create environment (only one time)
###c:\> python -m venv env
###
###activate enviroment
###c:\> env\Scripts\activate
###
###the input is a csv with "profile" on the first column and the header on the first line
###
import DeleteRacfProfiles as drp
import DeleteRacfGroups as drg

def main():
	
	credits()	
	option = choose_option()
	if option == '1':
		drp.delete_profiles()
	elif option == '2':
		drg.delete_groups()

	print('RACFbot is shutting down')

	key=input('press ENTER')

	print('bye')
	return
	
def credits():
	print('************************************************************************************')
	print('*                                                                                  *')
	print('*                                    RACFbot                                       *')
	print('*                                                                                  *')	
	print('*  v1.0 helps to delete profile in FAC-E          Author: Fabio Nozoy     feb/2021 *')
	print('*  v2.0 helps to delete groups in FAC-e           Author: Fabio Nozoy     feb/2021 *')
	print('*                                                                                  *')
	print('*  RACF URL: https://www.racf.ford.com                                             *')
	print('*  browser used is chrome                                                          *')
	print('*  language is Python                                                              *')
	print('*  libs: Selenium                                                                  *')
	print('************************************************************************************')
	
	
def choose_option():
	print('Choose one of the options below:')
	print('1 - PROFILE: helps to submit a request to delete RACF profiles of a given csv file')
	print('2 - GROUP:   helps to submit a request to delete RACF groups of a given csv file')
	print('**no other option available**')
	option = input('choose your option: ')
	if option != '1':
		if option != '2':
			print('Invalid option')
			print('bye')
			quit()
	return option
	

main()
