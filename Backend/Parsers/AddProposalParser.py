import sys, re
from Backend.Parsers.AddressParser import AddressParser

class AddProposalParser:
    @staticmethod
    def parse(json_request):
        errors = []
        try:
            if json_request["numerWniosku"] is None:
                errors.append("\'numerWniosku\' can\'t be null")
            if json_request["imie"] is None:
                errors.append("\'imie\' can\'t be null")
            if json_request["nazwisko"] is None:
                errors.append("\'nazwisko\' can\'t be null")
            if json_request["pesel"] is None:
                errors.append("\'pesel\' can\'t be null")
            if json_request["amount"] is None:
                errors.append("\'amount\' can\'t be null")
            elif not isinstance(json_request["amount"], float):
                errors.append("\'amount\' must be of type: float")
            if "wskPrzeterminowania" in json_request:
                if not re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2} ([0-9]{2}:){2}[0-9]{2}$", json_request["wskPrzeterminowania"]):
                    errors.append(f"\'{json_request['wskPrzeterminowania']}\' does not match the pattern \'yyyy-mm-dd hh:mm:ss\'")
            if json_request["home_address"] is None:
                errors.append("\'home_address\' can\'t be null")
            else:
                adress_parse_result = AddressParser.parse(json_request["home_address"])
                if adress_parse_result is not None:
                    errors.append(adress_parse_result)
            if json_request["mailing_address"] is None:
                errors.append("\'mailing_address\' can\'t be null")
            else:
                adress_parse_result = AddressParser.parse(json_request["mailing_address"])
                if adress_parse_result is not None:
                    errors.append(adress_parse_result)
        except Exception as e:
            return f"Error during parsing: {str(e)}"

        if len(errors) == 0:
            return None
        else:
            return ",".join(errors)
