# Official SWE-bench Evaluator Feedback

This is hidden evaluator information from the rejected original Pi submission. The resulting repair is feedback-assisted and is not a standard one-submission SWE-bench prediction.

Instance: `astropy__astropy-13033`

## Report

```json
{
    "astropy__astropy-13033": {
        "patch_is_None": false,
        "patch_exists": true,
        "patch_successfully_applied": true,
        "resolved": false,
        "tests_status": {
            "FAIL_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/timeseries/tests/test_sampled.py::test_required_columns"
                ]
            },
            "PASS_TO_PASS": {
                "success": [
                    "astropy/timeseries/tests/test_sampled.py::test_empty_initialization",
                    "astropy/timeseries/tests/test_sampled.py::test_empty_initialization_invalid",
                    "astropy/timeseries/tests/test_sampled.py::test_initialize_only_time",
                    "astropy/timeseries/tests/test_sampled.py::test_initialization_with_data",
                    "astropy/timeseries/tests/test_sampled.py::test_initialize_only_data",
                    "astropy/timeseries/tests/test_sampled.py::test_initialization_with_table",
                    "astropy/timeseries/tests/test_sampled.py::test_initialization_missing_time_delta",
                    "astropy/timeseries/tests/test_sampled.py::test_initialization_invalid_time_and_time_start",
                    "astropy/timeseries/tests/test_sampled.py::test_initialization_invalid_time_delta",
                    "astropy/timeseries/tests/test_sampled.py::test_initialization_with_time_in_data",
                    "astropy/timeseries/tests/test_sampled.py::test_initialization_n_samples",
                    "astropy/timeseries/tests/test_sampled.py::test_initialization_length_mismatch",
                    "astropy/timeseries/tests/test_sampled.py::test_initialization_invalid_both_time_and_time_delta",
                    "astropy/timeseries/tests/test_sampled.py::test_fold",
                    "astropy/timeseries/tests/test_sampled.py::test_fold_invalid_options",
                    "astropy/timeseries/tests/test_sampled.py::test_read_time_missing",
                    "astropy/timeseries/tests/test_sampled.py::test_read_time_wrong",
                    "astropy/timeseries/tests/test_sampled.py::test_read",
                    "astropy/timeseries/tests/test_sampled.py::test_periodogram[BoxLeastSquares]",
                    "astropy/timeseries/tests/test_sampled.py::test_periodogram[LombScargle]"
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
n __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/modkey.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/modkey.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/pliocomp.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/pliocomp.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcol.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcol.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolb.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolb.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcold.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcold.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcole.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcole.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoli.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcoli.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolj.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolj.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolk.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolk.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoll.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcoll.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcols.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcols.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolsb.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolsb.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolu.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolu.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolui.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolui.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluj.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcoluj.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluk.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcoluk.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putkey.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putkey.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/putkey.c: In function ‘ffprec’:
  cextern/cfitsio/lib/putkey.c:326:19: warning: comparison of integer expressions of different signedness: ‘size_t’ {aka ‘long unsigned int’} and ‘int’ [-Wsign-compare]
    326 |     for (ii=0; ii < keylength; ii++)       /* make sure keyword name is uppercase */
        |                   ^
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/putkey.c:8:
  In function ‘strncpy’,
      inlined from ‘ffpkls’ at cextern/cfitsio/lib/putkey.c:483:12:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated copying 2 bytes from a string of length 3 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/quantize.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/quantize.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/region.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/region.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/region.c:988:1: warning: "/*" within comment [-Wcomment]
    988 | /*---------------------------------------------------------------------------*/
        |
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/ricecomp.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/ricecomp.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/scalnull.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/scalnull.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/simplerng.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/simplerng.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/swapproc.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/swapproc.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcssub.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/wcssub.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcsutil.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/wcsutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/zcompress.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/zcompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/zcompress.c: In function ‘uncompress2file’:
  cextern/cfitsio/lib/zcompress.c:347:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    347 |             != (d_stream.total_out - bytes_out)) {
        |             ^~
  cextern/cfitsio/lib/zcompress.c: In function ‘compress2file_from_mem’:
  cextern/cfitsio/lib/zcompress.c:515:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    515 |             != (c_stream.total_out - bytes_out)) {
        |             ^~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/zuncompress.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/zuncompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/zuncompress.c: In function ‘write_buf’:
  cextern/cfitsio/lib/zuncompress.c:581:27: warning: comparison of integer expressions of different signedness: ‘long int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
    581 |       if (bytes_out + cnt > *memsize)
        |                           ^
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/adler32.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/adler32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/crc32.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/crc32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/deflate.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/deflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/infback.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/infback.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inffast.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/inffast.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inflate.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/inflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inftrees.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/inftrees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/trees.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/trees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/uncompr.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/uncompr.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/zutil.c -o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/zutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  creating /tmp/tmpyokdlxwh.build-lib/astropy/io
  creating /tmp/tmpyokdlxwh.build-lib/astropy/io/fits
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpy81ssvg4.build-temp/astropy/io/fits/src/compressionmodule.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/buffers.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/cfileio.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/checksum.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/drvrfile.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/drvrmem.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/drvrnet.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/drvrsmem.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/editcol.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/edithdu.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/eval_f.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/eval_l.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/eval_y.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/fits_hcompress.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/fits_hdecompress.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/fitscore.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcol.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcolb.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcold.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcole.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcoli.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcolj.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcolk.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcoll.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcols.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcolsb.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcolui.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcoluj.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getcoluk.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/getkey.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/group.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/grparser.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/histo.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/imcompress.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/iraffits.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/modkey.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/pliocomp.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcol.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolb.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcold.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcole.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcoli.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolj.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolk.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcoll.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcols.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolsb.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolu.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcolui.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcoluj.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putcoluk.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/putkey.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/quantize.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/region.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/ricecomp.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/scalnull.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/simplerng.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/swapproc.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/wcssub.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/wcsutil.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/zcompress.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/lib/zuncompress.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/adler32.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/crc32.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/deflate.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/infback.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/inffast.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/inflate.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/inftrees.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/trees.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/uncompr.o /tmp/tmpy81ssvg4.build-temp/cextern/cfitsio/zlib/zutil.o -o /tmp/tmpyokdlxwh.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.votable.tablewriter' extension
  creating /tmp/tmpy81ssvg4.build-temp/astropy/io/votable
  creating /tmp/tmpy81ssvg4.build-temp/astropy/io/votable/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/votable/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/votable/src/tablewriter.c -o /tmp/tmpy81ssvg4.build-temp/astropy/io/votable/src/tablewriter.o
  astropy/io/votable/src/tablewriter.c: In function ‘write_tabledata’:
  astropy/io/votable/src/tablewriter.c:270:30: warning: assignment discards ‘const’ qualifier from pointer target type [-Wdiscarded-qualifiers]
    270 |                 if ((str_tmp = PyUnicode_AsUTF8AndSize(str_val, &str_len)) == NULL) {
        |                              ^
  creating /tmp/tmpyokdlxwh.build-lib/astropy/io/votable
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpy81ssvg4.build-temp/astropy/io/votable/src/tablewriter.o -o /tmp/tmpyokdlxwh.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.ascii.cparser' extension
  creating /tmp/tmpy81ssvg4.build-temp/astropy/io/ascii
  creating /tmp/tmpy81ssvg4.build-temp/astropy/io/ascii/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/cparser.c -o /tmp/tmpy81ssvg4.build-temp/astropy/io/ascii/cparser.o
  In file included from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/io/ascii/cparser.c:610:
  /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/src/tokenizer.c -o /tmp/tmpy81ssvg4.build-temp/astropy/io/ascii/src/tokenizer.o
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
  creating /tmp/tmpyokdlxwh.build-lib/astropy/io/ascii
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpy81ssvg4.build-temp/astropy/io/ascii/cparser.o /tmp/tmpy81ssvg4.build-temp/astropy/io/ascii/src/tokenizer.o -o /tmp/tmpyokdlxwh.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.bls._impl' extension
  creating /tmp/tmpy81ssvg4.build-temp/astropy/timeseries
  creating /tmp/tmpy81ssvg4.build-temp/astropy/timeseries/periodograms
  creating /tmp/tmpy81ssvg4.build-temp/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/_impl.c -o /tmp/tmpy81ssvg4.build-temp/astropy/timeseries/periodograms/bls/_impl.o
  In file included from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/timeseries/periodograms/bls/_impl.c:610:
  /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/bls.c -o /tmp/tmpy81ssvg4.build-temp/astropy/timeseries/periodograms/bls/bls.o
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
  creating /tmp/tmpyokdlxwh.build-lib/astropy/timeseries
  creating /tmp/tmpyokdlxwh.build-lib/astropy/timeseries/periodograms
  creating /tmp/tmpyokdlxwh.build-lib/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpy81ssvg4.build-temp/astropy/timeseries/periodograms/bls/_impl.o /tmp/tmpy81ssvg4.build-temp/astropy/timeseries/periodograms/bls/bls.o -o /tmp/tmpyokdlxwh.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._stats' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/stats/_stats.c -o /tmp/tmpy81ssvg4.build-temp/./astropy/stats/_stats.o
  In file included from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/stats/_stats.c:611:
  /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpy81ssvg4.build-temp/./astropy/stats/_stats.o -o /tmp/tmpyokdlxwh.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._utils' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/io/fits/_utils.c -o /tmp/tmpy81ssvg4.build-temp/./astropy/io/fits/_utils.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpy81ssvg4.build-temp/./astropy/io/fits/_utils.o -o /tmp/tmpyokdlxwh.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.lombscargle.implementations.cython_impl' extension
  creating /tmp/tmpy81ssvg4.build-temp/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpy81ssvg4.build-temp/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c -o /tmp/tmpy81ssvg4.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o
  In file included from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c:610:
  /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmpyokdlxwh.build-lib/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpyokdlxwh.build-lib/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpy81ssvg4.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o -o /tmp/tmpyokdlxwh.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.cosmology.flrw.scalar_inv_efuncs' extension
  creating /tmp/tmpy81ssvg4.build-temp/astropy/cosmology
  creating /tmp/tmpy81ssvg4.build-temp/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/cosmology/flrw/scalar_inv_efuncs.c -o /tmp/tmpy81ssvg4.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o
  ./astropy/cosmology/flrw/scalar_inv_efuncs.c: In function ‘__pyx_f_7astropy_9cosmology_4flrw_17scalar_inv_efuncs_nufunc’:
  ./astropy/cosmology/flrw/scalar_inv_efuncs.c:6281:33: warning: comparison of integer expressions of different signedness: ‘unsigned int’ and ‘int’ [-Wsign-compare]
   6281 |   for (__pyx_t_4 = 0; __pyx_t_4 < __pyx_t_3; __pyx_t_4+=1) {
        |                                 ^
  creating /tmp/tmpyokdlxwh.build-lib/astropy/cosmology
  creating /tmp/tmpyokdlxwh.build-lib/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpy81ssvg4.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o -o /tmp/tmpyokdlxwh.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.compiler_version' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/_compiler.c -o /tmp/tmpy81ssvg4.build-temp/astropy/_compiler.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpy81ssvg4.build-temp/astropy/_compiler.o -o /tmp/tmpyokdlxwh.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so
  copying /tmp/tmpyokdlxwh.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so -> astropy/wcs
  copying /tmp/tmpyokdlxwh.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so -> astropy/convolution
  copying /tmp/tmpyokdlxwh.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so -> astropy/utils
  copying /tmp/tmpyokdlxwh.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpyokdlxwh.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpyokdlxwh.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpyokdlxwh.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so -> astropy/time
  copying /tmp/tmpyokdlxwh.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -> astropy/utils/xml
  copying /tmp/tmpyokdlxwh.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpyokdlxwh.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so -> astropy/io/votable
  copying /tmp/tmpyokdlxwh.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so -> astropy/io/ascii
  copying /tmp/tmpyokdlxwh.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/bls
  copying /tmp/tmpyokdlxwh.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpyokdlxwh.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpyokdlxwh.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/lombscargle/implementations
  copying /tmp/tmpyokdlxwh.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so -> astropy/cosmology/flrw
  copying /tmp/tmpyokdlxwh.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so -> astropy
  Editable install will be performed using a meta path finder.

  Options like `package-data`, `include/exclude-package-data` or
  `packages.find.exclude/include` may have no effect.

  adding '__editable___astropy_0_1_dev3_g298ccb478_d20260925_finder.py'
  adding '__editable__.astropy-0.1.dev3+g298ccb478.d20260925.pth'
  creating '/tmp/pip-ephem-wheel-cache-hhf_sswp/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4/tmpwxqfwj9h/.tmp-893nfi3v/astropy-0.1.dev3+g298ccb478.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' and adding '/tmp/tmp41qzkov_astropy-0.1.dev3+g298ccb478.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' to it
  adding 'astropy-0.1.dev3+g298ccb478.d20260925.dist-info/LICENSE.rst'
  adding 'astropy-0.1.dev3+g298ccb478.d20260925.dist-info/METADATA'
  adding 'astropy-0.1.dev3+g298ccb478.d20260925.dist-info/WHEEL'
  adding 'astropy-0.1.dev3+g298ccb478.d20260925.dist-info/entry_points.txt'
  adding 'astropy-0.1.dev3+g298ccb478.d20260925.dist-info/scm_file_list.json'
  adding 'astropy-0.1.dev3+g298ccb478.d20260925.dist-info/scm_version.json'
  adding 'astropy-0.1.dev3+g298ccb478.d20260925.dist-info/top_level.txt'
  adding 'astropy-0.1.dev3+g298ccb478.d20260925.dist-info/RECORD'
  /tmp/pip-build-env-hmm8ku3m/overlay/lib/python3.9/site-packages/setuptools/command/editable_wheel.py:348: InformationOnly: Editable installation.
  !!

          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************

  !!
    wheel_obj.write_files(unpacked)
  Building editable for astropy (pyproject.toml): finished with status 'done'
  Created wheel for astropy: filename=astropy-0.1.dev3+g298ccb478.d20260925-0.editable-cp39-cp39-linux_aarch64.whl size=19104 sha256=2c47f24ee467ddccf4a91e5ce65ed096d4ea0be9eaa92209ea11001ee5c0dc79
  Stored in directory: /tmp/pip-ephem-wheel-cache-hhf_sswp/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4
Successfully built astropy
Installing collected packages: astropy
  Attempting uninstall: astropy
    Found existing installation: astropy 0.1.dev3+g298ccb478.d20260925
    Uninstalling astropy-0.1.dev3+g298ccb478.d20260925:
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fits2bitmap
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitscheck
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsdiff
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsheader
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsinfo
      Removing file or directory /opt/miniconda3/envs/testbed/bin/samp_hub
      Removing file or directory /opt/miniconda3/envs/testbed/bin/showtable
      Removing file or directory /opt/miniconda3/envs/testbed/bin/volint
      Removing file or directory /opt/miniconda3/envs/testbed/bin/wcslint
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable__.astropy-0.1.dev3+g298ccb478.d20260925.pth
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable___astropy_0_1_dev3_g298ccb478_d20260925_finder.py
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__pycache__/__editable___astropy_0_1_dev3_g298ccb478_d20260925_finder.cpython-39.pyc
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astropy-0.1.dev3+g298ccb478.d20260925.dist-info/
      Successfully uninstalled astropy-0.1.dev3+g298ccb478.d20260925
  changing mode of /opt/miniconda3/envs/testbed/bin/fits2bitmap to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitscheck to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsdiff to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsheader to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsinfo to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/samp_hub to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/showtable to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/volint to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/wcslint to 755
Successfully installed astropy-0.1.dev3+g298ccb478.d20260925
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
+ git checkout 298ccb478e6bf092953bca67a3d29dc6c35f6752 astropy/timeseries/tests/test_sampled.py
Updated 0 paths from aac5ec5
+ git apply -v -
Checking patch astropy/timeseries/tests/test_sampled.py...
Applied patch astropy/timeseries/tests/test_sampled.py cleanly.
+ pytest -rA astropy/timeseries/tests/test_sampled.py
<frozen importlib._bootstrap>:228: RuntimeWarning: numpy.ndarray size changed, may indicate binary incompatibility. Expected 80 from C header, got 96 from PyObject
============================= test session starts ==============================
platform linux -- Python 3.9.25, pytest-7.4.0, pluggy-1.3.0

Running tests with Astropy version 0.1.dev3+g298ccb478.d20260925.
Running tests in astropy/timeseries/tests/test_sampled.py.

Date: 2026-09-25T01:47:26

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

ARCH_ON_CI: undefined
IS_CRON: undefined

rootdir: /testbed
configfile: setup.cfg
plugins: mock-3.11.1, openfiles-0.5.0, hypothesis-6.82.6, cov-4.1.0, astropy-0.10.0, astropy-header-0.2.2, xdist-3.3.1, filter-subpackage-0.1.2, remotedata-0.4.0, doctestplus-1.0.0, arraydiff-0.5.0
collected 25 items

astropy/timeseries/tests/test_sampled.py ......F.........s...ssF..       [100%]

=================================== FAILURES ===================================
_____________________ test_initialization_with_time_delta ______________________

files = None

    def update_leap_seconds(files=None):
        """If the current ERFA leap second table is out of date, try to update it.
    
        Uses `astropy.utils.iers.LeapSeconds.auto_open` to try to find an
        up-to-date table.  See that routine for the definition of "out of date".
    
        In order to make it safe to call this any time, all exceptions are turned
        into warnings,
    
        Parameters
        ----------
        files : list of path-like, optional
            List of files/URLs to attempt to open.  By default, uses defined by
            `astropy.utils.iers.LeapSeconds.auto_open`, which includes the table
            used by ERFA itself, so if that is up to date, nothing will happen.
    
        Returns
        -------
        n_update : int
            Number of items updated.
    
        """
        try:
            from astropy.utils import iers
    
>           table = iers.LeapSeconds.auto_open(files)

astropy/time/core.py:2824: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'astropy.utils.iers.iers.LeapSeconds'>
files = ['erfa', '/testbed/astropy/utils/iers/data/Leap_Second.dat', 'https://hpiers.obspm.fr/iers/bul/bulc/Leap_Second.dat', 'https://www.ietf.org/timezones/data/leap-seconds.list']

    @classmethod
    def auto_open(cls, files=None):
        """Attempt to get an up-to-date leap-second list.
    
        The routine will try the files in sequence until it finds one
        whose expiration date is "good enough" (see below).  If none
        are good enough, it returns the one with the most recent expiration
        date, warning if that file is expired.
    
        For remote files that are cached already, the cached file is tried
        first before attempting to retrieve it again.
    
        Parameters
        ----------
        files : list of path-like, optional
            List of files/URLs to attempt to open.  By default, uses
            ``cls._auto_open_files``.
    
        Returns
        -------
        leap_seconds : `~astropy.utils.iers.LeapSeconds`
            Up to date leap-second table
    
        Notes
        -----
        Bulletin C is released about 10 days after a possible leap second is
        introduced, i.e., mid-January or mid-July.  Expiration days are thus
        generally at least 150 days after the present.  We look for a file
        that expires more than 180 - `~astropy.utils.iers.Conf.auto_max_age`
        after the present.
        """
        offset = 180 - (30 if conf.auto_max_age is None else conf.auto_max_age)
        good_enough = cls._today() + TimeDelta(offset, format='jd')
    
        if files is None:
            # Basic files to go over (entries in _auto_open_files can be
            # configuration items, which we want to be sure are up to date).
            files = [getattr(conf, f, f) for f in cls._auto_open_files]
    
        # Remove empty entries.
        files = [f for f in files if f]
    
        # Our trials start with normal files and remote ones that are
        # already in cache.  The bools here indicate that the cache
        # should be used.
        trials = [(f, True) for f in files
                  if not urlparse(f).netloc or is_url_in_cache(f)]
        # If we are allowed to download, we try downloading new versions
        # if none of the above worked.
        if conf.auto_download:
            trials += [(f, False) for f in files if urlparse(f).netloc]
    
        self = None
        err_list = []
        # Go through all entries, and return the first one that
        # is not expired, or the most up to date one.
        for f, allow_cache in trials:
            if not allow_cache:
                clear_download_cache(f)
    
            try:
                trial = cls.open(f, cache=True)
            except Exception as exc:
                err_list.append(exc)
                continue
    
            if self is None or trial.expires > self.expires:
                self = trial
                self.meta['data_url'] = str(f)
                if self.expires > good_enough:
                    break
    
        if self is None:
            raise ValueError('none of the files could be read. The '
                             'following errors were raised:\n' + str(err_list))
    
        if self.expires < self._today() and conf.auto_max_age is not None:
>           warn('leap-second file is expired.', IERSStaleWarning)
E           astropy.utils.iers.iers.IERSStaleWarning: leap-second file is expired.

astropy/utils/iers/iers.py:1032: IERSStaleWarning

During handling of the above exception, another exception occurred:

    def test_initialization_with_time_delta():
>       ts = TimeSeries(time_start=datetime(2018, 7, 1, 10, 10, 10),
                        time_delta=TimeDelta(3, format='sec'),
                        data=[[10, 2, 3], [4, 5, 6]], names=['a', 'b'])

astropy/timeseries/tests/test_sampled.py:67: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
astropy/timeseries/sampled.py:122: in __init__
    time = time_start + time_delta
astropy/time/core.py:2208: in __add__
    out._set_scale('tai')
astropy/time/core.py:554: in _set_scale
    _check_leapsec()
astropy/time/core.py:2795: in _check_leapsec
    update_leap_seconds()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

files = None

    def update_leap_seconds(files=None):
        """If the current ERFA leap second table is out of date, try to update it.
    
        Uses `astropy.utils.iers.LeapSeconds.auto_open` to try to find an
        up-to-date table.  See that routine for the definition of "out of date".
    
        In order to make it safe to call this any time, all exceptions are turned
        into warnings,
    
        Parameters
        ----------
        files : list of path-like, optional
            List of files/URLs to attempt to open.  By default, uses defined by
            `astropy.utils.iers.LeapSeconds.auto_open`, which includes the table
            used by ERFA itself, so if that is up to date, nothing will happen.
    
        Returns
        -------
        n_update : int
            Number of items updated.
    
        """
        try:
            from astropy.utils import iers
    
            table = iers.LeapSeconds.auto_open(files)
            return erfa.leap_seconds.update(table)
    
        except Exception as exc:
>           warn("leap-second auto-update failed due to the following "
                 f"exception: {exc!r}", AstropyWarning)
E           astropy.utils.exceptions.AstropyWarning: leap-second auto-update failed due to the following exception: IERSStaleWarning('leap-second file is expired.')

astropy/time/core.py:2828: AstropyWarning
____________________________ test_required_columns _____________________________

    def test_required_columns():
    
        # Test the machinery that makes sure that the required columns are present
    
        ts = TimeSeries(time=INPUT_TIME,
                        data=[[10, 2, 3], [4, 5, 6]],
                        names=['a', 'b'])
    
        # In the examples below, the operation (e.g. remove_column) is actually
        # carried out before the checks are made, so we need to use copy() so that
        # we don't change the main version of the time series.
    
        # Make sure copy works fine
        ts.copy()
    
        with pytest.raises(ValueError) as exc:
            ts.copy().add_column(Column([3, 4, 5], name='c'), index=0)
        assert exc.value.args[0] == ("TimeSeries object is invalid - expected "
                                     "'time' as the first column but found 'c'")
    
        with pytest.raises(ValueError) as exc:
            ts.copy().add_columns([Column([3, 4, 5], name='d'),
                                   Column([3, 4, 5], name='e')], indexes=[0, 1])
        assert exc.value.args[0] == ("TimeSeries object is invalid - expected "
                                     "'time' as the first column but found 'd'")
    
        with pytest.raises(ValueError) as exc:
            ts.copy().keep_columns(['a', 'b'])
        assert exc.value.args[0] == ("TimeSeries object is invalid - expected "
                                     "'time' as the first column but found 'a'")
    
        with pytest.raises(ValueError) as exc:
            ts.copy().remove_column('time')
        assert exc.value.args[0] == ("TimeSeries object is invalid - expected "
                                     "'time' as the first column but found 'a'")
    
        with pytest.raises(ValueError) as exc:
            ts.copy().remove_columns(['time', 'a'])
        assert exc.value.args[0] == ("TimeSeries object is invalid - expected "
                                     "'time' as the first column but found 'b'")
    
        with pytest.raises(ValueError) as exc:
            ts.copy().rename_column('time', 'banana')
        assert exc.value.args[0] == ("TimeSeries object is invalid - expected "
                                     "'time' as the first column but found 'banana'")
    
        # https://github.com/astropy/astropy/issues/13009
        ts_2cols_required = ts.copy()
        ts_2cols_required._required_columns = ['time', 'a']
        with pytest.raises(ValueError) as exc:
            ts_2cols_required.remove_column('a')
>       assert exc.value.args[0] == ("TimeSeries object is invalid - expected "
                                     "['time', 'a'] as the first columns but found ['time', 'b']")
E       assert "TimeSeries o...but found 'b'" == "TimeSeries o...['time', 'b']"
E         - TimeSeries object is invalid - expected ['time', 'a'] as the first columns but found ['time', 'b']
E         ?                                         -      ------                                ---------   -
E         + TimeSeries object is invalid - expected 'time' as the first columns but found 'b'

astropy/timeseries/tests/test_sampled.py:403: AssertionError
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED astropy/timeseries/tests/test_sampled.py::test_empty_initialization
PASSED astropy/timeseries/tests/test_sampled.py::test_empty_initialization_invalid
PASSED astropy/timeseries/tests/test_sampled.py::test_initialize_only_time
PASSED astropy/timeseries/tests/test_sampled.py::test_initialization_with_data
PASSED astropy/timeseries/tests/test_sampled.py::test_initialize_only_data
PASSED astropy/timeseries/tests/test_sampled.py::test_initialization_with_table
PASSED astropy/timeseries/tests/test_sampled.py::test_initialization_missing_time_delta
PASSED astropy/timeseries/tests/test_sampled.py::test_initialization_invalid_time_and_time_start
PASSED astropy/timeseries/tests/test_sampled.py::test_initialization_invalid_time_delta
PASSED astropy/timeseries/tests/test_sampled.py::test_initialization_with_time_in_data
PASSED astropy/timeseries/tests/test_sampled.py::test_initialization_n_samples
PASSED astropy/timeseries/tests/test_sampled.py::test_initialization_length_mismatch
PASSED astropy/timeseries/tests/test_sampled.py::test_initialization_invalid_both_time_and_time_delta
PASSED astropy/timeseries/tests/test_sampled.py::test_fold
PASSED astropy/timeseries/tests/test_sampled.py::test_fold_invalid_options
PASSED astropy/timeseries/tests/test_sampled.py::test_read_time_missing
PASSED astropy/timeseries/tests/test_sampled.py::test_read_time_wrong
PASSED astropy/timeseries/tests/test_sampled.py::test_read
PASSED astropy/timeseries/tests/test_sampled.py::test_periodogram[BoxLeastSquares]
PASSED astropy/timeseries/tests/test_sampled.py::test_periodogram[LombScargle]
SKIPPED [1] astropy/timeseries/tests/test_sampled.py:272: could not import 'pandas': No module named 'pandas'
SKIPPED [2] ../opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pytest_remotedata/plugin.py:85: need --remote-data option to run
FAILED astropy/timeseries/tests/test_sampled.py::test_initialization_with_time_delta
FAILED astropy/timeseries/tests/test_sampled.py::test_required_columns - asse...
=================== 2 failed, 20 passed, 3 skipped in 0.09s ====================
+ git checkout 298ccb478e6bf092953bca67a3d29dc6c35f6752 astropy/timeseries/tests/test_sampled.py
Updated 1 path from aac5ec5

```
