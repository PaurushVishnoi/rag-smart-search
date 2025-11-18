import os
import boto3
import tempfile
import shutil

from rag_builder import load_notion_docs, chunk_documents, build_vector_store


# ----------------------------
# 1️⃣ Load secrets from SSM
# ----------------------------
def get_secret(name: str) -> str:
    ssm = boto3.client("ssm")
    return ssm.get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]


def load_environment_from_ssm():
    """
    Load all required environment variables from AWS SSM Parameter Store.
    """
    os.environ["OPENAI_API_KEY"] = get_secret("/rag/OPENAI_API_KEY")
    os.environ["NOTION_TOKEN"] = get_secret("/rag/NOTION_TOKEN")
    os.environ["ROOT_PAGE_ID"] = get_secret("/rag/ROOT_PAGE_ID")

    print("🔐 Loaded environment variables from SSM.")


# ----------------------------
# 2️⃣ Lambda Handler
# ----------------------------
def handler(event=None, context=None):
    print("🔄 Lambda triggered → Starting Notion sync...")

    # Load SSM secrets
    load_environment_from_ssm()

    # Create a temporary directory for vector DB
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Temporary working directory: {temp_dir}")

        # Set Chroma DB location to temp directory
        os.environ["CHROMA_DB_DIR"] = temp_dir

        # -------------------------------------------
        #  Fetch → Chunk → Embed → Build Vector Store
        # -------------------------------------------
        print("📥 Fetching Notion documents...")
        notion_docs = load_notion_docs()
        print(f"   → Loaded {len(notion_docs)} pages")

        print("✂️ Splitting into chunks...")
        chunks = chunk_documents(notion_docs)
        print(f"   → Created {len(chunks)} text chunks")

        print("🧠 Building vector database...")
        build_vector_store(chunks, persist_dir=temp_dir)
        print("   → Vector DB built successfully")

        # -------------------------------------------
        #  Optional: Upload DB to S3
        # -------------------------------------------
        """
        s3 = boto3.client("s3")
        bucket_name = "your-bucket-name"
        s3_prefix = "vector-db/"

        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, temp_dir)
                s3_key = s3_prefix + rel_path

                s3.upload_file(local_path, bucket_name, s3_key)
                print(f"   → Uploaded {s3_key} to S3")
        print("☁️ Vector DB uploaded to S3 successfully")
        """

    print("✅ Sync complete — Lambda finished.")

    return {"status": "success", "message": "Vector DB updated."}
