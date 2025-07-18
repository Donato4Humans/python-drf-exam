import time

from django.db import connections
from django.db.utils import OperationalError
from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):
    def teardown_databases(self, old_config, **kwargs):
        alias = 'default'
        connection = connections[alias]
        test_db_name = connection.settings_dict['TEST']['NAME']

        # Close all Django connections
        connections.close_all()

        # Log active connections for debugging
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pid, usename, datname, query "
                    "FROM pg_stat_activity "
                    "WHERE datname = %s AND pid <> pg_backend_pid();",
                    [test_db_name]
                )
                active_connections = cursor.fetchall()
                if active_connections:
                    print(f"Active connections to {test_db_name}: {active_connections}")
        except OperationalError:
            pass  # Connection may already be closed

        # Retry terminating connections
        for attempt in range(5):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT pg_terminate_backend(pg_stat_activity.pid) "
                        "FROM pg_stat_activity "
                        "WHERE datname = %s AND pid <> pg_backend_pid();",
                        [test_db_name]
                    )
                time.sleep(1)  # Increased delay for Neon pooling
                super().teardown_databases(old_config, **kwargs)
                return
            except OperationalError as e:
                if "database is being accessed by other users" in str(e):
                    print(f"Attempt {attempt + 1}: Waiting for connections to close...")
                    time.sleep(2)
                else:
                    raise
        raise OperationalError(f"Failed to drop test database {test_db_name} after 5 attempts")