from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time 
import re

def check_if_numerical(string):
	for i in string:
		if not(i.isnumeric() or i.isspace() or i == '-' or i == ',' or i == '.'):
			return False
	return True

class DataExtractor:
	def __init__(self, stock_name, delay, driver):
		self.stock_name = stock_name
		self.delay = delay
		self.driver = driver
		self.driver.implicitly_wait(self.delay)
		self.routes = {'income_statement': f'https://finance.yahoo.com/quote/{self.stock_name}/financials',
					   'balance_sheet': f'https://finance.yahoo.com/quote/{self.stock_name}/balance-sheet',
					   'cash_flow': f'https://finance.yahoo.com/quote/{self.stock_name}/cash-flow'}

	def __del__(self):
		self.driver.close()

	def extract_quarterly_data(self, route_name):
		self.driver.get(self.routes[route_name])

		try:
			advertisement = self.driver.find_element_by_css_selector(r'#consent > div > div > div.consent-footer.consent-actions > form > div > button.btn.primary')
			advertisement.click()
		except:
			pass

		try:
			advertisement = self.driver.find_element_by_css_selector(r'''body > div > div > div > form > div > button.btn.primary''')
			advertisement.click()
		except:
			pass

		quarterly = self.driver.find_element_by_css_selector(r'#Col1-1-Financials-Proxy > section > div.Mt\(18px\).Mb\(15px\) > div.Fl\(end\).smartphone_Fl\(n\).IbBox.smartphone_My\(10px\).smartphone_D\(b\) > button')

		quarterly.click()

		time.sleep(self.delay)
		table = self.driver.find_element_by_css_selector(r'#Col1-1-Financials-Proxy > section > div.Pos\(r\)')

		return table.text



STOCK_NAME = 'GOGL.OL'
data_extractor = DataExtractor(STOCK_NAME, 3, webdriver.Chrome())
writer = pd.ExcelWriter(STOCK_NAME + '.xlsx')

for route in ['income_statement', 'balance_sheet', 'cash_flow']:
	data = data_extractor.extract_quarterly_data(route).split('\n')

	dataframe = {}
	row_i = 1
	for n, d in enumerate(data):
		try:
			if check_if_numerical(data[n + 1]):
				dataframe[str(row_i) + ' ' + d] = data[n + 1].split(' ')
				row_i += 1
		except IndexError:
			pass

	dataframe = pd.DataFrame(dataframe)
	dataframe = dataframe.transpose()

	columns = re.findall(r'([a-zA-Z]{3}|\d{1,2}/\d{1,2}/\d{4})', data[1])

	dataframe.columns = columns

	dataframe.to_excel(writer, sheet_name=route)

del data_extractor
writer.save()