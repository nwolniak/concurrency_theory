from itertools import chain
import subprocess


class DiekertGraph:
    def __init__(self, W, D, n):
        self.W = W
        self.D = D
        self.n = n
        self.edges = self._create_graph()
        self.FNF = self._compute_FNF()

    def _create_graph(self):
        # creating edges
        all_edges = {}
        for idx, w1 in enumerate(self.W):
            for w2 in self.W[idx:]:
                if (w1, w2) in self.D:
                    if all_edges.get(w1):
                        all_edges[w1].append(w2)
                    else:
                        all_edges[w1] = [w2]

        # minimum graph
        edges = {}
        for node, children in all_edges.items():
            for idx, child in enumerate(children):
                if self._is_path(children[:idx] + children[idx + 1:], child, all_edges):
                    continue
                else:
                    if edges.get(node):
                        edges[node].append(child)
                    else:
                        edges[node] = [child]

        return edges

    def _is_path(self, s_children, t, all_edges):
        for s_child in s_children:
            if s_child == t:
                return True
            if all_edges.get(s_child) and self._is_path(all_edges[s_child], t, all_edges):
                return True
        return False

    def _compute_FNF(self):
        # find nodes at the top of the graph
        top_nodes = self._find_top_nodes()
        # from nodes at the top of the graph count max depth of other nodes
        node_max_depth_list = self._find_max_depth(top_nodes)

        # create FNF depending on max depth of each node
        FNF = [[]]
        last_depth = 0
        i = 0
        while node_max_depth_list:
            node, depth = node_max_depth_list.pop(0)
            if depth != last_depth:
                last_depth = depth
                FNF.append([])
                i += 1
            FNF[i].append(node)

        return FNF

    def _find_top_nodes(self):
        top_nodes = []
        for node in self.edges:
            if node not in chain.from_iterable(self.edges.values()):
                top_nodes.append(node)
        return top_nodes

    def _find_max_depth(self, top_nodes):
        queue = [node for node in top_nodes]
        depth = {}
        depth.update({node: 0 for node in top_nodes})
        depth.update({child: 0 for children in self.edges.values() for child in children})

        while queue:
            v = queue.pop(0)
            for child in self.edges.get(v, []):
                if depth[v] + 1 > depth[child]:
                    depth[child] = depth[v] + 1
                    queue.append(child)
        depth = sorted([(node, depth) for node, depth in depth.items()], key=lambda x: x[1])
        return depth

    def save(self, filename_dot, filename_img):
        with open(filename_dot, "w") as f:
            f.write(str(self))
            print("File graph.dot saved succesfully.")
            f.close()

        try:
            img_format = filename_img.split(".")[-1]
            subprocess.run('dot -T{} {} -o {}'.format(img_format, filename_dot, filename_img), check=True)
            print("File graph.{} saved successfully.".format(img_format))
        except subprocess.CalledProcessError:
            print('dot command does not exist')

    def get_FNF(self):
        return self.FNF

    def __str__(self):
        _str = ""
        _str += "digraph g{\nratio=1.0\nsplines=line\n"
        _color_list = ["#FF0000", "#FF8000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]
        for level, _fnf in enumerate(self.FNF):
            for node in _fnf:
                if self.edges.get(node):
                    for child in self.edges[node]:
                        _str += "{}->{}[style=bold,weight={}]\n".format(self.W.index(node), self.W.index(child), level+2)
                fillcolor = _color_list[level % 7]
                _str += '{}[label={},style="bold,filled",fillcolor="{}",level={}]\n'.format(self.W.index(node), node, fillcolor, level + 1)

        _str += "}"
        return _str
