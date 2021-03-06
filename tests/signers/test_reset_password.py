from django.test.utils import override_settings

from rest_registration.api.views.reset_password import ResetPasswordSigner
from tests.helpers.constants import (
    RESET_PASSWORD_VERIFICATION_URL,
    VERIFICATION_FROM_EMAIL
)
from tests.helpers.settings import override_rest_registration_settings
from tests.helpers.testcases import TestCase


@override_rest_registration_settings({
    'RESET_PASSWORD_VERIFICATION_URL': RESET_PASSWORD_VERIFICATION_URL,
    'VERIFICATION_FROM_EMAIL': VERIFICATION_FROM_EMAIL,
})
class ResetPasswordSignerTestCase(TestCase):

    def test_signer_with_different_secret_keys(self):
        user = self.create_test_user(is_active=False)
        data_to_sign = {'user_id': user.pk}
        secrets = [
            '#0ka!t#6%28imjz+2t%l(()yu)tg93-1w%$du0*po)*@l+@+4h',
            'feb7tjud7m=91$^mrk8dq&nz(0^!6+1xk)%gum#oe%(n)8jic7',
        ]
        signatures = []
        for secret in secrets:
            with override_settings(
                    SECRET_KEY=secret):
                signer = ResetPasswordSigner(data_to_sign)
                data = signer.get_signed_data()
                signatures.append(data[signer.SIGNATURE_FIELD])

        assert signatures[0] != signatures[1]
