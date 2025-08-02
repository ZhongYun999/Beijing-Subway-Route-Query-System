#convenient_path


import heapq
import datetime


def dijkstra_min_transfer_paths(graph, start, end, k=20, max_path_length=40):
    """
    使用Dijkstra算法计算从起点到终点的最少换乘路径，找出换乘次数最少的前k名
    :param graph: 图对象，表示站点和线路的网络结构
    :param start: 起始站点索引
    :param end: 终点站点索引
    :param k: 需要找到的最少换乘路径的数量
    :param max_path_length: 路径长度限制，防止路径过长
    :return: 包含最少换乘路径的列表，每个路径包含路径、总时间、总距离和换乘次数
    """
    # 初始化优先队列，路径列表和访问过的节点记录
    paths = []
    pq = [(0, 0, 0, start, [])]  # 优先队列元素格式为 (换乘次数, 总时间, 总距离, 当前站点, 当前路径)
    visited = {}  # 记录已访问节点和对应路径的最少换乘次数

    while pq and len(paths) < k:
        # 取出优先队列中的元素，优先级是换乘次数最少的路径
        transfer_count, current_time, current_distance, current_node, current_path = heapq.heappop(pq)

        # 如果当前路径超过了最大限制，则跳过
        if len(current_path) > max_path_length:
            continue

        # 如果到达终点，将路径添加到结果集
        if current_node == end:
            paths.append((current_path + [end], current_time, current_distance, transfer_count))
            continue

        # 如果当前节点已访问且换乘次数不比之前少，跳过该路径
        if (current_node, len(current_path)) in visited and visited[(current_node, len(current_path))] <= transfer_count:
            continue
        visited[(current_node, len(current_path))] = transfer_count

        # 遍历当前节点的所有相邻节点
        for edge in graph.out_edges(current_node):
            neighbor, travel_time, travel_distance, line_id, is_active = edge  # 取出相邻边信息
            
            # 如果边没有激活（不可用），则跳过
            if not is_active:
                continue

            # 构建新路径
            new_path = current_path + [current_node]
            new_time = current_time + travel_time
            new_distance = current_distance + travel_distance
            new_transfer_count = transfer_count

            # 判断是否发生换乘
            if current_path:
                last_node = current_path[-1]
                last_line_id = graph.get_edge(last_node, current_node)[3]  # 获取前一站的线路ID
                if last_line_id != line_id:
                    new_transfer_count += 1  # 换乘次数加1
                    new_time += 300  # 每次换乘增加5分钟

            # 将新路径信息加入优先队列
            heapq.heappush(pq, (new_transfer_count, new_time, new_distance, neighbor, new_path))

    # 按换乘次数排序，并返回前k个路径
    paths.sort(key=lambda x: x[3])
    return paths[:k]


def choose_best_path(paths):
    """
    从路径列表中挑选最佳路径，优先考虑换乘次数，如果相同则比较总时间和总距离
    :param paths: 包含路径、总时间、总距离和换乘次数的路径列表
    :return: 最佳路径
    """
    # 优先根据换乘次数排序，若相同则比较总时间，再比较总距离
    return min(paths, key=lambda x: (x[3], x[1], x[2]))


def calculate_fare(distance_km):
    """
    根据路径的总距离计算交通费用
    :param distance_km: 总距离（公里）
    :return: 费用（人民币元）
    """
    # 不同距离范围对应不同的费用标准
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
    计算从出发时间开始的到达时间
    :param start_time: 出发时间（datetime 对象）
    :param total_time_minutes: 路径的总时间（分钟）
    :return: 到达时间（datetime 对象）
    """
    return start_time + datetime.timedelta(minutes=total_time_minutes)


def query_station_transfer(graph, station_index_map, start_station, end_station, k=20):
    """
    查询从起点到终点的最少换乘路径，输出路径、时间和费用等信息
    :param graph: 图对象，包含站点和线路信息
    :param station_index_map: 站点名称到索引的映射字典
    :param start_station: 起始站名称
    :param end_station: 终点站名称
    :param k: 查询的最少换乘路径数量
    """
    # 获取起点和终点的索引
    start = station_index_map.get(start_station)
    end = station_index_map.get(end_station)

    if start is None or end is None:
        print(f"输入的站点 {start_station} 或 {end_station} 不存在。")
        return

    # 调用Dijkstra算法计算最少换乘的前k条路径
    top_k_paths = dijkstra_min_transfer_paths(graph, start, end, k)

    if not top_k_paths:
        print(f"无法从 {start_station} 到 {end_station}。")
        return

    # 选择换乘次数最少的最佳路径
    best_path = choose_best_path(top_k_paths)

    # 提取路径、总时间、总距离和换乘次数
    path, total_time, total_distance, transfer_count = best_path

    # 计算停车等待时间，每站停1分钟，终点站不停车
    waiting_time = (len(path) - 1) * 60  # 每站停1分钟

    # 计算最终时间，秒转换为分钟
    final_time_minutes = int((total_time + waiting_time) / 60)

    # 获取当前时间
    current_time = datetime.datetime.now().replace(second=0, microsecond=0)

    # 计算预计到达时间
    arrival_time = calculate_arrival_time(current_time, final_time_minutes)

    # 输出路径信息
    print(f"\n从 {start_station} 到 {end_station} 的最少换乘路径为：")

    # 获取起点到第二站的线路信息
    start_line_id = None
    if len(path) > 1:
        second_node = path[1]
        start_edge = graph.get_edge(start, second_node)
        start_line_id = start_edge[3]  # 获取线路ID

    # 打印起点的线路信息
    if start_line_id is not None:
        print(f"乘坐地铁 {start_line_id} ")

    last_line_id = start_line_id  # 用于记录上一条线路ID

    # 输出路径站点信息
    for i, idx in enumerate(path):
        station_name = list(station_index_map.keys())[list(station_index_map.values()).index(idx)]

        if i > 0:
            prev_node = path[i - 1]
            current_edge = graph.get_edge(prev_node, idx)
            current_line_id = current_edge[3]  # 当前线路ID

            if last_line_id and last_line_id != current_line_id:
                print(f"\n换乘线路：{current_line_id}")
                
            last_line_id = current_line_id

        # 打印站点名
        if idx == path[-1]:
            print(station_name)
        else:
            print(f"{station_name} \n↓")

    # 计算总距离并转换为公里
    total_distance_km = total_distance / 1000

    # 计算乘车费用
    fare = calculate_fare(total_distance_km)

    # 输出总时间、总距离、费用和到达时间
    print(f"\n总时间：{final_time_minutes} 分钟")
    print(f"总距离：{total_distance_km:.2f} 公里")
    print(f"乘车费用：{fare} 元")
    print(f"当前时间：{current_time.strftime('%H:%M')}")
    print(f"预计到达时间：{arrival_time.strftime('%H:%M')}")
