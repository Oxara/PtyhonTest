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
