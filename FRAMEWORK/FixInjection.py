import os, re


class FixInjectionOnProject:

    @staticmethod
    def RunOnEnterpriseHR():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\HR\EnterpriseHR\\enterprisehr.api"

        validation_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Validation"), r".*Validation\.cs$")
        FixInjectionOnFile.UpdateValidation(validation_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Services") , r".*Service\.cs$")
        FixInjectionOnFile.UpdateService(service_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Repository") , r".*Repository\.cs$")
        FixInjectionOnFile.UpdateRepository(service_Files)
        
class FixInjectionOnFile:
       
    @staticmethod
    def UpdateService(file_paths):
        for file_path in file_paths:

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')

            updated_lines = []
            for i, line in enumerate(lines):
                updated_line = line
                updated_line = FixCancellationTokenOnLine.AddApplicationServiceInterface(updated_line)
                updated_lines.append(updated_line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')

    @staticmethod
    def UpdateValidation(file_paths):
        for file_path in file_paths:

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')

            updated_lines = []
            for i, line in enumerate(lines):
                updated_line = line
                updated_line = FixCancellationTokenOnLine.AddApplicationValidationInterface(updated_line)
                updated_lines.append(updated_line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')


    @staticmethod
    def UpdateRepository(file_paths):
        for file_path in file_paths:

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')

            updated_lines = []
            for i, line in enumerate(lines):
                updated_line = line
                updated_line = FixCancellationTokenOnLine.AddApplicationRepositoryInterface(updated_line)
                updated_lines.append(updated_line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')



class FixCancellationTokenOnLine:
       
    @staticmethod
    def AddApplicationServiceInterface(line):
        if 'IApplicationService' in line: return line

        strip_line = line.strip()
        if strip_line.startswith('public interface I'): return line.rstrip() + ' : IApplicationService\n'
        return line  
    
    @staticmethod
    def AddApplicationValidationInterface(line):
        if 'IApplicationValidation' in line: return line

        strip_line = line.strip()
        if strip_line.startswith('public interface I'): return line.rstrip() + ' : IApplicationValidation\n'
        return line      

    @staticmethod
    def AddApplicationRepositoryInterface(line):
        if 'IApplicationRepository' in line: return line
        if 'IGeneralRepository' in line: return line

        strip_line = line.strip()
        if strip_line.startswith('public interface I'): return line.rstrip() + ' : IApplicationRepository\n'
        return line    

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


FixInjectionOnProject.RunOnEnterpriseHR()
