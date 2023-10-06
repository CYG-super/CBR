import numpy as np
import pandas as pd
global_df = None
global_df1 = None
def hsimilarity(incident_category, incident_reason, incident_severity,rank_core):
    global global_df  # 声明global_df为全局变量
    # 读取CSV文件
    d = pd.read_csv('D:\\CBR-YG\\CBR\\casematching\\casetofind.csv')
    rank1 = int(rank_core)
    # 目标案例属性值
    date = {
        "事故分类": incident_category,
        "事故原因": incident_reason,
        "事故严重程度": incident_severity,
    }
    # 案例属性权重
    date1 = {
        "事故分类": 0.1762,
        "事故原因": 0.4441,
        "事故严重程度": 0.2797,

    }

    mapping =  {'基本完好': 0, '轻微损伤': 1, '中度损伤': 2, '严重损伤': 3, '坍塌': 4}
    if date["事故严重程度"] in mapping:
        numeric_value = mapping[date["事故严重程度"]]
    else:
        print("无法找到对应的数字值")

    df = pd.DataFrame(d)

    df['事故分类'] = df['事故分类'].eq(date['事故分类']) * 1 * date1['事故分类']
    df['事故原因'] = df['事故原因'].eq(date['事故原因']) * 1 * date1['事故原因']
    df['事故严重程度'] = (1 - (df['事故严重程度'] - numeric_value).abs() / 4) * date1['事故严重程度']

    df["核心层相似度"] = np.nan
    for index, row in df.iterrows():
        df.loc[index, "核心层相似度"] = df.loc[index, "事故分类"] + df.loc[index, "事故原因"] + df.loc[index, "事故严重程度"]
    df1 = df.sort_values(by="核心层相似度", ascending=False).head(rank1)
    global_df = df1
    df1 = df1[['事故名称',"事故分类", "事故原因", "事故严重程度", "核心层相似度"]]
    # 将列名转换为中文
    df1.columns = ['事故名称','事故分类', '事故原因', '事故严重程度', '核心层相似度']

    # 将DataFrame转换为JSON字符串
    json_data = df1.to_json(orient='records', force_ascii=False)
    # print(json_data)
    return json_data

def zsimilarity(bridge_structure,bridge_material,accident_location,accident_season,accident_time,accident_region,accident_site,accident_area_level,rank_zh):
    global global_df  # 声明global_df为全局变量
    global global_df1
    rank2=int(rank_zh)
    date = {
        "桥梁结构": bridge_structure,
        "桥梁材料": bridge_material,
        "事故发生部位": accident_location,
        "事故发生季节": accident_season,
        "事故发生时段": accident_time,
        "事故发生区域": accident_region,
        "事故发生地点": accident_site,
        "事故发生地区级别": accident_area_level
    }
    date1 = {
         "桥梁结构": 0.0103,"桥梁材料": 0.0099, "事故发生部位": 0.0151, "事故发生季节": 0.0177,
        "事故发生时段": 0.0217, "事故发生区域": 0.0113, "事故发生地点": 0.0059, "事故发生地区级别": 0.0081
    }
    mapping = {'凌晨 (00:00—5:00)': 0, '清晨 (5:00-6:00)': 1, '早晨 (6:00-8:00)': 2, '上午 (8:00—11:00)': 3,
               '中午 (11:00—13:00)': 4,"下午 (13:00—17:00)":5,"傍晚 (17:00—18:00)":6,"晚上 (18:00—24:00)":7}
    if date["事故发生时段"] in mapping:
        numeric_value = mapping[date["事故发生时段"]]
    else:
        print("无法找到对应的数字值")
    df1 = global_df
    df1['桥梁结构'] = df1['桥梁结构'].eq(date['桥梁结构']) * 0.0103
    df1['桥梁材料'] = df1['桥梁材料'].eq(date["桥梁材料"]) * 0.0099
    df1['事故发生部位'] = df1['事故发生部位'].eq(date["事故发生部位"]) * 0.0151
    df1['事故发生季节'] = df1['事故发生季节'].eq(date["事故发生季节"]) * 0.0177
    df1['事故发生时段'] = (1 - (df1['事故发生时段'] - numeric_value).abs() / 7) * 0.0217
    df1['事故发生区域'] = df1['事故发生区域'].eq(date['事故发生区域']) * 0.0113
    df1['事故发生地点'] = df1['事故发生地点'].eq(date["事故发生地点"]) * 0.0059
    df1['事故发生地区级别'] = df1['事故发生地区级别'].eq(date["事故发生地区级别"]) * 0.0081

#一般层相似度计算
    df1["一般层相似度"] = np.nan
    for index, row in df1.iterrows():
      df1.loc[index, "一般层相似度"] = df1.loc[index, "桥梁结构"]+ df1.loc[index, "桥梁材料"] + df1.loc[index, "事故发生部位"]+ \
                                df1.loc[index, "事故发生季节"]+ df1.loc[index, "事故发生时段"]+ df1.loc[index, "事故发生区域"]\
                                + df1.loc[index, "事故发生地点"]+ df1.loc[index, "事故发生地区级别"]
    #总相似度计算并排序
    df1["总相似度"] = np.nan
    for index, row in df1.iterrows():
      df1.loc[index, "总相似度"] = df1.loc[index, "核心层相似度"]+ df1.loc[index, "一般层相似度"]
    df1 = df1.sort_values(by="总相似度",ascending=False).head(rank2)
    global_df1 = df1
    df1 = df1[["事故名称",'桥梁结构','桥梁材料','事故发生部位',"事故发生季节", "事故发生时段","事故发生区域","事故发生地点","事故发生地区级别","核心层相似度",'一般层相似度','总相似度']]
    # 将列名转换为中文
    df1.columns = [ "事故名称",'桥梁结构','桥梁材料','事故发生部位',"事故发生季节", "事故发生时段","事故发生区域","事故发生地点","事故发生地区级别","核心层相似度",'一般层相似度','总相似度']

    # 将DataFrame转换为JSON字符串
    json_data = df1.to_json(orient='records', force_ascii=False)
    print(json_data)
    return json_data
#


def gsolution():
    global global_df1
    df=global_df1
    df = df[["事故名称","事故具体时间","事故具体地点","事故响应措施","事故响应链","总相似度"]]
    df.colimus = ["事故名称","事故具体时间","事故具体地点","事故响应措施","事故响应链",'总相似度']
    json_data = df.to_json(orient='records', force_ascii=False)
    # print(json_data)
    return json_data
# hsimilarity("碰撞事故",'船只碰撞','坍塌',10)
# zsimilarity('梁式桥','钢筋混凝土桥','桥面','春','下午 (13:00—17:00)','东北区域','安徽六安','乡镇',5)
# gsolution()