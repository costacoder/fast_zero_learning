from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importa a metadata dos modelos registrados
from fast_zero.models import table_registry
from fast_zero.settings import Settings

# Configurar URL do banco de dados com o valor do Settings
config = context.config
config.set_main_option("sqlalchemy.url", Settings().DATABASE_URL)

# Configurar logs, se definido no alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define a metadata para o Alembic autogenerate
target_metadata = table_registry.metadata

def run_migrations_offline() -> None:
    """Executar migrações no modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executar migrações no modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
