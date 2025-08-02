# Beijing-Subway-Route-Query-System

Dijkstra算法解决地铁寻路问题

通过 json_loader.py 程序导入包含北京地铁站点、线路等信息的 stations.json 文件，使用 graph_builder.py 构建整个地铁网络的连通图。统提供了两种查询路径的方式：最短时间路径 和 最少换乘次数路径，这两个功能分别由 fast_path.py 和 convenient_path.py 实现。edit_path.py 中包含了 delete_path 和 add_path 两个函数，分别实现了删除和增加某条地铁线路的功能。fuzzy_search.py 使用模糊匹配算法帮助用户快速找到可能输入错误或不完整的地铁站或线路名称。所有这些功能在 main.py 中被整合，作为用户界面的入口，负责接收用户的输入（起始站、终点站、查询需求等），并根据用户选择调用相应的功能模块，输出最合适的路线方案。
