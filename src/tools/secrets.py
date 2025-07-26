"""Secret Manager integration for secure API key storage"""
import os
from typing import Optional

def get_secret(secret_id: str, project_id: Optional[str] = None) -> str:
    """
    Retrieve a secret from Google Secret Manager.
    Falls back to environment variable if Secret Manager fails.
    """
    try:
        from google.cloud import secretmanager
        
        # Create the Secret Manager client
        client = secretmanager.SecretManagerServiceClient()
        
        # Use provided project_id or get from environment
        if not project_id:
            project_id = os.getenv('GCP_PROJECT_ID', 'storygrow-796f0')
        
        # Build the resource name of the secret version
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        
        # Access the secret version
        response = client.access_secret_version(request={"name": name})
        
        # Return the secret value
        return response.payload.data.decode('UTF-8')
        
    except Exception as e:
        print(f"[Secrets] Failed to get secret {secret_id} from Secret Manager: {e}")
        # Fall back to environment variable
        env_var = secret_id.upper().replace('-', '_')
        return os.getenv(env_var, '')

def get_gemini_api_key() -> str:
    """Get Gemini API key from Secret Manager or environment"""
    return get_secret('gemini-api-key') or os.getenv('GEMINI_API_KEY', '')