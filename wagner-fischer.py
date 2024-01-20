import time


def pprint(array):
    [print(line) for line in array]
class Spellcheck:
    def __init__(self, numwords=333333):
        self.words_filename = 'words.txt'
        self.numwords=numwords
        self.spelling_filename = 'spellcorrection.txt'
        self.extended_words_filename = 'extended_words.txt'
        self.correctly_spelt_words = self.load_words()
    def load_words(self):
        wds = []
        if self.numwords <= 10000:
            filename = self.words_filename
        else:
            filename = self.extended_words_filename
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i > self.numwords-1:
                    return wds
                wds.append(line.strip())
        return wds
    def get_dist(self, ls):
        return ls[-1]
    def spellcheck_word(self, word, num_words_returned):
        if word in self.correctly_spelt_words:
            return
        else:
            rankings = []
            for destination in self.correctly_spelt_words:
                dist = self.calculate_distance(word, destination)
                if len(rankings) < num_words_returned:
                    rankings.append([destination, dist])
                    if len(rankings) == num_words_returned:
                        rankings.sort(key=self.get_dist)
                elif dist < rankings[-1][1]:
                    for i, x in enumerate(rankings):
                        if x[1] > dist:
                            break

                    rankings = rankings[:i] + [[destination, dist]] + rankings[i:-1]
                    self.update_text_file(rankings)
            self.update_text_file(rankings)
        return rankings
    def update_text_file(self, rankings):
        with open(self.spelling_filename, 'w') as f:
            for r in rankings:
                f.write(r[0])
                f.write(' : ')
                f.write(str(r[1]))
                f.write('\n')
    @staticmethod
    def calculate_distance(word, destination):
        word = '_' + word
        destination = '_' + destination
        wordlen, destinationlen = len(word), len(destination)
        distance_matrix = []
        [distance_matrix.append([None] * destinationlen) for _ in range(wordlen)]
        for i in range(len(distance_matrix)):
            distance_matrix[i][0] = i
        for i in range(len(distance_matrix[0])):
            distance_matrix[0][i] = i
        for i, line in enumerate(distance_matrix):
            for j, d in enumerate(line):
                if d is None:
                    change_letter = distance_matrix[i-1][j-1]
                    add_letter = distance_matrix[i-1][j] + 1
                    delete_letter = distance_matrix[i][j-1] + 1
                    if word[i] != destination[j]:
                        change_letter += 1
                    distance_matrix[i][j] = min(change_letter, add_letter, delete_letter)

        return distance_matrix[-1][-1]

spc = Spellcheck()
print(spc.spellcheck_word('spcyel', 100))
