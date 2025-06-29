from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)

async def generate_koji_cert(
    user_id: int,
    valid_days: int,
    ca_cert: x509.Certificate,
    ca_private_key: rsa.RSAPrivateKey,
    permissions: Dict[str, bool]
) -> Tuple[str, str]:
    try:
        if not isinstance(ca_cert, x509.Certificate):
            raise ValueError("Invalid CA certificate type")
        if not isinstance(ca_private_key, rsa.RSAPrivateKey):
            raise ValueError("Invalid CA private key type")

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Koji Client"),
            x509.NameAttribute(NameOID.COMMON_NAME, f"user-{user_id}"),
        ])

        valid_from = datetime.utcnow()
        valid_to = valid_from + timedelta(days=valid_days)

        extensions = [
            x509.BasicConstraints(ca=False, path_length=None),
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                content_commitment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False
            ),
            x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH])
        ]

        for perm, value in permissions.items():
            if value:
                try:
                    extensions.append(
                        x509.UnrecognizedExtension(
                            x509.ObjectIdentifier(f"1.3.6.1.4.1.2312.9.1.{perm.upper()}"),
                            b"\x01"
                        )
                    )
                except ValueError as e:
                    logger.warning(f"Failed to add permission {perm}: {str(e)}")

        builder = x509.CertificateBuilder()
        builder = builder.subject_name(subject)
        builder = builder.issuer_name(ca_cert.subject)
        builder = builder.public_key(public_key)
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.not_valid_before(valid_from)
        builder = builder.not_valid_after(valid_to)

        for ext in extensions:
            builder = builder.add_extension(ext, critical=False)

        certificate = builder.sign(
            private_key=ca_private_key,
            algorithm=hashes.SHA256()
        )

        cert_pem = certificate.public_bytes(
            encoding=serialization.Encoding.PEM
        ).decode('utf-8')
        
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        return cert_pem, key_pem

    except Exception as e:
        logger.error(f"Certificate generation failed: {str(e)}", exc_info=True)
        raise ValueError(f"Certificate generation error: {str(e)}")