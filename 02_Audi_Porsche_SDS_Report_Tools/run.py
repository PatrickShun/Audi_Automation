#! /usr/bin/env python

import os
import shutil
from model.Get_Config import Config
from model.tr_results import GetTResult
from model.write_report import WriteResult

config = Config()
testporj = ['word', 'sentence', 'nlu_stage', 'nlu_live']

def result_files(folder):
    print(folder)
    dir_files = []
    for roots, dirs, files in os.walk(folder):
        for dir in dirs:
            for file in os.listdir(os.path.join(roots, dir)):
                dir_file = os.path.join(os.path.join(roots, dir), file)
                if dir_file.endswith('.xls'):
                    dir_files.append(dir_file)
    return dir_files


def get_language(file):
    if any(['cantonese' in file, '粤语' in file]):
        return 'cantonese'
    elif any(['mandarin' in file, '中文' in file]):
        return 'mandarin'


def get_testsuit(file):
    filename = os.path.basename(file).replace('.xls', '')
    print(filename)
    if filename.split('_')[-2].lower() in ['cantonese', 'mandarin']:
        print(filename.split('_')[2])
        return filename.split('_')[2]
    elif filename.split('_')[-3] in ['氛围灯', '氛围灯训练集']:
        return '_'.join(filename.split('_')[-3:-1])
    elif filename.split('_')[-2].lower() == '中文':
        return 'mandarin'


def get_historicalData(file):
    if 'historical' in file:
        return 1
    else:
        return 0


def get_envirment(file):
    if all(['nlu' in file, 'live' in file]):
        return 'live'
    elif all(['nlu' in file, 'stage' in file]):
        return 'stage'


def get_testtype(file):
    if 'asr' in file:
        return 'asr'
    elif 'nlu' in file:
        return 'nlu'


def write_data(file, dir_report):
    global sum_data, detail_data
    print("FileName is ：" + file)
    language, testsuit, testtype, enviroment , hisbool = get_language(file), get_testsuit(file), get_testtype(file), get_envirment(file), get_historicalData(file)
    print (language, testsuit, testtype, enviroment, hisbool)  # mandarin 氛围灯_中文 nlu stage
    tr = GetTResult(file)
    if testtype == 'asr':
        sum_data = {'word': tr.sum_word_data(), 'sentence': tr.sum_sentence_data()}
        detail_data = tr.detail_asr_data()
    elif testtype == 'nlu':
        sum_data = {'nlu': tr.sum_nlu_data()}
        detail_data = tr.detail_nlu_data()

    wb.write_summary(testsuit, enviroment, sum_data, hisbool)
    wb.write_data(language, enviroment, testtype, detail_data)
    wb.save(dir_report)


if __name__ == '__main__':
    if not os.path.exists(config.dir_result):
        os.mkdir(config.dir_result)
    dir_report = os.path.join(config.dir_result, os.path.basename(config.dir_template))
    shutil.copyfile(config.dir_template, dir_report)
    asr_result_files = result_files(config.dir_asr)
    asr_his_result_files = result_files(config.dir_his_asr)
    nlu_result_files = result_files(config.dir_nlu)
    nlu_his_result_files = result_files(config.dir_his_nlu)
    wb = WriteResult(dir_report)

    # 遍历所有的ASR result xls；
    for file in asr_result_files:
        print(file)
        write_data(file, dir_report)
    for file in asr_his_result_files:
        write_data(file, dir_report)

    # 遍历所有的NLU result xls；
    for file in nlu_result_files:
        write_data(file, dir_report)
    for file in nlu_his_result_files:
        write_data(file, dir_report)

    wb.save(dir_report)













