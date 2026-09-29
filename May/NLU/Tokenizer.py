from NLU.Training_Data import training_data

def build_vocab (training_data: dict) -> dict:

    vocab = {"<UNK>": 0}

    for value in training_data.values():
        for sentence in value:
            split_sentence = sentence.lower().split()
            for word in split_sentence:
                if word not in vocab:
                    vocab[word] = len(vocab) 

    return vocab

vocab = build_vocab(training_data)

def encode (sentence: str) -> list[int]: 

    tokens = []
    split_sentence = sentence.lower().split()

    for word in split_sentence:
        if word in vocab:
            tokens.append(vocab.get(word))
        else:
            tokens.append(vocab["<UNK>"])

    return tokens
