import csv  # 导入csv文件
import py2neo  # 导入py2neo库
from py2neo import Graph, Node, Relationship, NodeMatcher

g = Graph("http://localhost:7474", username="neo4j", password="shencyg123")  # 连接neo4j，将'xxx'分别改为你的用户名和密码
g.delete_all()  # 清除neo4j中原有的结点等所有信息

with open('H:\Graduation Design\Neo4j\case.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for item in reader:
        # if reader.line_num==1:
        #    continue
        print("当前行数：", reader.line_num, "当前内容：", item)
        #创建节点以及节点的属性
        accident = Node("Accident", name=item[0],time=item[12],place=item[13],measure=item[14],evolution=item[15],number=item[16],loss=item[17])
        structure = Node("Structure", value=item[1])
        material = Node("Material",value=item[2])
        part = Node("Part",value=item[3])
        season = Node("Season",value=item[4])
        period = Node("Period",value=item[5])
        area = Node("Area",value=item[6])
        location = Node("Location",value=item[7])
        level = Node("Level",value=item[8])
        types = Node("Types",value=item[9])
        reason = Node("Reason",value=item[10])
        degree = Node("Degree",value=item[11])
        #创建关系
        relation1 = Relationship(accident, "bridge structure of", structure)
        relation2 = Relationship(accident, "bridge materials of", material)
        relation3 = Relationship(accident, "damaged parts of the bridge", part)
        relation4 = Relationship(accident, "period of accident occurrence", period)
        relation5 = Relationship(accident, "accident area of", area)
        relation6 = Relationship(accident, "accident location of", location)
        relation7 = Relationship(accident, "level of accident location", level)
        relation8 = Relationship(accident, "accident type of", types)
        relation9 = Relationship(accident, "accident cause of", reason)
        relation10 = Relationship(accident, "accident severity of", degree)
        relation11 = Relationship(accident, "accident season of", season)
        #将节点和关系添加到图谱中
        g.merge(accident, "Accident", "name")
        g.merge(structure, "Structure", "value")
        g.merge(material, "Material", "value")
        g.merge(part, "Part", "value")
        g.merge(season, "Season", "value")
        g.merge(period, "Period", "value")
        g.merge(area, "Area", "value")
        g.merge(location, "Location", "value")
        g.merge(level, "Level", "value")
        g.merge(types, "Types", "value")
        g.merge(reason, "Reason", "value")
        g.merge(degree, "Degree", "value")
     #   for i in range(1,11):
        g.merge(relation1)
        g.merge(relation2)
        g.merge(relation3)
        g.merge(relation4)
        g.merge(relation5)
        g.merge(relation6)
        g.merge(relation7)
        g.merge(relation8)
        g.merge(relation9)
        g.merge(relation10)
        g.merge(relation11)
    # 注意缩进
