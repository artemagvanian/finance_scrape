import pandas as pd

stocks = input('Enter the name of stock (as written in the Yahoo Finance): ').split()

for stock in stocks:
	stock += '.OL'
	blueprints = {
				  'Summary': f'https://finance.yahoo.com/quote/{stock}',
				  'Statistics': f'https://finance.yahoo.com/quote/{stock}/key-statistics',
				  'History': f'https://finance.yahoo.com/quote/{stock}/history',
				  'Financials': f'https://finance.yahoo.com/quote/{stock}/financials',
				  'Analysis': f'https://finance.yahoo.com/quote/{stock}/analysis',
				  'Balance Sheet': f'https://finance.yahoo.com/quote/{stock}/balance-sheet',
				  'Cash Flow': f'https://finance.yahoo.com/quote/{stock}/cash-flow',
				  }

	filename = stock + '.xlsx'

	writer = pd.ExcelWriter(filename)

	tables = {}

	for tag, url in blueprints.items():
		try:
			tables[tag] = pd.read_html(url) 
		except ValueError:
			pass

	for tag, tableset in tables.items():
		for n, table in enumerate(tableset):
			table.to_excel(writer, sheet_name=tag + ' ' + str(n + 1))

	writer.save()
