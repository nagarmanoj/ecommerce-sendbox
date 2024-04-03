import pandas as pd

class ImportProduct(object):
    def __init__(self,csv_file,chunk_size,chunk_index):
        self.csv_file = csv_file
        self.chunk_size = chunk_size
        self.chunkIndex = chunk_index

    def total_chunk_list(self,df):
        chunkList = []        
        for item in df:
            chunkList.append(item)
        return chunkList
        
    def import_data(self):
        print(self.chunk_size)
        print(self.csv_file)        
        chunk_list = self.total_chunk_list()
        totalChunk = len(chunk_list)               
        for index in range(0,totalChunk):
            if index == self.chunkIndex:
                currentChunk = chunk_list[index]
                print(currentChunk.info())        
                for index, row in currentChunk.iterrows():
                    print(row['title'])
                    
    
if __name__ == "__main__":
    file = 'New_CSV_Files/All Electronics.csv'
    chunk_size = 500
    chunk_index = 1
    csv_data = ImportProduct(file,chunk_size,chunk_index)
    data = csv_data.read_csv_file()