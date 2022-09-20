# referenced https://colab.research.google.com/drive/1F8wCEdcLT4cYPNT9EEhRd9cVh024V0L0#scrollTo=gVsPKEil1wLA
from re import L
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import numpy as np

# Open a PDF document.
fp = open('Data_Mining.pdf', 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser)
# Get the outlines of the document.
outlines = document.get_outlines()

def toc_relation_extractor(path):
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    # Get the outlines of the document.
    outlines = document.get_outlines()
    toc_list = []
    for i in outlines:
        toc_list.append(i[0])
    toc_depth = len(set(toc_list))
    #print(toc_list)
    #print(toc_depth)
    toc_list = []
    for k in range(toc_depth):
        temp_list = []
        toc_list.append(temp_list)

    #print(toc_list)
    triples = [['Head', 'Relation', 'Tail']]
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
            super_topics = toc_list[current_index-2][-1]
            relation = [current_name, " is a sub-chapter of ", super_topics]
            print(relation)
            triples.append(relation)
            previous_name = current_name
            continue

        if current_index - previous_index == 1:
            k = current_index - previous_index
            super_topics = toc_list[current_index-k-1][-1]
            relation = [current_name, " is a sub-chapter of ", super_topics]
            print(relation)
            triples.append(relation)

        previous_index = current_index
        previous_name = current_name

    #print('log')
    return triples

triples = toc_relation_extractor('Data_Mining.pdf')

