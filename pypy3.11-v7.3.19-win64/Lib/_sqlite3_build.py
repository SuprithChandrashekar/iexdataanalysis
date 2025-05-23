#-*- coding: utf-8 -*-
# pysqlite2/dbapi.py: pysqlite DB-API module
#
# Copyright (C) 2007-2008 Gerhard Häring <gh@ghaering.de>
#
# This file is part of pysqlite.
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#
# Note: This software has been modified for use in PyPy.

import sys, os
from cffi import FFI as _FFI

_ffi = _FFI()

_ffi.cdef("""
#define SQLITE_OK ...
#define SQLITE_ERROR ...
#define SQLITE_INTERNAL ...
#define SQLITE_PERM ...
#define SQLITE_ABORT ...
#define SQLITE_BUSY ...
#define SQLITE_LOCKED ...
#define SQLITE_NOMEM ...
#define SQLITE_READONLY ...
#define SQLITE_INTERRUPT ...
#define SQLITE_IOERR ...
#define SQLITE_CORRUPT ...
#define SQLITE_NOTFOUND ...
#define SQLITE_FULL ...
#define SQLITE_CANTOPEN ...
#define SQLITE_PROTOCOL ...
#define SQLITE_EMPTY ...
#define SQLITE_SCHEMA ...
#define SQLITE_TOOBIG ...
#define SQLITE_CONSTRAINT ...
#define SQLITE_MISMATCH ...
#define SQLITE_MISUSE ...
#define SQLITE_NOLFS ...
#define SQLITE_AUTH ...
#define SQLITE_FORMAT ...
#define SQLITE_RANGE ...
#define SQLITE_NOTADB ...
#define SQLITE_ROW ...
#define SQLITE_DONE ...
#define SQLITE_INTEGER ...
#define SQLITE_FLOAT ...
#define SQLITE_BLOB ...
#define SQLITE_NULL ...
#define SQLITE_TEXT ...
#define SQLITE3_TEXT ...

static void *const SQLITE_TRANSIENT;
#define SQLITE_UTF8 ...

#define SQLITE_DENY ...
#define SQLITE_IGNORE ...

#define SQLITE_ALTER_TABLE ...
#define SQLITE_ANALYZE ...
#define SQLITE_ATTACH ...
#define SQLITE_CREATE_INDEX ...
#define SQLITE_CREATE_TABLE ...
#define SQLITE_CREATE_TEMP_INDEX ...
#define SQLITE_CREATE_TEMP_TABLE ...
#define SQLITE_CREATE_TEMP_TRIGGER ...
#define SQLITE_CREATE_TEMP_VIEW ...
#define SQLITE_CREATE_TRIGGER ...
#define SQLITE_CREATE_VIEW ...
#define SQLITE_CREATE_VTABLE ...
#define SQLITE_DELETE ...
#define SQLITE_DETACH ...
#define SQLITE_DROP_INDEX ...
#define SQLITE_DROP_TABLE ...
#define SQLITE_DROP_TEMP_INDEX ...
#define SQLITE_DROP_TEMP_TABLE ...
#define SQLITE_DROP_TEMP_TRIGGER ...
#define SQLITE_DROP_TEMP_VIEW ...
#define SQLITE_DROP_TRIGGER ...
#define SQLITE_DROP_VIEW ...
#define SQLITE_DROP_VTABLE ...
#define SQLITE_FUNCTION ...
#define SQLITE_INSERT ...
#define SQLITE_NOTICE ...
#define SQLITE_PRAGMA ...
#define SQLITE_READ ...
#define SQLITE_RECURSIVE ...
#define SQLITE_REINDEX ...
#define SQLITE_SAVEPOINT ...
#define SQLITE_SELECT ...
#define SQLITE_TRANSACTION ...
#define SQLITE_UPDATE ...
#define SQLITE_WARNING ...
#define SQLITE_ABORT_ROLLBACK ...
#define SQLITE_BUSY_RECOVERY ...
#define SQLITE_CANTOPEN_FULLPATH ...
#define SQLITE_CANTOPEN_ISDIR ...
#define SQLITE_CANTOPEN_NOTEMPDIR ...
#define SQLITE_CORRUPT_VTAB ...
#define SQLITE_IOERR_ACCESS ...
#define SQLITE_IOERR_BLOCKED ...
#define SQLITE_IOERR_CHECKRESERVEDLOCK ...
#define SQLITE_IOERR_CLOSE ...
#define SQLITE_IOERR_DELETE ...
#define SQLITE_IOERR_DELETE_NOENT ...
#define SQLITE_IOERR_DIR_CLOSE ...
#define SQLITE_IOERR_DIR_FSYNC ...
#define SQLITE_IOERR_FSTAT ...
#define SQLITE_IOERR_FSYNC ...
#define SQLITE_IOERR_LOCK ...
#define SQLITE_IOERR_NOMEM ...
#define SQLITE_IOERR_RDLOCK ...
#define SQLITE_IOERR_READ ...
#define SQLITE_IOERR_SEEK ...
#define SQLITE_IOERR_SHMLOCK ...
#define SQLITE_IOERR_SHMMAP ...
#define SQLITE_IOERR_SHMOPEN ...
#define SQLITE_IOERR_SHMSIZE ...
#define SQLITE_IOERR_SHORT_READ ...
#define SQLITE_IOERR_TRUNCATE ...
#define SQLITE_IOERR_UNLOCK ...
#define SQLITE_IOERR_WRITE ...
#define SQLITE_LOCKED_SHAREDCACHE ...
#define SQLITE_READONLY_CANTLOCK ...
#define SQLITE_READONLY_RECOVERY ...

#define SQLITE_LIMIT_SQL_LENGTH ...
#define SQLITE_LIMIT_LENGTH ...
#define SQLITE_LIMIT_COLUMN ...
#define SQLITE_LIMIT_EXPR_DEPTH ...
#define SQLITE_LIMIT_COMPOUND_SELECT ...
#define SQLITE_LIMIT_VDBE_OP ...
#define SQLITE_LIMIT_FUNCTION_ARG ...
#define SQLITE_LIMIT_ATTACHED ...
#define SQLITE_LIMIT_LIKE_PATTERN_LENGTH ...
#define SQLITE_LIMIT_VARIABLE_NUMBER ...
#define SQLITE_LIMIT_TRIGGER_DEPTH ...

#define SQLITE_SERIALIZE_NOCOPY ...
#define SQLITE_DESERIALIZE_FREEONCLOSE ...
#define SQLITE_DESERIALIZE_RESIZEABLE ...

#define SQLITE_TRACE_STMT ...

static const long SQLITE_OPEN_URI;
static const long SQLITE_OPEN_READWRITE;
static const long SQLITE_OPEN_CREATE;

const char *sqlite3_libversion(void);
int sqlite3_libversion_number(void);

typedef ... sqlite3;
typedef ... sqlite3_stmt;
typedef ... sqlite3_context;
typedef ... sqlite3_value;
typedef long long int sqlite3_int64;
typedef unsigned long long int sqlite3_uint64;

int sqlite3_open(
    const char *filename,   /* Database filename (UTF-8) */
    sqlite3 **ppDb          /* OUT: SQLite db handle */
);

int sqlite3_open_v2(
  const char *filename,   /* Database filename (UTF-8) */
  sqlite3 **ppDb,         /* OUT: SQLite db handle */
  int flags,              /* Flags */
  const char *zVfs        /* Name of VFS module to use */
);

int sqlite3_close(sqlite3 *);

int sqlite3_busy_timeout(sqlite3*, int ms);
int sqlite3_prepare_v2(
    sqlite3 *db,            /* Database handle */
    const char *zSql,       /* SQL statement, UTF-8 encoded */
    int nByte,              /* Maximum length of zSql in bytes. */
    sqlite3_stmt **ppStmt,  /* OUT: Statement handle */
    const char **pzTail     /* OUT: Pointer to unused portion of zSql */
);
int sqlite3_finalize(sqlite3_stmt *pStmt);
int sqlite3_data_count(sqlite3_stmt *pStmt);
int sqlite3_column_count(sqlite3_stmt *pStmt);
const char *sqlite3_column_name(sqlite3_stmt*, int N);
int sqlite3_get_autocommit(sqlite3*);
int sqlite3_reset(sqlite3_stmt *pStmt);
int sqlite3_step(sqlite3_stmt*);
int sqlite3_errcode(sqlite3 *db);
int sqlite3_extended_errcode(sqlite3 *db);
const char *sqlite3_errmsg(sqlite3*);
int sqlite3_changes(sqlite3*);

int sqlite3_bind_blob(sqlite3_stmt*, int, const void*, int n, void(*)(void*));
int sqlite3_bind_double(sqlite3_stmt*, int, double);
int sqlite3_bind_int(sqlite3_stmt*, int, int);
int sqlite3_bind_int64(sqlite3_stmt*, int, sqlite3_int64);
int sqlite3_bind_null(sqlite3_stmt*, int);
int sqlite3_bind_text(sqlite3_stmt*, int, const char*, int n, void(*)(void*));
int sqlite3_bind_text16(sqlite3_stmt*, int, const void*, int, void(*)(void*));
int sqlite3_bind_value(sqlite3_stmt*, int, const sqlite3_value*);
int sqlite3_bind_zeroblob(sqlite3_stmt*, int, int n);

const void *sqlite3_column_blob(sqlite3_stmt*, int iCol);
int sqlite3_column_bytes(sqlite3_stmt*, int iCol);
double sqlite3_column_double(sqlite3_stmt*, int iCol);
int sqlite3_column_int(sqlite3_stmt*, int iCol);
sqlite3_int64 sqlite3_column_int64(sqlite3_stmt*, int iCol);
const unsigned char *sqlite3_column_text(sqlite3_stmt*, int iCol);
const void *sqlite3_column_text16(sqlite3_stmt*, int iCol);
int sqlite3_column_type(sqlite3_stmt*, int iCol);
const char *sqlite3_column_decltype(sqlite3_stmt*,int);

void sqlite3_progress_handler(sqlite3*, int, int(*)(void*), void*);
int sqlite3_trace_v2(
  sqlite3*,
  unsigned uMask,
  int(*xCallback)(unsigned,void*,void*,void*),
  void *pCtx
);
char *sqlite3_expanded_sql(sqlite3_stmt *pStmt);

int sqlite3_create_collation(
    sqlite3*,
    const char *zName,
    int eTextRep,
    void*,
    int(*xCompare)(void*,int,const void*,int,const void*)
);
int sqlite3_set_authorizer(
    sqlite3*,
    int (*xAuth)(void*,int,const char*,const char*,const char*,const char*),
    void *pUserData
);
int sqlite3_create_function(
    sqlite3 *db,
    const char *zFunctionName,
    int nArg,
    int eTextRep,
    void *pApp,
    void (*xFunc)(sqlite3_context*,int,sqlite3_value**),
    void (*xStep)(sqlite3_context*,int,sqlite3_value**),
    void (*xFinal)(sqlite3_context*)
);
void *sqlite3_aggregate_context(sqlite3_context*, int nBytes);

int sqlite3_create_window_function(
    sqlite3 *db,
    const char *zFunctionName,
    int nArg,
    int eTextRep,
    void *pApp,
    void (*xStep)(sqlite3_context*,int,sqlite3_value**),
    void (*xFinal)(sqlite3_context*),
    void (*xValue)(sqlite3_context*),
    void (*xInverse)(sqlite3_context*,int,sqlite3_value**),
    void(*xDestroy)(void*)
);

sqlite3_int64 sqlite3_last_insert_rowid(sqlite3*);
int sqlite3_bind_parameter_count(sqlite3_stmt*);
const char *sqlite3_bind_parameter_name(sqlite3_stmt*, int);
int sqlite3_total_changes(sqlite3*);

int sqlite3_prepare(
    sqlite3 *db,            /* Database handle */
    const char *zSql,       /* SQL statement, UTF-8 encoded */
    int nByte,              /* Maximum length of zSql in bytes. */
    sqlite3_stmt **ppStmt,  /* OUT: Statement handle */
    const char **pzTail     /* OUT: Pointer to unused portion of zSql */
);

void sqlite3_result_blob(sqlite3_context*, const void*, int, void(*)(void*));
void sqlite3_result_double(sqlite3_context*, double);
void sqlite3_result_error(sqlite3_context*, const char*, int);
void sqlite3_result_error16(sqlite3_context*, const void*, int);
void sqlite3_result_error_toobig(sqlite3_context*);
void sqlite3_result_error_nomem(sqlite3_context*);
void sqlite3_result_error_code(sqlite3_context*, int);
void sqlite3_result_int(sqlite3_context*, int);
void sqlite3_result_int64(sqlite3_context*, sqlite3_int64);
void sqlite3_result_null(sqlite3_context*);
void sqlite3_result_text(sqlite3_context*, const char*, int, void(*)(void*));
void sqlite3_result_text16(sqlite3_context*, const void*, int, void(*)(void*));
void sqlite3_result_text16le(sqlite3_context*,const void*, int,void(*)(void*));
void sqlite3_result_text16be(sqlite3_context*,const void*, int,void(*)(void*));
void sqlite3_result_value(sqlite3_context*, sqlite3_value*);
void sqlite3_result_zeroblob(sqlite3_context*, int n);

const void *sqlite3_value_blob(sqlite3_value*);
int sqlite3_value_bytes(sqlite3_value*);
int sqlite3_value_bytes16(sqlite3_value*);
double sqlite3_value_double(sqlite3_value*);
int sqlite3_value_int(sqlite3_value*);
sqlite3_int64 sqlite3_value_int64(sqlite3_value*);
const unsigned char *sqlite3_value_text(sqlite3_value*);
const void *sqlite3_value_text16(sqlite3_value*);
const void *sqlite3_value_text16le(sqlite3_value*);
const void *sqlite3_value_text16be(sqlite3_value*);
int sqlite3_value_type(sqlite3_value*);
int sqlite3_value_numeric_type(sqlite3_value*);

int sqlite3_sleep(int);
const char *sqlite3_errstr(int);
int sqlite3_complete(const char *sql);

int sqlite3_limit(sqlite3*, int, int);

void *sqlite3_malloc(int);
void *sqlite3_malloc64(sqlite3_uint64);
void sqlite3_free(void*);

// APIs for BLOBs

typedef ... sqlite3_blob;
int sqlite3_blob_open(
  sqlite3*,
  const char *zDb,
  const char *zTable,
  const char *zColumn,
  sqlite3_int64 iRow,
  int flags,
  sqlite3_blob **ppBlob
);
int sqlite3_blob_close(sqlite3_blob *);
int sqlite3_blob_bytes(sqlite3_blob *);
int sqlite3_blob_read(sqlite3_blob *, void *Z, int N, int iOffset);
int sqlite3_blob_write(sqlite3_blob *, const void *z, int n, int iOffset);

int sqlite3_threadsafe(void);
void sqlite3_interrupt(sqlite3*);
""")

