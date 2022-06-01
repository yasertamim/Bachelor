

import codecs
import csv

# list of correct grammatical patterns
grammar_list = [["adv", "aux", "pron", "verb", "part", "verb", "mark"], ["aux", "pron", "verb", "det", "noun", "mark"],
                ["pron", "verb", "adp", "propn", "punct"], ["pron", "verb", "adp", "noun", "punct"],
                ["aux", "pron", "verb", "det", "noun", "mark"],
                ["aux", "pron", "verb", "det", "propn", "mark"], ["pron", "verb", "pron", "det", "propn", "punct"],
                ["pron", "verb", "pron", "det", "noun", "punct"],
                ["adv", "verb", "pron", "mark"], ["verb", "pron", "adp", "propn", "mark"],
                ["pron", "aux", "adv", "verb", "noun", "punct"],
                ["pron", "verb", "pron", "adv", "punct"], ["adv", "verb", "pron", "propn", "adv", "punct"],
                ["adv", "verb", "adp1", "adj", "adp", "pron", "punct"],
                ["adv", "verb", "pron", "adv", "adp", "noun", "punct"], ["adv", "verb", "adv", "noun", "det", "mark"],
                ["adv", "aux", "adv", "pron", "noun", "adp", "adj", "punct"]
    , ["pron", "verb", "adv", "punct"], ["pron", "aux", "adv", "adj", "punct"], ["verb", "pron", "adp", "noun", "mark"],
                ["noun", "verb", "noun", "punct"]]


# sentence tokenizer
def sent_tokenizer(sentance):
    first_split = sentance.split(' ')

    # check for punctiouation
    last_char = first_split[len(first_split) - 1]
    # check if the last word in the sentence contains '.' or '?' and splite it
    if last_char[len(last_char) - 1] == ".":
        new_char = last_char.replace(".", "")
        first_split.remove(last_char)
        first_split.append(new_char)
        first_split.append(".")
    if last_char[len(last_char) - 1] == "?":
        new_char = last_char.replace("?", "")
        first_split.remove(last_char)
        first_split.append(new_char)

        first_split.append("?")
    # print(first_split)

    pos = word_tagger(first_split)

    return pos


# tagging the words in the sentence
def word_tagger(list_of_words):
    pos_token = []

    for w in list_of_words:

        if w == 'å':
            pos_token.append([w, "part"])
            return pos_token

        dataset = codecs.open('data.DICT', 'r', encoding='UTF-8')
        for p in dataset:
            p_split = p.split(' ')
            if w == p_split[0].lower():
                if ([w, p_split[1].lower().replace('\n', '')] not in pos_token):
                    pos_token.append([w, p_split[1].lower().replace('\n', '')])
                    break

    return pos_token

# this function is used to train the corpus
def feed_brain(sentence):
    sent = sent_tokenizer(sentence)

    temp =[]
    read = open('brain.csv', 'r')
    reader = csv.reader(read)

    for l in reader:
        temp.append(l)

    for i in range(len(sent)):

        count = 0
        if i < len(sent) - 1:
            for line in temp:
                if len(line)> 0:
                    if sent[i][1] == "adp" or sent[i][1] == "sconj" or sent[i][1] == "cconj":
                        break

                    if line[0] == sent[i][1] and line[1] == sent[i + 1][1]:
                        count += 1
                        val = count + int(line[2])
                        line[2] = str(val)
                        break

    for i in temp:
        if len(i) == 0:
            temp.remove(i)

    f = open('brain.csv', 'w',newline='')
    write = csv.writer(f)
    for k in temp:
        write.writerow(k)




# the main function that perform the checking and correction
def check_text(text):
    new = sent_tokenizer(text.lower())
    result = []
    result2 =[]

    for i in new:
        result.append(i)
    for i in range(len(new)):

        if i == len(new)-1:
            return result
        else:
            first = result[i]
            second = result[i+1]

            f = open('brain.csv', 'r')
            reader = csv.reader(f)

            for k in reader:
                accurancy1 = 0
                accurancy2 = 0


                if k[0] == first[1] and k[1]== second[1]:


                    f2 = open('brain.csv', 'r')
                    reader2 = csv.reader(f2)
                    for n in reader2:
                        if len(n)!= 0:
                            if n[0] == k[1] and n[1] == k[0]:
                                accurancy2 += int(n[2])
                                accurancy1 += int(k[2])
                                if accurancy2 > accurancy1:
                                    result[i] = second
                                    result[i+1] = first

                                    break

                                else:
                                    result[i+1] = second
                                    result[i] = first
                                    break






    return result

# test
sent = "jeg ikke er fornøyd"
res = check_text(sent)
temp = []
for i in res:
    temp.append(i[0])
print("--------------------Test------------------------------")
print(f"The inserted erroneous sentence: jeg ikke er fornøyd")
print(f"The correction: {' '.join(temp)}")
print("------------------------------------------------------")