class ResponseConstructor:
    def __init__(self):
        self.message = {}

    def validate_field(self, key, value, mandatory=True):
        if not value and mandatory:
            self.message.update({key: ['Field is mandatory.']})

    def get_response(self):
        return self.message
