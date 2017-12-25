# 1:error
# 2:warning
# 3:info
# 4:debug
# 5:verbose

class DebugLog:
    Log_Level = 1;
    
    @staticmethod
    def error(text):
        if 1 <= DebugLog.Log_Level:
            print(text)

    @staticmethod
    def warning(text):
        if 2 <= DebugLog.Log_Level:
            print(text)

    @staticmethod
    def info(text):
        if 3 <= DebugLog.Log_Level:
            print(text)

    @staticmethod
    def debug(text):
        if 4 <= DebugLog.Log_Level:
            print(text)

    @staticmethod
    def verbose(text):
        if 5 <= DebugLog.Log_Level:
            print(text)