import sys

class lms_stdout():
    former_stdout = sys.stdout
    former_stderr = sys.stderr
    
    def __init__(self):
        sys.stdout = self
        sys.stderr = self
        
    # def __del__(self):
        # sys.stdout = lms_stdout.former_stdout # AttributeError: 'NoneType' object has no attribute 'former_stdout' # after file was put inside lms folder
        # sys.stderr = lms_stdout.former_stderr # AttributeError: 'NoneType' object has no attribute 'former_stdout' # after file was put inside lms folder

    def write(self,string):
        lms_stdout.former_stdout.write(string)
        try:
            self.output += string
        except AttributeError:
            self.output = string

    def flush(self):
        lms_stdout.former_stdout.flush()
            
    def get_unread_data(self) -> str:
        try:
            len_output = len(self.output)
        except AttributeError:
            return ""
        try:
            len_collected = self.len_collected
        except AttributeError:
            len_collected = 0
        new_content = self.output[len_collected:]
        self.len_collected = len_output
        return new_content

    def mark_data_as_read(self):
        self.get_unread_data()

