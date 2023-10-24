import datetime

class File:
    def __init__(
        self, output_file_path):
        """ Initialize file object.
        :params output_file_path: Output file path (path)
        """
        timestamp_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.output_file_path = f"output/{timestamp_now}_{output_file_path}"

    def write(
        self, output):
        """ Write output to file.
        :params output: Output to write (string)
        """
        with open(self.output_file_path, 'w') as f:
            f.write(output)