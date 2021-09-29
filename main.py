
from hypothesis import given, strategies as st, assume


class BinarySearchTree:
    def __init__(self, value=None, left_tree=None, right_tree=None):
        if value is None:
            self.type = 'EmptyBST'
            self.value = None
            self.left_tree = None
            self.right_tree = None
        elif type(value) is BinarySearchTree:
            self.value = value.value
            self.left_tree = value.left_tree
            self.right_tree = value.right_tree
            self.type = value.type
        elif type(value) is list:
            empty_tree = BinarySearchTree()
            for v in value:
                empty_tree = empty_tree.insert(v)

            self.value = empty_tree.value
            self.left_tree = empty_tree.left_tree
            self.right_tree = empty_tree.right_tree
            self.type = empty_tree.type
        else:
            self.type = 'NodeBST'
            self.value = value
            self.left_tree = BinarySearchTree(left_tree)
            self.right_tree = BinarySearchTree(right_tree)

    def __str__(self):
        if self.type == 'EmptyBST':
            return 'EmptyTree'
        else:
            return f'(v: {self.value} | left: {self.left_tree}  | right: {self.right_tree})'

    def __repr__(self):
        if self.type == 'EmptyBST':
            return 'EmptyTree'
        else:
            return f'(v: {self.value} | left: {self.left_tree}  | right: {self.right_tree})'

    def __eq__(self, other):
        if self.type != other.type:
            return False

        if self.type == 'EmptyBST':
            return True

        if self.value != other.type:
            return False

        return self.left_tree == other.left_tree and self.right_tree == other.right_tree

    def insert(self, x):
        if self.type == 'EmptyBST':
            return BinarySearchTree(x)

        if x >= self.value:
        # if x < self.value:
            if self.right_tree is None:
                return BinarySearchTree(self.value, self.left_tree, BinarySearchTree(x))
            else:
                return BinarySearchTree(self.value, self.left_tree, self.right_tree.insert(x))
        else:
            if self.left_tree is None:
                return BinarySearchTree(self.value, BinarySearchTree(x), self.right_tree)
            else:
                return BinarySearchTree(self.value, self.left_tree.insert(x), self.right_tree)

    def delete(self, x):
        if self.type == 'EmptyBST':
            return BinarySearchTree(self.value, self.left_tree, self.right_tree)
        elif self.value == x:
            if self.right_tree.type == 'NodeBST':
                return BinarySearchTree(
                    self.right_tree.value,
                    self.left_tree,
                    self.right_tree.delete(self.right_tree.value)
                )
            elif self.left_tree.type == 'NodeBST':
                return BinarySearchTree(
                    self.left_tree.value,
                    self.left_tree.delete(self.left_tree.value),
                    self.right_tree
                )
            else:
                return BinarySearchTree()
        else:
            if self.value > x:
                return BinarySearchTree(
                    self.value,
                    self.left_tree.delete(x),
                    self.right_tree
                )
            else:
                return BinarySearchTree(
                    self.value,
                    self.left_tree,
                    self.right_tree.delete(x)
                )

    def search(self, x):
        if self.type == 'EmptyBST':
            return False
        elif self.value == x:
            return True
        elif self.value <= x:
            return self.right_tree.search(x)
        else:
            return self.left_tree.search(x)


def is_bst(tree):
    if tree.type == 'EmptyBST':
        return True

    if tree.left_tree.type == 'NodeBST':
        if tree.value <= tree.left_tree.value:
            return False

    if tree.right_tree.type == 'NodeBST':
        if tree.value > tree.right_tree.value:
            return False

    return is_bst(tree.left_tree) and is_bst(tree.right_tree)


@given(t=st.builds(BinarySearchTree, st.lists(st.integers())), x=st.integers())
def insert_preservation(t, x):
    assert is_bst(t.insert(x))


@given(t=st.builds(BinarySearchTree, st.lists(st.integers())), x=st.integers())
def insert_delete_inverse(t, x):
    assert t == t.insert(x).delete(x)



if __name__ == '__main__':
    zero = BinarySearchTree(0).insert(1).insert(5).insert(3).insert(-1)

    insert_preservation()
    # insert_delete_inverse()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
