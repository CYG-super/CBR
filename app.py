from flask import Flask, session, g, render_template, request,jsonify
from blueprints import config
from blueprints.exts import db, mail
from blueprints.models import UserModel
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate
from casematching.model import hsimilarity,zsimilarity,gsolution
from casematching.case import allcase,detailed_info
import csv
from Neo4j.query_graph import query


app = Flask(__name__)


# 绑定配置文件
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(auth_bp)


# flask db init：只需要执行一次
# flask db migrate：将orm模型生成迁移脚本
# flask db upgrade：将迁移脚本映射到数据库中

@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


# http://127.0.0.1:5000 首页
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/introduction', methods=['GET', 'POST'])
def introduction():
    return render_template('introduction.html')

@app.route('/case', methods=['GET', 'POST'])
def case():
    return render_template('case.html')

@app.route('/case/basic-info', methods=['GET', 'POST'])
def get_basic_data():
    json_data = allcase()
    return json_data

@app.route('/case/detailed-info', methods=['GET', 'POST'])
def get_detailed_data():
    json_data = detailed_info()
    return json_data


@app.route('/find', methods=['GET', 'POST'])
def find():
    return render_template('find.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add.html')

@app.route('/add/submit_form', methods=['GET', 'POST'])
def add_form():
    bridge_structure = request.form['bridge_structure']
    bridge_material = request.form['bridge_material']
    accident_location = request.form['accident_location']
    accident_season = request.form['accident_season']
    accident_time = request.form['accident_time']
    accident_region = request.form['accident_region']
    accident_site = request.form['accident_site']
    accident_area_level = request.form['accident_area_level']
    incident_category = request.form['incident_category']
    incident_reason = request.form['incident_reason']
    incident_severity = request.form['incident_severity']
    decision = request.form['decision']
    event_name = request.form['event_name']
    event_time = request.form['event_time']
    event_location = request.form['event_location']
    event_chain = request.form['event_chain']

    mapping1 = {'基本完好': 0, '轻微损伤': 1, '中度损伤': 2, '严重损伤': 3, '坍塌': 4}
    if incident_severity in mapping1:
        numeric_severity = mapping1[incident_severity]
        print(numeric_severity)
    else:
        print("无法找到对应的数字值")

    mapping2 = {'凌晨 (00:00—5:00)': 0, '清晨 (5:00-6:00)': 1, '早晨 (6:00-8:00)': 2, '上午 (8:00—11:00)': 3,
                '中午 (11:00—13:00)': 4, "下午 (13:00—17:00)": 5, "傍晚 (17:00—18:00)": 6, "晚上 (18:00—24:00)": 7}
    if accident_time in mapping2:
        numeric_time = mapping2[accident_time]
        print(numeric_time)
    else:
        print("无法找到对应的数字值")
    # 定义要写入CSV的行数据
    row_data = [event_name, bridge_structure, bridge_material, accident_location,
                accident_season, numeric_time, accident_region, accident_site,
                accident_area_level, incident_category, incident_reason,
                numeric_severity, event_time, event_location, decision, event_chain]

    csv_file = 'D:\\CBR-YG\\CBR\\casematching\\casetofind.csv'

    # 打开CSV文件，以追加模式写入数据
    with open(csv_file, 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row_data)

    return "ok"




@app.route('/solution', methods=['GET', 'POST'])
def solution():
    return render_template('solution.html')


@app.route('/get_all_relation', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')

@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    # print(name)
    json_data=query(str(name))
    return jsonify(json_data)

@app.route('/calculate_similarity', methods=['GET','POST'])
def calculate_similarity():
    incident_category = request.form['incident_category']
    incident_reason = request.form['incident_reason']
    incident_severity = request.form['incident_severity']

    # 将值存储在会话中
    session['incident_category'] = incident_category
    session['incident_reason'] = incident_reason
    session['incident_severity'] = incident_severity
    
    rank_core=request.form['rank_core']
    # print(rank_core)

    json_data = hsimilarity(str(incident_category),str(incident_reason),str(incident_severity),rank_core)
    # print(json_data)
    return json_data

@app.route('/comprehensive_similarity', methods=['GET','POST'])
def comprehensive_similarity():
    bridge_structure = request.form['bridge_structure']
    bridge_material = request.form['bridge_material']
    accident_location = request.form['accident_location']
    accident_season = request.form['accident_season']
    accident_time = request.form['accident_time']
    accident_region = request.form['accident_region']
    accident_site = request.form['accident_site']
    accident_area_level = request.form['accident_area_level']
    rank_zh=request.form['rank_zh']

    # 将值存储在会话中
    session['bridge_structure'] = bridge_structure
    session['bridge_material'] = bridge_material
    session['accident_location'] = accident_location
    session['accident_season'] = accident_season
    session['accident_time'] = accident_time
    session['accident_region'] = accident_region
    session['accident_site'] = accident_site
    session['accident_area_level'] = accident_area_level

    json_data = zsimilarity(bridge_structure,bridge_material,accident_location,accident_season,accident_time,accident_region,accident_site,accident_area_level,rank_zh
)
    # print(json_data)
    return json_data

@app.route('/get_solution', methods=['GET', 'POST'])
def get_solution():
    json_data = gsolution()
    return json_data

@app.route('/solution/submit_form',methods=['GET','POST'])
def solve_solution():
    # 获取表单提交的值
    decision = request.form['decision']
    event_name = request.form['event_name']
    event_time = request.form['event_time']
    event_location = request.form['event_location']
    event_chain = request.form['event_chain']
    # print(decision)
    # print(decision,event_name,event_time,event_location,event_chain)
    # 从session中获取之前的值
    incident_category = session.get('incident_category')
    incident_reason = session.get('incident_reason')
    incident_severity = session.get('incident_severity')
    bridge_structure = session.get('bridge_structure')
    bridge_material = session.get('bridge_material')
    accident_location = session.get('accident_location')
    accident_season = session.get('accident_season')
    accident_time = session.get('accident_time')
    accident_region = session.get('accident_region')
    accident_site = session.get('accident_site')
    accident_area_level = session.get('accident_area_level')

    mapping1 = {'基本完好': 0, '轻微损伤': 1, '中度损伤': 2, '严重损伤': 3, '坍塌': 4}
    if incident_severity in mapping1:
        numeric_severity = mapping1[incident_severity]
        print(numeric_severity)
    else:
        print("无法找到对应的数字值")

    mapping2 = {'凌晨 (00:00—5:00)': 0, '清晨 (5:00-6:00)': 1, '早晨 (6:00-8:00)': 2, '上午 (8:00—11:00)': 3,
               '中午 (11:00—13:00)': 4, "下午 (13:00—17:00)": 5, "傍晚 (17:00—18:00)": 6, "晚上 (18:00—24:00)": 7}
    if accident_time in mapping2:
        numeric_time = mapping2[accident_time]
        print(numeric_time)
    else:
        print("无法找到对应的数字值")
    # 定义要写入CSV的行数据
    row_data = [event_name, bridge_structure, bridge_material, accident_location,
                accident_season, numeric_time, accident_region, accident_site,
                accident_area_level, incident_category, incident_reason,
                numeric_severity, event_time, event_location, decision, event_chain]

    csv_file = 'D:\\CBR-YG\\CBR\\casematching\\casetofind.csv'

    # 打开CSV文件，以追加模式写入数据
    with open(csv_file, 'a',encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row_data)

    return "ok"


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
