import logging, sys
from excelIO import work1, work2, StreamToLogger

from FPaths import RUN2LOG
logging.basicConfig(
   level=logging.ERROR,
   format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
   filename=RUN2LOG,
   filemode='a'
)



if __name__ == "__main__":
    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl
    work2()