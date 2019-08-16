from linkshorten.models import Link
from flask_login import current_user
from linkshorten import db, convert_to_base62, convert_to_base10
from linkshorten.main.utils import my_select, clean_input, my_insert, valid_url, find_url
from flask import render_template, request, abort, Blueprint, redirect, url_for
from base64 import b64encode, b64decode

main = Blueprint('main', __name__)
@main.route("/", methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		link1 = request.form.get('link1')
		link2 = request.form.get('link2')
		link3 = request.form.get('link3')

		# Random link creation for users who logged in.
		if valid_url(link1) and link2=='':
			longurl = b64encode(link1.encode('ascii')).decode('utf-8')
			user_id = str(current_user).split(' ')[1].strip('>')
			link = Link(link=longurl, isspecial=0, user_id=user_id)
			db.session.add(link)
			db.session.commit()
			return render_template('home.html', link='http://linkshortener.domain/'+convert_to_base62(link.id))
		
		# Special link creation for users who logged in.
		elif current_user.is_authenticated and len(link2) < 15 and valid_url(link1):
			# if not exists; if not  b64decode(find_url(str(convert_to_base10(link1)),'speciallink')).decode('utf-8')
			longurl = b64encode(link1.encode('ascii')).decode('utf-8')
			user_id = str(current_user).split(' ')[1].strip('>')
			my_insert(link2, longurl, user_id, 'speciallink')
			return render_template('home.html', link='http://linkshortener.domain/'+str(link2))

		# Random link creation for any user.
		elif valid_url(link3):
			longurl = b64encode(link3.encode('ascii')).decode('utf-8')
			user_id = str(current_user).split(' ')[1].strip('>')
			link = Link(link=longurl, isspecial=0, user_id=user_id)
			db.session.add(link)
			db.session.commit()
			return render_template('home.html', link='http://linkshortener.domain/'+convert_to_base62(link.id))
		
		else:
			return abort(403)
	
	elif request.method =='GET':
		return render_template('home.html')
	
	else:
		return abort(403)

@main.route("/page/about")
def about():
    return render_template('about.html', title='About')

@main.route("/page/contact")
def contact():
    return render_template('contact.html', title='Contact')

@main.route("/page/links")
def links():
	links = my_select('table_all','link')
	speciallinks = my_select('table_all','speciallink')
	return render_template('links.html', title='Links', links=links, speciallinks=speciallinks)
	

@main.route("/<string:target_link>", methods=['GET'])
def redirecter(target_link):
	if target_link not in ['page']:
		target_link = clean_input(target_link)
		try:
			target_link = find_url(str(convert_to_base10(target_link)),'speciallink')
			return redirect(b64decode(target_link))
		except:
			target_link = find_url(str(convert_to_base10(target_link)),'link')
			return redirect(b64decode(target_link))
		
		else:
			abort(404)	
			

"""

link = Link(link=link1)
db.session.add(link)
db.session.commit()
flash('Your post has been created!', 'success')
if not find_url(str(convert_to_base10()),'speciallink'): #id için kontrol
if not base64_encode(uzunurl) in select uzunurlbase64 from link: # 
insert  isspecial=1 

If URL in list:
* redirect to URL
longurl = b64encode(b'https://www.test4.com').decode('utf-8')
print(longurl)

"""