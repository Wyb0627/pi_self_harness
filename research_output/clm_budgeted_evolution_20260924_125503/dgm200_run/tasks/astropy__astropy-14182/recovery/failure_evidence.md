# Official SWE-bench Evaluator Feedback

This is hidden evaluator information from the rejected original Pi submission. The resulting repair is feedback-assisted and is not a standard one-submission SWE-bench prediction.

Instance: `astropy__astropy-14182`

## Report

```json
{
    "astropy__astropy-14182": {
        "patch_is_None": false,
        "patch_exists": true,
        "patch_successfully_applied": true,
        "resolved": false,
        "tests_status": {
            "FAIL_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows"
                ]
            },
            "PASS_TO_PASS": {
                "success": [
                    "astropy/io/ascii/tests/test_rst.py::test_read_normal",
                    "astropy/io/ascii/tests/test_rst.py::test_read_normal_names",
                    "astropy/io/ascii/tests/test_rst.py::test_read_normal_names_include",
                    "astropy/io/ascii/tests/test_rst.py::test_read_normal_exclude",
                    "astropy/io/ascii/tests/test_rst.py::test_read_unbounded_right_column",
                    "astropy/io/ascii/tests/test_rst.py::test_read_unbounded_right_column_header",
                    "astropy/io/ascii/tests/test_rst.py::test_read_right_indented_table",
                    "astropy/io/ascii/tests/test_rst.py::test_trailing_spaces_in_row_definition",
                    "astropy/io/ascii/tests/test_rst.py::test_write_normal"
                ],
                "failure": []
            },
            "FAIL_TO_FAIL": {
                "success": [],
                "failure": []
            },
            "PASS_TO_FAIL": {
                "success": [],
                "failure": []
            }
        }
    }
}
```

## Test Output Tail

