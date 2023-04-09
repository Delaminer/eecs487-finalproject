from transformers import BertTokenizer, AutoTokenizer, BertForPreTraining, BertModel, AdamW
from transformers import BertForSequenceClassification
from torch.nn import CosineEmbeddingLoss
import torch
from torch.nn import functional as F

# from transformers import get_linear_schedule_with_warmup
# scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps, num_train_steps)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased", return_dict=True)
optimizer = AdamW(model.parameters(), lr=1e-5)

# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
original = "What is the difference between the and a? "
duplicate = "How would i use a and the?"

def get_inputs(sentence):
        
    encoding = tokenizer([sentence], return_tensors='pt', padding=True, truncation=True)
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']
    return input_ids, attention_mask

criterion = CosineEmbeddingLoss()
labels = torch.tensor([1,0]).unsqueeze(0)
input_id1, attention_mask1 = get_inputs(original)
input_id2, attention_mask2 = get_inputs(duplicate)
out1 = model(input_id1, attention_mask=attention_mask1)
out2 = model(input_id2, attention_mask=attention_mask2)
y = 1
# print(outputs)
# print(outputs.last_hidden_state.shape)
# print(outputs.pooler_output.shape)
# print(outputs.keys())
temp = out1.pooler_output[0]
print(out1.pooler_output[0])
loss = criterion(out1.pooler_output[0], out2.pooler_output[0], torch.tensor(y, dtype=torch.float))
# loss = F.cross_entropy(labels, outputs.logitd)
input_id1, attention_mask1 = get_inputs(original)
out1 = model(input_id1, attention_mask=attention_mask1)
print(out1.pooler_output[0] == temp)
loss.backward()
optimizer.step()
print(loss.item())

input_id1, attention_mask1 = get_inputs(original)
out1 = model(input_id1, attention_mask=attention_mask1)
print(out1.pooler_output[0] == temp)