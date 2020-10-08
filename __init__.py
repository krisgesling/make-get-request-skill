import requests
from os.path import join

from mycroft import MycroftSkill, intent_handler


class MakeGetRequest(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.settings_change_callback = self.check_settings

    def check_settings(self):
        """Check if minimum required Skill settings are available."""
        self.trigger_phrase = self.settings.get('trigger_phrase')
        self.url = self.settings.get('url')
        if self.trigger_phrase and self.url:
            self.update_intent_file()
            self.enable_intent('make.request.intent')
        else:
            self.disable_intent('make.request.intent')

    def update_intent_file(self):
        """Update intent file with trigger phrase from settings."""
        intent_file = join(self.root_dir, 'locale', self.lang, 
                        'make.request.intent')
        with open(intent_file, 'w') as f: 
            f.write(self.trigger_phrase) 
        
    @intent_handler('make.request.intent')
    def handle_request(self, message):
        """Make the actual GET request."""
        key = self.settings.get('param_key')
        value = self.settings.get('param_value')
        response_on_success = self.settings.get('response_on_success')
        response_on_failure = self.settings.get('response_on_failure')

        params = {}
        if key and value:
            params[key] = value

        try:
            req_response = requests.get(self.settings.get('url'), params=params)
            if 200 <= req_response.status_code <= 299:
                if response_on_success:
                    self.speak(response_on_success)
            elif response_on_failure:
                self.speak(response_on_failure)
        except:
            if response_on_failure:
                self.speak(response_on_failure)
            else:
                self.speak_dialog('error')


def create_skill():
    return MakeGetRequest()

