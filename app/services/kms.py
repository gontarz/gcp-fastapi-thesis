from google.cloud import kms

from config import get_settings

client = kms.KeyManagementServiceClient()


def create_kms_key_for_user(user_id: str):
    settings = get_settings()

    key_id = f"key-{user_id}"

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

    try:
        created_key = client.create_crypto_key(
            request={
                "parent": key_ring_name,
                "crypto_key_id": key_id,
                "crypto_key": key,
            }
        )
        return {"key_name": created_key.name}
    except Exception as e:
        return {"error": str(e)}


def create_key_version(
        # project_id: str, location_id: str, key_ring_id: str, key_id: str
        user_id: str

) -> kms.CryptoKey:
    """
    Creates a new version of the given key.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key for which to create a new version (e.g. 'my-key').

    Returns:
        CryptoKeyVersion: Cloud KMS key version.

    """
    settings = get_settings()

    key_id = f"key-{user_id}"

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
