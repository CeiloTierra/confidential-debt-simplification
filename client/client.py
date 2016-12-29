import logging

import utils.messages.message_formats as msg
from utils.crypto import rsa
from utils.messages.connection import connect, ConflictError, ForbiddenError, \
    UnauthorizedError


class ProtocolError(Exception):
    """ Raised when an error anticipated in the protocol """

    def __init__(self, message):
        self.message = message


class UserExistsError(ProtocolError):
    """ Raised when trying to add a client that already exists """
    pass


class PermissionDeniedError(ProtocolError):
    """
    Raised when a client does not have permission to execute some
    operation.
    """
    pass


class SecurityError(ProtocolError):
    """
    Raised by the client to indicate an error due to security as
    occurred.
    """
    pass


logger = logging.Logger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Client:
    """ Interface for the client """

    # default group ID
    GROUP_ID = "1"  # FIXME add support for multiple groups

    def __init__(self, group_server_url: str,
                 group_server_pubkey: str,
                 main_server_pubkey: str,
                 email: str, key_path=None, keys=None):

        self.group_server_url = group_server_url
        self.group_server_pubkey = group_server_pubkey
        self.main_server_pubkey = main_server_pubkey
        self.email = email

        if key_path:
            self.key, self.pubkey = rsa.load_keys(key_path)
        elif keys:
            self.key, self.pubkey = keys
        else:
            self.key, self.pubkey = rsa.generate_keys()

        self.proxy_server_address = ""
        self.proxy_server_pubkey = ""

    @property
    def id(self) -> str:
        return self.pubkey

    def invite(self, invitee_id: str, invitee_email: str):
        """
        Invites a new user to the group.

        :param invitee_id: invited user's ID.
        :param invitee_email: invited user's email.
        :raise ClientExistsError: if invitee is already registered
        """
        request = msg.UserInvite.make_request(
            group_uuid=self.GROUP_ID,
            inviter=self.id,
            invitee=invitee_id,
            invitee_email=invitee_email,
            inviter_signature=msg.UserInvite.sign(
                key=self.key,
                signature_name="inviter",
                group_uuid=self.GROUP_ID,
                inviter=self.id,
                invitee=invitee_id,
                invitee_email=invitee_email,
            )
        )

        with connect(self.group_server_url) as connection:
            connection.request(request)

            try:
                # response can be ignored since it is only an acknowledgement
                connection.get_response(msg.UserInvite)

            except ConflictError:
                raise UserExistsError("Invited client is already registered")
            except ForbiddenError:
                raise PermissionDeniedError("Inviter is not registered")
            except UnauthorizedError:
                raise SecurityError("Signature verification failed")

    def join(self, secret_code: str, inviter_id: str):
        """
        Tries to have the client join a group.

        :param secret_code: secret code provided by email.
        :param inviter_id: ID of the inviter.
        """
        request = msg.GroupServerJoin.make_request(
            group_uuid=self.GROUP_ID,
            user=self.id,
            secret_code=secret_code,
            user_signature=msg.GroupServerJoin.sign(
                key=self.key,
                signature_name='user',
                group_uuid=self.GROUP_ID,
                user=self.id,
                secret_code=secret_code
            )
        )

        with connect(self.group_server_url) as connection:
            connection.request(request)

            try:
                response = connection.get_response(msg.GroupServerJoin)

            except ConflictError:
                raise UserExistsError("User is already registered")
            except ForbiddenError:
                raise PermissionDeniedError("Secret code was not accepted")
            except UnauthorizedError:
                raise SecurityError("Signature verification failed")

            try:
                msg.GroupServerJoin.verify(
                    key=inviter_id,
                    signature_name='invite',
                    signature=response.inviter_signature,
                    group_uuid=self.GROUP_ID,
                    inviter=inviter_id,
                    user=self.id,
                    user_email=self.email,
                )

                # TODO store signature

            except rsa.InvalidSignature:
                raise SecurityError("Inviter signature is invalid")

            try:
                msg.GroupServerJoin.verify(
                    key=self.group_server_pubkey,
                    signature_name='group',
                    signature=response.group_signature,
                    group_uuid=self.GROUP_ID,
                    inviter_signature=response.inviter_signature,
                )

                # TODO store signature

            except rsa.InvalidSignature:
                raise SecurityError("Group server signature is invalid")

    def confirm_join(self, group_signature):
        """
        Sends a confirm join to the group server. This completes the joining
        process. It assumes that both the inviter and group signatures have
        already been verified. DO NOT CALL THIS METHOD WITH NON-VERIFIED
        SIGNATURES!

        :param group_signature: invite signed by the group server
        """
        request = msg.ConfirmJoin.make_request(
            group_uuid=self.GROUP_ID,
            user=self.id,
            signature=msg.ConfirmJoin.sign(
                key=self.key,
                signature_name='user',
                group_server_signature=group_signature
            )
        )

        with connect(self.group_server_url) as connection:
            connection.request(request)

            try:
                # response can be ignored since it is only an acknowledgement
                connection.get_response(msg.UserInvite)

            except ConflictError:
                raise UserExistsError("User is already confirmed")
            except ForbiddenError:
                raise PermissionDeniedError("User can not confirm join of "
                                            "another user")
            except UnauthorizedError:
                raise SecurityError("Signature verification failed")

    def issue_UOMe(self, borrower: str, value: int, description: str):
        request = msg.IssueUOMe.make_request(
            group_uuid=self.GROUP_ID,
            user=self.id,
            borrower=borrower,
            value=value,
            description=description,
            user_signature=msg.IssueUOMe.sign(
                key=self.key,
                signature_name='user',
                group_uuid=self.GROUP_ID,
                user=self.id,
                borrower=borrower,
                value=str(value),
                description=description
            )
        )

        with connect(self.group_server_url) as connection:
            connection.request(request)

            try:
                response = connection.get_response(msg.IssueUOMe)

            except ForbiddenError:
                raise PermissionDeniedError("User can not issue UOMes")
            except UnauthorizedError:
                raise SecurityError("Signature verification failed")

            try:
                msg.IssueUOMe.verify(
                    key=self.main_server_pubkey,
                    signature_name='main',
                    signature=response.main_signature,
                    uome_uuid=response.uome_uuid,
                    group_uuid=self.GROUP_ID,
                    user=self.id,
                    borrower=borrower,
                    value=str(value),
                    description=description,
                )

                # TODO store signature
                # TODO store the UOMe-ID

            except rsa.InvalidSignature:
                raise SecurityError("Main server signature is invalid")

    def pending_UOMes(self):
        pass

    def accept_UOMe(self, UOMe_number):
        pass

    def cancel_UOMe(self, UOMe_number):
        pass

    def totals(self):
        pass
