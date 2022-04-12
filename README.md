# table2sql


[![CI](https://github.com/piotrgredowski/table2sql/actions/workflows/ci.yml/badge.svg)](https://github.com/piotrgredowski/table2sql/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=piotrgredowski_table2sql&metric=alert_status)](https://sonarcloud.io/dashboard?id=piotrgredowski_table2sql)
[![codecov](https://codecov.io/gh/piotrgredowski/table2sql/branch/main/graph/badge.svg?token=fNkIDyWLq7)](https://codecov.io/gh/piotrgredowski/table2sql)
[![CodeQL](https://github.com/piotrgredowski/table2sql/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/piotrgredowski/table2sql/actions/workflows/codeql-analysis.yml)

[![PyPI version](https://badge.fury.io/py/table2sql.svg)](https://badge.fury.io/py/table2sql)

Python CLI tool which allows you to convert file with table (CSV and Excel) to SQL insert statements.

[Docs](https://gredowski.com/table2sql/)

## Basic usage

`some.csv`

```csv
a,b,c,d
int,str,float,sql
1,2,3,(SELECT id FROM another.table WHERE name = 'Paul')
5,6,7,(SELECT id FROM another.table WHERE name = 'Paul')
```

Command:

```bash
table2sql some.csv --output-table some.table --has-types-row
```

Result:

```sql
INSERT INTO some.table (a, b, c, d)
VALUES (1, '2', 3.0, (SELECT id FROM another.table WHERE name = 'Paul')), (5, '6', 7.0, (SELECT id FROM another.table WHERE name = 'Paul'));
```

## Install

```bash
pip install table2sql
```
