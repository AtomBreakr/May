import torch.nn as nn
from NLU.Tokenizer import encode

class IntentClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, num_intents):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.hidden_layer = nn.Linear(embedding_dim, embedding_dim)
        self.relu = nn.ReLU()
        self.output_layer = nn.Linear(embedding_dim, num_intents)

    def forward(self, x):
        embedded = self.embedding(x)
        pooled = embedded.mean(dim=0)
        hidden = self.relu(self.hidden_layer(pooled))
        output = self.output_layer(hidden)
        return output
