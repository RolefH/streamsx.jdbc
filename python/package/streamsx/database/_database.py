# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2018

import datetime
import requests
from tempfile import gettempdir
import streamsx.spl.op
import streamsx.spl.types
from streamsx.topology.schema import CommonSchema, StreamSchema
from streamsx.spl.types import rstring


def _add_driver_file(topology):
    url = "https://github.com/IBMStreams/streamsx.jdbc/raw/master/samples/JDBCSample/opt/db2jcc4.jar"
    r = requests.get(url)
    filename = 'db2jcc4.jar'
    tmpdirname = gettempdir()
    tmpfile = tmpdirname + '/' + filename
    with open(tmpfile, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    topology.add_file_dependency(tmpfile, 'opt')
    return 'opt/'+filename

def _read_db2_credentials(credentials):
    jdbcurl = ""
    username = ""
    password = ""
    if isinstance(credentials, dict):
        username = credentials.get('username')
        password = credentials.get('password')
        jdbcurl = credentials.get('jdbcurl')
    else:
        raise TypeError(credentials)
    return jdbcurl, username, password
    
def run_statement(stream, credentials, schema=None, sql=None, sql_attribute=None, sql_params=None, transaction_size=1, name=None):
    """Runs a SQL statement using DB2 client driver and JDBC database interface.

    The statement is called once for each input tuple received. Result sets that are produced by the statement are emitted as output stream tuples.
    
    Supports two ways to specify the statement:

    * Statement is part of the input stream. You can specify which input stream attribute contains the statement with the ``sql_attribute`` argument. If input stream is of type ``CommonSchema.String``, then you don't need to specify the ``sql_attribute`` argument.
    * Statement is given with the ``sql`` argument. The statement can contain parameter markers that are set with input stream attributes specified by ``sql_params`` argument.

    Example with "insert" statement and values passed with input stream, where the input stream "sample_stream" is of type "sample_schema"::

        import streamsx.database as db
        
        sample_schema = StreamSchema('tuple<rstring A, rstring B>')
        ...
        sql_insert = 'INSERT INTO RUN_SAMPLE (A, B) VALUES (?, ?)'
        inserts = db.run_statement(create_table, credentials, schema=sample_schema, sql=sql_insert, sql_params="A, B")


    Args:
        stream(Stream): Stream of tuples containing the SQL statements or SQL statement parameter values. Supports ``streamsx.topology.schema.StreamSchema`` (schema for a structured stream) or ``CommonSchema.String``  as input.
        credentials(dict): The credentials of the IBM cloud DB2 warehouse service in JSON.
        schema(StreamSchema): Schema for returned stream. Defaults to input stream schema if not set.             
        sql(str): String containing the SQL statement. Use this as alternative option to ``sql_attribute`` parameter.
        sql_attribute(str): Name of the input stream attribute containing the SQL statement. Use this as alternative option to ``sql`` parameter.
        sql_params(str): The values of SQL statement parameters. These values and SQL statement parameter markers are associated in lexicographic order. For example, the first parameter marker in the SQL statement is associated with the first sql_params value.
        transaction_size(int): Size of the bulk to submit to Elasticsearch. The default value is 1.      
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        Output Stream.
    """

    if sql_attribute is None and sql is None:
        if stream.oport.schema == CommonSchema.String:
            sql_attribute = 'string'
        else:
            raise ValueError("Either sql_attribute or sql parameter must be set.")

    if schema is None:
        schema = stream.oport.schema

    jdbcurl, username, password = _read_db2_credentials(credentials)

    _op = _JDBCRun(stream, schema, jdbcUrl=jdbcurl, jdbcUser=username, jdbcPassword=password, transactionSize=transaction_size, name=name)
    if sql_attribute is not None:
        _op.params['statementAttr'] = _op.attribute(stream, sql_attribute)
    else:
        _op.params['statement'] = sql
    if sql_params is not None:
        _op.params['statementParamAttrs'] = sql_params
    _op.params['jdbcClassName'] = 'com.ibm.db2.jcc.DB2Driver'
    _op.params['jdbcDriverLib'] = _add_driver_file(stream.topology)

    return _op.outputs[0]


class _JDBCRun(streamsx.spl.op.Invoke):
    def __init__(self, stream, schema=None, jdbcClassName=None, jdbcDriverLib=None, jdbcUrl=None, batchSize=None, checkConnection=None, commitInterval=None, commitPolicy=None, hasResultSetAttr=None, isolationLevel=None, jdbcPassword=None, jdbcProperties=None, jdbcUser=None, keyStore=None, keyStorePassword=None, reconnectionBound=None, reconnectionInterval=None, reconnectionPolicy=None, sqlFailureAction=None, sqlStatusAttr=None, sslConnection=None, statement=None, statementAttr=None, statementParamAttrs=None, transactionSize=None, trustStore=None, trustStorePassword=None, vmArg=None, name=None):
        topology = stream.topology
        kind="com.ibm.streamsx.jdbc::JDBCRun"
        inputs=stream
        schemas=schema
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if jdbcClassName is not None:
            params['jdbcClassName'] = jdbcClassName
        if jdbcDriverLib is not None:
            params['jdbcDriverLib'] = jdbcDriverLib
        if jdbcUrl is not None:
            params['jdbcUrl'] = jdbcUrl
        if batchSize is not None:
            params['batchSize'] = batchSize
        if checkConnection is not None:
            params['checkConnection'] = checkConnection
        if commitInterval is not None:
            params['commitInterval'] = commitInterval
        if commitPolicy is not None:
            params['commitPolicy'] = commitPolicy
        if hasResultSetAttr is not None:
            params['hasResultSetAttr'] = hasResultSetAttr
        if isolationLevel is not None:
            params['isolationLevel'] = isolationLevel
        if jdbcPassword is not None:
            params['jdbcPassword'] = jdbcPassword
        if jdbcProperties is not None:
            params['jdbcProperties'] = jdbcProperties
        if jdbcUser is not None:
            params['jdbcUser'] = jdbcUser
        if keyStore is not None:
            params['keyStore'] = keyStore
        if keyStorePassword is not None:
            params['keyStorePassword'] = keyStorePassword
        if reconnectionBound is not None:
            params['reconnectionBound'] = reconnectionBound
        if reconnectionInterval is not None:
            params['reconnectionInterval'] = reconnectionInterval
        if reconnectionPolicy is not None:
            params['reconnectionPolicy'] = reconnectionPolicy
        if sqlFailureAction is not None:
            params['sqlFailureAction'] = sqlFailureAction
        if sqlStatusAttr is not None:
            params['sqlStatusAttr'] = sqlStatusAttr
        if sslConnection is not None:
            params['sslConnection'] = sslConnection
        if statement is not None:
            params['statement'] = statement
        if statementAttr is not None:
            params['statementAttr'] = statementAttr
        if statementParamAttrs is not None:
            params['statementParamAttrs'] = statementParamAttrs
        if transactionSize is not None:
            params['transactionSize'] = transactionSize
        if trustStore is not None:
            params['trustStore'] = trustStore
        if trustStorePassword is not None:
            params['trustStorePassword'] = trustStorePassword

        super(_JDBCRun, self).__init__(topology,kind,inputs,schema,params,name)



