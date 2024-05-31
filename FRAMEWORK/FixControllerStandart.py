import os

from GUI.IO_Helper import IO_Helper


class FixControllerStandartonOnProject:

    @staticmethod
    def RunOnFramwork():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\Framework\\Draft.Framework"

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\Framework.Presantation.WebAPI\Controllers"), r".*Controller\.cs$")
        FixControllerStandartnOnFile.UpdateController(controller_Files)

    @staticmethod
    def RunOnEnterpriseHR():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\HR\EnterpriseHR\\enterprisehr.api"

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.WebAPI\Controllers.HR"), r".*Controller\.cs$")
        FixControllerStandartnOnFile.UpdateController(controller_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.WebAPI\Controllers.Platform"), r".*Controller\.cs$")
        FixControllerStandartnOnFile.UpdateController(controller_Files)
        
class FixControllerStandartnOnFile:
       
    @staticmethod
    def UpdateController(file_paths):
        for file_path in file_paths:

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')

            updated_lines = []
            for i, line in enumerate(lines):
                updated_line = line
                updated_line = FixCancellationStandartOnLine.FixNaming(updated_line)
                updated_lines.append(updated_line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')


class FixCancellationStandartOnLine:
       
    @staticmethod
    def FixNaming(line):

        strip_line = line.strip()
        if 'Task' in strip_line or 'Http'  in strip_line:

            if 'GetEntityPage' in strip_line: return line.replace('GetEntityPage', 'GetAllByPaging')
            if 'GetAllEntities' in strip_line: return line.replace('GetAllEntities', 'GetAll')        
            if 'GetTranslations' in strip_line: return line.replace('GetTranslations', 'GetAllTranslations')      
            if 'GetEntity' in strip_line : return line.replace('GetEntity', 'Get')     
            if 'InsertEntity' in strip_line: return line.replace('InsertEntity', 'Insert')    
            if 'UpdateEntity' in strip_line: return line.replace('UpdateEntity', 'Update')   
            if 'DeleteEntity' in strip_line: return line.replace('DeleteEntity', 'Delete')  
            if 'GetAllDocumentManagementByReference' in strip_line: return line.replace('GetAllDocumentManagementByReference', 'GetAllByReference')        
            if 'GetAllDocumentManagementByType' in strip_line: return line.replace('GetAllDocumentManagementByType', 'GetAllByType')        
            if 'GetMissingTechnicalKeys' in strip_line: return line.replace('GetMissingTechnicalKeys', 'GetAllMissingTechnicalKeys')    
            if 'GetAllByPicklist' in strip_line: return line.replace('GetAllByPicklist', 'GetAllByIdPicklist')   
            if 'GetAllByParent' in strip_line: return line.replace('GetAllByParent', 'GetAllByIdParent')   
            if 'GetResourcesByPrefix' in strip_line: return line.replace('GetResourcesByPrefix', 'GetAllByPrefix')    
            if 'GetPublicResources' in strip_line: return line.replace('GetPublicResources', 'GetAllPublicResource')    
            if 'GetSessionCompanies' in strip_line: return line.replace('GetSessionCompanies', 'GetAllSessionCompany')       
            if 'GetSessionMenu' in strip_line: return line.replace('GetSessionMenu', 'GetAllSessionMenu')     
            if 'GetSessionActions' in strip_line: return line.replace('GetSessionActions', 'GetAllSessionAction')       
            if 'GetControllerActionSelectionList' in strip_line: return line.replace('GetControllerActionSelectionList', 'GetAllControllerActionSelection')      
            if 'GetAuthorizedControllerActions' in strip_line: return line.replace('GetAuthorizedControllerActions', 'GetAllAuthorizedControllerAction')       
            if 'RegisterControllerActions' in strip_line: return line.replace('RegisterControllerActions', 'SaveAllControllerAction')   
            if 'GetRoleControllerActionSelectionList' in strip_line: return line.replace('GetRoleControllerActionSelectionList', 'GetAllRoleControllerActionSelection')      
            if 'GetAuthorizedRoleControllerActions' in strip_line: return line.replace('GetAuthorizedRoleControllerActions', 'GetAllAuthorizedRoleControllerAction')       
            if 'RegisterRoleControllerActions' in strip_line: return line.replace('RegisterRoleControllerActions', 'SaveAllRoleControllerAction')     
        return line  

FixControllerStandartonOnProject.RunOnFramwork()
FixControllerStandartonOnProject.RunOnEnterpriseHR()