from django.db import connection

def setup():
	cursor = connection.cursor()

	cursor.execute("UPDATE django_site SET DOMAIN = 'localhost:8000', name = 'Sharebear' WHERE id=1;")
	
	cursor.execute("INSERT INTO socialaccount_socialapp (provider, name, secret, client_id, 'key');")

	cursor.execute("VALUES ('facebook', 'Facebook', 'd72b3941e320be583285bb00a28aa226', '357482904425644', '');")

	cursor.execute("INSERT INTO socialaccount_socialapp_sites (socialapp_id, site_id) VALUES (1,1);")
	row = cursor.fetchone()
	return row

setup()