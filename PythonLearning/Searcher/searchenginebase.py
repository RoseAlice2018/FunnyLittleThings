class SearchEngineBase(object):
    def __init__(self) -> None:
        pass 

    def add_corpus(self, file_path):
        with open(file_path, 'r') as fin:
            text = fin.read()
            self.process_corpus(file_path, text)

    def process_corpus(self, id, text):
        raise Exception('process_corpus not implemented.')

    def search(self, query):
        raise Exception('search not implemented.')

def main(search_engine):
    for file_path in ['./doc/1.txt', './doc/2.txt', './doc/3.txt', './doc/4.txt', './doc/5.txt']:
        search_engine.add_corpus(file_path)
    
    while True:
        query = input()
        results = search_engine.search(query)
        print('found {} result(s):'.format(len(results)))
        for result in results:
            print(result)

    