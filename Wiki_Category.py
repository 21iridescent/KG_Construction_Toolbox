import os.path

from mediawiki import MediaWiki
import pandas as pd
import mediawiki
import argparse

parser = argparse.ArgumentParser(description="Wiki Cate.")
parser.add_argument('--in_dir', type=str, default='metabook.xlsx')
parser.add_argument('--out_dir', type=str, default='/output')
args = parser.parse_args()

c_p = os.getcwd()
'ss'
print(c_p)

wikipedia = MediaWiki()
path = os.path.join(c_p, args.in_dir)
# entity = pd.read_excel(path, names=['subject'])

# entities = ['data mining', 'bubble sort']
class Wiki_Category_extractor:
    def __init__(self):
        self.cat_rel = pd.DataFrame(columns=['entity name', 'relation', 'categories'])

    def read(self, path):
        self.c_p = os.getcwd()
        self.path = os.path.join(self.c_p, path)
        self.entity = pd.read_excel(self.path, names=['subject', 'subject2'])
        # return self.entity

    def extract(self):
        df = self.entity
        for index, row in df.iterrows():
            index = 0
            entity_name = row['subject']
            print(entity_name)
            try:
                # try to load the wikipedia page
                page = wikipedia.page(entity_name, auto_suggest=False)
                # print('Correct: {}'.format(entity))
                # entity_wiki.append(page)

                # name_list.append(entity)
                # entity_title = str(page.title)
                # entity_summary = str(page.summary)
                # entity_content = str(page.content)
                # entity_links = str(page.links)
                # print(entity_links)

                entity_categories = str(page.categories)

                '''
                temp = pd.DataFrame({'entity name':entity_name, 'wikipedia title': entity_title,'wikidata id': id, 
                      'summary':entity_summary, 'content':entity_content, 'links': entity_links, 
                             'categories': entity_categories}, index=[index])
                '''

                entity_categories = entity_categories.replace('[', '').replace(']', '')
                entity_categories = entity_categories.replace("'", '').split(', ')

                for i in entity_categories:
                    temp = pd.DataFrame({'entity name': entity_name,
                                         'relation': 'wiki-categories',
                                         'categories': i}, index=[index])
                    index = index + 1
                    # cat_rel = cat_rel.append(temp)
                    self.cat_rel = pd.concat([self.cat_rel, temp])

            except (mediawiki.exceptions.PageError, KeyError):
                # if a "PageError" was raised, ignore it and continue to next link
                # print('Error: {}'.format(entity))
                # error_list.append(entity_name)
                '''
                temp = pd.DataFrame({'entity name':entity_name, 'wikidata id': id, 
                      'summary':' ', 'content':' ', 'links': ' ', 
                             'categories': ' '}, index=[index])
                '''
                temp = pd.DataFrame({'entity name': entity_name,
                                     'relation': 'wiki-categories',
                                     'categories': 'PageError'}, index=[index])
                # cat_rel = cat_rel.concat(temp)
                self.cat_rel = pd.concat([self.cat_rel, temp])
                # error_entity = error_entity.append(temp)
                continue

            except mediawiki.exceptions.DisambiguationError as e:
                # print('DisambiguationError: {}'.format(e.options))
                # print(type(e.options[0]))
                temp = pd.DataFrame({'entity name': entity_name,
                                     'relation': 'wiki-categories',
                                     'categories': 'DisambiguationError'}, index=[index])
                # cat_rel = cat_rel.concat(temp)
                self.cat_rel = pd.concat([self.cat_rel, temp])
                continue
        # print(cat_rel)
        return self.cat_rel

    def save(self):
        # file_name = args.in_dir.strip('.xlsx')
        file_name = 'result_' + args.in_dir
        folder = os.getcwd() + args.out_dir
        # os.mkdir(args.out_dir)
        # path = os.path.join(args.out_dir, file_name)
        # print(path)

        if not os.path.exists(folder):
            os.makedirs(folder)

        folder_path = folder + '/' + file_name
        print(folder_path)
        # print(self.cat_rel)
        self.cat_rel.to_excel(folder_path)

# print(entity)