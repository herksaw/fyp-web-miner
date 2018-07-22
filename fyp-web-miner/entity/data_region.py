class DataRegion:
    def __init__(self, p, i, j, k):
        self.p = p
        self.i = i
        self.j = j
        self.k = k

    def set_region_start_preorder_position(self, p):
        self.p = p

    def set_region_start_relative_position(self, i):
        self.i = i

    def set_node_comb(self, j):
        self.j = j

    def set_node_count(self, k):
        self.k = k

    def get_region_start_preorder_position(self):
        return self.p

    def get_region_start_relative_position(self):
        return self.i

    def get_node_comb(self):
        return self.j

    def get_node_count(self):
        return self.k

    def is_same(self, dr):
        return self.p == dr.p and self.i == dr.i and self.j == dr.j and self.k == dr.k
