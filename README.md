# boil

A simple boilerplate code generator.

## Initializing

By default, boil reads from a database located in its source directory. To generate this database, run:

```bash
make all
```

OR

```bash
python3 prepare.py
```

## Testing

To run unit tests, run:

```bash
make test
```

OR

```bash
python3 -m unittest -v tests.test
```
