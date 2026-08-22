#!/usr/bin/env python3
"""Convert a PostgreSQL dump to SQLite3 database."""

import os
import re
import sqlite3
import sys


def parse_create_table(lines, idx):
    """Parse a CREATE TABLE statement starting at idx, return (table_name, sql, next_idx)."""
    line = lines[idx]
    m = re.match(r'CREATE TABLE public\."?(\w+)"?\s*\(', line)
    if not m:
        return None, None, idx + 1
    table_name = m.group(1)
    parts = [f'CREATE TABLE "{table_name}" (']
    idx += 1
    while idx < len(lines):
        line = lines[idx]
        if line.strip() == ');':
            parts.append(');')
            return table_name, '\n'.join(parts), idx + 1
        # Convert PG types to SQLite types
        col_line = line
        # Remove schema prefix
        col_line = col_line.replace('public.', '')

        # Parse column definition: leading whitespace, column_name, then type
        # We need to only replace the TYPE portion, not the column name
        col_match = re.match(r'^(\s+"?\w+"?\s+)(.*)', col_line)
        if col_match:
            prefix = col_match.group(1)  # column name part
            type_part = col_match.group(2)  # type and constraints
            # Apply type conversions only to the type part
            type_part = re.sub(r'\bboolean\b', 'INTEGER', type_part)
            type_part = re.sub(r'character varying\(\d+\)', 'TEXT', type_part)
            type_part = re.sub(r'character varying', 'TEXT', type_part)
            type_part = re.sub(r'numeric\(\d+,\d+\)', 'REAL', type_part)
            type_part = re.sub(r'\binteger\b', 'INTEGER', type_part)
            type_part = re.sub(r'\bbigint\b', 'INTEGER', type_part)
            type_part = re.sub(r'\bsmallint\b', 'INTEGER', type_part)
            type_part = re.sub(r'\bdate\b(?!\w)', 'TEXT', type_part)
            type_part = re.sub(r'timestamp with(out)? time zone', 'TEXT', type_part)
            type_part = re.sub(r'\btimestamp\b', 'TEXT', type_part)
            type_part = re.sub(r'double precision', 'REAL', type_part)
            type_part = re.sub(r'\bbytea\b', 'BLOB', type_part)
            col_line = prefix + type_part
        parts.append(col_line)
        idx += 1
    return table_name, '\n'.join(parts), idx


def parse_copy_block(lines, idx):
    """Parse COPY ... FROM stdin block. Returns (table_name, columns, rows, next_idx)."""
    line = lines[idx]
    m = re.match(r'COPY public\."?(\w+)"?\s*\((.+?)\)\s*FROM stdin;', line)
    if not m:
        return None, None, None, idx + 1
    table_name = m.group(1)
    columns = [c.strip().strip('"') for c in m.group(2).split(',')]
    rows = []
    idx += 1
    while idx < len(lines):
        line = lines[idx]
        if line.strip() == '\\.':
            return table_name, columns, rows, idx + 1
        # Tab-separated values
        values = line.split('\t')
        converted = []
        for v in values:
            if v == '\\N':
                converted.append(None)
            elif v == 't':
                converted.append(1)
            elif v == 'f':
                converted.append(0)
            else:
                converted.append(v)
        rows.append(converted)
        idx += 1
    return table_name, columns, rows, idx


