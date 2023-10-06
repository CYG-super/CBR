import pandas as pd

def allcase():
    d = pd.read_csv('D:\\CBR-YG\\CBR\\casematching\\casetofind.csv')
    df = pd.DataFrame(d)

    # 定义事故严重程度和事故发生时段的映射字典
    severity_mapping = {0: '基本完好', 1: '轻微损伤', 2: '中度损伤', 3: '严重损伤', 4: '坍塌'}
    period_mapping = {0: '凌晨 (00:00—5:00)', 1: '清晨 (5:00-6:00)', 2: '早晨 (6:00-8:00)', 3: '上午 (8:00—11:00)',
                      4: '中午 (11:00—13:00)', 5: '下午 (13:00—17:00)', 6: '傍晚 (17:00—18:00)', 7: '晚上 (18:00—24:00)'}

    # 替换事故严重程度和事故发生时段的数字为对应的文字
    df['事故严重程度'] = df['事故严重程度'].map(severity_mapping)
    df['事故发生时段'] = df['事故发生时段'].map(period_mapping)

    df = df[
        ["事故名称", "桥梁结构", "桥梁材料", "事故发生部位", "事故发生季节", "事故发生时段", "事故发生区域", "事故发生地点", "事故发生地区级别", "事故分类", "事故原因",
         "事故严重程度"]]
    df.columns = ["事故名称", "桥梁结构", "桥梁材料", "事故发生部位", "事故发生季节", "事故发生时段", "事故发生区域", "事故发生地点", "事故发生地区级别",
                  "事故分类", "事故原因", "事故严重程度"]

    json_data = df.to_json(orient='records', force_ascii=False)
    # print(json_data)
    return json_data

def detailed_info():
    d = pd.read_csv('D:\\CBR-YG\\CBR\\casematching\\casetofind.csv')
    df = pd.DataFrame(d)
    df = df[["事故名称","事故具体时间","事故具体地点","事故响应措施","事故响应链"]]
    df.columns = ["事故名称","事故具体时间","事故具体地点","事故响应措施","事故响应链"]
    json_data = df.to_json(orient='records', force_ascii=False)
    # print(json_data)
    return json_data
# detailed_info()


# allcase()