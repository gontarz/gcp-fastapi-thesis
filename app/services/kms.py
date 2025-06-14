from google.cloud import kms

from config import get_settings

client = kms.KeyManagementServiceClient()


def create_kms_key_for_user(key_id: str) -> str:
    settings = get_settings()

    # Build the parent key ring name.
    key_ring_name = client.key_ring_path(
        project=settings.GCP_PROJECT_ID,
        location=settings.GCP_REGION,
        key_ring=settings.GCP_KEY_RING_ID,
    )

    # Build the key.
    purpose = kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    algorithm = kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    key = {
        "purpose": purpose,
        "version_template": {
            "algorithm": algorithm,
        },
    }

    created_key = client.create_crypto_key(
            request={
                "parent": key_ring_name,
                "crypto_key_id": key_id,
                "crypto_key": key,
            }
        )

    return created_key.name


def create_key_version(key_id: str) -> str:
    settings = get_settings()

    # Build the parent key name.
    key_name = client.crypto_key_path(
        project=settings.GCP_PROJECT_ID,
        location=settings.GCP_REGION,
        key_ring=settings.GCP_KEY_RING_ID,
        crypto_key=key_id
    )

    # Build the key version.
    version = {}

    # Call the API.
    created_version = client.create_crypto_key_version(
        request={"parent": key_name, "crypto_key_version": version}
    )
    print(f"Created key version: {created_version.name}")  # TODO
    return created_version.name


def validate_kms_key(key_name: str) -> bool:
    try:
        client.get_crypto_key(request={"name": key_name})
    except Exception:
        return False
    return True