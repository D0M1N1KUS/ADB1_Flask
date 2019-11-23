import re
from Backend.Parsers.AddressParser import AddressParser

class AddProposalParser:
    @staticmethod
    def parse(json_request):
        errors = []
        try:
            # if "applicationId" not in json_request:
            #     errors.append("\'applicationId\' can\'t be null")
            if "clientType" not in json_request:
                errors.append("\'clientType\' can\'t be null")
            if "loanType" not in json_request:
                errors.append("\'loanType\' can\'t be null")
            if "firstName" not in json_request:
                errors.append("\'firstName\' can\'t be null")
            if "lastName" not in json_request:
                errors.append("\'lastName\' can\'t be null")
            if "pesel" not in json_request:
                errors.append("\'pesel\' can\'t be null")
            elif not re.search("^[0-9]{11}$", json_request["pesel"]):
                errors.append("\'pesel\' doesn\'t match pesel pattern")
            if "mailingStreet" not in json_request:
                errors.append("\'mailingStreet\' can\'t be null")
            if "mailingCity" not in json_request:
                errors.append("\'mailingCity\' can\'t be null")
            if "mailingPostalCode" not in json_request:
                errors.append("\'mailingPostalCode\' can\'t be null")
            elif not re.search("^[0-9]{2}-[0-9]{3}$", json_request["mailingPostalCode"]):
                errors.append("\'mailingPostalCode\' doesn\'t match post code pattern")
            if "amount" not in json_request:
                errors.append("\'amount\' can\'t be null")
            elif not isinstance(json_request["amount"], float):
                errors.append("\'amount\' must be of type: float")

        except Exception as e:
            return f"Error during parsing: {str(e)}"

        if len(errors) == 0:
            return None
        else:
            return ",".join(errors)
