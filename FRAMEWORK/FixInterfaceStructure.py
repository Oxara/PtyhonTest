import os, re

class FixControllerStandartonOnProject:

    @staticmethod
    def RunOnEnterpriseHR():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\HR\EnterpriseHR\\enterprisehr.api"

        project_path =os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Repository")
        repository_Interface_Files = IO_Helper.GetFiles(project_path, r".*Repository\.cs$")
        FixInterfaceStructure.FixFolder(project_path, repository_Interface_Files, "Repository")
        FixInterfaceStructure.remove_empty_folders(project_path)

        project_path =os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Services")
        repository_Interface_Files = IO_Helper.GetFiles(project_path, r".*Service\.cs$")
        FixInterfaceStructure.FixFolder(project_path, repository_Interface_Files, "Service")
        FixInterfaceStructure.remove_empty_folders(project_path)

        project_path =os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Validation")
        repository_Interface_Files = IO_Helper.GetFiles(project_path, r".*Validation\.cs$")
        FixInterfaceStructure.FixFolder(project_path, repository_Interface_Files, "Validation") 
        FixInterfaceStructure.remove_empty_folders(project_path)

class FixInterfaceStructure:
       
    @staticmethod
    def FixFolder(project_path, file_paths, appFolder):
        for file_path in file_paths:

            # _Base ile başlayan klasördeki dosyalara atla
            if "_Injection" in file_path:
                continue

            file_name = os.path.basename(file_path)
            
            # I ile başlayanları file_paths path'inin altındaki Interface klasörüne kes & yapıştır
            if file_name.startswith("I"):
                  target_path = os.path.join(project_path, "Interface")
            else: target_path = os.path.join(project_path, appFolder)
                
            # Eğer target_path mevcut değilse, oluştur
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            # Dosyayı taşı
            new_path = os.path.join(target_path, file_name)     
            os.rename(file_path, new_path)

    def remove_empty_folders(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                if not os.listdir(folder_path):  # Klasör boşsa
                    os.rmdir(folder_path)        # Klasörü sil


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


FixControllerStandartonOnProject.RunOnEnterpriseHR()