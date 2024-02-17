from IO.IO_Helper import IO_Helper
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import pandas as pd, re, os

from OYAK.OyakModels import EnumModel, MatchResultModel, ServiceModel

class AnaylzeOYAKUI:

    ENUM_DIRECTORY = r"C:\PROJECT\OYAK.UI\app\Global\Enums\RoleEnums"
    SOLUTION_DIRECTORY = r"C:\PROJECT\OYAK.UI"

    @staticmethod
    def Start():

        component_Files = AnaylzeOYAKUI.GetComponents()
        enum_results = AnaylzeOYAKUI.LookUpForEnum(component_Files)

        AnaylzeOYAKUI.SaveToExcel(enum_results, "component_result.xlsx", 'Enum')
        
        service_Files = AnaylzeOYAKUI.GetServices()
        service_Results = AnaylzeOYAKUI.LookUpForActions(service_Files)

        AnaylzeOYAKUI.SaveToExcel(service_Results, "service_result.xlsx", 'Service')

    @staticmethod
    def LookUpForEnum(file_paths):
        menuEnums = set(enum for enum in AnaylzeOYAKUI.GetMenuCodes())
        actionEnums = set(enum for enum in AnaylzeOYAKUI.GetActionCodes())
        enums = menuEnums.union(actionEnums)
    
        match_results = []
        with ThreadPoolExecutor() as executor:
            partial_process_file = partial(AnaylzeOYAKUI.ProcessEnumFile, enums=enums)
            for result in executor.map(partial_process_file, file_paths):
                if result: match_results.extend(result)

        return match_results
            
    @staticmethod
    def ProcessEnumFile(file_path, enums: EnumModel):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        match_Results = []
        for enum in enums:
            pattern = rf'\b{re.escape(enum.name)}\b'
            matches = re.finditer(pattern, content)
            for match in matches:
                match_Result = MatchResultModel()
                match_Result.FileName = file_path
                match_Result.EnumType = enum.name
                match_Result.EnumValue = enum.value
                match_Results.append(match_Result)
        return match_Results

    @staticmethod
    def LookUpForActions(file_paths):
    
        match_results = []
        with ThreadPoolExecutor() as executor:
            partial_process_file = partial(AnaylzeOYAKUI.ProcessServiceFile)
            for result in executor.map(partial_process_file, file_paths):
                if result: match_results.extend(result)

        return match_results

    @staticmethod
    def ProcessServiceFile(file_path):
        with open(file_path, 'r') as file:
            content = file.readlines()

            action_list = []
            service_name = None

            # Service name regex

            service_name_pattern = re.compile(r'export\s+class\s+(\w+)Service')
            action_pattern =  re.compile(r"return this._apiservice\.GetAuthorization\(ApiUrlEnum\.IK, '(.+?)'")

            for line in content:
                match = service_name_pattern.search(line)
                if match:
                    service_name = match.group(1)
                    break

            for line in content:
                # Search for actions
                action_matches = action_pattern.findall(line)
                for action_match in action_matches:
                    serviceModel = ServiceModel()
                    serviceModel.Service = file_path
                    serviceModel.Service = service_name
                    serviceModel.API_Url = action_match
                    action_list.append(serviceModel)

        return action_list

    @staticmethod
    def SaveToExcel(match_results, file_name, sheet_name):
        if match_results:
            data = [matched_result.__dict__ for matched_result in match_results]
            df = pd.DataFrame(data)
            excel_file_path = file_name
            df.to_excel(excel_file_path, index=False, sheet_name=sheet_name)

    @staticmethod
    def GetServices(): return IO_Helper.GetFiles(AnaylzeOYAKUI.SOLUTION_DIRECTORY, r".*service\.ts$")

    @staticmethod
    def GetComponents(): return  IO_Helper.GetFiles(AnaylzeOYAKUI.SOLUTION_DIRECTORY, r".*component\.ts$")

    @staticmethod
    def GetMenuCodes():

        class_content = IO_Helper.ReadLines(os.path.join(AnaylzeOYAKUI.ENUM_DIRECTORY, r"MenuCodeEnum.ts"), 'utf-8')
        menu_enum = AnaylzeOYAKUI.GetEnumModel("MenuCodeEnum", class_content)
        return menu_enum

    @staticmethod
    def GetActionCodes():

        class_content = IO_Helper.ReadLines(os.path.join(AnaylzeOYAKUI.ENUM_DIRECTORY, r"MenuActionEnum.ts"), 'utf-8')
        action_enum = AnaylzeOYAKUI.GetEnumModel("MenuActionEnum", class_content)
        return action_enum

    @staticmethod
    def GetEnumModel(enum_name, content):
        properties = []
        for line in content:
            if '=' in line:
                parts = line.split('=')
                property_name = parts[0].replace("public static", "").strip()
                property_value = parts[1].strip().rstrip(';')
                enum_model = EnumModel(name=f"{enum_name}.{property_name}", value=property_value)
                properties.append(enum_model)
        return properties
    
    @staticmethod
    def GetEnumValue(properties, name):
        for prop in properties:
            if prop.name == name:
                return prop.value
        return None        

