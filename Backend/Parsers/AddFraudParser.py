class AddFraudParser:
    @staticmethod
    def parse(json_request):
        errors = []
        try:
            if "applicationId" not in json_request:
                errors.append("\'applicationId\' can\'t be null")
            if "reason" not in json_request:
                errors.append("\'reason\' can\'t be null")
            if "authority" not in json_request:
                errors.append("\'authority\' can\'t be null")
        except Exception as e:
            return f"Error during parsing: {str(e)}"

        if len(errors) == 0:
            return None
        else:
            return ",".join(errors)
