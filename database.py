import sqlite3
from datetime import date, timedelta
from typing import List, Dict, Optional

class DataBase:
	def __init__(self, filename='birthdays.db'):
		self.conn = sqlite3.connect(filename)
		self.cur = self.conn.cursor()

		self.cur.execute("""
			CREATE TABLE IF NOT EXISTS birthdays (
				user_id INTEGER,
				name TEXT,
				birth_date TEXT,
				PRIMARY KEY (user_id, name)
			)
			"""
		)

		self.conn.commit()

	def add_birthday(self, user_id: int, name: str, birth_date: str) -> None:
		try:
			self.cur.execute(
				'INSERT OR REPLACE INTO birthdays VALUES (?, ?, ?)', 
				(user_id, name, birth_date)
			)
			self.conn.commit()

			return 200
		except:
			return 500


	def delete_birthday(self, user_id: int, name: str):
		try:
			self.cur.execute('DELETE FROM birthdays WHERE user_id = ? AND name = ?', (user_id, name))
			self.conn.commit()

			return self.cur.rowcount > 0
		except:
			return None

	def get_birthdays(self, user_id: int) -> List[Dict[str, str]]:
		self.cur.execute('SELECT name, birth_date FROM birthdays WHERE user_id = ?', (user_id,))
		rows = self.cur.fetchall()

		return [{'name': row[0], 'birth_date': row[1]} for row in rows]

	def data_notif(self):
		self.cur.execute('SELECT DISTINCT user_id, name, birth_date FROM birthdays')
		
		return self.cur.fetchall()

	def __del__(self):
		self.conn.close()

