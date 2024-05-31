import os
import re

class IO_Helper:
    
    @staticmethod
    def GetFiles(directory, pattern):
        matching_files = []

        # Directory'deki tüm dosya ve dizinleri dolaş
        for root, dirs, files in os.walk(directory):
            for file_name in files:

                # Dosyanın tam yolu
                full_path = os.path.join(root, file_name)

                # Dosya adı regex deseniyle eşleşiyorsa listeye ekle
                if re.match(pattern, file_name): matching_files.append(full_path)

        return matching_files
    
    @staticmethod
    def ReadLines(file_path, encoding):
        with open(file_path, 'r', encoding = encoding) as file: return file.readlines()

    @staticmethod
    def Read(file_path, encoding):
        with open(file_path, 'r', encoding = encoding) as file: return file.read()


    @staticmethod
    def WriteLines(file_path, updated_lines, encoding):
        with open(file_path, 'w', encoding = encoding) as file: file.writelines(updated_lines)

    @staticmethod

    def RemoveEmptyFolders(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                if not os.listdir(folder_path):  # Klasör boşsa
                    os.rmdir(folder_path)        # Klasörü sil