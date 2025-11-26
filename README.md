# Group 3

## Python for Amazon Web Services

* Python integrates with AWS through the **boto3 SDK**.
* Supports automation for **EC2, S3, Lambda, DynamoDB, IAM, SNS, SQS, CloudWatch**.
* Enables provisioning, configuration, monitoring, and serverless workflows.
* Common use cases:

  * Upload/download objects to S3.
  * Start/stop EC2 instances.
  * Trigger Lambda functions.
  * Publish messages to SNS.
  * Push/receive messages in SQS.
* Security requirements:

  * IAM user or role with required permissions.
  * Credentials via environment variables or IAM roles.
* Execution environments:

  * Local machine with AWS CLI configured.
  * Lambda Python runtime.
  * EC2 or container environments.

## Python for Google Cloud

* Python integrates with Google Cloud through **google-cloud-* client libraries**.
* Supports Compute Engine, Cloud Storage, BigQuery, Pub/Sub, Cloud Functions.
* Common operations:

  * Upload/download objects to Cloud Storage.
  * Run queries on BigQuery.
  * Publish/subscribe to Pub/Sub topics.
  * Invoke Cloud Functions.
* Authentication via **service account key** or **Application Default Credentials**.
* Execution environments:

  * Local machine with `gcloud` configured.
  * Cloud Functions Python runtime.
  * Compute Engine or container environments.

## Python for Windows Azure

* Python integrates with Azure via the **Azure SDK for Python (azure-*)**.
* Supports Azure Resource Manager, Virtual Machines, Storage Accounts, Blob Storage, Functions, Service Bus, Cosmos DB.
* Common operations:

  * Upload/download blobs.
  * Manage VMs (start, stop, list).
  * Send/receive messages through Service Bus queues.
  * Insert/query documents in Cosmos DB.
* Authentication options:

  * Service Principal (Client ID + Secret).
  * Managed Identity (recommended for Azure VMs/functions).
  * Azure CLI authentication.
* Execution environments:

  * Local machine with Azure CLI logged in.
  * Azure Functions (Python runtime).
  * Azure VM, App Service, Container Apps.

## Python for MapReduce

* Python supports MapReduce using **Hadoop Streaming**, **PySpark**, and **MRJob**.
* Enables distributed processing across clusters for large datasets.
* Common stages:

  * **Map:** Transform input into key-value pairs.
  * **Shuffle:** Group by key.
  * **Reduce:** Aggregate values.
* Execution environments:

  * Hadoop cluster (HDFS + YARN).
  * AWS EMR / Google Dataproc.
  * Local PySpark standalone mode.
* Use cases:

  * Log processing.
  * Word frequency analysis.
  * Aggregation of large distributed datasets.
* Python libraries:

  * `pyspark` (most common).
  * `mrjob` (simple local + EMR execution).
  * Hadoop Streaming with raw Python scripts.

## Python Packages of Interest

* Python ecosystem provides specialized libraries for data processing, cloud automation, web development, machine learning, and systems scripting.
* Core package categories:

  * **Data Analysis:** `pandas`, `numpy`.
  * **Web Requests & APIs:** `requests`, `httpx`.
  * **Cloud SDKs:** `boto3` (AWS), `google-cloud-*`, `azure-*`.
  * **Machine Learning:** `scikit-learn`, `tensorflow`, `torch`.
  * **Web Frameworks:** `django`, `flask`, `fastapi`.
  * **Task Automation:** `fabric`, `invoke`.
  * **Messaging & Queues:** `kafka-python`, `pika`.
  * **Databases:** `sqlalchemy`, `pymongo`, `psycopg2`.
* Widely used in enterprise systems, DevOps pipelines, data engineering, and backend development.

## Python Web Application Framework – Django

* High-level Python framework for rapid web development.
* Core components:

  * **Models:** database abstraction using ORM.
  * **Views:** request handling logic.
  * **Templates:** HTML rendering system.
  * **URL routing:** maps paths to views.
  * **Forms:** validation and rendering.
  * **Admin site:** auto-generated CRUD interface.
* Built-in security: CSRF, XSS protection, SQL injection defense.
* Supports PostgreSQL, MySQL, SQLite, Oracle.
* Suitable for enterprise systems, APIs, dashboards, CMS, e-commerce.

## Development with Django

* Typical workflow:

  * Create project.
  * Create app.
  * Define models → run migrations.
  * Implement views (function-based or class-based).
  * Configure URL patterns.
  * Build templates for rendering.
  * Use Django ORM for database operations.
  * Add admin configurations.
  * Deploy via Gunicorn, Nginx, Docker, or cloud services.
* Typical project structure:

  ```txt
  project/
      settings.py
      urls.py
      app/
          models.py
          views.py
          urls.py
          templates/
  ```
