# SimilarCodeMapping

This project is used for mapping similar java methods.

1. code2vec:
https://github.com/tech-srl/code2vec

2. JPredict & CSharpextractor (use the version in code2vec direction if you want to extract CS functions from code) are used to extract methods code pairs from code documents. 

3. APIProjection is the a project which is used for training the CNN model and predict the result.  

If you have questions about the model and the training/testing data, please read the document: introduction of the model.

Data:
1. J2EE similar java methods: 
https://www.jianguoyun.com/p/DVhW_XQQh7jKBhjk_ccB

2. data from BigCloneBench: 

https://github.com/clonebench/BigCloneBench

This is a small part I used in my training process: https://www.jianguoyun.com/p/DfBSXNQQh7jKBhjj_ccB