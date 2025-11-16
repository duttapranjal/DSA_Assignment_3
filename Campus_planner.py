class Building:
    def __init__(self, building_id, name, location):
        self.id = building_id
        self.name = name
        self.location = location

    def __str__(self):
        return f"{self.id} - {self.name} - {self.location}"


class BSTNode:
    def __init__(self, building):
        self.data = building
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, building):
        self.root = self._insert(self.root, building)

    def _insert(self, node, building):
        if not node:
            return BSTNode(building)
        if building.id < node.data.id:
            node.left = self._insert(node.left, building)
        else:
            node.right = self._insert(node.right, building)
        return node

    def search(self, building_id):
        return self._search(self.root, building_id)

    def _search(self, node, building_id):
        if not node:
            return None
        if node.data.id == building_id:
            return node.data
        if building_id < node.data.id:
            return self._search(node.left, building_id)
        return self._search(node.right, building_id)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(str(node.data))
            self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(str(node.data))
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(str(node.data))


class AVLNode:
    def __init__(self, building):
        self.data = building
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def insert(self, root, building):
        if not root:
            return AVLNode(building)
        if building.id < root.data.id:
            root.left = self.insert(root.left, building)
        else:
            root.right = self.insert(root.right, building)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # LL
        if balance > 1 and building.id < root.left.data.id:
            return self.rotate_right(root)

        # RR
        if balance < -1 and building.id > root.right.data.id:
            return self.rotate_left(root)

        # LR
        if balance > 1 and building.id > root.left.data.id:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # RL
        if balance < -1 and building.id < root.right.data.id:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def rotate_left(self, z):
        y = z.right
        t2 = y.left

        y.left = z
        z.right = t2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def rotate_right(self, z):
        y = z.left
        t3 = y.right

        y.right = z
        z.left = t3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        return root.height if root else 0

    def get_balance(self, root):
        return (self.get_height(root.left) -
                self.get_height(root.right)) if root else 0

    def inorder(self, root):
        return [] if not root else \
            self.inorder(root.left) + [str(root.data)] + self.inorder(root.right)

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_matrix = [[0]*vertices for _ in range(vertices)]
        self.adj_list = [[] for _ in range(vertices)]

    def add_edge(self, u, v, w=1):
        self.adj_matrix[u][v] = w
        self.adj_matrix[v][u] = w
        self.adj_list[u].append((v, w))
        self.adj_list[v].append((u, w))

    # BFS
    def bfs(self, start):
        visited = [False] * self.V
        queue = [start]
        visited[start] = True
        order = []

        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor, _ in self.adj_list[node]:
                if not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
        return order

    # DFS
    def dfs(self, start):
        visited = [False] * self.V
        result = []
        self._dfs(start, visited, result)
        return result

    def _dfs(self, node, visited, result):
        visited[node] = True
        result.append(node)
        for neighbor, _ in self.adj_list[node]:
            if not visited[neighbor]:
                self._dfs(neighbor, visited, result)

    # Dijkstra
    def dijkstra(self, src):
        import heapq
        dist = [float('inf')] * self.V
        dist[src] = 0
        pq = [(0, src)]

        while pq:
            d, node = heapq.heappop(pq)
            for neigh, w in self.adj_list[node]:
                if dist[node] + w < dist[neigh]:
                    dist[neigh] = dist[node] + w
                    heapq.heappush(pq, (dist[neigh], neigh))
        return dist

    # Kruskal
    def kruskal(self):
        edges = []
        for u in range(self.V):
            for v, w in self.adj_list[u]:
                if u < v:
                    edges.append((w, u, v))

        edges.sort()
        parent = list(range(self.V))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        mst = []
        for w, u, v in edges:
            pu, pv = find(u), find(v)
            if pu != pv:
                mst.append((u, v, w))
                parent[pu] = pv
        return mst


class ExpNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class ExpressionTree:
    def build(self, postfix):
        stack = []
        for char in postfix:
            if char.isdigit():
                stack.append(ExpNode(int(char)))
            else:
                node = ExpNode(char)
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
        return stack.pop()

    def evaluate(self, node):
        if str(node.value).isdigit():
            return node.value
        left_val = self.evaluate(node.left)
        right_val = self.evaluate(node.right)

        if node.value == '+': return left_val + right_val
        if node.value == '-': return left_val - right_val
        if node.value == '*': return left_val * right_val
        if node.value == '/': return left_val / right_val


class CampusSystem:
    def __init__(self):
        self.bst = BST()
        self.avl = AVLTree()
        self.avl_root = None

    def add_building_record(self, building):
        self.bst.insert(building)
        self.avl_root = self.avl.insert(self.avl_root, building)

    def list_campus_locations(self):
        return {
            "BST_Inorder": self.bst.inorder(),
            "BST_Preorder": self.bst.preorder(),
            "BST_Postorder": self.bst.postorder(),
            "AVL_Inorder": self.avl.inorder(self.avl_root)
        }


if __name__ == "__main__":
    system = CampusSystem()

    buildings = [
        Building(3, "Library", "Central Block"),
        Building(1, "Admin", "North Block"),
        Building(5, "Hostel", "East Wing"),
        Building(2, "CSE Dept", "Tech Building"),
        Building(4, "Auditorium", "South Block")
    ]

    for b in buildings:
        system.add_building_record(b)

    print("\n=== TREE TRAVERSALS ===")
    for k, v in system.list_campus_locations().items():
        print(k, " => ", v)

    print("\n=== GRAPH OPERATIONS ===")
    g = Graph(5)
    g.add_edge(0, 1, 10)
    g.add_edge(1, 2, 5)
    g.add_edge(2, 3, 7)
    g.add_edge(3, 4, 2)

    print("BFS from 0:", g.bfs(0))
    print("DFS from 0:", g.dfs(0))
    print("Dijkstra from 0:", g.dijkstra(0))
    print("Kruskal MST:", g.kruskal())

    print("\n=== EXPRESSION TREE (ENERGY BILL) ===")
    exp = ExpressionTree()
    root = exp.build("23*54*+")
    print("Expression Result:", exp.evaluate(root))
