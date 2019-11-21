import re
import sys


class AddressParser:
    @staticmethod
    def parse_home_address(json_request):
        errors = []
        try:
            if "homeStreet" not in json_request:
                errors.append("\'homeStreet\' can\'t be null")
            if "homeCity" not in json_request:
                errors.append("\'homeCity\' can\'t be null")
            if "homePostalCode" not in json_request:
                errors.append("\'homePostalCode\' can\'t be null")
            elif not re.search("^[0-9]{2}-[0-9]{3}$", json_request["homePostalCode"]):
                errors.append("\'homePostalCode\' doesn\'t match post code pattern")
            if "mailingStreet" not in json_request:
                errors.append("\'mailingStreet\' can\'t be null")
            if "mailingCity" not in json_request:
                errors.append("\'mailingCity\' can\'t be null")
            if "mailingPostalCode" not in json_request:
                errors.append("\'mailingPostalCode\' can\'t be null")
            elif not re.search("^[0-9]{2}-[0-9]{3}$", json_request["homePostalCode"]):
                errors.append("\'mailingPostalCode\' doesn\'t match post code pattern")
        except Exception as e:
            return f"Error during parsing: {str(e)}"

        if len(errors) == 0:
            return None
        else:
            return ",".join(errors)
