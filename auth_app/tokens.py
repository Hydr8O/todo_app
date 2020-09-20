from django.contrib.auth.tokens import PasswordResetTokenGenerator

class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)

activation_token_generator = ActivationTokenGenerator()

def generate_activation_token(user):
    return activation_token_generator.make_token(user)

def check_activation_token(user, token):
    return activation_token_generator.check_token(user, token)