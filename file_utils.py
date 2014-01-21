__author__ = 'rogersjeffrey'
import gzip
def read_gzip_files(gzip_file):
        f = gzip.open(gzip_file, 'rb')
        file_content = f.read()
        file_data=file_content.strip().split("\n")
        f.close()
        return file_data