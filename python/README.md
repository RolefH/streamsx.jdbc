# Python streamsx.database package

This exposes SPL operators in the `com.ibm.streamsx.jdbc` toolkit as Python methods.

Package is organized using standard packaging to upload to PyPi.

The package is uploaded to PyPi in the standard way:
```
cd python/package
python setup.py sdist bdist_wheel upload -r pypi
```
Note: This is done using the `ibmstreams` account at pypi.org and requires `.pypirc` file containing the credentials in your home directory.

Package details: https://pypi.python.org/pypi/streamsx.database

Documentation is using Sphinx and can be built locally using:
```
cd python/package/docs
make html
```
and viewed using
```
firefox python/package/docs/build/html/index.html
```

The documentation is also setup at `readthedocs.io`.

Documentation links:
* http://streamsxdatabase.readthedocs.io/en/pypackage

## Test

Package can be tested with TopologyTester using the [Streaming Analytics](https://www.ibm.com/cloud/streaming-analytics) service and [DB2 Warehouse](https://console.bluemix.net/docs/services/Db2whc/index.html#getting_started) service on IBM Cloud.

DB2 Warehouse service credentials are located in a file referenced by environment variable DB2_CREDENTIALS.

```
cd python/package
python3 -u -m unittest streamsx.database.tests.test_database.TestDB
```
