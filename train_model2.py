import data_loader as dl
import model_utils as M 
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense, LSTM, InputLayer, Bidirectional, TimeDistributed,Embedding, Activation,Flatten,Bidirectional,Input,concatenate
from keras.optimizers import Adam
from keras.utils import plot_model
from sklearn.model_selection import train_test_split

MAX_LENGTH = 50

data = dl.load_dataset()
embedder = dl.get_embedder()
padded_sent_dataset, padded_tag_dataset, X, Y, MAX_LENGTH = dl.preprocess_data(data)
tag2id,id2tag = dl.get_tag_dicts(padded_tag_dataset)

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3,shuffle=True)
embedding_matrix = dl.get_embedding_matrix(embedder)

# Model 2 Architecture
model2 = Sequential(name="Bi directional single layer LSTM")
model2.add(Embedding(input_dim=embedding_matrix.shape[0],output_dim=embedding_matrix.shape[1],
                    weights=[embedding_matrix],trainable=False,input_length=MAX_LENGTH,name='embedding_1'))
model2.add(Bidirectional(LSTM(64, return_sequences=True),name='bi_lstm_1'))
model2.add(TimeDistributed(Dense(len(tag2id),activation='softmax',name='dense_1'),name='timedist_1'))
model2.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy',M.ignore_class_accuracy(9)])
 
model2.summary()
plot_model(model2)

# Training
history2 = model2.fit(X_train,Y_train,epochs=20,batch_size=128,validation_split=0.2,verbose=1)
M.plot_model_history(model2,history2)

# Evaluation
model2.evaluate(X_test,Y_test)

# Code provided by Shreyansh Chordia