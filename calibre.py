import subprocess
import json
__author__ = 'gyp'


class Calibre:
    @staticmethod
    def get_book_data(library_path, book_id):
        book_id = int(book_id)
	dbargs = ["list", "--for-machine",
                  "-s", "id:%d" % book_id,
                  "-f", "all" ]
        if library_path:
            dbargs +=  ["--with-library", "%s" % library_path]
        json_results = Calibre._call_calibredb(dbargs)
        results = json.loads(json_results)
        if len(results) == 0:
            return None

        return results[0]

    @staticmethod
    def _call_calibredb(parameters):
        return subprocess.check_output(["calibredb"] + list(parameters)).decode()

    @staticmethod
    def set_custom(book_id, field_name, field_value):
        Calibre._call_calibredb("set_custom", field_name, str(int(book_id)), field_value)
