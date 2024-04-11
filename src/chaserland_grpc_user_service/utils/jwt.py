from __future__ import annotations

import base64
import json

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


class JWTBearer:
    def __init__(self, access_token: str, token_type: str) -> None:
        self.access_token = access_token
        self.token_type = token_type

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value: str):
        self._access_token = value

    @property
    def token_type(self):
        return self._token_type

    @token_type.setter
    def token_type(self, value: str):
        self._token_type = value

    def to_jwt(self, encoding="utf-8") -> JWT:
        header, payload, _ = self.access_token.split(".")
        return JWT(
            header=JWTHeader(**JWT.decode(header, encoding=encoding)),
            payload=JWTPayload(**JWT.decode(payload, encoding=encoding)),
        )

    def verify(
        self,
        public_key: str,
        mode: str = "fips-186-3",
        encoding: str = "utf-8",
    ) -> bool:
        try:
            header, payload, signature = self.access_token.split(".")
        except ValueError:
            return False
        signature = JWT.addPadding(signature)
        message = f"{header}.{payload}"
        public_key = ECC.import_key(public_key)
        verifier = DSS.new(public_key, mode)
        try:
            verifier.verify(
                SHA256.new(message.encode(encoding)),
                base64.urlsafe_b64decode(signature),
            )
            return True
        except ValueError:
            return False


class JWTHeader:
    def __init__(self, alg: str, typ: str = "JWT") -> None:
        self.alg = alg
        self.typ = typ

    @property
    def alg(self):
        return self._alg

    @alg.setter
    def alg(self, value: str):
        self._alg = value

    @property
    def typ(self):
        return self._typ

    def to_urlsafe_base64(self, encoding: str = "utf-8") -> str:
        return JWT.encode(self.model_dump(), encoding=encoding)


class JWTPayload(dict):
    def to_urlsafe_base64(self, encoding: str = "utf-8") -> str:
        return JWT.encode(self, encoding=encoding)


class JWT:
    def __init__(self, header: JWTHeader, payload: JWTPayload) -> None:
        self.header = header
        self.payload = payload

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value: JWTHeader):
        self._header = value

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value: JWTPayload):
        self._payload = value

    @staticmethod
    def encode(data: dict | bytes, encoding: str = "utf-8") -> str:
        if isinstance(data, dict):
            return (
                base64.urlsafe_b64encode(json.dumps(data).encode(encoding))
                .decode(encoding)
                .replace("=", "")
            )
        if isinstance(data, bytes):
            return base64.urlsafe_b64encode(data).decode(encoding).replace("=", "")

        raise ValueError(f"Unsupported data type: {type(data)}")

    @staticmethod
    def decode(data: str, encoding: str = "utf-8") -> dict:
        return json.loads(
            base64.urlsafe_b64decode(JWT.addPadding(data)).decode(encoding)
        )

    @staticmethod
    def addPadding(data: str) -> str:
        return data + "=" * (4 - len(data) % 4)

    def generate_bearer_string(
        self,
        private_key: str,
        mode: str = "fips-186-3",
        encoding: str = "utf-8",
    ) -> str:
        if mode not in ["fips-186-3", "deterministic-rfc6979"]:
            raise ValueError(f"Unsupported mode: {mode}")
        header = self.header.to_urlsafe_base64(encoding=encoding)
        payload = JWT.encode(self.payload)
        message = f"{header}.{payload}"
        private_key = ECC.import_key(private_key)
        signer = DSS.new(private_key, mode)
        signature = JWT.encode(signer.sign(SHA256.new(message.encode(encoding))))
        return f"{message}.{signature}"

    def to_bearer(
        self,
        private_key: str,
        mode: str = "fips-186-3",
        encoding: str = "utf-8",
    ) -> JWTBearer:
        return JWTBearer(
            access_token=self.generate_bearer_string(private_key, mode, encoding),
            token_type="bearer",
        )
