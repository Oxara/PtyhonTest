import os, re


class FixCancellationTokenOnProject:

    @staticmethod
    def RunOnFramwork():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\Framework\\Draft.Framework"

        repository_Interface_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Repository"), r".*Repository\.cs$")
        FixCancellationTokenOnFile.UpdateRepository(repository_Interface_Files)

        validation_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Validation"), r".*Validation\.cs$")
        FixCancellationTokenOnFile.UpdateValidation(validation_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\Framework.Application.Services") , r".*Service\.cs$")
        FixCancellationTokenOnFile.UpdateService(service_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\Framework.Presantation.WebAPI\Controllers"), r".*Controller\.cs$")
        FixCancellationTokenOnFile.UpdateController(controller_Files)

    @staticmethod
    def RunOnEnterpriseHR():

        SOLUTION_DIRECTORY = "C:\\PROJECT\\code.vbt.com.tr\\HR\EnterpriseHR\\enterprisehr.api"

        repository_Interface_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Repository"), r".*Repository\.cs$")
        FixCancellationTokenOnFile.UpdateRepository(repository_Interface_Files)

        validation_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Validation"), r".*Validation\.cs$")
        FixCancellationTokenOnFile.UpdateValidation(validation_Files)

        service_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Application\\HR.Application.Services") , r".*Service\.cs$")
        FixCancellationTokenOnFile.UpdateService(service_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.WebAPI\Controllers.HR"), r".*Controller\.cs$")
        FixCancellationTokenOnFile.UpdateController(controller_Files)

        controller_Files = IO_Helper.GetFiles(os.path.join(SOLUTION_DIRECTORY, "Presantation\\HR.Presantation.WebAPI\Controllers.Platform"), r".*Controller\.cs$")
        FixCancellationTokenOnFile.UpdateController(controller_Files)


class FixCancellationTokenOnFile:
       
    @staticmethod
    def UpdateRepository(file_paths):
        for file_path in file_paths:
            
            # Bu dosyaları atla
            if file_path.endswith("GeneralRepository.cs"): continue
            if file_path.endswith("SessionRepository.cs"): continue
            if file_path.endswith("SessionCacheRepository.cs"): continue

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')

            updated_lines = []
            for i, line in enumerate(lines):
                updated_line = line
                updated_line = FixCancellationTokenOnLine.ReplaceAsyncMethods(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceTaskInterface(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceTaskMethod(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceGetPagedData(updated_line) 
                updated_line = FixCancellationTokenOnLine.ReplaceAwaitCall(updated_line)
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
                updated_line = FixCancellationTokenOnLine.ReplaceAsyncMethods(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceTaskInterface(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceTaskMethod(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceModelRelevation(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceAwaitCall(updated_line)
                updated_line = FixCancellationTokenOnLine.ClearBaseSearchQuery(updated_line)

                updated_line, lines = FixCancellationTokenOnMultipleLine.ReplaceAwaitCallWithMultiLine(i, updated_line, lines)
                updated_lines.append(updated_line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')

    @staticmethod
    def UpdateService(file_paths):
        for file_path in file_paths:

            # Bu dosyaları atla
            if file_path.endswith("LocalizationService.cs"): continue
            if file_path.endswith("SessionService.cs"): continue
            if file_path.endswith("TokenService.cs"): continue

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')
            lines = FixCancellationTokenOnMultipleLine.UpdateUsingStatements(lines)

            updated_lines = []
            for i, line in enumerate(lines):
                updated_line = line
                updated_line, lines = FixCancellationTokenOnMultipleLine.AddCancellationTokenOnServiceRequest(i, updated_line, lines)       
                updated_lines.append(updated_line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')

            updated_lines = []             
            for i, line in enumerate(lines):
                updated_line = line
                updated_line = FixCancellationTokenOnLine.ReplaceAsyncMethods(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceTaskInterface(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceTaskMethod(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceNullableExpression(updated_line)                
                updated_line = FixCancellationTokenOnLine.ReplaceGuardClause(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceAuditRequest(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceAwaitCall(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceServiceRequest(updated_line)

                # Kalanlar için son şans
                # updated_line, lines = FixCancellationTokenOnMultipleLine.ReplaceAwaitCallWithMultiLine(i, updated_line, lines)    
                updated_lines.append(updated_line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')

    @staticmethod
    def UpdateController(file_paths):
        for file_path in file_paths:

            # Dosyayı aç ve içeriğini oku
            lines = IO_Helper.ReadLines(file_path, 'utf-8')
            lines = FixCancellationTokenOnMultipleLine.UpdateUsingStatements(lines)

            updated_lines = []
            for i, line in enumerate(lines):
                updated_line = line
                updated_line = FixCancellationTokenOnLine.ReplaceAsyncMethods(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceTaskMethod(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceGetAllServiceCall(updated_line)
                updated_line = FixCancellationTokenOnLine.ReplaceAwaitCall(updated_line)
                updated_lines.append(updated_line)

            # Dosyayı güncelle
            lines = IO_Helper.WriteLines(file_path, updated_lines, 'utf-8')


class FixCancellationTokenOnLine:
       
    @staticmethod
    def ReplacePaging(line):
        if 'cancellationToken' in line: return line

        strip_line = line.strip()
        if 'GetPagedData' in strip_line and strip_line.endswith(');'): return line.replace(');', ', cancellationToken);')   
        return line 

    @staticmethod
    def ReplaceGetAllServiceCall(line):
        if 'cancellationToken' in line: return line
        if 'Cache' in line: return line

        strip_line = line.strip()
        if 'await' in strip_line and 'Service' in strip_line: 
            if strip_line.endswith('();'): return line.replace(');', 'null, cancellationToken);')
            if strip_line.endswith(');'):  return line.replace(');', ', cancellationToken);')
        return line     

    @staticmethod
    def ReplaceTaskInterface(line):
        if 'cancellationToken' in line: return line

        strip_line = line.strip()
        if strip_line.startswith('Task'): 
            if strip_line.endswith('();'): return line.replace(');', 'CancellationToken cancellationToken);')  
            if strip_line.endswith(');'):  return line.replace(');', ', CancellationToken cancellationToken);')   
        return line  

    @staticmethod
    def ReplaceTaskMethod(line):
        if 'cancellationToken' in line: return line

        strip_line = line.strip()
        if 'async Task' in strip_line: 
            if strip_line.endswith('()'): return line.replace(')', 'CancellationToken cancellationToken)') 
            if strip_line.endswith(')'):  return line.replace(')', ', CancellationToken cancellationToken)')          
        return line  

    @staticmethod
    def ReplaceGetPagedData(line):
        if 'cancellationToken' in line: return line

        strip_line = line.strip()
        if 'GetPagedData' in strip_line and strip_line.endswith(');'): return line.replace(');', ', cancellationToken);')  
        return line

    @staticmethod
    def ReplaceModelRelevation(line):
        if 'cancellationToken' in line: return line

        strip_line = line.strip()
        if 'ModelRelationValidation' in strip_line and strip_line.endswith(');'): return line.replace(');', ', cancellationToken);')  
        return line

    @staticmethod
    def ReplaceGuardClause(line):
        if 'Ensure' in line: return line
        if 'cancellationToken' in line: return line

        strip_line = line.strip()
        if 'GuardClause' in strip_line and 'Validation' in strip_line:
            if strip_line.endswith('(),'): return line.replace('),', 'cancellationToken),')  
            if strip_line.endswith('),'):  return line.replace('),', ', cancellationToken),')  
        return line  
    
    @staticmethod
    def ReplaceAuditRequest(line):
        if 'Ensure' in line: return line
        if 'cancellationToken' in line: return line

        strip_line = line.strip()
        if 'AuditModel(workContext))' in strip_line:
            return line.replace(f'AuditModel(workContext))', f'AuditModel(workContext), cancellationToken)')  
        return line      

    @staticmethod
    def ReplaceAsyncMethods(line):
        line = line.replace(f'ToListAsync()', f'ToListAsync(cancellationToken)')
        line = line.replace(f'FirstOrDefaultAsync()', f'FirstOrDefaultAsync(cancellationToken)')
        line = line.replace(f'CountAsync()', f'CountAsync(cancellationToken)')
        line = line.replace(f'AnyAsync()', f'AnyAsync(cancellationToken)')
        return line    
    
    @staticmethod
    def ReplaceNullableExpression(line):
        return line.replace(f', bool>> expression = null,', f', bool>> expression,')

    @staticmethod
    def ReplaceServiceRequest(line):
        return line.replace(f'async ()', f'async (cancellationToken)')  
   
    @staticmethod
    def ReplaceAwaitCall(line):
        if 'Ensure' in line: return line        
        if 'cancellationToken' in line: return line
        if 'Cache' in line: return line

        if '(await' in line:
            index_await = line.find('(await')

            index_close_parenthesis_with_dot = line.find(')).', index_await)
            index_close_parenthesis = line.rfind('))', index_await)

            if index_close_parenthesis_with_dot != -1:
                
                if line[index_close_parenthesis_with_dot - 1] == '(':
                    line = line[:index_close_parenthesis_with_dot] + "cancellationToken" + line[index_close_parenthesis_with_dot:]
                else:
                    line = line[:index_close_parenthesis_with_dot] + ", cancellationToken" + line[index_close_parenthesis_with_dot:]
                return line 
            
            elif index_close_parenthesis != -1:

                if line[index_close_parenthesis - 1] == '(':
                    line = line[:index_close_parenthesis] + "cancellationToken" + line[index_close_parenthesis:]
                else:
                    line = line[:index_close_parenthesis] + ", cancellationToken" + line[index_close_parenthesis:]
                return line 

        elif 'await' in line:
            index_await = line.find('await')

            index_close_parenthesis_with_dot_and_where = line.find(').Where', index_await)
            index_close_parenthesis_with_dot_and_first = line.find(').First', index_await)            
            index_close_parenthesis_with_dot = line.find(').', index_await)
            index_close_parenthesis = line.rfind(')', index_await)

            if index_close_parenthesis_with_dot_and_where != -1 and index_close_parenthesis_with_dot_and_where < index_close_parenthesis:
                return line
            
            elif index_close_parenthesis_with_dot_and_first != -1 and index_close_parenthesis_with_dot_and_first < index_close_parenthesis:

                if line[index_close_parenthesis - 1] == '(':
                    line = line[:index_close_parenthesis] + "cancellationToken" + line[index_close_parenthesis:]
                else:
                    line = line[:index_close_parenthesis] + ", cancellationToken" + line[index_close_parenthesis:]
                return line          

            elif index_close_parenthesis_with_dot != -1:
                
                if line[index_close_parenthesis_with_dot - 1] == '(':
                    line = line[:index_close_parenthesis_with_dot] + "cancellationToken" + line[index_close_parenthesis_with_dot:]
                else:
                    line = line[:index_close_parenthesis_with_dot] + ", cancellationToken" + line[index_close_parenthesis_with_dot:]
                return line 
            
            elif index_close_parenthesis != -1:

                if line[index_close_parenthesis - 1] == '(':
                    line = line[:index_close_parenthesis] + "cancellationToken" + line[index_close_parenthesis:]
                else:
                    line = line[:index_close_parenthesis] + ", cancellationToken" + line[index_close_parenthesis:]
                return line 
            
        return line 

    @staticmethod
    def ClearBaseSearchQuery(line):
        return line.replace(f'BaseSearchQuery(cancellationToken)', f'BaseSearchQuery()')  

class FixCancellationTokenOnMultipleLine:
       
    @staticmethod
    def UpdateUsingStatements(lines):
        # Check if using System.Threading; exists
        using_threading = False
        for line in lines:
            if line.strip() == 'using System.Threading;':
                using_threading = True
                break

        # If using System.Threading; does not exist, add it after existing using statements
        if not using_threading:
            last_using_index = next((i for i, line in enumerate(lines[::-1]) if line.strip().startswith('using ')), len(lines))
            last_using_index = len(lines) - last_using_index
            lines.insert(last_using_index, 'using System.Threading;\n')

        return lines
    
    @staticmethod
    def ReplaceAwaitCallWithMultiLine(i, line, lines):   
        if 'await' in line and '(' in line:
            
            index = i
            while index < len(lines) and ')' not in lines[index]:
                index += 1

            if i <= index and 'cancellationToken' not in lines[index].strip():
                lines[index] = lines[index].replace(')', ', cancellationToken)') 

        return line, lines
    
    @staticmethod
    def AddCancellationTokenOnServiceRequest(i, line, lines):   
        if 'Run(new ServiceRequest<' in line or 'Transaction(new ServiceRequest<' in line:
            
            checkLine = lines[i + 2]
            if 'CancellationToken' not in checkLine:
                lines[i + 2] = '\t\t\t\tCancellationToken = cancellationToken,\n' + lines[i + 2]

        return line, lines


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


# FixCancellationTokenOnProject.RunOnFramwork()
FixCancellationTokenOnProject.RunOnEnterpriseHR()
