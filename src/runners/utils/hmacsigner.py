import hashlib
import hmac
import json
from typing import Union

from game_contracts.message import MessageEnvelope


class HMACSigner:
    def __init__(self, secret: Union[str, bytes]):
        self.secret = secret.encode() if isinstance(secret, str) else secret

    def sign(self, envelope: MessageEnvelope) -> str:
        serialized = self._serialize_for_signing(envelope)
        return hmac.new(self.secret, serialized, hashlib.sha256).hexdigest()

    def verify(self, envelope: MessageEnvelope, signature: str) -> bool:
        expected = self.sign(envelope)
        return hmac.compare_digest(expected, signature)

    def _serialize_for_signing(self, envelope: MessageEnvelope) -> bytes:
        signing_fields = {
            "client_id": envelope.client_id,
            "game_id": envelope.game_id,
            "seq": envelope.seq,
            "payload": envelope.payload,
        }
        return json.dumps(signing_fields, sort_keys=True).encode()
