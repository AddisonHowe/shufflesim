import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
        

class Shuffler:

    def __init__(self, shuffle_accuracy, split_accuracy):
        self.shuffle_accuracy = shuffle_accuracy
        self.split_accuracy = split_accuracy
        self.n = 52
        self.deck = np.arange(self.n)
        self.split_error_func = st.truncexpon(self.n)

    def split_and_shuffle(self):
        side0, side1 = self.split(self.deck)
        return self.shuffle(side0, side1)

    def split(self, deck):
        halfidx = self.n // 2
        plus_or_minus = np.random.randint(2) * 2 - 1
        offset = int(self.split_error_func.rvs())
        splitidx = halfidx + plus_or_minus * offset
        side0 = deck[0:splitidx]  # bottom half
        side1 = deck[splitidx:]  # top half
        return side0, side1

    def shuffle(self, side0, side1):
        """
        Args:
            side0: One side of deck. Index 0 is the top card, last to fall.
            side1: One side of deck. Index 0 is the top card, last to fall.
        """
        n0 = len(side0)
        n1 = len(side1)
        sides = [side0, side1]
        ns = [n0, n1]
        p = self.shuffle_accuracy
        shuffled = np.empty(self.n, dtype=int)
        shuffled[:] = -1
        idx0 = 0
        idx1 = 0
        idxs = [idx0, idx1]
        idx = 0
        current_side = np.random.choice(2)
        if n0 == 0:
            return side1.copy()
        if n1 == 0:
            return side0.copy()
        while idx < self.n:
            shuffled[idx] = sides[current_side][idxs[current_side]]
            ns[current_side] -= 1
            idxs[current_side] += 1
            idx += 1
            if ns[current_side] == 0:
                # Nothing left in current side
                current_side = 1 - current_side
                shuffled[idx:] = sides[current_side][idxs[current_side]:]
                break
            flip = np.random.rand() < p
            if flip:
                current_side = 1 - current_side
        assert len(np.unique(shuffled)) == 52, f"Deck length: {len(np.unique(shuffled))}"
        return shuffled
        
def main():
    shuffle_acc = 0.50
    split_acc = 0.95
    shuffler = Shuffler(shuffle_acc, split_acc)

    ntrials = 5
    deck_history = np.empty([ntrials + 1, len(shuffler.deck)])
    deck_history[0] = shuffler.deck.copy()
    for i in range(1, ntrials + 1):
        new_deck = shuffler.split_and_shuffle()
        deck_history[i] = new_deck
        shuffler.deck = new_deck

    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(12,5))
    for i in range(len(shuffler.deck)):
        ax1.plot(deck_history[:,i])

    ax2.plot([0, ntrials], deck_history[[0, -1]])
    print(shuffler.deck)
    print(len(np.unique(shuffler.deck)))
    plt.show()

if __name__ == "__main__":
    main()
