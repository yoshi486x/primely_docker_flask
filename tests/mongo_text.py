import pprint as pp
import datetime

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['test_database']

stack1 = {
    'attendances': {
        '年休取得日数': 1.0,
        '所定内勤務時間数': 139.3,
        '所定勤務日数': 19,
        '所定勤務時間数': 147.15,
        '時間外勤務時間数(1.25)': 31.35,
        '深夜勤務時間数(0.25)': 1.45
        },
    'deductions': {
        '健康保険料': 13600,
        '厚生年金保険料': 29280,
        '所得税': 7290,
        '社食利用料': 8727,
        '雇用保険料': 943
        }
}

# stack2 = {
#     'name': 'customer2',
#     'pip': ['go', 'java'],
#     'data': datetime.datetime.utcnow()
# }

db_stacks = db.stacks
stack_id = db_stacks.insert_one(stack1).inserted_id
print(stack_id, type(stack_id))
print("###############")
pp.pprint(db_stacks.find_one({'_id': stack_id}))