def _has_load_extension():
    """Only available since 3.3.6"""
    unverified_ffi = _FFI()
    unverified_ffi.cdef("""
    typedef ... sqlite3;
    int sqlite3_enable_load_extension(sqlite3 *db, int onoff);
    """)
    libname = 'sqlite3'
    if sys.platform == 'win32':
        import os
        _libname = os.path.join(os.path.dirname(sys.executable), libname)
        if os.path.exists(_libname + '.dll'):
            libname = _libname
    unverified_lib = unverified_ffi.dlopen(libname)
    return hasattr(unverified_lib, 'sqlite3_enable_load_extension')

def _has_backup():
    """Only available since 3.6.11"""
    unverified_ffi = _FFI()
    unverified_ffi.cdef("""
    typedef ... sqlite3;
    typedef ... sqlite3_backup;
    sqlite3_backup* sqlite3_backup_init(sqlite3 *, const char* , sqlite3 *, const char*);
    """)
    libname = 'sqlite3'
    if sys.platform == 'win32':
        import os
        _libname = os.path.join(os.path.dirname(sys.executable), libname)
        if os.path.exists(_libname + '.dll'):
            libname = _libname
    unverified_lib = unverified_ffi.dlopen(libname)
    return hasattr(unverified_lib, 'sqlite3_backup_init')

