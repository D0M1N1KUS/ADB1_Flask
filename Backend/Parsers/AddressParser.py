import re
import sys


class AddressParser:
    @staticmethod
    def parse(json_request):
        errors = []
        try:
            if json_request is None:
                raise Exception("Passed empty object to parser")
            if json_request["street"] is None:
                errors.append("\'name\' can\'t be null")
            if json_request["town"] is None:
                errors.append("\'name\' can\'t be null")
            if json_request["post_code"] is None:
                errors.append("\'name\' can\'t be null")
            elif not re.search("^[0-9]{2}-[0-9]{3}$", json_request["post_code"]):
                errors.append("\'post_code\' doesn\'t match post code pattern")
        except Exception as e:
            return f"Error during parsing: {str(e)}"

        if len(errors) == 0:
            return None
        else:
            return ",".join(errors)
