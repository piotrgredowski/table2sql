# table2sql

Python CLI tool which allows you to convert file with table (for now only CSV) to SQL insert statements.


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
