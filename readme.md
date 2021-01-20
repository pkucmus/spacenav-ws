# Websockets exposer for the spacenav driver

This is a **work in progress** service that is supposed to make Onshape work with spacenav.

[FreeSpacenav/spacenavd](https://github.com/FreeSpacenav/spacenavd)

https://github.com/FreeSpacenav/spacenavd/issues/30

## Deploy

### Install deps

With PIP, or Poetry

```
pip install -r requirements.txt
```

or

```
poetry install
```

### Run

```
uvicorn main:app --host 0.0.0.0 --port 8181 --reload
```

open http://127.0.0.1:8181 and toggle your SpaceMouse.