def _get_version():
    unverified_ffi = _FFI()
    unverified_ffi.cdef("""
    int sqlite3_libversion_number(void);
    """)
    libname = 'sqlite3'
    if sys.platform == 'win32':
        import os
        _libname = os.path.join(os.path.dirname(sys.executable), libname)
        if os.path.exists(_libname + '.dll'):
            libname = _libname
    unverified_lib = unverified_ffi.dlopen(libname)
    return unverified_lib.sqlite3_libversion_number()


if _has_load_extension():
    _ffi.cdef("int sqlite3_enable_load_extension(sqlite3 *db, int onoff);")
    _ffi.cdef("int sqlite3_load_extension(sqlite3 *db, const char *, "
                                                 "const char *, char **);")
if _has_backup():
    _ffi.cdef("""
typedef ... sqlite3_backup;
sqlite3_backup *sqlite3_backup_init(sqlite3 *, const char*, sqlite3 *, const char*);
int sqlite3_backup_step(sqlite3_backup *p, int nPage);
int sqlite3_backup_finish(sqlite3_backup *p);
int sqlite3_backup_remaining(sqlite3_backup *p);
int sqlite3_backup_pagecount(sqlite3_backup *p);
""")

SQLITE3_VERSION = _get_version()
if SQLITE3_VERSION >= 3008003:
    _ffi.cdef("""
        #define SQLITE_DETERMINISTIC ...
    """)

