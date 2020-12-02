import IPython
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM
import matplotlib as mpl
import matplotlib.pylab as plt
from scipy.spatial.distance import cosine

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Print out the tokens.
#print (tokenized_text)
#print(list(tokenizer.vocab.keys())[4300:4400])

# Define a new example sentence with multiple meanings of the word "bank"
text = "After stealing money from the bank vault, the bank robber was seen " \
        "fishing on the Mississippi river bank."
question = "questions is this one, who is CEO of LG"
# Add the special tokens.
marked_text = "[CLS] " + text + " [SEP]"
marked_question = "[CLS] " + question + " [SEP]"

# Split the sentence into tokens.
tokenized_text = tokenizer.tokenize(marked_text)
tokenized_question = tokenizer.tokenize(marked_question)

# Map the token strings to their vocabulary indeces.
indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
indexed_q_tokens = tokenizer.convert_tokens_to_ids(tokenized_question)

# Display the words with their indeces.
#for tup in zip(tokenized_text, indexed_tokens):
    #print('{:<12} {:>6,}'.format(tup[0], tup[1]))
#print('')
#for tup in zip(tokenized_question, indexed_q_tokens):
    #print('{:<12} {:>6,}'.format(tup[0], tup[1]))

segments_ids = [1] * len(tokenized_text) ## batch? init 1
segments_q_ids = [1] * len(tokenized_question)

# Python list를 PyTorch tensor로 변환하기 
tokens_tensor = torch.tensor([indexed_tokens])
segments_tensors = torch.tensor([segments_ids])

tokens_q_tensor = torch.tensor([indexed_q_tokens])
segments_q_tensors = torch.tensor([segments_q_ids])

# 미리 학습된 모델(가중치) 불러오기
model = BertModel.from_pretrained('bert-base-uncased')

# 모델 "evaluation" 모드 : feed-forward operation
model.eval()

# 우린 forward pass만 하지 [오차역전파해서 가중치 업데이트, 학습시키기] 이런거 안 하니까 no_grad()
# no_grad() 쓰면 계산 더 빠름 

# 각 레이어의 은닉상태 확인하기
with torch.no_grad():
    encoded_layers, _ = model(tokens_tensor, segments_tensors)
    encoded_q_layers, _ = model(tokens_q_tensor, segments_q_tensors)
    
token_embeddings = torch.stack(encoded_layers, dim=0) # dim = 0
token_embeddings.size() # torch.Size([12, 1, 22, 768])

token_q_embeddings = torch.stack(encoded_q_layers, dim=0) # dim = 0
token_q_embeddings.size()

token_embeddings = torch.squeeze(token_embeddings, dim=1)   # dim = 1 
token_embeddings.size()  # torch.Size([12, 22, 768])

token_q_embeddings = torch.stack(encoded_q_layers, dim=1) # dim = 1
token_q_embeddings.size()

# Mark each of the 22 tokens as belonging to sentence "1".
segments_ids = [1] * len(tokenized_text)
segments_q_ids = [1] * len(tokenized_question)

##print(segments_ids)
##print('')
##print(segments_q_ids)

# Convert inputs to PyTorch tensors
tokens_tensor = torch.tensor([indexed_tokens])
segments_tensors = torch.tensor([segments_ids])

tokens_q_tensor = torch.tensor([indexed_q_tokens])
segments_q_tensors = torch.tensor([segments_q_ids])
'''
# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert-base-uncased')

# Put the model in "evaluation" mode, meaning feed-forward operation.
model.eval()
'''
print ("(Text) Number of layers:", len(encoded_layers))
layer_i = 0

print ("(Question) Number of layers:", len(encoded_q_layers))
layer_q_i = 0

print ("(Text) Number of batches:", len(encoded_layers[layer_i]))
batch_i = 0
print ("(Question) Number of batches:", len(encoded_q_layers[layer_q_i]))
batch_q_i = 0

