import os, re

class FixLazyResoulutionOnProject:

    @staticmethod
    def RunOnFramwork():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\Framework\\Draft.Framework"

        repository_Interface_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Repository"), r".*Repository\.cs$")
        FixLazyResoulutionOnFile.UpdateOnSection(repository_Interface_Files)

        validation_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Validation"), r".*Validation\.cs$")
        FixLazyResoulutionOnFile.UpdateOnSection(validation_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Services") , r".*Service\.cs$")
        FixLazyResoulutionOnFile.UpdateOnSection(service_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\Framework.Presantation.WebAPI\Controllers"), r".*Controller\.cs$")
        FixLazyResoulutionOnFile.UpdateOnSection(controller_Files)

    @staticmethod
    def RunOnEnterpriseHR():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\HR\EnterpriseHR\\enterprisehr.api"

        repository_Interface_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Repository"), r".*Repository\.cs$")
        FixLazyResoulutionOnFile.UpdateOnSection(repository_Interface_Files)

        validation_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Validation"), r".*Validation\.cs$")
        FixLazyResoulutionOnFile.UpdateOnSection(validation_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Services") , r".*Service\.cs$")
        FixLazyResoulutionOnFile.UpdateOnSection(service_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.WebAPI\Controllers"), r".*Controller\.cs$")
        FixLazyResoulutionOnFile.UpdateOnSection(controller_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.MobileAPI\Controllers"), r".*Controller\.cs$")
        FixLazyResoulutionOnFile.UpdateOnSection(controller_Files)        

        
class FixLazyResoulutionOnFile:
       
    @staticmethod
    def UpdateOnSection(file_paths):
        for file_path in file_paths:

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.Read(file_path, 'utf-8')

            # Düzenli ifade ile eşleştirme ve loglama
            pattern = re.compile(r'private readonly (\w+) (\w+) = serviceProvider\.GetRequiredService<\1>\(\);')
            matches = pattern.findall(lines)

            # İlk güncelleme: Lazy<> ile değiştir
            updated_code = pattern.sub(r'private readonly Lazy<\1> \2 = serviceProvider.GetRequiredService<Lazy<\1>>();', lines)

            # İkinci güncelleme: await [değişkenAdı]. -> await [değişkenAdı].Value.
            for match in matches:
                variable_name = match[1]
                await_pattern = re.compile(rf'{variable_name}\.')
                updated_code = await_pattern.sub(rf'{variable_name}.Value.', updated_code)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_code, 'utf-8')

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

# FixLazyResoulutionOnProject.RunOnFramwork()
FixLazyResoulutionOnProject.RunOnEnterpriseHR()