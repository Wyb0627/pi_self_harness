# Official SWE-bench Evaluator Feedback

This is hidden evaluator information from the rejected original Pi submission. The resulting repair is feedback-assisted and is not a standard one-submission SWE-bench prediction.

Instance: `astropy__astropy-13579`

## Report

```json
{
    "astropy__astropy-13579": {
        "patch_is_None": false,
        "patch_exists": true,
        "patch_successfully_applied": true,
        "resolved": false,
        "tests_status": {
            "FAIL_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_coupled_world_slicing"
                ]
            },
            "PASS_TO_PASS": {
                "success": [
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_invalid_slices",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_sanitize_slice[item0-4-expected0]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_sanitize_slice[item1-5-expected1]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_sanitize_slice[item2-10-expected2]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_ellipsis",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_pixel_to_world_broadcasting",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_world_to_pixel_broadcasting",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_spectral_slice",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_spectral_range",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_celestial_slice",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_celestial_range",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_celestial_range_rot",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_no_array_shape",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_ellipsis_none_types",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice10-slice20-expected0]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice11-slice21-expected1]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice12-slice22-expected2]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice13-slice23-expected3]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice14-slice24-expected4]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice15-slice25-expected5]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice16-slice26-expected6]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice17-slice27-expected7]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice18-slice28-expected8]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice19-slice29-expected9]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice110-slice210-expected10]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice111-slice211-expected11]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice112-slice212-expected12]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice113-slice213-expected13]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice114-slice214-expected14]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice115-slice215-expected15]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice116-3-3]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice117-3-5]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice118-3-3]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice119-3-5]",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_nested_slicing",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_too_much_slicing",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_1d_sliced_low_level",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_dropped_dimensions",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_dropped_dimensions_4d",
                    "astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_pixel_to_world_values_different_int_types"
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
           ~~~~~~~~~~~~~~~~~~~~~~~~~
  cextern/cfitsio/lib/iraffits.c: In function ‘hputc’:
  cextern/cfitsio/lib/iraffits.c:1909:12: note: length computed here
   1909 |     lval = strlen (value);
        |            ^~~~~~~~~~~~~~
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/iraffits.c:51:
  In function ‘strncpy’,
      inlined from ‘hputc’ at cextern/cfitsio/lib/iraffits.c:1992:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated before terminating nul copying as many bytes from a string as its length [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  cextern/cfitsio/lib/iraffits.c: In function ‘hputc’:
  cextern/cfitsio/lib/iraffits.c:1908:16: note: length computed here
   1908 |     lkeyword = strlen (keyword);
        |                ^~~~~~~~~~~~~~~~
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/iraffits.c:51:
  In function ‘strncpy’,
      inlined from ‘hputc’ at cextern/cfitsio/lib/iraffits.c:2009:2:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated before terminating nul copying as many bytes from a string as its length [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  cextern/cfitsio/lib/iraffits.c: In function ‘hputc’:
  cextern/cfitsio/lib/iraffits.c:1909:12: note: length computed here
   1909 |     lval = strlen (value);
        |            ^~~~~~~~~~~~~~
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/iraffits.c:51:
  In function ‘strncpy’,
      inlined from ‘hputc’ at cextern/cfitsio/lib/iraffits.c:2001:2:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated before terminating nul copying as many bytes from a string as its length [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  cextern/cfitsio/lib/iraffits.c: In function ‘hputc’:
  cextern/cfitsio/lib/iraffits.c:1909:12: note: length computed here
   1909 |     lval = strlen (value);
        |            ^~~~~~~~~~~~~~
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/iraffits.c:51:
  In function ‘strncpy’,
      inlined from ‘hputc’ at cextern/cfitsio/lib/iraffits.c:2020:6:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output may be truncated copying between 0 and 49 bytes from a string of length 49 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘hputs’ at cextern/cfitsio/lib/iraffits.c:1875:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin___strncpy_chk’ specified bound depends on the length of the source argument [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  cextern/cfitsio/lib/iraffits.c: In function ‘hputs’:
  cextern/cfitsio/lib/iraffits.c:1869:13: note: length computed here
   1869 |     lcval = strlen (cval);
        |             ^~~~~~~~~~~~~
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/iraffits.c:51:
  In function ‘strncpy’,
      inlined from ‘iraftofits.isra’ at cextern/cfitsio/lib/iraffits.c:624:11:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output may be truncated copying 80 bytes from a string of length 80 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘iraftofits.isra’ at cextern/cfitsio/lib/iraffits.c:864:10:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output may be truncated copying 80 bytes from a string of length 80 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘iraftofits.isra’ at cextern/cfitsio/lib/iraffits.c:853:13:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output may be truncated copying 80 bytes from a string of length 80 [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/modkey.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/modkey.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/pliocomp.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/pliocomp.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcol.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcol.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolb.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolb.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcold.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcold.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcole.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcole.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoli.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcoli.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolj.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolj.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolk.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolk.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoll.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcoll.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcols.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcols.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolsb.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolsb.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolu.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolu.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolui.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolui.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluj.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcoluj.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluk.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcoluk.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putkey.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putkey.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/quantize.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/quantize.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/region.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/region.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/region.c:988:1: warning: "/*" within comment [-Wcomment]
    988 | /*---------------------------------------------------------------------------*/
        |
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/ricecomp.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/ricecomp.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/scalnull.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/scalnull.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/simplerng.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/simplerng.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/swapproc.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/swapproc.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcssub.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/wcssub.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcsutil.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/wcsutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/zcompress.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/zcompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/zcompress.c: In function ‘uncompress2file’:
  cextern/cfitsio/lib/zcompress.c:347:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    347 |             != (d_stream.total_out - bytes_out)) {
        |             ^~
  cextern/cfitsio/lib/zcompress.c: In function ‘compress2file_from_mem’:
  cextern/cfitsio/lib/zcompress.c:515:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    515 |             != (c_stream.total_out - bytes_out)) {
        |             ^~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/zuncompress.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/zuncompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/zuncompress.c: In function ‘write_buf’:
  cextern/cfitsio/lib/zuncompress.c:581:27: warning: comparison of integer expressions of different signedness: ‘long int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
    581 |       if (bytes_out + cnt > *memsize)
        |                           ^
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/adler32.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/adler32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/crc32.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/crc32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/deflate.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/deflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/infback.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/infback.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inffast.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/inffast.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inflate.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/inflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inftrees.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/inftrees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/trees.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/trees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/uncompr.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/uncompr.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/zutil.c -o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/zutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/io
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/io/fits
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp214j6sdx.build-temp/astropy/io/fits/src/compressionmodule.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/buffers.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/cfileio.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/checksum.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/drvrfile.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/drvrmem.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/drvrnet.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/drvrsmem.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/editcol.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/edithdu.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/eval_f.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/eval_l.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/eval_y.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/fits_hcompress.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/fits_hdecompress.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/fitscore.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcol.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcolb.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcold.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcole.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcoli.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcolj.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcolk.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcoll.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcols.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcolsb.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcolui.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcoluj.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getcoluk.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/getkey.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/group.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/grparser.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/histo.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/imcompress.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/iraffits.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/modkey.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/pliocomp.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcol.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolb.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcold.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcole.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcoli.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolj.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolk.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcoll.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcols.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolsb.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolu.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcolui.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcoluj.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putcoluk.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/putkey.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/quantize.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/region.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/ricecomp.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/scalnull.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/simplerng.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/swapproc.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/wcssub.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/wcsutil.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/zcompress.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/lib/zuncompress.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/adler32.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/crc32.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/deflate.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/infback.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/inffast.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/inflate.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/inftrees.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/trees.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/uncompr.o /tmp/tmp214j6sdx.build-temp/cextern/cfitsio/zlib/zutil.o -o /tmp/tmpqqzbi1dc.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.votable.tablewriter' extension
  creating /tmp/tmp214j6sdx.build-temp/astropy/io/votable
  creating /tmp/tmp214j6sdx.build-temp/astropy/io/votable/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/votable/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/votable/src/tablewriter.c -o /tmp/tmp214j6sdx.build-temp/astropy/io/votable/src/tablewriter.o
  astropy/io/votable/src/tablewriter.c: In function ‘write_tabledata’:
  astropy/io/votable/src/tablewriter.c:270:30: warning: assignment discards ‘const’ qualifier from pointer target type [-Wdiscarded-qualifiers]
    270 |                 if ((str_tmp = PyUnicode_AsUTF8AndSize(str_val, &str_len)) == NULL) {
        |                              ^
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/io/votable
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp214j6sdx.build-temp/astropy/io/votable/src/tablewriter.o -o /tmp/tmpqqzbi1dc.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.ascii.cparser' extension
  creating /tmp/tmp214j6sdx.build-temp/astropy/io/ascii
  creating /tmp/tmp214j6sdx.build-temp/astropy/io/ascii/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/cparser.c -o /tmp/tmp214j6sdx.build-temp/astropy/io/ascii/cparser.o
  In file included from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/io/ascii/cparser.c:698:
  /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/src/tokenizer.c -o /tmp/tmp214j6sdx.build-temp/astropy/io/ascii/src/tokenizer.o
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
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/io/ascii
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp214j6sdx.build-temp/astropy/io/ascii/cparser.o /tmp/tmp214j6sdx.build-temp/astropy/io/ascii/src/tokenizer.o -o /tmp/tmpqqzbi1dc.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.bls._impl' extension
  creating /tmp/tmp214j6sdx.build-temp/astropy/timeseries
  creating /tmp/tmp214j6sdx.build-temp/astropy/timeseries/periodograms
  creating /tmp/tmp214j6sdx.build-temp/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/_impl.c -o /tmp/tmp214j6sdx.build-temp/astropy/timeseries/periodograms/bls/_impl.o
  In file included from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/timeseries/periodograms/bls/_impl.c:698:
  /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/bls.c -o /tmp/tmp214j6sdx.build-temp/astropy/timeseries/periodograms/bls/bls.o
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
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/timeseries
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/timeseries/periodograms
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp214j6sdx.build-temp/astropy/timeseries/periodograms/bls/_impl.o /tmp/tmp214j6sdx.build-temp/astropy/timeseries/periodograms/bls/bls.o -o /tmp/tmpqqzbi1dc.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._stats' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/stats/_stats.c -o /tmp/tmp214j6sdx.build-temp/./astropy/stats/_stats.o
  In file included from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/stats/_stats.c:699:
  /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp214j6sdx.build-temp/./astropy/stats/_stats.o -o /tmp/tmpqqzbi1dc.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._utils' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/io/fits/_utils.c -o /tmp/tmp214j6sdx.build-temp/./astropy/io/fits/_utils.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp214j6sdx.build-temp/./astropy/io/fits/_utils.o -o /tmp/tmpqqzbi1dc.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.lombscargle.implementations.cython_impl' extension
  creating /tmp/tmp214j6sdx.build-temp/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmp214j6sdx.build-temp/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c -o /tmp/tmp214j6sdx.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o
  In file included from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c:698:
  /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp214j6sdx.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o -o /tmp/tmpqqzbi1dc.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.cosmology.flrw.scalar_inv_efuncs' extension
  creating /tmp/tmp214j6sdx.build-temp/astropy/cosmology
  creating /tmp/tmp214j6sdx.build-temp/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/cosmology/flrw/scalar_inv_efuncs.c -o /tmp/tmp214j6sdx.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o
  ./astropy/cosmology/flrw/scalar_inv_efuncs.c: In function ‘__pyx_f_7astropy_9cosmology_4flrw_17scalar_inv_efuncs_nufunc’:
  ./astropy/cosmology/flrw/scalar_inv_efuncs.c:6370:33: warning: comparison of integer expressions of different signedness: ‘unsigned int’ and ‘int’ [-Wsign-compare]
   6370 |   for (__pyx_t_4 = 0; __pyx_t_4 < __pyx_t_3; __pyx_t_4+=1) {
        |                                 ^
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/cosmology
  creating /tmp/tmpqqzbi1dc.build-lib/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp214j6sdx.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o -o /tmp/tmpqqzbi1dc.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.compiler_version' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/_compiler.c -o /tmp/tmp214j6sdx.build-temp/astropy/_compiler.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp214j6sdx.build-temp/astropy/_compiler.o -o /tmp/tmpqqzbi1dc.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so -> astropy/wcs
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so -> astropy/convolution
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so -> astropy/utils
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so -> astropy/time
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -> astropy/utils/xml
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so -> astropy/io/votable
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so -> astropy/io/ascii
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/bls
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/lombscargle/implementations
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so -> astropy/cosmology/flrw
  copying /tmp/tmpqqzbi1dc.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so -> astropy
  Editable install will be performed using a meta path finder.

  Options like `package-data`, `include/exclude-package-data` or
  `packages.find.exclude/include` may have no effect.

  adding '__editable___astropy_0_1_dev3_g0df94ff70_d20260925_finder.py'
  adding '__editable__.astropy-0.1.dev3+g0df94ff70.d20260925.pth'
  creating '/tmp/pip-ephem-wheel-cache-1o_0afpd/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4/tmp273zc9sh/.tmp-dat8iznk/astropy-0.1.dev3+g0df94ff70.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' and adding '/tmp/tmpwrvmvllpastropy-0.1.dev3+g0df94ff70.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' to it
  adding 'astropy-0.1.dev3+g0df94ff70.d20260925.dist-info/LICENSE.rst'
  adding 'astropy-0.1.dev3+g0df94ff70.d20260925.dist-info/METADATA'
  adding 'astropy-0.1.dev3+g0df94ff70.d20260925.dist-info/WHEEL'
  adding 'astropy-0.1.dev3+g0df94ff70.d20260925.dist-info/entry_points.txt'
  adding 'astropy-0.1.dev3+g0df94ff70.d20260925.dist-info/scm_file_list.json'
  adding 'astropy-0.1.dev3+g0df94ff70.d20260925.dist-info/scm_version.json'
  adding 'astropy-0.1.dev3+g0df94ff70.d20260925.dist-info/top_level.txt'
  adding 'astropy-0.1.dev3+g0df94ff70.d20260925.dist-info/RECORD'
  /tmp/pip-build-env-08vlrq3m/overlay/lib/python3.9/site-packages/setuptools/command/editable_wheel.py:348: InformationOnly: Editable installation.
  !!

          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************

  !!
    wheel_obj.write_files(unpacked)
  Building editable for astropy (pyproject.toml): finished with status 'done'
  Created wheel for astropy: filename=astropy-0.1.dev3+g0df94ff70.d20260925-0.editable-cp39-cp39-linux_aarch64.whl size=19024 sha256=2413615161636474ab873b09f537b0aacbee5db0425ef4a7f80892c9082d7b8e
  Stored in directory: /tmp/pip-ephem-wheel-cache-1o_0afpd/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4
Successfully built astropy
Installing collected packages: astropy
  Attempting uninstall: astropy
    Found existing installation: astropy 0.1.dev3+g0df94ff70.d20260925
    Uninstalling astropy-0.1.dev3+g0df94ff70.d20260925:
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fits2bitmap
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitscheck
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsdiff
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsheader
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsinfo
      Removing file or directory /opt/miniconda3/envs/testbed/bin/samp_hub
      Removing file or directory /opt/miniconda3/envs/testbed/bin/showtable
      Removing file or directory /opt/miniconda3/envs/testbed/bin/volint
      Removing file or directory /opt/miniconda3/envs/testbed/bin/wcslint
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable__.astropy-0.1.dev3+g0df94ff70.d20260925.pth
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable___astropy_0_1_dev3_g0df94ff70_d20260925_finder.py
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__pycache__/__editable___astropy_0_1_dev3_g0df94ff70_d20260925_finder.cpython-39.pyc
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astropy-0.1.dev3+g0df94ff70.d20260925.dist-info/
      Successfully uninstalled astropy-0.1.dev3+g0df94ff70.d20260925
  changing mode of /opt/miniconda3/envs/testbed/bin/fits2bitmap to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitscheck to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsdiff to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsheader to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsinfo to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/samp_hub to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/showtable to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/volint to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/wcslint to 755
Successfully installed astropy-0.1.dev3+g0df94ff70.d20260925
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
+ git checkout 0df94ff7097961e92fd7812036a24b145bc13ca8 astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py
Updated 0 paths from 143afe3
+ git apply -v -
Checking patch astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py...
Applied patch astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py cleanly.
+ pytest -rA astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py
============================= test session starts ==============================
platform linux -- Python 3.9.25, pytest-7.4.0, pluggy-1.3.0

Running tests with Astropy version 0.1.dev3+g0df94ff70.d20260925.
Running tests in astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py.

Date: 2026-09-25T03:46:42

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
collected 41 items

astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py ................... [ 46%]
.....................F                                                   [100%]

=================================== FAILURES ===================================
__________________________ test_coupled_world_slicing __________________________

    def test_coupled_world_slicing():
        fits_wcs = WCS(header=COUPLED_WCS_HEADER)
        sl = SlicedLowLevelWCS(fits_wcs, 0)
        world = fits_wcs.pixel_to_world_values(0,0,0)
        out_pix = sl.world_to_pixel_values(world[0], world[1])
    
>       assert np.allclose(out_pix[0], 0)
E       assert False
E        +  where False = <function allclose at 0xf356d7f88db0>(array(1.81818182e+11), 0)
E        +    where <function allclose at 0xf356d7f88db0> = np.allclose

astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py:937: AssertionError
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_invalid_slices
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_sanitize_slice[item0-4-expected0]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_sanitize_slice[item1-5-expected1]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_sanitize_slice[item2-10-expected2]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_ellipsis
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_pixel_to_world_broadcasting
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_world_to_pixel_broadcasting
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_spectral_slice
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_spectral_range
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_celestial_slice
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_celestial_range
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_celestial_range_rot
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_no_array_shape
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_ellipsis_none_types
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice10-slice20-expected0]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice11-slice21-expected1]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice12-slice22-expected2]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice13-slice23-expected3]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice14-slice24-expected4]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice15-slice25-expected5]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice16-slice26-expected6]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice17-slice27-expected7]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice18-slice28-expected8]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice19-slice29-expected9]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice110-slice210-expected10]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice111-slice211-expected11]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice112-slice212-expected12]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice113-slice213-expected13]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice114-slice214-expected14]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice115-slice215-expected15]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice116-3-3]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice117-3-5]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice118-3-3]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_combine_slices[slice119-3-5]
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_nested_slicing
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_too_much_slicing
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_1d_sliced_low_level
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_dropped_dimensions
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_dropped_dimensions_4d
PASSED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_pixel_to_world_values_different_int_types
FAILED astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py::test_coupled_world_slicing
========================= 1 failed, 40 passed in 0.28s =========================
+ git checkout 0df94ff7097961e92fd7812036a24b145bc13ca8 astropy/wcs/wcsapi/wrappers/tests/test_sliced_wcs.py
Updated 1 path from 143afe3

```
