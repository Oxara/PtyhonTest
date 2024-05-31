import os, re

from GUI.IO_Helper import IO_Helper

class FixServiceMessageModelOnProject:

    @staticmethod
    def RunOnFramwork():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\Framework\\Draft.Framework"

        repository_Interface_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Repository"), r".*Repository\.cs$")
        FixServiceMessageModelOnFile.ClearLines(repository_Interface_Files)

        validation_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Validation"), r".*Validation\.cs$")
        FixServiceMessageModelOnFile.ClearLines(validation_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Services") , r".*Service\.cs$")
        FixServiceMessageModelOnFile.ClearLines(service_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\Framework.Presantation.WebAPI\Controllers"), r".*Controller\.cs$")
        FixServiceMessageModelOnFile.ClearLines(controller_Files)

    @staticmethod
    def RunOnEnterpriseHR():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\HR\EnterpriseHR\\enterprisehr.api"

        repository_Interface_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Repository"), r".*Repository\.cs$")
        FixServiceMessageModelOnFile.ClearLines(repository_Interface_Files)

        validation_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Validation"), r".*Validation\.cs$")
        FixServiceMessageModelOnFile.ClearLines(validation_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Services") , r".*Service\.cs$")
        FixServiceMessageModelOnFile.ClearLines(service_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.WebAPI\Controllers.HR"), r".*Controller\.cs$")
        FixServiceMessageModelOnFile.ClearLines(controller_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.MobileAPI\Controllers.Platform"), r".*Controller\.cs$")
        FixServiceMessageModelOnFile.ClearLines(controller_Files)

class FixServiceMessageModelOnFile:
       
    @staticmethod
    def ClearLines(file_paths):
        for file_path in file_paths:

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')

            updated_lines = []
            for i, line in enumerate(lines):
                if FixServiceMessageModelOnLine.ClearLine(line) is not None:  # Satırı silmek istemiyorsak
                   updated_lines.append(line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')

class FixServiceMessageModelOnLine:
       
    @staticmethod
    def ClearLine(line):

        if re.search(r'^\s*Service\s*=', line): return None  # Satırı silmek için None döndür
        if re.search(r'^\s*Action\s*=', line): return None  # Satırı silmek için None döndür
        return line

FixServiceMessageModelOnProject.RunOnFramwork()
FixServiceMessageModelOnProject.RunOnEnterpriseHR()