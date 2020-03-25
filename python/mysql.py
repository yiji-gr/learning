import MySQLdb
import random

db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="xxx")

cursor = db.cursor()
table_name = "yyy"

# ---------create table-------------------
sql = f"""
	create table if not exists {table_name}(
		id int not null auto_increment,
		price int not null,
		num int not null,
		total int,
		primary key (id))
	"""
cursor.execute(sql)

# ---------insert into table-------------------
# for i in range(1, 11):
# 	sql = f"insert into {table_name}(price, num) values({random.randint(0,100)}, {random.randint(0,100)})"
# 	try:
# 		cursor.execute(sql)
# 		db.commit()
# 	except MySQLdb.Error as e:
# 		db.rollback()
# 		try:
# 			print(f"Error {e.args[0]}:{e.args[1]}")
# 		except IndexError:
# 			print("MySQL Error:%s" % str(e))

# ---------select from table-------------------
# sql = f"select * from {table_name} where price > 50"
# try:
# 	cursor.execute(sql)
# 	result = cursor.fetchall()
# 	for row in result:
# 		print(f"id={row[0]}, price={row[1]}, num={row[2]}, total={row[3]}")
# except MySQLdb.Error as e:
# 	db.rollback()
# 	try:
# 		print(f"Error {e.args[0]}:{e.args[1]}")
# 	except IndexError:
# 		print("MySQL Error:%s" % str(e))

# ---------update table-------------------
# sql = f"update {table_name} set total = price * num where price < 50"
# try:
# 	cursor.execute(sql)
# 	db.commit()
# except MySQLdb.Error as e:
# 	db.rollback()
# 	try:
# 		print(f"Error {e.args[0]}:{e.args[1]}")
# 	except IndexError:
# 		print("MySQL Error:%s" % str(e))

# ---------delete from table-------------------
sql = f"delete from {table_name} where num % 2 = 0"
try:
	cursor.execute(sql)
	db.commit()
except MySQLdb.Error as e:
	db.rollback()
	try:
		print(f"Error {e.args[0]}:{e.args[1]}")
	except IndexError:
		print("MySQL Error:%s" % str(e))

db.close()