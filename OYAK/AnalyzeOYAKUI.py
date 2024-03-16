from concurrent.futures import ThreadPoolExecutor
from functools import partial
import pandas as pd, re, os

class MatchResultModel:
    FileName : str
    EnumType : str
    EnumValue : str
    LineContent : str

class EnumModel:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

class ServiceModel:
    FileName : str
    Service : str
    UI_Action : str
    API_Url : str

class ComponentServiceModel:
    FileName : str
    Service : str

class AnalyzeOYAKUI:

    ENUM_DIRECTORY = r"C:\PROJECT\OYAK.UI\app\Global\Enums\RoleEnums"
    SOLUTION_DIRECTORY = r"C:\PROJECT\OYAK.UI"

    @staticmethod
    def Start():

        component_Files = AnalyzeOYAKUI.GetComponents()
        enum_results = AnalyzeOYAKUI.LookUpForEnum(component_Files)

        AnalyzeOYAKUI.SaveToExcel(enum_results, "component_Enum.xlsx", 'Enum')
        
        component_files_With_enum = list(set(result.FileName for result in enum_results))
        component_service_Results = AnalyzeOYAKUI.LookUpForComponentServices(component_files_With_enum)
        AnalyzeOYAKUI.SaveToExcel(component_service_Results, "component_ImportedServices_with_Enum.xlsx", 'ComponentServices')

        component_service_Results = AnalyzeOYAKUI.LookUpForComponentServices(component_Files)
        AnalyzeOYAKUI.SaveToExcel(component_service_Results, "component_AllImportedServices.xlsx", 'ComponentServices')

        service_Files = AnalyzeOYAKUI.GetServices()
        service_Results = AnalyzeOYAKUI.LookUpForActions(service_Files)

        AnalyzeOYAKUI.SaveToExcel(service_Results, "service_APIMethods.xlsx", 'API Methods')

    @staticmethod
    def LookUpForEnum(file_paths):
        menuEnums = set(enum for enum in AnalyzeOYAKUI.GetMenuCodes())
        actionEnums = set(enum for enum in AnalyzeOYAKUI.GetActionCodes())
        enums = menuEnums.union(actionEnums)
    
        match_results = []
        with ThreadPoolExecutor() as executor:
            partial_process_file = partial(AnalyzeOYAKUI.ProcessEnumFile, enums=enums)
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
            partial_process_file = partial(AnalyzeOYAKUI.ProcessServiceFile)
            for result in executor.map(partial_process_file, file_paths):
                if result: match_results.extend(result)

        return match_results
    
    @staticmethod
    def LookUpForComponentServices(file_paths):
    
        match_results = []
        with ThreadPoolExecutor() as executor:
            partial_process_file = partial(AnalyzeOYAKUI.ProcessComponentService)
            for result in executor.map(partial_process_file, file_paths):
                if result: match_results.extend(result)

        return match_results    

    @staticmethod
    def ProcessServiceFile(file_path):

        with open(file_path, 'r', encoding='utf-8') as file:
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
                    action_item = ServiceModel()
                    action_item.FileName = file_path
                    action_item.Service = service_name
                    action_item.API_Url = action_match
                    action_list.append(action_item)

        return action_list

    @staticmethod
    def ProcessComponentService(cmoponent):

        with open(cmoponent, 'r', encoding='utf-8') as file:
            content = file.readlines()
            service_list = []            

            for line in content:
                if "import" in line and ".service\";" in line:
                    importedFile = re.findall(r'from .*', line)[0]
                    importedServiceIndex = importedFile.rfind('/')
                    importedService = importedFile[importedServiceIndex + 1:]

                    service_item = ComponentServiceModel()
                    service_item.FileName = cmoponent
                    service_item.Service = importedService.replace('";','')
                    service_list.append(service_item)

        return service_list

    @staticmethod
    def SaveToExcel(match_results, file_name, sheet_name):
        if match_results:
            data = [matched_result.__dict__ for matched_result in match_results]
            df = pd.DataFrame(data)
            excel_file_path = file_name
            df.to_excel(excel_file_path, index=False, sheet_name=sheet_name)

    @staticmethod
    def GetServices(): return IO_Helper.GetFiles(AnalyzeOYAKUI.SOLUTION_DIRECTORY, r".*service\.ts$")

    @staticmethod
    def GetComponents(): return  IO_Helper.GetFiles(AnalyzeOYAKUI.SOLUTION_DIRECTORY, r".*component\.ts$")

    @staticmethod
    def GetMenuCodes():

        class_content = IO_Helper.ReadLines(os.path.join(AnalyzeOYAKUI.ENUM_DIRECTORY, r"MenuCodeEnum.ts"), 'utf-8')
        menu_enum = AnalyzeOYAKUI.GetEnumModel("MenuCodeEnum", class_content)
        return menu_enum

    @staticmethod
    def GetActionCodes():

        class_content = IO_Helper.ReadLines(os.path.join(AnalyzeOYAKUI.ENUM_DIRECTORY, r"MenuActionEnum.ts"), 'utf-8')
        action_enum = AnalyzeOYAKUI.GetEnumModel("MenuActionEnum", class_content)
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

AnalyzeOYAKUI.Start()