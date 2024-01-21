class Spellcheck:
    def __init__(self, numwords=10000, words_filename='words.txt', extended_words_filename='extended_words.txt',
                 correction_filename='spellcorrection.txt'):
        self.__words_filename = words_filename
        self.__extended_words_filename = extended_words_filename
        # words contains 10,000 words, whereas extended_words contains 333,000
        # both are ordered by use frequency, meaning that the output is first by edit distance, second by use frequency
        self.__numwords = numwords
        # number of words to compare against
        self.__spelling_filename = correction_filename
        self.__correctly_spelt_words = self.__load_words()

    def __update_text_file(self, rankings):
        with open(self.__spelling_filename, 'w') as f:
            [f.write(f'{r[0]} : {r[1]}\n') for r in rankings]

    def __load_words(self):
        wds = []
        if self.__numwords <= 10000:
            filename = self.__words_filename
            # uses the smaller file for efficiency if it can be used so that you don't need to
            # download the larger file unless you need the extra words
        else:
            filename = self.__extended_words_filename

        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i > self.__numwords - 1:
                    return wds
                wds.append(line.strip())
        # this means that if over 330,000 words are requested, it caps at 330,000
        return wds

    @staticmethod
    def __insert_word(rankings, array):
        dist = array[1]
        if len(rankings) == 0:
            return [array]
        for i, (_, y) in enumerate(rankings):
            if y > dist:
                return rankings[:i] + [array] + rankings[i:]
        # returns at the raw length - is adjusted later if the array needs to be a certain length
        return rankings + [array]

    def spellcheck_word(self, word, num_words_returned=10, write_to_text_file=False):
        if word in self.__correctly_spelt_words:
            return word
        else:
            rankings = []
            for destination in self.__correctly_spelt_words:
                dist = self.calculate_edit_distance(word, destination)
                # the number of insertions, deletions and changes of letters summed
                if len(rankings) < num_words_returned:
                    rankings = self.__insert_word(rankings, [destination, dist])
                    if write_to_text_file:
                        self.__update_text_file(rankings)
                elif dist < rankings[-1][1]:
                    rankings = self.__insert_word(rankings, [destination, dist])[:num_words_returned]
                    if write_to_text_file:
                        self.__update_text_file(rankings)
            return rankings

    @staticmethod
    def calculate_edit_distance(word, destination):
        if not(word and destination):   # using the strings as booleans - len of 0 is False.
            return max(len(word), len(destination))

        word = '_' + word
        destination = '_' + destination
        word_len, destination_len = len(word), len(destination)
        past_line = list(range(destination_len))

        # This uses the wagner-fischer method
        for i in range(1, word_len):
            current_line = [i]
            for j in range(1, destination_len):
                change_letter = past_line[j - 1]
                add_letter = past_line[j] + 1
                delete_letter = current_line[j - 1] + 1
                if word[i] != destination[j]:
                    change_letter += 1
                current_line.append(min(change_letter, add_letter, delete_letter))
            past_line = current_line
        return current_line[-1]