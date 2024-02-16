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