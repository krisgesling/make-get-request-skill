from mycroft import MycroftSkill, intent_file_handler


class MakeGetRequest(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('request.get.make.intent')
    def handle_request_get_make(self, message):
        self.speak_dialog('request.get.make')


def create_skill():
    return MakeGetRequest()

