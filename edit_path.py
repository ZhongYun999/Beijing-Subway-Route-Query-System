#edit_path.py


def delete_path(graph, line_id):
    """
    根据线路ID删除线路，将所有属于该线路的边的is_active状态设为False。
    :param graph: 图对象，表示整个站点和线路的结构
    :param line_id: 要删除的线路ID
    """
    # 遍历图中所有节点
    for vi in range(graph._vnum):
        edges_to_update = []  # 用于记录需要更新状态的边
        # 获取当前节点vi的所有相邻边
        for edge in graph.out_edges(vi):
            vj, time, distance, edge_line_id, is_active = edge  # 解包边的信息
            if edge_line_id == line_id:
                edges_to_update.append(vj)  # 如果边属于指定线路，将目标节点加入更新列表
        
        # 更新所有相关边的激活状态，将其设为不可用
        for vj in edges_to_update:
            graph.add_edge(vi, vj, float('inf'), float('inf'), line_id, False)


def add_path(graph, line_id):
    """
    根据线路ID恢复线路，将所有属于该线路的边的is_active状态设为True。
    :param graph: 图对象，表示整个站点和线路的结构
    :param line_id: 要恢复的线路ID
    """
    # 遍历图中所有节点
    for vi in range(graph._vnum):
        edges_to_update = []  # 用于记录需要更新状态的边
        # 获取当前节点vi的所有相邻边
        for edge in graph.out_edges(vi):
            vj, time, distance, edge_line_id, is_active = edge  # 解包边的信息
            if edge_line_id == line_id and not is_active:
                edges_to_update.append(vj)  # 如果边属于指定线路且未激活，将目标节点加入更新列表
        
        # 更新所有相关边的激活状态，将其设为可用
        for vj in edges_to_update:
            graph.add_edge(vi, vj, time, distance, line_id, True)

