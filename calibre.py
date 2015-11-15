import subprocess
import json
__author__ = 'gyp'


class Calibre:
    @staticmethod
    def get_book_data(book_id):
        book_id = int(book_id)
        json_results = Calibre._call_calibredb("list",
                                              "--for-machine",
                                              "-s", "id:%d" % book_id,
                                              "-f", "all")
        results = json.loads(json_results)
        if len(results) == 0:
            return None

        return results[0]

    @staticmethod
    def _call_calibredb(*args):
        return subprocess.check_output(["calibredb"] + list(args)).decode()

    @staticmethod
    def set_custom(book_id, field_name, field_value):
        Calibre._call_calibredb("set_custom", field_name, str(int(book_id)), field_value)