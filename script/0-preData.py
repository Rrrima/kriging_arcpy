import xlrd
import xlwt
workbook = xlrd.open_workbook('ori-data.xls')
tables = []
outbooks = []
outsheets = []
for i in range(31):
	tables.append(workbook.sheets()[i])
	nrows = tables[i].nrows
	ncols = tables[i].ncols
	outbooks.append(xlwt.Workbook(encoding = 'ascii'))
	outsheets.append(outbooks[i].add_sheet('data'))
	for x in range(nrows):
		for y in range(ncols):
#			print(tables[i].cell(x,y).value)
			outsheets[i].write(x,y,tables[i].cell(x,y).value)
	outbooks[i].save('%d.xls'%(i+1))

