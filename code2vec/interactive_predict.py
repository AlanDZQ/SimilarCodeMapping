import traceback

from common import common
from extractor import Extractor
import os

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = 'JavaExtractor/JavaExtractor.jar'
# JAR_PATH = 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'


class InteractivePredictor:
    exit_keywords = ['exit', 'quit', 'q']

    def __init__(self, config, model):
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(config,
                                        jar_path=JAR_PATH,
                                        max_path_length=MAX_PATH_LENGTH,
                                        max_path_width=MAX_PATH_WIDTH)

    def read_file(self, input_filename):
        with open(input_filename, 'r') as file:
            return file.readlines()

    # def predict(self):
    #     input_filename = 'Input.java'
    #     print('Starting interactive prediction...')
    #     while True:
    #         print(
    #             'Modify the file: "%s" and press any key when ready, or "q" / "quit" / "exit" to exit' % input_filename)
    #         user_input = input()
    #         if user_input.lower() in self.exit_keywords:
    #             print('Exiting...')
    #             return
    #         try:
    #             predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(input_filename)
    #         except ValueError as e:
    #             print(e)
    #             continue
    #         results, code_vectors = self.model.predict(predict_lines)
    #         prediction_results = common.parse_results(results, hash_to_string_dict, topk=SHOW_TOP_CONTEXTS)
    #         for i, method_prediction in enumerate(prediction_results):
    #             print('Original name:\t' + method_prediction.original_name)
    #             for name_prob_pair in method_prediction.predictions:
    #                 print('\t(%f) predicted: %s' % (name_prob_pair['probability'], name_prob_pair['name']))
    #             print('Attention:')
    #             for attention_obj in method_prediction.attention_paths:
    #                 print('%f\tcontext: %s,%s,%s' % (
    #                 attention_obj['score'], attention_obj['token1'], attention_obj['path'], attention_obj['token2']))
    #             if self.config.EXPORT_CODE_VECTORS:
    #                 print('Code vector:')
    #                 print(' '.join(map(str, code_vectors[i])))


    # def predict(self):
    #     files = list_all_files('/Users/apple/Desktop/Test_Neg')
    #     print('Starting interactive prediction...')
    #     out = open("Test_Neg.txt", mode='w')
    #     for file in files:
    #         if file.split('.')[-1] == 'java':
    #             try:
    #                 predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(file)
    #             except ValueError as e:
    #                 print(e)
    #                 continue
    #             results, code_vectors = self.model.predict(predict_lines)
    #             # prediction_results = common.parse_results(results, hash_to_string_dict, topk=SHOW_TOP_CONTEXTS)
    #             if len(code_vectors) == 2:
    #                 out.write(' '.join(map(str, code_vectors[0])) + ' ')
    #                 out.write(' '.join(map(str, code_vectors[1])) + ' ')
    #                 out.write('\n')
    #     out.close()


    def predict(self):
        files = list_all_files('/Users/apple/Desktop/test')
        print('Starting interactive prediction...')
        out = open("./data/ABC.txt", mode='w')
        for file in files:
            if file.split('.')[-1] == 'java':
                # print(file)
                try:
                    predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(file)
                except ValueError as e:
                    print(e)
                    continue
                results, code_vectors = self.model.predict(predict_lines)
                prediction_results = common.parse_results(results, hash_to_string_dict, topk=SHOW_TOP_CONTEXTS)
                for i, method_prediction in enumerate(prediction_results):
                    out.write(file + ' ' + method_prediction.original_name + ' ' + ' '.join(map(str, code_vectors[i])))
                    out.write('\n')
        out.close()



def list_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for file in list:
        path = os.path.join(rootdir, file)
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files