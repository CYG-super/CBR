from py2neo import Graph
graph = Graph('bolt://localhost:7687', username='neo4j', password='123456')
LIST = [0,4,11,10,9,8,7,6,5,3,2,1]
CATEGORY_LIST = {"Accident":0,"Structure":1, "Material":2, "Part":3, "Season":4, "Period":5, "Area":6,"Location":7,"Level":8,"types":9,"Reason":10,"Degree":11}
CATEGORY_LIST1 = [0,1,2,3,4,5,6,7,8,9,10,11]
Link_LIST = ["事故发生季节",'事故严重程度','事故原因','事故类型','事故发生地点等级','事故发生地点','事故发生区域','事故发生时段','桥梁受损部位','桥梁材料','桥梁结构']

def query(name):
    cypher_query = """
        MATCH (n)-[r]->(m)
        WHERE n.name = "%s"
        RETURN n, r, m
        """%name

    result = graph.run(cypher_query)
    nodes = []
    links = []

    for record in result:
        source = record['n']
        # print(source)
        target = record['m']
        # print(target)
        # rel = record['r']
        # print(rel)
        # i=0
        nodes.append({
                    'name': source['name'],
                    'id': source.identity,
                })

        nodes.append({
                    'name': target['value'],
                    'id': target.identity,
                })

        links.append({
                'source': source.identity,
                'target': target.identity,
            })

    my_set = set(item['id'] for item in nodes)
    result = [item for item in nodes if item['id'] in my_set and not my_set.discard(item['id'])]
    # print(result)
    i=0
    for re in result:
        # print(i)
        re['category']=LIST[i]
        i+=1
    j=0
    for link in links:
        link['value'] = Link_LIST[j]
        j+=1

    json_data = {
        'nodes': result,
        'links': links
    }
    # print(json_data)
    return json_data