```text
rc, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘iraftofits.isra’ at cextern/cfitsio/lib/iraffits.c:823:10:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output may be truncated copying 80 bytes from a string of length 80 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘iraftofits.isra’ at cextern/cfitsio/lib/iraffits.c:811:9:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output may be truncated copying 80 bytes from a string of length 80 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘iraftofits.isra’ at cextern/cfitsio/lib/iraffits.c:880:11:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output may be truncated copying 80 bytes from a string of length 80 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/modkey.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/modkey.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/modkey.c:8:
  In function ‘strncpy’,
      inlined from ‘ffikls’ at cextern/cfitsio/lib/modkey.c:1282:12:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated copying 2 bytes from a string of length 3 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘ffmkls’ at cextern/cfitsio/lib/modkey.c:783:12:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated copying 2 bytes from a string of length 3 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffpunt’ at cextern/cfitsio/lib/modkey.c:567:9:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output may be truncated copying between 0 and 72 bytes from a string of length 72 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffpunt’ at cextern/cfitsio/lib/modkey.c:562:13:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output may be truncated copying between 0 and 72 bytes from a string of length 72 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/pliocomp.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/pliocomp.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcol.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcol.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/putcol.c: In function ‘ffiter’:
  cextern/cfitsio/lib/putcol.c:1268:101: warning: ‘__builtin___snprintf_chk’ output may be truncated before the last format character [-Wformat-truncation=]
   1268 |                    "TemporaryCol column must have defined datatype and repeat for column %d (ffiter)",
        |                                                                                                     ^
  In file included from /usr/include/stdio.h:894,
                   from cextern/cfitsio/lib/fitsio.h:64,
                   from cextern/cfitsio/lib/fitsio2.h:4,
                   from cextern/cfitsio/lib/putcol.c:11:
  /usr/include/aarch64-linux-gnu/bits/stdio2.h:71:10: note: ‘__builtin___snprintf_chk’ output between 80 and 82 bytes into a destination of size 81
     71 |   return __builtin___snprintf_chk (__s, __n, __USE_FORTIFY_LEVEL - 1,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     72 |                                    __glibc_objsize (__s), __fmt,
        |                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     73 |                                    __va_arg_pack ());
        |                                    ~~~~~~~~~~~~~~~~~
  cextern/cfitsio/lib/putcol.c:1586:83: warning: ‘ (ffiter)’ directive output may be truncated writing 9 bytes into a region of size between 5 and 26 [-Wformat-truncation=]
   1586 |                        "Invalid repeat (%ld) for temporary output column number %d (ffiter)",
        |                                                                                   ^~~~~~~~~
  In file included from /usr/include/stdio.h:894,
                   from cextern/cfitsio/lib/fitsio.h:64,
                   from cextern/cfitsio/lib/fitsio2.h:4,
                   from cextern/cfitsio/lib/putcol.c:11:
  /usr/include/aarch64-linux-gnu/bits/stdio2.h:71:10: note: ‘__builtin___snprintf_chk’ output between 65 and 86 bytes into a destination of size 81
     71 |   return __builtin___snprintf_chk (__s, __n, __USE_FORTIFY_LEVEL - 1,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     72 |                                    __glibc_objsize (__s), __fmt,
        |                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     73 |                                    __va_arg_pack ());
        |                                    ~~~~~~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolb.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolb.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcold.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcold.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcole.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcole.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoli.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcoli.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolj.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolj.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolk.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolk.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoll.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcoll.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcols.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcols.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolsb.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolsb.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolu.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolu.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolui.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolui.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluj.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcoluj.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluk.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcoluk.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putkey.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putkey.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/putkey.c: In function ‘ffprec’:
  cextern/cfitsio/lib/putkey.c:326:19: warning: comparison of integer expressions of different signedness: ‘size_t’ {aka ‘long unsigned int’} and ‘int’ [-Wsign-compare]
    326 |     for (ii=0; ii < keylength; ii++)       /* make sure keyword name is uppercase */
        |                   ^
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/putkey.c:8:
  In function ‘strncpy’,
      inlined from ‘ffpkls’ at cextern/cfitsio/lib/putkey.c:487:12:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated copying 2 bytes from a string of length 3 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/quantize.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/quantize.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/region.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/region.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/region.c:988:1: warning: "/*" within comment [-Wcomment]
    988 | /*---------------------------------------------------------------------------*/
        |
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/ricecomp.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/ricecomp.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/scalnull.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/scalnull.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/simplerng.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/simplerng.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/swapproc.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/swapproc.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcssub.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/wcssub.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/wcssub.c:3:
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:847:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:852:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:858:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:889:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:898:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:907:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:916:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:925:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:934:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:945:9:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 50 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘ffgtwcs’ at cextern/cfitsio/lib/wcssub.c:1040:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output truncated copying 77 bytes from a string of length 80 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcsutil.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/wcsutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/zcompress.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/zcompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/zcompress.c: In function ‘uncompress2file’:
  cextern/cfitsio/lib/zcompress.c:347:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    347 |             != (d_stream.total_out - bytes_out)) {
        |             ^~
  cextern/cfitsio/lib/zcompress.c: In function ‘compress2file_from_mem’:
  cextern/cfitsio/lib/zcompress.c:515:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    515 |             != (c_stream.total_out - bytes_out)) {
        |             ^~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/zuncompress.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/zuncompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/zuncompress.c: In function ‘write_buf’:
  cextern/cfitsio/lib/zuncompress.c:581:27: warning: comparison of integer expressions of different signedness: ‘long int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
    581 |       if (bytes_out + cnt > *memsize)
        |                           ^
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/adler32.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/adler32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/compress.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/compress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/crc32.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/crc32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/deflate.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/deflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/gzclose.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/gzclose.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/gzlib.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/gzlib.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/gzread.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/gzread.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/gzwrite.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/gzwrite.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/infback.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/infback.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inffast.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/inffast.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inflate.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/inflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inftrees.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/inftrees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/trees.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/trees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/uncompr.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/uncompr.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/zutil.c -o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/zutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  creating /tmp/tmp28jffd3_.build-lib/astropy/io
  creating /tmp/tmp28jffd3_.build-lib/astropy/io/fits
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpnmvbu21_.build-temp/astropy/io/fits/src/compressionmodule.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/buffers.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/cfileio.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/checksum.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/drvrfile.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/drvrmem.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/drvrnet.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/drvrsmem.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/editcol.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/edithdu.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/eval_f.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/eval_l.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/eval_y.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/fits_hcompress.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/fits_hdecompress.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/fitscore.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcol.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcolb.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcold.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcole.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcoli.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcolj.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcolk.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcoll.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcols.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcolsb.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcolui.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcoluj.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getcoluk.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/getkey.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/group.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/grparser.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/histo.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/imcompress.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/iraffits.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/modkey.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/pliocomp.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcol.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolb.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcold.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcole.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcoli.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolj.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolk.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcoll.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcols.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolsb.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolu.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcolui.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcoluj.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putcoluk.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/putkey.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/quantize.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/region.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/ricecomp.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/scalnull.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/simplerng.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/swapproc.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/wcssub.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/wcsutil.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/zcompress.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/lib/zuncompress.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/adler32.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/compress.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/crc32.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/deflate.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/gzclose.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/gzlib.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/gzread.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/gzwrite.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/infback.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/inffast.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/inflate.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/inftrees.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/trees.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/uncompr.o /tmp/tmpnmvbu21_.build-temp/cextern/cfitsio/zlib/zutil.o -o /tmp/tmp28jffd3_.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.votable.tablewriter' extension
  creating /tmp/tmpnmvbu21_.build-temp/astropy/io/votable
  creating /tmp/tmpnmvbu21_.build-temp/astropy/io/votable/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/votable/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/votable/src/tablewriter.c -o /tmp/tmpnmvbu21_.build-temp/astropy/io/votable/src/tablewriter.o
  astropy/io/votable/src/tablewriter.c: In function ‘write_tabledata’:
  astropy/io/votable/src/tablewriter.c:270:30: warning: assignment discards ‘const’ qualifier from pointer target type [-Wdiscarded-qualifiers]
    270 |                 if ((str_tmp = PyUnicode_AsUTF8AndSize(str_val, &str_len)) == NULL) {
        |                              ^
  creating /tmp/tmp28jffd3_.build-lib/astropy/io/votable
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpnmvbu21_.build-temp/astropy/io/votable/src/tablewriter.o -o /tmp/tmp28jffd3_.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.ascii.cparser' extension
  creating /tmp/tmpnmvbu21_.build-temp/astropy/io/ascii
  creating /tmp/tmpnmvbu21_.build-temp/astropy/io/ascii/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/cparser.c -o /tmp/tmpnmvbu21_.build-temp/astropy/io/ascii/cparser.o
  In file included from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/io/ascii/cparser.c:698:
  /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/src/tokenizer.c -o /tmp/tmpnmvbu21_.build-temp/astropy/io/ascii/src/tokenizer.o
  astropy/io/ascii/src/tokenizer.c: In function ‘push’:
  astropy/io/ascii/src/tokenizer.c:124:54: warning: comparison of integer expressions of different signedness: ‘long int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
    124 |     if (self->col_ptrs[col] - self->output_cols[col] >=
        |                                                      ^~
  astropy/io/ascii/src/tokenizer.c: In function ‘tokenize’:
  astropy/io/ascii/src/tokenizer.c:424:42: warning: comparison of integer expressions of different signedness: ‘size_t’ {aka ‘long unsigned int’} and ‘int’ [-Wsign-compare]
    424 |                     if (self->source_pos == -1
        |                                          ^~
  astropy/io/ascii/src/tokenizer.c:360:9: warning: enumeration value ‘QUOTED_FIELD_NEWLINE’ not handled in switch [-Wswitch]
    360 |         switch (self->state)
        |         ^~~~~~
  creating /tmp/tmp28jffd3_.build-lib/astropy/io/ascii
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpnmvbu21_.build-temp/astropy/io/ascii/cparser.o /tmp/tmpnmvbu21_.build-temp/astropy/io/ascii/src/tokenizer.o -o /tmp/tmp28jffd3_.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.bls._impl' extension
  creating /tmp/tmpnmvbu21_.build-temp/astropy/timeseries
  creating /tmp/tmpnmvbu21_.build-temp/astropy/timeseries/periodograms
  creating /tmp/tmpnmvbu21_.build-temp/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/_impl.c -o /tmp/tmpnmvbu21_.build-temp/astropy/timeseries/periodograms/bls/_impl.o
  In file included from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/timeseries/periodograms/bls/_impl.c:698:
  /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/bls.c -o /tmp/tmpnmvbu21_.build-temp/astropy/timeseries/periodograms/bls/bls.o
  astropy/timeseries/periodograms/bls/bls.c: In function ‘run_bls’:
  astropy/timeseries/periodograms/bls/bls.c:92: warning: ignoring ‘#pragma omp parallel’ [-Wunknown-pragmas]
     92 | #pragma omp parallel
        |
  astropy/timeseries/periodograms/bls/bls.c:116: warning: ignoring ‘#pragma omp parallel’ [-Wunknown-pragmas]
    116 |     #pragma omp parallel for reduction(+:sum_y), reduction(+:sum_ivar)
        |
  astropy/timeseries/periodograms/bls/bls.c:125: warning: ignoring ‘#pragma omp parallel’ [-Wunknown-pragmas]
    125 |     #pragma omp parallel for
        |
  creating /tmp/tmp28jffd3_.build-lib/astropy/timeseries
  creating /tmp/tmp28jffd3_.build-lib/astropy/timeseries/periodograms
  creating /tmp/tmp28jffd3_.build-lib/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpnmvbu21_.build-temp/astropy/timeseries/periodograms/bls/_impl.o /tmp/tmpnmvbu21_.build-temp/astropy/timeseries/periodograms/bls/bls.o -o /tmp/tmp28jffd3_.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._stats' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/stats/_stats.c -o /tmp/tmpnmvbu21_.build-temp/./astropy/stats/_stats.o
  In file included from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/stats/_stats.c:698:
  /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpnmvbu21_.build-temp/./astropy/stats/_stats.o -o /tmp/tmp28jffd3_.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._utils' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/io/fits/_utils.c -o /tmp/tmpnmvbu21_.build-temp/./astropy/io/fits/_utils.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpnmvbu21_.build-temp/./astropy/io/fits/_utils.o -o /tmp/tmp28jffd3_.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.lombscargle.implementations.cython_impl' extension
  creating /tmp/tmpnmvbu21_.build-temp/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpnmvbu21_.build-temp/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c -o /tmp/tmpnmvbu21_.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o
  In file included from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c:698:
  /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmp28jffd3_.build-lib/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmp28jffd3_.build-lib/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpnmvbu21_.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o -o /tmp/tmp28jffd3_.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.cosmology.flrw.scalar_inv_efuncs' extension
  creating /tmp/tmpnmvbu21_.build-temp/astropy/cosmology
  creating /tmp/tmpnmvbu21_.build-temp/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/cosmology/flrw/scalar_inv_efuncs.c -o /tmp/tmpnmvbu21_.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o
  ./astropy/cosmology/flrw/scalar_inv_efuncs.c: In function ‘__pyx_f_7astropy_9cosmology_4flrw_17scalar_inv_efuncs_nufunc’:
  ./astropy/cosmology/flrw/scalar_inv_efuncs.c:6370:33: warning: comparison of integer expressions of different signedness: ‘unsigned int’ and ‘int’ [-Wsign-compare]
   6370 |   for (__pyx_t_4 = 0; __pyx_t_4 < __pyx_t_3; __pyx_t_4+=1) {
        |                                 ^
  creating /tmp/tmp28jffd3_.build-lib/astropy/cosmology
  creating /tmp/tmp28jffd3_.build-lib/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpnmvbu21_.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o -o /tmp/tmp28jffd3_.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.compiler_version' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/_compiler.c -o /tmp/tmpnmvbu21_.build-temp/astropy/_compiler.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpnmvbu21_.build-temp/astropy/_compiler.o -o /tmp/tmp28jffd3_.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so
  copying /tmp/tmp28jffd3_.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so -> astropy/wcs
  copying /tmp/tmp28jffd3_.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so -> astropy/convolution
  copying /tmp/tmp28jffd3_.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so -> astropy/utils
  copying /tmp/tmp28jffd3_.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmp28jffd3_.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmp28jffd3_.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmp28jffd3_.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so -> astropy/time
  copying /tmp/tmp28jffd3_.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -> astropy/utils/xml
  copying /tmp/tmp28jffd3_.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmp28jffd3_.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so -> astropy/io/votable
  copying /tmp/tmp28jffd3_.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so -> astropy/io/ascii
  copying /tmp/tmp28jffd3_.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/bls
  copying /tmp/tmp28jffd3_.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmp28jffd3_.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmp28jffd3_.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/lombscargle/implementations
  copying /tmp/tmp28jffd3_.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so -> astropy/cosmology/flrw
  copying /tmp/tmp28jffd3_.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so -> astropy
  Editable install will be performed using a meta path finder.

  Options like `package-data`, `include/exclude-package-data` or
  `packages.find.exclude/include` may have no effect.

  adding '__editable___astropy_0_1_dev3_ga5917978b_d20260925_finder.py'
  adding '__editable__.astropy-0.1.dev3+ga5917978b.d20260925.pth'
  creating '/tmp/pip-ephem-wheel-cache-g6mjxyp1/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4/tmpq6df_1f7/.tmp-u7k5tewk/astropy-0.1.dev3+ga5917978b.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' and adding '/tmp/tmpd14fnky3astropy-0.1.dev3+ga5917978b.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' to it
  adding 'astropy-0.1.dev3+ga5917978b.d20260925.dist-info/LICENSE.rst'
  adding 'astropy-0.1.dev3+ga5917978b.d20260925.dist-info/METADATA'
  adding 'astropy-0.1.dev3+ga5917978b.d20260925.dist-info/WHEEL'
  adding 'astropy-0.1.dev3+ga5917978b.d20260925.dist-info/entry_points.txt'
  adding 'astropy-0.1.dev3+ga5917978b.d20260925.dist-info/scm_file_list.json'
  adding 'astropy-0.1.dev3+ga5917978b.d20260925.dist-info/scm_version.json'
  adding 'astropy-0.1.dev3+ga5917978b.d20260925.dist-info/top_level.txt'
  adding 'astropy-0.1.dev3+ga5917978b.d20260925.dist-info/RECORD'
  /tmp/pip-build-env-li5y85zj/overlay/lib/python3.9/site-packages/setuptools/command/editable_wheel.py:348: InformationOnly: Editable installation.
  !!

          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************

  !!
    wheel_obj.write_files(unpacked)
  Building editable for astropy (pyproject.toml): finished with status 'done'
  Created wheel for astropy: filename=astropy-0.1.dev3+ga5917978b.d20260925-0.editable-cp39-cp39-linux_aarch64.whl size=19154 sha256=bb9a0e48cad9f0dd5c839dc3f993bca55dffdb641a11e0f2125d98c8fb2d098f
  Stored in directory: /tmp/pip-ephem-wheel-cache-g6mjxyp1/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4
Successfully built astropy
Installing collected packages: astropy
  Attempting uninstall: astropy
    Found existing installation: astropy 0.1.dev3+ga5917978b.d20260925
    Uninstalling astropy-0.1.dev3+ga5917978b.d20260925:
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fits2bitmap
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitscheck
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsdiff
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsheader
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsinfo
      Removing file or directory /opt/miniconda3/envs/testbed/bin/samp_hub
      Removing file or directory /opt/miniconda3/envs/testbed/bin/showtable
      Removing file or directory /opt/miniconda3/envs/testbed/bin/volint
      Removing file or directory /opt/miniconda3/envs/testbed/bin/wcslint
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable__.astropy-0.1.dev3+ga5917978b.d20260925.pth
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable___astropy_0_1_dev3_ga5917978b_d20260925_finder.py
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__pycache__/__editable___astropy_0_1_dev3_ga5917978b_d20260925_finder.cpython-39.pyc
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astropy-0.1.dev3+ga5917978b.d20260925.dist-info/
      Successfully uninstalled astropy-0.1.dev3+ga5917978b.d20260925
  changing mode of /opt/miniconda3/envs/testbed/bin/fits2bitmap to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitscheck to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsdiff to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsheader to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsinfo to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/samp_hub to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/showtable to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/volint to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/wcslint to 755
Successfully installed astropy-0.1.dev3+ga5917978b.d20260925
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
+ git checkout a5917978be39d13cd90b517e1de4e7a539ffaa48 astropy/io/ascii/tests/test_rst.py
Updated 0 paths from a57acf6
+ git apply -v -
Checking patch astropy/io/ascii/tests/test_rst.py...
Applied patch astropy/io/ascii/tests/test_rst.py cleanly.
+ pytest -rA astropy/io/ascii/tests/test_rst.py
<frozen importlib._bootstrap>:228: RuntimeWarning: numpy.ndarray size changed, may indicate binary incompatibility. Expected 80 from C header, got 96 from PyObject
[1m============================= test session starts ==============================[0m
platform linux -- Python 3.9.25, pytest-7.4.0, pluggy-1.3.0

Running tests with Astropy version 0.1.dev3+ga5917978b.d20260925.
Running tests in astropy/io/ascii/tests/test_rst.py.

Date: 2026-09-25T04:17:30

Platform: Linux-6.8.0-117-generic-aarch64-with-glibc2.35

Executable: /opt/miniconda3/envs/testbed/bin/python

Full Python Version: 
3.9.25 (main, Nov  3 2025, 22:33:42) 
[GCC 11.2.0]

encodings: sys: utf-8, locale: UTF-8, filesystem: utf-8
byteorder: little
float info: dig: 15, mant_dig: 15

Package versions: 
Numpy: 1.25.2
Scipy: not available
Matplotlib: not available
h5py: not available
Pandas: not available
PyERFA: 2.0.0.3
Cython: not available
Scikit-image: not available
asdf: not available
pyarrow: not available

Using Astropy options: remote_data: none.

CI: undefined
ARCH_ON_CI: undefined
IS_CRON: undefined

rootdir: /testbed
configfile: setup.cfg
plugins: mock-3.11.1, openfiles-0.5.0, hypothesis-6.82.6, cov-4.1.0, astropy-0.10.0, astropy-header-0.2.2, xdist-3.3.1, filter-subpackage-0.1.2, remotedata-0.4.0, doctestplus-1.0.0, arraydiff-0.5.0
collected 10 items

astropy/io/ascii/tests/test_rst.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31mF[0m[31m                            [100%][0m

=================================== FAILURES ===================================
[31m[1m__________________________ test_rst_with_header_rows ___________________________[0m

    def test_rst_with_header_rows():
        """Round-trip a table with header_rows specified"""
        lines = [
            "======= ======== ====",
            "   wave response ints",
            "     nm       ct     ",
            "float64  float32 int8",
            "======= ======== ====",
            "  350.0      1.0    1",
            "  950.0      2.0    2",
            "======= ======== ====",
        ]
>       tbl = QTable.read(lines, format="ascii.rst", header_rows=["name", "unit", "dtype"])

[1m[31mastropy/io/ascii/tests/test_rst.py[0m:206: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
[1m[31mastropy/table/connect.py[0m:62: in __call__
    out = self.registry.read(cls, *args, **kwargs)
[1m[31mastropy/io/registry/core.py[0m:219: in read
    data = reader(*args, **kwargs)
[1m[31mastropy/io/ascii/connect.py[0m:19: in io_read
    return read(filename, **kwargs)
[1m[31mastropy/io/ascii/ui.py[0m:425: in read
    reader = get_reader(**new_kwargs)
[1m[31mastropy/io/ascii/ui.py[0m:183: in get_reader
    reader = core._get_reader(Reader, Inputter=Inputter, Outputter=Outputter, **kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

Reader = <class 'astropy.io.ascii.rst.RST'>, Inputter = None, Outputter = None
kwargs = {'fill_values': [('', '0')], 'header_rows': ['name', 'unit', 'dtype']}
FastBasic = <class 'astropy.io.ascii.fastbasic.FastBasic'>
reader_kwargs = {'header_rows': ['name', 'unit', 'dtype']}

    def _get_reader(Reader, Inputter=None, Outputter=None, **kwargs):
        """Initialize a table reader allowing for common customizations.  See ui.get_reader()
        for param docs.  This routine is for internal (package) use only and is useful
        because it depends only on the "core" module.
        """
    
        from .fastbasic import FastBasic
    
        if issubclass(Reader, FastBasic):  # Fast readers handle args separately
            if Inputter is not None:
                kwargs["Inputter"] = Inputter
            return Reader(**kwargs)
    
        # If user explicitly passed a fast reader with enable='force'
        # (e.g. by passing non-default options), raise an error for slow readers
        if "fast_reader" in kwargs:
            if kwargs["fast_reader"]["enable"] == "force":
                raise ParameterError(
                    "fast_reader required with "
                    "{}, but this is not a fast C reader: {}".format(
                        kwargs["fast_reader"], Reader
                    )
                )
            else:
                del kwargs["fast_reader"]  # Otherwise ignore fast_reader parameter
    
        reader_kwargs = {k: v for k, v in kwargs.items() if k not in extra_reader_pars}
>       reader = Reader(**reader_kwargs)
[1m[31mE       TypeError: __init__() got an unexpected keyword argument 'header_rows'[0m

[1m[31mastropy/io/ascii/core.py[0m:1692: TypeError
==================================== PASSES ====================================
[36m[1m=========================== short test summary info ============================[0m
[32mPASSED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_read_normal[0m
[32mPASSED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_read_normal_names[0m
[32mPASSED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_read_normal_names_include[0m
[32mPASSED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_read_normal_exclude[0m
[32mPASSED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_read_unbounded_right_column[0m
[32mPASSED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_read_unbounded_right_column_header[0m
[32mPASSED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_read_right_indented_table[0m
[32mPASSED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_trailing_spaces_in_row_definition[0m
[32mPASSED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_write_normal[0m
[31mFAILED[0m astropy/io/ascii/tests/test_rst.py::[1mtest_rst_with_header_rows[0m - TypeError: __init__() got an unexpected keyword argument 'header_rows'
[31m========================= [31m[1m1 failed[0m, [32m9 passed[0m[31m in 0.03s[0m[31m ==========================[0m
+ git checkout a5917978be39d13cd90b517e1de4e7a539ffaa48 astropy/io/ascii/tests/test_rst.py
Updated 1 path from a57acf6

```
