import shutil
from os import path
from csv import writer
from psycopg2 import DatabaseError
from datetime import datetime
from itertools import islice
ERROR_LOG_DEFAULT_HEADER = ['TimeStamp', 'file', 'function', 'line', 'args', 'traceback', 'custom_message']
ACTION_LOG_DEFAULT_HEADER = ['TimeStamp', 'function', 'custom_message']


# ==================================== #
# ---------- LOG OPERATIONS ---------- #
# ==================================== #
class BaseLog(object):
    def __init__(self, header, log_dir, log_file):
        # Check arguments
        assert log_dir is not None
        assert log_file is not None
        # Constitute full path
        self.log_header = header
        self.log_dir = log_dir
        self.log_path = path.join(log_dir, log_file)
        if not path.isfile(self.log_path):
            with open(self.log_path, 'w') as f:
                # Get writer object
                writer_object = writer(f, delimiter=';')
                # Write header
                writer_object.writerow(self.log_header)
                f.close()
        else:
            print(f'Log file {self.log_path} already exists.')
        self.is_initialized = True
        self.max_lines = 1000
        return
    def write_entry(self, fields):
        # Open the input and output files
        with open(self.log_path, 'r') as infile:
            lines = infile.readlines()
        # Trim the lines
        n_excess = max(1, len(lines)-self.max_lines)
        new_line = ";".join(fields) + '\n'
        trimmed_lines = [lines[0]] + lines[n_excess:] + [new_line]
        # Write the trimmed lines back to the file
        with open(self.log_path, 'w') as file:
            file.writelines(trimmed_lines)


class ErrorLog(BaseLog):
    def __init__(self, log_dir=None, log_file=None):
        super().__init__(ERROR_LOG_DEFAULT_HEADER, log_dir, log_file)
    def new_entry(self, log_vars, custom_message='no message provided'):
        # Make sure logger object was initialized
        if not self.is_initialized:
            raise NotImplemented('Logger not initialized - check caller function')
        # --- Get exception info
        # Get time stamp
        time_now = datetime.now()
        err_stmp = '%i%i%i_%ih%imin' % (time_now.day,
                                        time_now.month,
                                        time_now.year,
                                        time_now.hour,
                                        time_now.minute)
        if isinstance(log_vars, list):
            output = [err_stmp] + log_vars
            assert len(output)==len(self.log_header)
        elif isinstance(log_vars, Exception):
            # Get file
            err_fil = log_vars.__traceback__.tb_frame.f_code.co_filename
            # Get function
            err_fcn = log_vars.__traceback__.tb_frame.f_code.co_name
            # Get line number
            err_lin = str(log_vars.__traceback__.tb_lineno)
            # Get args
            err_arg = log_vars.__traceback__.tb_frame.f_code.co_consts.__str__()
            # Get tracback
            err_msg = log_vars.__doc__
            # Log output
            output = [err_stmp, err_fil, err_fcn, err_lin, err_arg, err_msg, custom_message]
        # --- Manage log file size
        self.write_entry(output)
        return


class ActionLog(BaseLog):
    def __init__(self, log_dir=None, log_file=None):
        super().__init__(ACTION_LOG_DEFAULT_HEADER, log_dir, log_file)
    def new_entry(self, caller_fcn=None, custom_message=None):
        assert caller_fcn is not None
        assert custom_message is not None
        # Make sure logger object was initialized
        if not self.is_initialized:
            raise NotImplemented('Logger not initialized - check caller function')
        # --- Get exception info
        # Get time stamp
        time_now = datetime.now()
        err_stmp = '%i%i%i_%ih%imin' % (time_now.day,
                                        time_now.month,
                                        time_now.year,
                                        time_now.hour,
                                        time_now.minute)
        # Log output
        output = [err_stmp, caller_fcn, custom_message]
        # --- Manage log file size
        self.write_entry(output)
        return


if __name__ == '__main__':
    from apps.lib.localvars import PATH_TO_LOGS

    # --- TEST ACTION LOG
    """
    actionLog = ActionLog(PATH_TO_LOGS, 'test_actions.csv')
    for i_ in range(1010):
        actionLog.new_entry('Main module caller', f'Added line number {i_}')
    """
    # --- TEST ERROR LOG
    errorLog = ErrorLog(PATH_TO_LOGS, 'test_errors.csv')
    for i_ in range(1010):
        try:
            total = 1/0
        except (Exception, DatabaseError) as error:
            errorLog.new_entry(error, f'Added line number {i_}')