if SQLITE3_VERSION >= 3007016:
    _ffi.cdef("""
#define SQLITE_CONSTRAINT_CHECK ...
#define SQLITE_CONSTRAINT_COMMITHOOK ...
#define SQLITE_CONSTRAINT_FOREIGNKEY ...
#define SQLITE_CONSTRAINT_FUNCTION ...
#define SQLITE_CONSTRAINT_NOTNULL ...
#define SQLITE_CONSTRAINT_PRIMARYKEY ...
#define SQLITE_CONSTRAINT_TRIGGER ...
#define SQLITE_CONSTRAINT_UNIQUE ...
#define SQLITE_CONSTRAINT_VTAB ...
#define SQLITE_READONLY_ROLLBACK ...
""")

if SQLITE3_VERSION >= 3007017:
    _ffi.cdef("""
#define SQLITE_IOERR_MMAP ...
#define SQLITE_NOTICE_RECOVER_ROLLBACK ...
#define SQLITE_NOTICE_RECOVER_WAL ...
""")

if SQLITE3_VERSION >= 3008000:
    _ffi.cdef("""
#define SQLITE_BUSY_SNAPSHOT ...
#define SQLITE_IOERR_GETTEMPPATH ...
#define SQLITE_WARNING_AUTOINDEX ...
""")

