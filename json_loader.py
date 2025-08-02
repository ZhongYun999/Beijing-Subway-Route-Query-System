#json_loader.py


import json


class StationEdge:
    def __init__(self, station, line, distance, speed, time):
        """
        初始化站点边的属性。
        :param station: 目标站点名称
        :param line: 线路 ID
        :param distance: 边的距离（单位：米）
        :param speed: 行驶速度（单位：米/秒）
        :param time: 行驶时间（单位：秒）
        """
        self.station = station
        self.line = line
        self.distance = distance
        self.speed = speed
        self.time = time
        self.line_id = line


class Station:
    def __init__(self, name, edges, lines, line_siz):
        """
        初始化站点的属性。
        :param name: 站点名称
        :param edges: 站点的所有边（即邻接边）
        :param lines: 站点所在的所有线路
        :param line_siz: 站点的线路大小
        """
        self.name = name
        self.edges = edges
        self.lines = lines
        self.line_siz = line_siz


def json_to_stations(json_file):
    """
    从 JSON 文件中加载站点数据并转换为站点对象。
    :param json_file: 包含站点数据的 JSON 文件路径
    :return: 一个字典，其中键为站点名称，值为 Station 对象
    """
    # 打开并读取 JSON 文件
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    stations = {}
    # 遍历 JSON 数据中的每个站点
    for station_name, station_info in json_data.items():
        # 创建 StationEdge 对象的列表
        edges = [
            StationEdge(
                edge['station'],  # 目标站点
                edge['line'],     # 线路 ID
                edge['distance'], # 边的距离
                edge['speed'],    # 行驶速度
                edge['time']      # 行驶时间
            )
            for edge in station_info['edge']
        ]

        # 创建 Station 对象
        station = Station(
            name=station_name,
            edges=edges,
            lines=station_info['lines'],
            line_siz=station_info['line_siz']
        )
        # 将 Station 对象添加到字典中
        stations[station_name] = station

    return stations
