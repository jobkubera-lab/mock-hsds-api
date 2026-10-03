> **KUBERA REFERENCE / UPSTREAM STUDY REPOSITORY**
>
> This repository is retained by `jobkubera-lab` for reference and engineering study. It is not presented as original KUBERA code. Original upstream authorship and licensing remain authoritative. Upstream: [openreferral/mock-hsds-api](https://github.com/openreferral/mock-hsds-api).

HSDS Mock API
=================

This is a very basic Mock API for testing tooling related to the [HSDS Specification](https://docs.openreferral.org).

## How it works

You provide HSDS data as JSON files inside the `data/` directory, divided up by different schema type. You just need to provide files containing individual services, organizations, taxonomies etc. where the file name is the UUID of that object, and the script will handle the rest.

Example: the `service` object with UUID `ac148810-d857-441c-9679-408f346de14b` should be stored as the file `data/services/ac148810-d857-441c-9679-408f346de14b.json`

The Mock API will handle retrieving lists of objects for you and build the `Page` schema required by the HSDS API Specification, so all you need to do is provide the JSON files representing your objects to mock an API setup.

The Mock API will run on port 5000, so to get a list of all services you'll need to visit `http://localhost:5000/services`. Some users report not being able to access `localhost:5000`, so depending on the configuration of your system you might need to use `http://127.0.0.1:5000/services` instead.

## Running the application

1. Set up the Python virtual environment:

```bash
python3 -m venv .ve
source .ve/bin/activate
```
2. Install the dependencies into the environment

```bash
pip install -r requirements.txt
```

3. Run the application `./app.py`

4. Start querying the API: `http://localhost:5000` or `http://127.0.0.1:5000`

## Limitations

### No support for parameters

There is currently no support for parameters in the Mock API on any endpoint

### Large datasets may cause you to run out of memory

This tool is designed to mock up a basic API with some data for you to test HSDS tools against an API. It doesn't attempt to paginate or stream any data, and naïvely puts responses in a single `Page` object. This means if you dump 4000 services into the `data/services/` directory, the mock API will respond to `GET /services` by giving you a single page of 4000 services!