if SQLITE3_VERSION >= 3008001:
    _ffi.cdef("""
#define SQLITE_CANTOPEN_CONVPATH ...
#define SQLITE_IOERR_CONVPATH ...
""")

if SQLITE3_VERSION >= 3008002:
    _ffi.cdef("""
#define SQLITE_CONSTRAINT_ROWID ...
""")

if SQLITE3_VERSION >= 3008003:
    _ffi.cdef("""
#define SQLITE_READONLY_DBMOVED ...
""")

if SQLITE3_VERSION >= 3008007:
    _ffi.cdef("""
#define SQLITE_AUTH_USER ...
#define SQLITE_LIMIT_WORKER_THREADS ...
""")

if SQLITE3_VERSION >= 3009000:
    _ffi.cdef("""
#define SQLITE_IOERR_VNODE ...
""")

if SQLITE3_VERSION >= 3010000:
    _ffi.cdef("""
#define SQLITE_IOERR_AUTH ...
""")

if SQLITE3_VERSION >= 3014001:
    _ffi.cdef("""
#define SQLITE_OK_LOAD_PERMANENTLY ...
""")

if SQLITE3_VERSION >= 3021000:
    _ffi.cdef("""
#define SQLITE_IOERR_BEGIN_ATOMIC ...
#define SQLITE_IOERR_COMMIT_ATOMIC ...
#define SQLITE_IOERR_ROLLBACK_ATOMIC ...
""")

