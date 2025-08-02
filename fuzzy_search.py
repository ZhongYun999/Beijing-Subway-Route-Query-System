# fuzzy_search.py


from fuzzywuzzy import process


def fuzzy_search(query, choices):
    """
    使用模糊匹配寻找最接近的项。    
    :param query: 用户输入的查询字符串
    :param choices: 可供匹配的候选项列表
    :return: 最匹配的结果，或 None 如果没有匹配结果
    """
    result = process.extractOne(query, choices)
    return result[0] if result else None

def get_all_lines(stations):
    """
    从所有站点的 `lines` 字段和 `edges` 中提取出所有可能的地铁线路名称。
    
    :param stations: 站点数据的字典
    :return: 包含所有地铁线路名称的集合
    """
    lines_set = set()
    for station_name, station_obj in stations.items():
        # 从每个站点的 `lines` 列表中提取线路
        lines_set.update(station_obj.lines)
        
        # 从每个站点的 `edges` 中提取线路的 `line_id`
        for edge in station_obj.edges:
            lines_set.add(edge.line_id)
    
    return list(lines_set)
