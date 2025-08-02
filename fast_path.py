#fast_path.py


import heapq
import datetime


def dijkstra_top_k_paths(graph, start, end, k=20, max_path_length=40):
    """
    使用Dijkstra算法计算从起点到终点的最短时间路径，找出用时最短的前k条路径。
    :param graph: 图对象
    :param start: 起始站点索引
    :param end: 终点站点索引
    :param k: 需要找到的路径数量
    :param max_path_length: 路径长度限制
    :return: 最短路径的列表，每个路径包含路径、总时间、总距离和换乘次数
    """
    # 初始化路径列表、优先队列和访问记录
    paths = []  # 存储找到的路径
    pq = [(0, 0, 0, start, [])]  # (总时间, 换乘次数, 总距离, 当前站点, 当前路径)
    visited = {}  # 记录访问过的节点和路径的最佳时间

    while pq and len(paths) < k:
        current_time, transfer_count, current_distance, current_node, current_path = heapq.heappop(pq)
        
        # 如果当前路径长度超过限制，则跳过
        if len(current_path) > max_path_length:
            continue

        if current_node == end:
            # 如果到达终点，将路径加入结果列表
            paths.append((current_path + [end], current_time, current_distance, transfer_count))
            continue
        
        # 如果当前节点和路径长度的时间不优，则跳过
        if (current_node, len(current_path)) in visited and visited[(current_node, len(current_path))] <= current_time:
            continue
        visited[(current_node, len(current_path))] = current_time
        
        # 遍历当前节点的所有相邻节点
        for edge in graph.out_edges(current_node):
            neighbor, travel_time, travel_distance, line_id, is_active = edge
            
            # 判断边是否是激活状态
            if not is_active:
                continue  # 如果边未激活，跳过
            
            new_path = current_path + [current_node]
            new_time = current_time + travel_time
            new_distance = current_distance + travel_distance
            new_transfer_count = transfer_count
            
            # 判断是否换乘
            if current_path:
                last_node = current_path[-1]
                last_line_id = graph.get_edge(last_node, current_node)[3]  # 上一个边的线路
                if last_line_id != line_id:
                    new_transfer_count += 1  # 换乘次数加1
                    new_time += 300  # 换乘时间300秒

            # 计算新的总时间时，包括每个站点的停靠时间（每站1分钟）
            heapq.heappush(pq, (new_time, new_transfer_count, new_distance, neighbor, new_path))
    
    # 按时间排序并返回前k个结果
    paths.sort(key=lambda x: x[1])
    return paths[:k]

def calculate_fare(distance_km):
    """
    根据距离计算轨道交通费用。
    轨道交通价格为：6公里(含)内3元;6公里至12公里(含)4元;12公里至22公里(含)5元;22公里至32公里(含)6元;32公里以上部分，每增加1元可乘坐20公里。
    :param distance_km: 路径的总距离（以公里为单位）
    :return: 费用（人民币元）
    """
    if distance_km <= 6:
        return 3
    elif distance_km <= 12:
        return 4
    elif distance_km <= 22:
        return 5
    elif distance_km <= 32:
        return 6
    else:
        extra_distance = distance_km - 32
        extra_fare = (extra_distance // 20) + 1  # 每超过20公里加1元
        return 6 + extra_fare
    
def calculate_arrival_time(start_time, total_time_minutes):
    """
    根据出发时间和路径总时间，计算到达终点的时间。
    :param start_time: 当前时间（datetime 对象）
    :param total_time_minutes: 路径的总时间（分钟）
    :return: 到达终点的时间（datetime 对象）
    """
    arrival_time = start_time + datetime.timedelta(minutes=total_time_minutes)
    return arrival_time

def query_station_time(graph, station_index_map, start_station, end_station, k=20):
    """
    查询从起点站到终点站的最短时间路径，包含换乘时间和到达时间。
    :param graph: 图对象
    :param station_index_map: 站点名称到索引的映射
    :param start_station: 起始站名称
    :param end_station: 终点站名称
    :param k: 需要找到的路径数量
    """
    # 获取起点和终点的索引
    start = station_index_map.get(start_station)
    end = station_index_map.get(end_station)

    if start is None or end is None:
        print(f"输入的站点 {start_station} 或 {end_station} 不存在。")
        return

    # 调用Dijkstra算法计算最短时间的前k条路径
    top_k_paths = dijkstra_top_k_paths(graph, start, end, k)

    if not top_k_paths:
        print(f"无法从 {start_station} 到 {end_station}。")
        return

    # 选择总时间最短的路径
    best_path = min(top_k_paths, key=lambda x: x[1])

    # 提取路径、总时间、总距离和换乘次数
    path, total_time, total_distance, transfer_count = best_path

    # 计算停车等待时间，每站停1分钟，终点站不停车
    waiting_time = (len(path) - 1) * 60  # 每站停1分钟，60秒

    # 计算最终时间（秒 -> 分钟），并将其转换为整数
    final_time_minutes = int((total_time + waiting_time) / 60)

    # 获取当前时间
    current_time = datetime.datetime.now().replace(second=0, microsecond=0)

    # 计算预计到达时间
    arrival_time = calculate_arrival_time(current_time, final_time_minutes)

    # 输出路径和总时间
    print("\n从 {} 到 {} 的最短时间路径为：".format(start_station, end_station))

    # 获取起点与第二站之间的边
    start_line_id = None
    if len(path) > 1:
        second_node = path[1]
        start_edge = graph.get_edge(start, second_node)
        start_line_id = start_edge[3]  # 获取起点到第二站的线路 ID

    # 打印起点线路信息
    if start_line_id is not None:
        print(f"乘坐地铁 {start_line_id} ")

    # 用于跟踪上一条边的线路 ID
    last_line_id = start_line_id

    for i, idx in enumerate(path):
        station_name = list(station_index_map.keys())[list(station_index_map.values()).index(idx)]

        # 如果不是第一个站点，检查是否需要换乘
        if i > 0:
            prev_node = path[i - 1]
            current_edge = graph.get_edge(prev_node, idx)
            current_line_id = current_edge[3]  # 当前边的线路 ID
            
            if last_line_id and last_line_id != current_line_id:
                print("\n换乘线路：{}".format(current_line_id))
                
            last_line_id = current_line_id

        # 打印站点名
        if idx == path[-1]:  # 如果是最后一个站点
            print(station_name)
        else:
            print(f"{station_name} \n↓")

    # 将总距离从米转换为公里
    total_distance_km = total_distance / 1000

    # 计算乘车费用
    fare = calculate_fare(total_distance_km)

    print(f"\n总时间：{final_time_minutes} 分钟")
    print(f"总距离：{total_distance_km:.2f} 公里")
    print(f"乘车费用：{fare} 元")

    # 输出当前时间和预计到达时间，精确到分钟
    print(f"当前时间：{current_time.strftime('%H:%M')}")
    print(f"预计到达时间：{arrival_time.strftime('%H:%M')}")
