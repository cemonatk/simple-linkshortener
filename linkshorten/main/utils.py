from sqlite3 import Row, connect
from re import compile, match, IGNORECASE
from linkshorten import convert_to_base62, convert_to_base10

#from linkshorten.config import return_db
#db_path = return_db()

db_path = 'linkshorten/site.db'

def clean_input(value):
    return ''.join(c for c in value if c.isalnum() or c in ['.','/',':'])

def my_select(value, table): 
	if len(value) > 9:
		return ''
	try:
		con = connect(db_path)
		if value is 'table_all':
			cur = con.cursor()
			con.row_factory = Row
			if table is 'link':
				cur.execute('SELECT * FROM link WHERE isspecial=0 ORDER BY id DESC LIMIT 6')
			elif table is 'speciallink':
				cur.execute('SELECT * FROM link WHERE isspecial=1 ORDER BY id ASC LIMIT 6')
			else:
				return ''
			table_all = cur.fetchall()
			con.close()
			return table_all
		else:
			c = con.cursor()
			if table is 'link' and value.isdigit():
				c.execute('SELECT * FROM link WHERE isspecial=0 AND id=(?)', str(clean_input(value)))
			elif table is 'speciallink' and value.isdigit():
				c.execute('SELECT * FROM link WHERE isspecial=1 AND id=(?)', str(clean_input(value)))
			else:
				return ''
			column = c.fetchone()
			con.close()
			return column
	except:
		return ''

def find_url(value, table):
	con = connect(db_path)
	c = con.cursor()
	if table is 'link' and value.isdigit():
		c.execute('SELECT link FROM link WHERE isspecial=0 AND id=(?)', [(str(clean_input(value)))])
	elif table is 'speciallink' and value.isalnum():
		c.execute('SELECT link FROM link WHERE isspecial=1 AND id= (?)', [(str(clean_input(value)))])
	else:
		return ''
	column = c.fetchone()
	con.close()
	return ''.join(column)
	
	# this cleans terminal warnings	
	#if not column is None:
	#	return ''.join(column)
	#else:
	#	return ''


def my_insert(shorturl, link, user_id, table):
	#try:
		# INSERT OR IGNORE INTO link (id, link, isspecial, user_id) VALUES (123213, 'asdasdasdasdASD===', 1, 3);
	user_id = str(user_id)
	con = connect(db_path)
	if table is 'link':
		cur = con.cursor()
		cur.executemany("INSERT OR IGNORE INTO link (link, isspecial, user_id) VALUES (?, ?, ?)", [(clean_input(link), 0, clean_input(user_id))])
		con.commit()
	elif table is 'speciallink':
		query = "INSERT OR IGNORE INTO link (id, link, isspecial, user_id) VALUES (?, ?, ?, ?)"
		cur = con.cursor()
		linkid = convert_to_base10(shorturl)
		if user_id.isdigit():
			cur.executemany(query, [(linkid, link , 1, user_id)])
			con.commit()
		else:
			return ''
	con.close()
	return ''
#	except:
#		return ''

def valid_url(value):
	# Thanks to cetver, https://stackoverflow.com/a/7160778, a solution from django url validation regex.
	regex = compile(
	r'^(?:http|ftp)s?://'
	r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
	r'localhost|'
	r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
	r'(?::\d+)?' 
	r'(?:/?|[/?]\S+)$', IGNORECASE)
	return match(regex, str(value)) is not None



"""
Test Cases, Usage:

Select:
ID ,link, shorturl, user_id = my_select('2','speciallink')

print(ID ,link, shorturl, user_id)

ID ,link = my_select('2','link')

print(ID ,link)

for row in my_select('table_all','speciallink'):
	print(row)


target_link = find_url('','speciallink') + find_url('11','link')
print(target_link)

Insert:
my_insert('www.test1.com','','','link')
print(my_select('table_all','link')[-1])

my_insert('www.test3.com','test',3,'speciallink')
print(my_select('table_all','speciallink')[-1])

valid_url:

print(valid_url('http://www.google.com'))

"""