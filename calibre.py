import subprocess
import json
__author__ = 'gyp'


class Calibre:
    def __init__(self, library_path = None):
        self._library_path = library_path

    def get_book_data(self, book_id):
        book_id = int(book_id)
        json_results = self._call_calibredb("list",
                                              "--for-machine",
                                              "-s", "id:%d" % book_id,
                                              "-f", "all")
        results = json.loads(json_results)
        if len(results) == 0:
            return None

        return results[0]

    def _call_calibredb(self, *args):
        call_args = ["calibredb"] + list(args)
        if self._library_path:
            call_args += ["--with-library", "%s" % self._library_path]
        return subprocess.check_output(call_args).decode()

    def set_custom(self, book_id, field_name, field_value):
        self._call_calibredb("set_custom", field_name, str(int(book_id)), field_value)