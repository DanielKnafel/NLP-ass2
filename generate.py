import argparse
import random
from collections import defaultdict


class Node:
    def __init__(self, symbol, terminal):
        self.next = []
        self.terminal = terminal
        self.symbol = symbol


class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)
        self._parse_tree = []
        self.tree = ""

    def add_rule(self, lhs, rhs, weight):
        assert (isinstance(lhs, str))
        assert (isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w, l, r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l, r, w)
        return grammar

    def is_terminal(self, symbol):
        return symbol not in self._rules

    # def gen(self, symbol):
    #     if self.is_terminal(symbol):
    #         self._parse_tree.append(('term', symbol))
    #
    #         return symbol
    #     else:
    #         expansion = self.random_expansion(symbol)
    #         self._parse_tree.append(('non-term', symbol))
    #         return " ".join(self.gen(s) for s in expansion)

    def gen(self, symbol):
        if self.is_terminal(symbol):
            self._parse_tree.append(('term', symbol))
            self.tree += " " + symbol
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            self.tree += f" ({symbol} "
            self._parse_tree.append(('non-term', symbol))
            path = [self.gen(s) for s in expansion]
            self.tree += ')'
            return " ".join(path)

    # def gen_from_tree(self, symbol, node):
    #     new_node = Node(symbol, self.is_terminal(symbol))
    #     node.next.append(new_node)
    #     if self.is_terminal(symbol):
    #         self._parse_tree.append(('term', symbol))
    #         return symbol
    #     else:
    #         expansion = self.random_expansion(symbol)
    #         # self.tree = f"({symbol} {self.tree})"
    #         self._parse_tree.append(('non-term', symbol))
    #         return " ".join(self.gen_from_tree(s, new_node) for s in expansion)

    def random_sent(self):
        self._parse_tree.clear()
        start = Node('start', False)
        # x = self.gen_from_tree('ROOT', start)
        # x = self.gen1("ROOT")
        # return (self.gen("ROOT"), self._parse_tree, start.next)
        return (self.gen("ROOT"),self.tree)

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


def print_sentences(grammar, n, t):
    pcfg = PCFG.from_file(grammar)
    for i in range(n):
        # sent, tree, root = pcfg.random_sent()
        sent, tree = pcfg.random_sent()
        print(sent)
        if t:
            # print_tree(root)
            # print(make_tree(tree))
            print(tree)

# def print_tree(root):
#     print("".join(recursive_dfs(root[0])))
#
# def recursive_dfs(root, path=[]):
#     if root.terminal:
#         path.append(f" {root.symbol}")
#         # leaf node, backtrack
#         return path
#     else:
#         path.append(f"({root.symbol}")
#     for neighbour in root.next:
#         path = recursive_dfs(neighbour, path)
#     return path + [")"]


# def make_tree(tree):
#     tree_sent = ""
#
#     i = 0
#     while i < len(tree):
#         type, symbol = tree[i]
#         if type == "non-term":
#             tree_sent += '(' + symbol + ' '
#             i += 1
#         else:
#             while i < len(tree) and tree[i][0] == "term":
#                 tree_sent += tree[i][1] + ' '
#                 i += 1
#             tree_sent = tree_sent[:-1] + ')'
#     return tree_sent
#

def main():
    parser = argparse.ArgumentParser(description='flags parser')
    # Required positional argument
    parser.add_argument('grammar', type=str,
                        help='A grammar file to be used')
    # Optional argument
    parser.add_argument('-n', type=int,
                        help='number of sentences to make')
    # Switch
    parser.add_argument('-t', action='store_true',
                        help='A boolean switch')

    args = parser.parse_args()

    if 'n' in args:
        print_sentences(args.grammar, args.n, args.t)
    # if 't' in args:
    #     print_tree()
    else:
        print_sentences(1)


if __name__ == '__main__':
    main()
