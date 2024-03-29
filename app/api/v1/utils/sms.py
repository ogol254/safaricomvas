from __future__ import print_function

import africastalking


class SMS:
    def __init__(self):
                # Set your app credentials
        self.username = "sandbox"
        self.api_key = "657d265600a307dac2e623fca122f9a71703e28eaa10175cd6815b136562cb3f"
        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)
        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self):
        # Set the numbers you want to send to in international format
        recipients = ["+254790463533"]

        # Set your message
        message = "I'm a lumberjack and it's ok, I sleep all night and I work all day"

        # Set your shortCode or senderId
        sender = 15710
        try:
                            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(message, recipients, sender)
            print(response)
        except Exception as e:
            print('Encountered an error while sending: %s' % str(e))


if __name__ == '__main__':
    SMS().send()
