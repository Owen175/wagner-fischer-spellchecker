class Spellcheck:
    def __init__(self, numwords=10000):
        self.words_filename = 'words.txt'
        self.numwords = numwords
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
                if i > self.numwords - 1:
                    return wds
                wds.append(line.strip())
        return wds
    def insert_word(self, rankings, array):
        dist = array[1]
        if len(rankings) == 0:
            return [array]
        for i, (_, y) in enumerate(rankings):
            if y > dist:
                return rankings[:i] + [array] + rankings[i:]
        return rankings + [array]
    def get_dist(self, ls):
        return ls[-1]

    def spellcheck_word(self, word, num_words_returned, writeToTextFile=False):
        if word in self.correctly_spelt_words:
            return word
        else:
            rankings = []
            for destination in self.correctly_spelt_words:
                dist = self.calculate_distance(word, destination)
                if len(rankings) < num_words_returned:
                    rankings = self.insert_word(rankings, [destination, dist])
                    if writeToTextFile:
                        self.update_text_file(rankings)
                elif dist < rankings[-1][1]:
                    rankings = self.insert_word(rankings, [destination, dist])[:num_words_returned]
                    if writeToTextFile:
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
        if word == '' or destination == '':
            return max(len(word), len(destination))
        word = '_' + word
        destination = '_' + destination
        wordlen, destinationlen = len(word), len(destination)
        pastLine = list(range(destinationlen))
        for i in range(1, wordlen):
            currentLine = [i]
            for j in range(1, destinationlen):
                change_letter = pastLine[j - 1]
                add_letter = pastLine[j] + 1
                delete_letter = currentLine[j - 1] + 1
                if word[i] != destination[j]:
                    change_letter += 1
                currentLine.append(min(change_letter, add_letter, delete_letter))
            pastLine = currentLine
        return currentLine[-1]


spc = Spellcheck()
print(spc.spellcheck_word('oogabooga', 10))
print(29554718100/100000000000)
