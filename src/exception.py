import sys
import logging

#function to fetch the error message received
def error_message_detail(error,error_detail:sys):
    #esc_tab provides information about the error raised
    _,_,exc_tb = error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )

    return error_message


#custom class inherting from Exception Class
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    #Enable printing of the error message itself
    def __str__(self):
        return self.error_message