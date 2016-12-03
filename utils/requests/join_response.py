from utils.crypto import rsa
from utils.requests.parameters import signature
from utils.requests.response import Response


class JoinResponse(Response):
    """
    Join Response - response to a join request.
    """

    method = "JOIN"

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "main_server_signature": signature,
        "inviter_signature": signature,
        "register_server_signature": signature,
    }

    @staticmethod
    def build(main_server_signature: bytes, inviter_signature: bytes,
              register_server_signature: bytes):
        """
        Factory method for an Join response. Use this method to create
        Join responses instead of the default initializer.

        Returns an Join response signed by the given signer. This method
        abstracts which parameters are signed by the signer.
        """
        parameters_values = {
            "main_server_signature": main_server_signature,
            "inviter_signature": inviter_signature,
            "register_server_signature": register_server_signature,
        }

        return JoinResponse(parameters_values)

    def verify(self, inviter: bytes, invitee: bytes, invitee_email: str,
               main_server_key: bytes, register_server_key: bytes, ):
        """
        Verifies if the signatures in the join request are valid.
        """
        rsa.verify(main_server_key, self.main_server_signature, invitee)
        rsa.verify(register_server_key, self.register_server_signature,
                   inviter, invitee, invitee_email.encode())
        rsa.verify(inviter, self.inviter_signature,
                   inviter, invitee, invitee_email.encode())

    @property
    def main_server_signature(self) -> bytes:
        return self._parameters_values["main_server_signature"]

    @property
    def inviter_signature(self) -> bytes:
        return self._parameters_values["inviter_signature"]

    @property
    def register_server_signature(self) -> bytes:
        return self._parameters_values["register_server_signature"]
