import argparse
from collections import defaultdict
import random

class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)
        self._parse_tree = []

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def gen(self, symbol):
        if self.is_terminal(symbol): 
            self._parse_tree.append(('term', symbol))
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            self._parse_tree.append(('non-term', symbol))
            return " ".join(self.gen(s) for s in expansion)

    def random_sent(self):
        self._parse_tree.clear()
        return (self.gen("ROOT"), self._parse_tree)

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r

def print_sentences(grammar, n, t):
    pcfg = PCFG.from_file(grammar)
    for i in range(n):
        sent, tree = pcfg.random_sent()
        print(sent)
        if t:
            print(make_tree(tree))

def make_tree(tree):
    tree_sent = ""
    
    i = 0
    while i < len(tree):
        type, symbol = tree[i]
        if type == "non-term":
            tree_sent += '(' + symbol + ' '
            i += 1
        else:
            while i < len(tree) and tree[i][0] == "term":
                tree_sent += tree[i][1] + ' '
                i += 1
            tree_sent = tree_sent[:-1] + ')'
    return tree_sent



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

