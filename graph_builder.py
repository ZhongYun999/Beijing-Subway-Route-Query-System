#graph_builder.py


from Graph import GraphAL


def stations_to_graph(stations):
    """
    将站点信息转换为图结构。   
    :param stations: 包含所有站点信息的字典，其中每个站点信息包含边的信息
    :return: 图对象和站点名称到索引的映射
    """
    station_names = list(stations.keys())
    station_index_map = {name: i for i, name in enumerate(station_names)}
    
    # 创建一个图，边的权重包含时间、距离和激活状态
    graph = GraphAL(unconn=float('inf'))
    
    # 添加所有顶点
    for _ in station_names:
        graph.add_vertex()
    
    # 添加所有边，边的权重使用时间、距离和线路信息，激活状态默认为True
    for station_name, station_obj in stations.items():
        vi = station_index_map[station_name]
        
        for edge in station_obj.edges:
            vj = station_index_map[edge.station]
            time = edge.time  # 时间
            distance = edge.distance  # 距离
            line_id = edge.line_id  # 线路名称
            is_active = True  # 初始时所有边都设为激活
            graph.add_edge(vi, vj, time, distance, line_id, is_active)
    
    return graph, station_index_map