if SQLITE3_VERSION >= 3022000:
    _ffi.cdef("""
#define SQLITE_ERROR_MISSING_COLLSEQ ...
#define SQLITE_ERROR_RETRY ...
#define SQLITE_READONLY_CANTINIT ...
#define SQLITE_READONLY_DIRECTORY ...
""")

if SQLITE3_VERSION >= 3024000:
    _ffi.cdef("""
#define SQLITE_CORRUPT_SEQUENCE ...
#define SQLITE_LOCKED_VTAB ...
""")

if SQLITE3_VERSION >= 3025000:
    _ffi.cdef("""
#define SQLITE_CANTOPEN_DIRTYWAL ...
#define SQLITE_ERROR_SNAPSHOT ...
""")

if SQLITE3_VERSION >= 3031000:
    _ffi.cdef("""
#define SQLITE_CANTOPEN_SYMLINK ...
#define SQLITE_CONSTRAINT_PINNED ...
#define SQLITE_OK_SYMLINK ...
""")

if SQLITE3_VERSION >= 3032000:
    _ffi.cdef("""
#define SQLITE_BUSY_TIMEOUT ...
#define SQLITE_CORRUPT_INDEX ...
#define SQLITE_IOERR_DATA ...
""")

if SQLITE3_VERSION >= 3034000:
    _ffi.cdef("""
#define SQLITE_IOERR_CORRUPTFS ...
""")

if SQLITE3_VERSION >= 3036000:
    _ffi.cdef("""
unsigned char *sqlite3_serialize(
    sqlite3 *db,
    const char *zSchema,
    sqlite3_int64 *piSize,
    unsigned int mFlags
);
int sqlite3_deserialize(
    sqlite3 *db,
    const char *zSchema,
    unsigned char *pData,
    sqlite3_int64 szDb,
    sqlite3_int64 szBuf,
    unsigned mFlags
);
""")


libraries=['sqlite3']
if sys.platform.startswith('freebsd'):
    _localbase = os.environ.get('LOCALBASE', '/usr/local')
    extra_args = dict(
        libraries=libraries,
        include_dirs=[os.path.join(_localbase, 'include')],
        library_dirs=[os.path.join(_localbase, 'lib')]
    )
else:
    extra_args = dict(
        libraries=libraries,
    )

SOURCE = """
#include <sqlite3.h>

#ifndef SQLITE_OPEN_URI
static const long SQLITE_OPEN_URI = 0;
#endif
#ifndef SQLITE_OPEN_READWRITE
static const long SQLITE_OPEN_READWRITE = 0;
#endif
#ifndef SQLITE_OPEN_CREATE
static const long SQLITE_OPEN_CREATE = 0;
#endif
"""

_ffi.set_source("_sqlite3_cffi", SOURCE, **extra_args)


if __name__ == "__main__":
    _ffi.compile()
    if sys.platform == 'win32':
        # copy dlls from externals to the pwd
        # maybe we should link to libraries instead of the dlls
        # to avoid this mess
        import os, glob, shutil
        path_parts = os.environ['PATH'].split(';')
        candidates = [x for x in path_parts if 'externals' in x]

        def copy_from_path(dll):
            for c in candidates:
                files = glob.glob(os.path.join(c, dll + '*.dll'))
                if files:
                    for fname in files:
                        print('copying', fname)
                        shutil.copy(fname, '.')

        if candidates:
            for lib in libraries:
                copy_from_path(lib)
