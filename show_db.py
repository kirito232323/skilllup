import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
print('Tables:')
for row in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print(row[0])
print('\nUsers:')
for row in c.execute('SELECT id, email, first_name, last_name, account_role, is_staff, is_superuser FROM core_skillupuser'):
    print(row)
print('\nJob roles:')
for row in c.execute('SELECT id, role_name FROM core_jobrole'):
    print(row)
print('\nRecommendations:')
for row in c.execute('SELECT id, user_id, module_id, status FROM core_recommendation'):
    print(row)
conn.close()
