import codecs


# list of correct grammatical patterns
grammar_list = [["adv","aux","pron","verb","part","verb","mark"],["aux","pron","verb","det","noun","mark"],
                ["pron","verb","adp","propn","punct"],["pron","verb","adp","noun","punct"],["aux","pron","verb","det","noun","mark"],
                ["aux","pron","verb","det","propn","mark"],["pron","verb","pron","det","propn","punct"],["pron","verb","pron","det","noun","punct"],
                ["adv","verb","pron","mark"],["verb","pron","adp","propn","mark"],["pron","aux","adv","verb","noun","punct"],
                ["pron","verb","pron","adv","punct"],["adv","verb","pron","propn","adv","punct"],["adv","verb","adp1","adj","adp","pron","punct"],
                ["adv","verb","pron","adv","adp","noun","punct"],["adv","verb","adv","noun","det","mark"],["adv","aux","adv","pron","noun","adp","adj","punct"]
               ,["pron","verb","adv","punct"],["pron","aux","adv","adj","punct"],["verb","pron","adp","noun","mark"],["noun","verb","noun","punct"]]

# sentence tokenizer
def sent_tokenizer(sentance):
    first_split =  sentance.split(' ')

    # check for punctiouation
    last_char = first_split[len(first_split)-1]
    # check if the last word in the sentence contains '.' or '?' and splite it
    if  last_char[len(last_char)-1] == ".":
        new_char =last_char.replace(".","")
        first_split.remove(last_char)
        first_split.append(new_char)
        first_split.append(".")
    if  last_char[len(last_char)-1] == "?":
        new_char = last_char.replace("?", "")
        first_split.remove(last_char)
        first_split.append(new_char)

        first_split.append("?")
    #print(first_split)

    pos = word_tagger(first_split)

    return pos

# tagging the words in the sentence
def word_tagger(list_of_words):
    pos_token = []

    for w in list_of_words:

        if w == 'å':
            pos_token.append([w, "part"])
            return pos_token

        dataset = codecs.open('data.DICT', 'r',encoding='UTF-8')
        for p in dataset:
            p_split = p.split(' ')
            if w == p_split[0].lower():
                if([w,p_split[1].lower().replace('\n','')] not in pos_token):
                    pos_token.append([w,p_split[1].lower().replace('\n','')])
                    break


    return pos_token

# the main function that perform the checking and correction for rule-based technique
def error_check(sentence):
    alternatives = []
    sent_token = sent_tokenizer(sentence)
    sentence_pos = []
    sentence_word = []

    # add the words in the sentence
    for i in sent_token:
        sentence_word.append(i[0])
    # add the class of each word
    for i in sent_token:
        sentence_pos.append(i[1])

    # loop over grammar list to find a list that have the same length as the sentence
    # and its elements are the same as the sentence words as well
    for sent in grammar_list:
        temp_sent_token = sent_tokenizer(sentence)
        altern = []
        check = all(item in sent for item in sentence_pos)
        if len(sent) == len(sentence_pos) and check:
            # this list is to rearrange the words in the given sentence in right order
            # based on the right patern in grammar list
            for i in range(len(sent)):
                altern.append("0")
            # this variable is to determine the index of the word in altern
            index = 0
            for pos in sent:
                for word in temp_sent_token:
                    if word[1] == pos:
                        if altern[sent.index(pos)] =="0":
                            altern[sent.index(pos)] = word[0]
                            break
            res = ' '.join(altern)
            alternatives.append(res)
    return alternatives

# test
sent8 = "jeg har spist ikke maten."
print("--------------------Test------------------------------")
print(f"The inserted erroneous sentence: {sent8} ")
print(f"The correction:{error_check(sent8)} " )
print("---------------------------------------------------")