print ("(Text) Number of tokens:", len(encoded_layers[layer_i][batch_i]))
token_i = 0
print ("(Question) Number of tokens:", len(encoded_q_layers[layer_q_i][batch_q_i]))
token_q_i = 0

print ("(Text) Number of hidden units:", len(encoded_layers[layer_i][batch_i][token_i]))
print ("(Question) Number of hidden units:", len(encoded_q_layers[layer_q_i][batch_q_i][token_q_i]))

# For the 5th token in our sentence, select its feature values from layer 5.
token_i = 5
layer_i = 5
vec = encoded_layers[layer_i][batch_i][token_i]

token_q_i = 5
layer_q_i = 5
vec_q = encoded_q_layers[layer_q_i][batch_q_i][token_q_i]

# Plot the values as a histogram to show their distribution.
#plt.figure(figsize=(10,10))
#plt.hist(vec, bins=200)
##plt.show()

# `encoded_layers` is a Python list.
#print('     Type of encoded_layers: ', type(encoded_layers))
#print('')
#print('     Type of encoded_q_layers: ', type(encoded_q_layers))

# Each layer in the list is a torch tensor.
print('')
print('Tensor shape for each layer: ', encoded_layers[0].size())
print('Tensor shape for each q_layer: ', encoded_q_layers[0].size())
print('')
# Concatenate the tensors for all layers. We use `stack` here to
# create a new dimension in the tensor.
token_embeddings = torch.stack(encoded_layers, dim=0)
token_embeddings.size()
print('')
token_q_embeddings = torch.stack(encoded_q_layers, dim=0)
token_q_embeddings.size()

## eliminate batch dim
token_embeddings = torch.squeeze(token_embeddings, dim = 1)
token_embeddings.size()
print('')
token_q_embeddings = torch.squeeze(token_q_embeddings, dim = 1)
token_q_embeddings.size()
# `token_embeddings` is a [22 x 12 x 768] tensor.

# Swap dimensions 0 and 1.
#token_embeddings = token_embeddings.torch.permute(1,0,2)
#token_embeddings.size()
#print('')
#token_q_embeddings = token_q_embeddings.torch.permute(1,0,2)
#token_q_embeddings.size()

# Stores the token vectors, with shape [22 x 3,072]
token_vecs_cat = []
token_q_vecs_cat = []

# For each token in the sentence...
for token in token_embeddings:  
    # `token` is a [12 x 768] tensor

    # Concatenate the vectors (that is, append them together) from the last 
    # four layers.
    # Each layer vector is 768 values, so `cat_vec` is length 3,072.
    cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)
    
    # Use `cat_vec` to represent `token`.
    token_vecs_cat.append(cat_vec)
print ('vec Shape is: %d x %d' % (len(token_vecs_cat), len(token_vecs_cat[0])))
for token in token_q_embeddings:  
    # `token` is a [12 x 768] tensor

    # Concatenate the vectors (that is, append them together) from the last 
    # four layers.
    # Each layer vector is 768 values, so `cat_vec_q` is length 3,072.
    cat_vec_q = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)
    
    # Use `cat_vec` to represent `token`.
    token_q_vecs_cat.append(cat_vec)
print ('q_vec Shape is: %d x %d' % (len(token_q_vecs_cat), len(token_q_vecs_cat[0])))

# Stores the token vectors, with shape [22 x 3,072]
token_vecs_cat = []



# Stores the token vectors, with shape [22 x 768]
token_vecs_sum = []
token_vecs_q_sum = []

# `token_embeddings` is a [22 x 12 x 768] tensor.

# For each token in the sentence...
for token in token_embeddings:

    # `token` is a [12 x 768] tensor

    # Sum the vectors from the last four layers.
    sum_vec = torch.sum(token[-4:], dim=0)
    
    # Use `sum_vec` to represent `token`.
    token_vecs_sum.append(sum_vec)
