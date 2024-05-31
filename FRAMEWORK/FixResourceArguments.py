import os, re

from GUI.IO_Helper import IO_Helper


class FixResourceArgumentsOnProject:

    @staticmethod
    def RunOnFramwork():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\Framework\\Draft.Framework"

        repository_Interface_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Repository"), r".*Repository\.cs$")
        FixResourceArgumentsOnFile.UpdateOnSection(repository_Interface_Files)

        validation_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Validation"), r".*Validation\.cs$")
        FixResourceArgumentsOnFile.UpdateOnSection(validation_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Services") , r".*Service\.cs$")
        FixResourceArgumentsOnFile.UpdateOnSection(service_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\Framework.Presantation.WebAPI\Controllers"), r".*Controller\.cs$")
        FixResourceArgumentsOnFile.UpdateOnSection(controller_Files)

    @staticmethod
    def RunOnEnterpriseHR():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\HR\EnterpriseHR\\enterprisehr.api"

        repository_Interface_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Repository"), r".*Repository\.cs$")
        FixResourceArgumentsOnFile.UpdateOnSection(repository_Interface_Files)

        validation_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Validation"), r".*Validation\.cs$")
        FixResourceArgumentsOnFile.UpdateOnSection(validation_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Services") , r".*Service\.cs$")
        FixResourceArgumentsOnFile.UpdateOnSection(service_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.WebAPI\Controllers.HR"), r".*Controller\.cs$")
        FixResourceArgumentsOnFile.UpdateOnSection(controller_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.MobileAPI\Controllers.Platform"), r".*Controller\.cs$")
        FixResourceArgumentsOnFile.UpdateOnSection(controller_Files)


class FixResourceArgumentsOnFile:
       
    @staticmethod
    def UpdateOnSection(file_paths):
        for file_path in file_paths:

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')

            updated_lines = []
            for i, line in enumerate(lines):
                updated_line = line
                updated_line = FixResourceArgumentsOnLine.FixNaming(updated_line)
                updated_lines.append(updated_line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')


class FixResourceArgumentsOnLine:
       
    @staticmethod
    def FixNaming(line):

        updated_code = re.sub(r'Argument\s*=\s*(.+),', r'Arguments = [\1],', line)
        updated_code = re.sub(r'Argument\s*=\s*(.+)', r'Arguments = [\1]', line)
        return updated_code

# FixResourceArgumentsOnProject.RunOnFramwork()
FixResourceArgumentsOnProject.RunOnEnterpriseHR()