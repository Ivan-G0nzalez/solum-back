# 🗄️ Database Migration Guide

## 📋 Prerequisites

1. **Install Alembic**: `pip install alembic`
2. **Set up environment variables** (create `.env` file):
   ```bash
   DB_TYPE=postgres
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=solum_health
   ```

## 🚀 Initial Setup

### 1. Initialize Alembic (if not done)
```bash
alembic init alembic
```

### 2. Create Initial Migration
```bash
alembic revision --autogenerate -m "Initial migration"
```

### 3. Review Migration
Check the generated file in `alembic/versions/` and make sure it looks correct.

### 4. Apply Migration
```bash
alembic upgrade head
```

## 📝 Common Commands

### Create New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>

# Apply one migration forward
alembic upgrade +1
```

### Rollback Migrations
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

### Check Status
```bash
# Show current migration status
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic show <revision_id>
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Error**: Make sure your models are imported in `alembic/env.py`
2. **Connection Error**: Check your database credentials in `.env`
3. **Metadata Error**: Ensure `target_metadata` is set correctly

### Reset Migrations
If you need to start fresh:
```bash
# Remove all migration files
rm -rf alembic/versions/*

# Remove alembic_version table from database
# (manually or using your database client)

# Create new initial migration
alembic revision --autogenerate -m "Fresh start"
alembic upgrade head
```

## 📊 Database Schema

After running migrations, you should have these tables:

- **clinic**: Stores clinic information
- **call**: Stores call records with clinic relationship
- **evaluation**: Stores call evaluations with call relationship

## 🎯 Best Practices

1. **Always review** generated migrations before applying
2. **Use descriptive** migration messages
3. **Test migrations** in development before production
4. **Backup database** before major migrations
5. **Use transactions** for complex migrations

## 🔄 Workflow

1. Make changes to your SQLModel classes
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Review the generated migration file
4. Apply migration: `alembic upgrade head`
5. Test your application 