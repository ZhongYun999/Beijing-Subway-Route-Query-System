#mian.py


import json_loader
import fast_path
import convenient_path
import edit_path
import graph_builder
from fuzzy_search import fuzzy_search, get_all_lines  # 引入模糊查询模块


# 全局变量声明
graph = None
station_index_map = None
stations = None


def main():
    global graph, station_index_map, stations

    """
    主程序入口点，提供用户界面以执行不同的操作。
    用户可以选择：
    1. 查询时间最短的路径
    2. 查询换乘最少的路径
    3. 删除地铁线路
    4. 增加地铁线路
    0. 退出程序
    """
    
    # 加载 JSON 数据
    json_file = 'stations.json'
    stations = json_loader.json_to_stations(json_file)

    # 生成站点索引映射，方便通过站点名称快速查找索引
    station_index_map = {name: i for i, name in enumerate(stations.keys())}
    
    # 生成图并更新全局变量
    graph, _ = graph_builder.stations_to_graph(stations)

    while True:
        print()

        # 提供选择：时间短或换乘少，或增删线路
        print("欢迎使用北京地铁路线查询系统！")
        print("1. 查询时间最短的路径")
        print("2. 查询换乘最少的路径")
        print("3. 删除地铁线路")
        print("4. 增加地铁线路")
        print("0. 退出程序")

        option = input("请选择您的操作：").strip()

        # 退出程序
        if option == '0':
            print("感谢您使用北京地铁路线查询系统！")
            break

        # 判断输入是否合法
        if option not in ['1', '2', '3', '4']:
            print("无效的选择，请输入 0、1、2、3 或 4。")
            continue

        print()

        # 如果选择 1 或 2，则进行路径查询
        if option in ['1', '2']:
            # 用户输入起点和终点
            start_station = input("请输入起点站：").strip()
            end_station = input("请输入终点站：").strip()

            # 进行模糊匹配
            all_stations = list(stations.keys())
            start_station = fuzzy_search(start_station, all_stations) or start_station
            end_station = fuzzy_search(end_station, all_stations) or end_station

            print()

            # 根据用户选择调用相应的路径查询函数
            if option == '1':
                # 查询时间最短的路径
                fast_path.query_station_time(graph, station_index_map, start_station, end_station)
            elif option == '2':
                # 查询换乘最少的路径
                convenient_path.query_station_transfer(graph, station_index_map, start_station, end_station)

        # 如果选择 3 或 4，则进行线路增删操作
        elif option == '3':
            # 用户输入要删除的地铁线路名称
            line_id = input("请输入要删除的地铁线路名称：").strip()

            # 获取所有线路名称
            all_lines = get_all_lines(stations)
            
            # 进行模糊匹配
            line_id = fuzzy_search(line_id, all_lines) or line_id

            # 生成站点的连通图，确保更新后的图反映所有的变化
            graph, _ = graph_builder.stations_to_graph(stations)

            # 调用删除线路的函数
            edit_path.delete_path(graph, line_id)

            print(f"已删除线路 {line_id}。")

        elif option == '4':
            # 用户输入要增加的地铁线路名称
            line_id = input("请输入要增加的地铁线路名称：").strip()

            # 获取所有线路名称
            all_lines = get_all_lines(stations)
            
            # 进行模糊匹配
            line_id = fuzzy_search(line_id, all_lines) or line_id

            # 生成站点的连通图，确保更新后的图反映所有的变化
            graph, _ = graph_builder.stations_to_graph(stations)

            # 调用增加线路的函数
            edit_path.add_path(graph, line_id)

            print(f"已增加线路 {line_id}。")


if __name__ == "__main__":
    main()
