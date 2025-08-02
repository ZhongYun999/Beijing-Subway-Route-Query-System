#Graph.py


class GraphError(ValueError):
    """图错误类，继承自 ValueError，用于图相关操作中的异常处理。"""
    pass


class Graph:
    def __init__(self, mat, unconn=0):
        """
        初始化图的邻接矩阵。
        :param mat: 邻接矩阵，表示图的连接关系
        :param unconn: 表示无连接的值，默认为 0
        :raises ValueError: 如果邻接矩阵不是方阵
        """
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise ValueError("Argument for 'Graph' must be a square matrix.")
        self._mat = [mat[i][:] for i in range(vnum)]  # 深拷贝矩阵
        self._unconn = unconn
        self._vnum = vnum

    def vertex_num(self):
        """
        获取图中顶点的数量。        
        :return: 顶点数量
        """
        return self._vnum

    def _invalid(self, v):
        """
        检查给定的顶点索引是否有效。        
        :param v: 顶点索引
        :return: 如果索引无效则返回 True，否则返回 False
        """
        return 0 > v or v >= self._vnum

    def add_vertex(self):
        """
        不支持添加顶点的方法，抛出异常。        
        :raises GraphError: 异常，表明不支持此操作
        """
        raise GraphError("Adj-Matrix does not support 'add_vertex'.")

    def add_edge(self, vi, vj, val=1):
        """
        添加或更新边的权重。        
        :param vi: 起点索引
        :param vj: 终点索引
        :param val: 边的权重值，默认为 1
        :raises GraphError: 如果顶点索引无效
        """
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not a valid vertex.")
        self._mat[vi][vj] = val

    def get_edge(self, vi, vj):
        """
        获取两个顶点之间的边的权重值。        
        :param vi: 起点索引
        :param vj: 终点索引
        :return: 边的权重值
        :raises GraphError: 如果顶点索引无效
        """
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not a valid vertex.")
        return self._mat[vi][vj]

    def out_edges(self, vi):
        """
        获取从指定顶点出发的所有边。        
        :param vi: 起点索引
        :return: 从顶点 vi 出发的所有边的列表
        :raises GraphError: 如果顶点索引无效
        """
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._out_edges(self._mat[vi], self._unconn)

    @staticmethod
    def _out_edges(row, unconn):
        """
        处理邻接矩阵的行数据，提取出边的信息。        
        :param row: 邻接矩阵中的一行，表示一个顶点的所有边
        :param unconn: 无连接的标记值
        :return: 边的列表，每个边包含目标顶点和边的权重
        """
        edges = []
        for i in range(len(row)):
            if row[i] != unconn:
                edges.append((i, row[i]))
        return edges


class GraphAL(Graph):
    def __init__(self, mat=None, unconn=float('inf')):
        """
        初始化图的邻接表。        
        :param mat: 邻接矩阵，表示图的连接关系，默认为空
        :param unconn: 表示无连接的值，默认为无穷大
        :raises ValueError: 如果邻接矩阵不是方阵
        """
        if mat is None:
            mat = []
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise ValueError("Argument for 'GraphAL' must be a square matrix.")
        self._mat = [self._out_edges(mat[i], unconn) for i in range(vnum)]
        self._vnum = vnum
        self._unconn = unconn

    def add_vertex(self):
        """
        添加一个新顶点，并返回其索引。        
        :return: 新顶点的索引
        """
        self._mat.append([])
        self._vnum += 1
        return self._vnum - 1

    def add_edge(self, vi, vj, time, distance, line_id, is_active=True):
        """
        添加一条边到图中，包含时间、距离、线路信息和激活状态。        
        :param vi: 起点索引
        :param vj: 终点索引
        :param time: 边的时间权重
        :param distance: 边的距离信息
        :param line_id: 线路信息
        :param is_active: 边的激活状态，默认为 True
        :raises ValueError: 如果图为空或顶点无效
        """
        if self._vnum == 0:
            raise ValueError("Cannot add edge to an empty graph")
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError(f"{vi} or {vj} is not a valid vertex.")
        
        row = self._mat[vi]
        i = 0
        while i < len(row):
            if row[i][0] == vj:
                # 更新已存在的边
                self._mat[vi][i] = (vj, time, distance, line_id, is_active)
                return
            if row[i][0] > vj:
                break
            i += 1
        # 插入新边
        self._mat[vi].insert(i, (vj, time, distance, line_id, is_active))

    def get_edge(self, vi, vj):
        """
        获取两个顶点之间的边的详细信息，包括激活状态。        
        :param vi: 起点索引
        :param vj: 终点索引
        :return: 边的详细信息 (vj, 时间, 距离, 线路, 激活状态)
        :raises ValueError: 如果顶点无效
        """
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError(f"{vi} or {vj} is not a valid vertex.")
        for edge in self._mat[vi]:
            if edge[0] == vj:
                return edge  # 返回 (vj, 时间, 距离, 线路, 激活状态)
        return (self._unconn, self._unconn, None, False)  # 如果没有找到，返回无穷大、无线路和False状态

    def out_edges(self, vi):
        """
        获取从指定顶点出发的所有边的信息。        
        :param vi: 起点索引
        :return: 从顶点 vi 出发的所有边的详细信息列表 (vj, 时间, 距离, 线路, 激活状态)
        :raises ValueError: 如果顶点无效
        """
        if self._invalid(vi):
            raise ValueError(f"{vi} is not a valid vertex.")
        return self._mat[vi]
