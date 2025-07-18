from configs.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'autoria'),
        'USER': os.getenv('DB_USER', 'admin'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'AbCdEf123456'),
        'HOST': os.getenv('DB_HOST', 'ep-silent-hill-123456.us-east-2.aws.neon.tech'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': os.getenv('DB_SSL_MODE', 'require'),
        },
        'TEST': {
            'NAME': 'test_neondb',
            'DEPENDENCIES': [],
            'MIRROR': None,
        },
        'CONN_MAX_AGE': 0,  # Close connections after each request for tests
    }
}
# Disable Celery for tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = None
CELERY_TASK_IGNORE_RESULT = True
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
# Use custom test runner
TEST_RUNNER = 'core.test_runner.CustomTestRunner'