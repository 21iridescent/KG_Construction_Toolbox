# referenced https://colab.research.google.com/drive/1F8wCEdcLT4cYPNT9EEhRd9cVh024V0L0#scrollTo=gVsPKEil1wLA
from re import L
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import numpy as np
import pandas as pd
import re
import xlsxwriter
from ultilis import convert_title

def toc_relation_extractor(path):
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    # Get the outlines of the document.
    outlines = document.get_outlines()
    print(outlines)
    toc_list = []
    for i in outlines:
        toc_list.append(i[0])
    toc_depth = len(set(toc_list))
    #print(toc_list)
    print('toc depth: {}'.format(toc_depth))
    toc_list = []

    stopwords = ['Summary', 'Exercises', 'Bibliographic Notes', ]
    for k in range(toc_depth):
        temp_list = []
        toc_list.append(temp_list)
    print(toc_list)
    triples = []
    previous_index = 1
    previous_name = 'test'
    #print(outlines)
    outlines = document.get_outlines()
    #for i in outlines:
        #print(i)
    for outline in outlines:
        # print('yes')
        current_index = outline[0]
        #print(current_index)
        #print(current_index)
        current_name = outline[1]
        toc_list[current_index-1].append(current_name)

        if current_index - previous_index == 0 and current_index > 1:
            # previous_index = current_index
            '''
            super_topics = toc_list[current_index-2][-1]
            current_name = current_name.replace('Chapter ', '')
            super_topics = super_topics.replace('Chapter ', '')
            super_topics = re.sub('(^\d*.\d*.\d*.\d*\s)', '', super_topics)
            current_name = re.sub('(^\d*.\d*.\d*.\d*\s)', '', current_name)
            '''
            super_topics = convert_title(super_topics)
            current_name = convert_title(current_name)
            print(super_topics)
            relation = [current_name, "is a sub-chapter of", super_topics]
            #print(relation)
            inter = list(set(stopwords).intersection(set(relation)))
            #print(inter)
            if inter == []:
                triples.append(relation)
            previous_name = current_name
            continue

        elif current_index - previous_index == 1:
            k = current_index - previous_index
            super_topics = toc_list[current_index-k-1][-1]
            """
            current_name = current_name.replace('Chapter ', '')
            super_topics = super_topics.replace('Chapter ', '')
            current_name = re.sub('(^\d*.\d*.\d*.\d*\s)', '', current_name)
            #current_name = re.sub('(\d*\.*\d*\s)', ' ', current_name).replace('chapter ', '')
            super_topics = re.sub('(^\d*.\d*.\d*.\d*\s)', '', super_topics)
            """
            super_topics = convert_title(super_topics)
            current_name = convert_title(current_name)
            # print(super_topics)
            relation = [current_name, "is a sub-chapter of", super_topics]
            inter = list(set(stopwords).intersection(set(relation)))
            #print(inter)
            if inter == []:
                triples.append(relation)

        elif current_index - previous_index < 0 and current_index != 1:
            super_topics = toc_list[current_index-2][-1]
            super_topics = convert_title(super_topics)
            current_name = convert_title(current_name)
            '''
            current_name = current_name.replace('Chapter ', '')
            super_topics = super_topics.replace('Chapter ', '')

            current_name = re.sub('(^\d*.\d*.\d*.\d*\s)', '', current_name)
            super_topics = re.sub('(^\d*.\d*.\d*.\d*\s)', '', super_topics)
            '''
            relation = [current_name, "is a sub-chapter of", super_topics]
            inter = list(set(stopwords).intersection(set(relation)))
            # print(inter)
            if inter == []:
                triples.append(relation)

        previous_index = current_index
        previous_name = current_name
    return triples

def save(triples, path='../toc3.xlsx'):
    # file_name = args.in_dir.strip('.xlsx')
    df = pd.DataFrame(triples, columns=['subject', 'relation', 'object'])
    #csv.to_excel('1.xlsx', sheet_name='data')
    '''
    file_name = 'result_' + args.in_dir
    folder = os.getcwd() + args.out_dir

    if not os.path.exists(folder):
        os.makedirs(folder)
   
    folder_path = folder + '/' + file_name
    print(folder_path)
    # print(self.cat_rel)
    '''
    #df.to_excel(path, index=False)
    df.to_excel(path, engine='xlsxwriter')

#triples = toc_relation_extractor('Data_Mining.pdf')

triples = toc_relation_extractor('Data Mining_ The Textbook [Aggarwal 2015-04-14].pdf')
save(triples)

