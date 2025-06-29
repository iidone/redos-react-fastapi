from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
import os

_CA_CACHE = {
    'cert': None,
    'key': None
}

def init_ca():
    os.makedirs("certs", exist_ok=True)

    if not os.path.exists("certs/ca.key") or not os.path.exists("certs/ca.crt"):
        ca_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, "My CA"),
        ])
        
        ca_cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(ca_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.utcnow())
            .not_valid_after(datetime.utcnow() + timedelta(days=3650))  # 10 лет
            .add_extension(
                x509.BasicConstraints(ca=True, path_length=None),
                critical=True
            )
            .sign(ca_key, hashes.SHA256())
        )

        with open("certs/ca.key", "wb") as f:
            f.write(ca_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open("certs/ca.crt", "wb") as f:
            f.write(ca_cert.public_bytes(serialization.Encoding.PEM))