print ('vec Shape is: %d x %d' % (len(token_vecs_sum), len(token_vecs_sum[0])))
print('')
for token in token_q_embeddings:

    # `token` is a [12 x 768] tensor

    # Sum the vectors from the last four layers.
    sum_vec_q = torch.sum(token[-4:], dim=0)
    
    # Use `sum_vec` to represent `token`.
    token_vecs_q_sum.append(sum_vec_q)
print ('q_vec Shape is: %d x %d' % (len(token_vecs_q_sum), len(token_vecs_q_sum[0])))

# `encoded_layers` has shape [12 x 1 x 22 x 768]

# `token_vecs` is a tensor with shape [22 x 768]
token_vecs = encoded_layers[11][0]
token_q_vecs = encoded_q_layers[11][0]

# Calculate the average of all 22 token vectors.
sentence_embedding = torch.mean(token_vecs, dim=0)
sentence_q_embedding = torch.mean(token_q_vecs, dim=0)

print ("Our final sentence embedding vector of shape:", sentence_embedding.size())
print ("Our final sentence embedding question vector of shape:", sentence_q_embedding.size())

for i, token_str in enumerate(tokenized_text):
    print (i, token_str)
print('---')
'''
test_list = []
obj_list = []

idx = 0    
for idx in range(len(encoded_layers)): ## 테스트
    print("test indexed word  ", idx+1, " : ",  str(token_vecs_sum[idx][:5]))
    test_list.append(str(token_vecs_sum[idx][:5]))
    idx += 1
print('')
for i, token_str in enumerate(tokenized_question):
    print (i, token_str)
idx = 0
for idx in range(len(encoded_q_layers)): ## 테스트 2
    #print("test indexed q word  ", idx+1, " : ", str(token_vecs_q_sum[idx][:5]))
    idx += 1

idx = 0
for idx in range(len(encoded_q_layers)):
    test_list.append(str(token_vecs_sum[idx][:5]))
    idx += 1

idx = 0
for idx in range(len(encoded_q_layers)):
    st = test_list[idx]
    st = st[8:-2]
    obj_list.append(st)
    idx += 1
print(obj_list)
'''



print('First 5 vector values for each instance of WORD.')
print('')
print("[6] indexed word  ", str(token_vecs_sum[6][:5]))
print("[10] indexed word  ", str(token_vecs_sum[10][:5]))

print(''+'')
print("[6] indexed q word  ", str(token_vecs_q_sum[6][:5]))
print("[10] indexed q word  ", str(token_vecs_q_sum[10][:5]))

print('')
# Calculate the cosine similarity between the word bank 
# in "bank robber" vs "river bank" (different meanings).
#diff_bank = 1 - cosine(token_vecs_sum[10], token_vecs_sum[19])

# Calculate the cosine similarity between the word bank
# in "bank robber" vs "bank vault" (same meaning).
same_bank = 1 - cosine(token_vecs_sum[10], token_vecs_sum[6])
print('Vector similarity for  *similar*  meanings:  %.2f' % same_bank)
#print('Vector similarity for *different* meanings:  %.2f' % diff_bank)

same_bank_q = 1 - cosine(token_vecs_q_sum[10], token_vecs_q_sum[6])
print('q Vector similarity for  *similar*  meanings:  %.2f' % same_bank_q)

### tensor vector : tensor(['...', '...', ...]) convert to ['...', '...', '...', ...]
init_list = []
vec_param = []

idx = 0
for idx in range(len(encoded_q_layers)):
    init_list.append(str(token_vecs_sum[idx][:5]))
    idx += 1
print('token_vec_sum_list\n')
print(init_list)

idx = 0
for idx in range(len(encoded_q_layers)):
    st = init_list[idx]
    st = st[8:-2]
    vec_param.append(st)
    idx += 1
print('')
print('remove "tensor([]) part"\n')
print(vec_param)