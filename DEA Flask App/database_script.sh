DB_NAME="filedata"
DB_USER="postgres"
DB_PASSWORD="1234"

# Function to create database
create_db() {
    echo "Creating database $DB_NAME..."
    psql -U postgres -c "CREATE DATABASE $DB_NAME;"
}


create_tables() {
    echo "Creating tables..."
    psql -d $DB_NAME -U $DB_USER -c "CREATE TABLE files_table (id SERIAL PRIMARY KEY, filename varchar(80) NOT NULL, content TEXT NOT NULL);"
}

# Main execution
echo "Setting up new computer..."

# Create database
create_db

# Create tables (if needed)
create_tables

echo "Database setup completed."