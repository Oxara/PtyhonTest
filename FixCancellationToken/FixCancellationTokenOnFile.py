from FixCancellationToken.FixCancellationTokenOnLine import FixCancellationTokenOnLine
from FixCancellationToken.FixCancellationTokenOnMultipleLine import FixCancellationTokenOnMultipleLine
from IO.IO_Helper import IO_Helper

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