def main():
    # The v1 dump is real production data and is kept outside the repo working
    # tree. Pass it explicitly, or set KOALIXCRM_LEGACY_DUMP.
    default_input = os.environ.get('KOALIXCRM_LEGACY_DUMP')
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    elif default_input:
        input_file = default_input
    else:
        raise SystemExit(
            'No input dump given. Pass it as the first argument or set '
            'KOALIXCRM_LEGACY_DUMP. The v1 dump contains customer data and is '
            'deliberately not stored in this repo.'
        )
    output_file = sys.argv[2] if len(sys.argv) > 2 else '/app/koalixcrm/db.sqlite3'

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    conn = sqlite3.connect(output_file)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=OFF;")  # Disable during import
    cur = conn.cursor()

    tables_created = 0
    tables_loaded = 0
    total_rows = 0
    idx = 0

    # First pass: CREATE TABLEs
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('CREATE TABLE public.'):
            table_name, sql, idx = parse_create_table(lines, idx)
            if sql:
                try:
                    cur.execute(sql)
                    tables_created += 1
                    print(f"  Created table: {table_name}")
                except Exception as e:
                    print(f"  ERROR creating table {table_name}: {e}")
                    print(f"    SQL: {sql[:200]}")
        else:
            idx += 1

    conn.commit()

    # Second pass: COPY data
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('COPY public.'):
            table_name, columns, rows, idx = parse_copy_block(lines, idx)
            if table_name and rows:
                col_names = ', '.join(f'"{c}"' for c in columns)
                placeholders = ', '.join(['?'] * len(columns))
                sql = f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})'
                try:
                    cur.executemany(sql, rows)
                    tables_loaded += 1
                    total_rows += len(rows)
                    print(f"  Loaded {len(rows)} rows into {table_name}")
                except Exception as e:
                    print(f"  ERROR loading data into {table_name}: {e}")
                    # Try row by row to find problematic rows
                    loaded = 0
                    for i, row in enumerate(rows):
                        try:
                            cur.execute(sql, row)
                            loaded += 1
                        except Exception as e2:
                            if i < 3:
                                print(f"    Row {i} error: {e2}")
                                print(f"    Row data: {row[:5]}...")
                    if loaded:
                        print(f"    Loaded {loaded}/{len(rows)} rows individually")
                        total_rows += loaded
            elif table_name:
                print(f"  Skipped {table_name} (no data)")
        else:
            idx += 1

    conn.commit()

    # Third pass: PRIMARY KEY constraints (as unique indexes since SQLite
    # can't add PKs after table creation, and we want to keep it simple)
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        # ALTER TABLE ONLY public.X ADD CONSTRAINT Y PRIMARY KEY (cols);
        if 'PRIMARY KEY' in line and 'ADD CONSTRAINT' in line:
            m = re.search(
                r'ALTER TABLE ONLY public\."?(\w+)"?\s+ADD CONSTRAINT\s+\S+\s+PRIMARY KEY\s*\((.+?)\)',
                line
            )
            if m:
                tbl = m.group(1)
                cols = m.group(2).strip()
                # SQLite doesn't support ADD PRIMARY KEY, create unique index instead
                idx_name = f"pk_{tbl}"
                sql = f'CREATE UNIQUE INDEX IF NOT EXISTS "{idx_name}" ON "{tbl}" ({cols})'
                try:
                    cur.execute(sql)
                except Exception as e:
                    print(f"  WARN: PK index on {tbl}: {e}")
        idx += 1

    conn.commit()

    # Fourth pass: CREATE INDEX
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('CREATE INDEX') or line.startswith('CREATE UNIQUE INDEX'):
            # Collect full statement (may span multiple lines)
            stmt = line
            while not stmt.rstrip().endswith(';') and idx + 1 < len(lines):
                idx += 1
                stmt += ' ' + lines[idx]
            # Clean up PG-specific syntax
            stmt = stmt.replace('public.', '')
            stmt = re.sub(r'USING \w+\s*', '', stmt)
            try:
                cur.execute(stmt)
            except Exception as e:
                print(f"  WARN: Index: {e}")
        idx += 1

    conn.commit()

    # Update sequences (set SQLite autoincrement counters via sqlite_sequence)
    # Not strictly needed since SQLite handles rowid automatically

    conn.execute("PRAGMA foreign_keys=ON;")
    conn.close()

    print(f"\nDone! Created {tables_created} tables, loaded {total_rows} rows across {tables_loaded} tables.")
    print(f"Output: {output_file}")


if __name__ == '__main__':
    main()
