import glob
from tqdm import tqdm
import re

split_end_word = '.?!;:。？！；…'

def books(top_file=0):  # formatted_one_article_per_line
    global split_end_word
    books_path = './data/english_data/books1/epubtxt'  # 读取路径, 下面一个文件一本书
    output_filename = './data/origin_data/books1' + (f'.{top_file}' if top_file else '') + '.txt'  # 保存路径

    with open(output_filename, 'w', encoding='utf8') as ofile:
        paths = glob.glob(books_path + '/' + '*.txt', recursive=True)
        if top_file:
            paths = paths[:top_file]  # 提取前几个
        save_doc_num = 0  # 保存的文档数量
        save_line_num = 0
        for i, filename in tqdm(enumerate(paths), 'books'):
            with open(filename, mode='r', encoding='utf-8-sig') as file:
                text = []
                for line in file:
                    if line.strip() == '':
                        continue
                    # 句子切割
                    # sents = re.split(f'(?<=[{split_end_word}])(?=[^{split_end_word}])', line)  # save_doc_num: 17868 save_line_num: 118259328
                    sents = [line.strip()]  # save_doc_num: 17868 save_line_num: 36775223
                    for sent in sents:
                        sent = sent.lstrip(f' {split_end_word}').strip()
                        if sent:
                            text.append(sent)
                # 文章结束
                save_line_num += len(text) + 1
                text = '\n'.join(text) + '\n\n'
                ofile.write(text)
                save_doc_num += 1
    print('save_doc_num:', save_doc_num, 'save_line_num:', save_line_num)


def wiki(top_n=0):  # formatted_one_article_per_line
    global split_end_word
    books_path = './data/english_data/wiki'  # 读取路径, 下面一个文件一批文章
    output_filename = './data/origin_data/wiki' + (f'.{top_n}' if top_n else '') + '.txt'  # 保存路径

    with open(output_filename, 'w', encoding='utf8') as ofile:
        paths = glob.glob(books_path + '/wiki_*', recursive=True)
        save_doc_num = 0  # 保存的文档数量
        save_line_num = 0
        for filename in sorted(paths):
            print(filename)
            with open(filename, mode='r', encoding='utf-8-sig') as file:
                pbar = tqdm(desc='wiki')
                while True:
                    text = []
                    jump = True
                    # 遇到文章开头
                    for line in file:
                        line = line.strip()
                        if line[:9] == '<doc id="' and line[-2:] == '">':
                            jump = False
                            break
                    # 文章内部
                    for line in file:
                        line = line.strip()
                        if line == '</doc>':
                            jump = False
                            break
                        # 句子切割
                        sents = re.split(f'(?<=[{split_end_word}])(?=[^{split_end_word}])', line)
                        for sent in sents:
                            sent = sent.lstrip(f' {split_end_word}').strip()
                            if sent:
                                text.append(sent)
                    # 文章结束
                    if len(text) > 1:
                        save_line_num += len(text) + 1
                        text = '\n'.join(text) + '\n\n'
                        ofile.write(text)
                        pbar.update(1)
                        save_doc_num += 1
                    if jump or top_n and save_doc_num >= top_n:
                        break
            if top_n and save_doc_num >= top_n:  # 提取前几个
                break
    # save_doc_num: 7012241 save_line_num: 174294489
    print('save_doc_num:', save_doc_num, 'save_line_num:', save_line_num)


def 合并语料():
    paths = [  # formatted_one_article_per_line
        './data/origin_data/wiki.txt',
        './data/origin_data/books1.txt',
    ]
    ouput_path = './data/origin_data/wikibook.txt'
    with open(ouput_path, 'w', encoding='utf8') as w:
        save_doc_num = 0  # 保存的文档数量
        save_line_num = 0
        for p in paths:
            print(p)
            with open(p, 'r', encoding='utf8') as r:
                for line in tqdm(r, '合并语料'):
                    if line == '\n':
                        save_doc_num += 1
                    w.write(line)
                    save_line_num += 1
    # save_doc_num: 7030109 save_line_num: 211069712
    print('save_doc_num:', save_doc_num, 'save_line_num:', save_line_num)


if __name__ == '__main__':
    # books()
    wiki(100)
    # 合并语料()