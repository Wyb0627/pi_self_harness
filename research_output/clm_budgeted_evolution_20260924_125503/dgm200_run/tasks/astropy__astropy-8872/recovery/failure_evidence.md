# Official SWE-bench Evaluator Feedback

This is hidden evaluator information from the rejected original Pi submission. The resulting repair is feedback-assisted and is not a standard one-submission SWE-bench prediction.

Instance: `astropy__astropy-8872`

## Report

```json
{
    "astropy__astropy-8872": {
        "patch_is_None": false,
        "patch_exists": true,
        "patch_successfully_applied": true,
        "resolved": false,
        "tests_status": {
            "FAIL_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_preserve_dtype"
                ]
            },
            "PASS_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_1",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_2",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_3",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_nan_inf",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_unit_property",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_copy",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_subok",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_order",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_ndmin",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_non_quantity_with_unit",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_creation_via_view",
                    "astropy/units/tests/test_quantity.py::TestQuantityCreation::test_rshift_warns",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_addition",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_subtraction",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_multiplication",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_division",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_commutativity",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_power",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_matrix_multiplication",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_unary",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_abs",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_incompatible_units",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_non_number_type",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_dimensionless_operations",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_complicated_operation",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_comparison",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_numeric_converters",
                    "astropy/units/tests/test_quantity.py::TestQuantityOperations::test_array_converters",
                    "astropy/units/tests/test_quantity.py::test_quantity_conversion",
                    "astropy/units/tests/test_quantity.py::test_quantity_value_views",
                    "astropy/units/tests/test_quantity.py::test_quantity_conversion_with_equiv",
                    "astropy/units/tests/test_quantity.py::test_quantity_conversion_equivalency_passed_on",
                    "astropy/units/tests/test_quantity.py::test_self_equivalency",
                    "astropy/units/tests/test_quantity.py::test_si",
                    "astropy/units/tests/test_quantity.py::test_cgs",
                    "astropy/units/tests/test_quantity.py::TestQuantityComparison::test_quantity_equality",
                    "astropy/units/tests/test_quantity.py::TestQuantityComparison::test_quantity_equality_array",
                    "astropy/units/tests/test_quantity.py::TestQuantityComparison::test_quantity_comparison",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_dimensionless_quantity_repr",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_dimensionless_quantity_str",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_dimensionless_quantity_format",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_scalar_quantity_str",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_scalar_quantity_repr",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_array_quantity_str",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_array_quantity_repr",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_scalar_quantity_format",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_uninitialized_unit_format",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_to_string",
                    "astropy/units/tests/test_quantity.py::TestQuantityDisplay::test_repr_latex",
                    "astropy/units/tests/test_quantity.py::test_decompose",
                    "astropy/units/tests/test_quantity.py::test_decompose_regression",
                    "astropy/units/tests/test_quantity.py::test_arrays",
                    "astropy/units/tests/test_quantity.py::test_array_indexing_slicing",
                    "astropy/units/tests/test_quantity.py::test_array_setslice",
                    "astropy/units/tests/test_quantity.py::test_inverse_quantity",
                    "astropy/units/tests/test_quantity.py::test_quantity_mutability",
                    "astropy/units/tests/test_quantity.py::test_quantity_initialized_with_quantity",
                    "astropy/units/tests/test_quantity.py::test_quantity_string_unit",
                    "astropy/units/tests/test_quantity.py::test_quantity_invalid_unit_string",
                    "astropy/units/tests/test_quantity.py::test_implicit_conversion",
                    "astropy/units/tests/test_quantity.py::test_implicit_conversion_autocomplete",
                    "astropy/units/tests/test_quantity.py::test_quantity_iterability",
                    "astropy/units/tests/test_quantity.py::test_copy",
                    "astropy/units/tests/test_quantity.py::test_deepcopy",
                    "astropy/units/tests/test_quantity.py::test_equality_numpy_scalar",
                    "astropy/units/tests/test_quantity.py::test_quantity_pickelability",
                    "astropy/units/tests/test_quantity.py::test_quantity_initialisation_from_string",
                    "astropy/units/tests/test_quantity.py::test_unsupported",
                    "astropy/units/tests/test_quantity.py::test_unit_identity",
                    "astropy/units/tests/test_quantity.py::test_quantity_to_view",
                    "astropy/units/tests/test_quantity.py::test_quantity_tuple_power",
                    "astropy/units/tests/test_quantity.py::test_quantity_fraction_power",
                    "astropy/units/tests/test_quantity.py::test_inherit_docstrings",
                    "astropy/units/tests/test_quantity.py::test_repr_array_of_quantity",
                    "astropy/units/tests/test_quantity.py::TestQuantityMatplotlib::test_plot",
                    "astropy/units/tests/test_quantity.py::test_unit_class_override",
                    "astropy/units/tests/test_quantity.py::TestQuantityMimics::test_mimic_input[QuantityMimic]",
                    "astropy/units/tests/test_quantity.py::TestQuantityMimics::test_mimic_input[QuantityMimic2]",
                    "astropy/units/tests/test_quantity.py::TestQuantityMimics::test_mimic_setting[QuantityMimic]",
                    "astropy/units/tests/test_quantity.py::TestQuantityMimics::test_mimic_setting[QuantityMimic2]"
                ]
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
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘fits_uncompress_table’ at cextern/cfitsio/lib/imcompress.c:8673:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated before terminating nul copying 7 bytes from a string of the same length [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘imcomp_get_compressed_image_par’ at cextern/cfitsio/lib/imcompress.c:5188:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin___strncat_chk’ output may be truncated copying 11 bytes from a string of length 70 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘fits_compress_table’ at cextern/cfitsio/lib/imcompress.c:8533:6:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin_strncat’ output may be truncated copying between 0 and 29 bytes from a string of length 70 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncat’,
      inlined from ‘fits_compress_table’ at cextern/cfitsio/lib/imcompress.c:8406:3:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:138:10: warning: ‘__builtin_strncat’ output may be truncated copying between 0 and 29 bytes from a string of length 70 [-Wstringop-truncation]
    138 |   return __builtin___strncat_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    139 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/iraffits.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/iraffits.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  In file included from /usr/include/string.h:535,
                   from cextern/cfitsio/lib/iraffits.c:51:
  In function ‘strncpy’,
      inlined from ‘iraftofits’ at cextern/cfitsio/lib/iraffits.c:576:11:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated before terminating nul copying 3 bytes from a string of the same length [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘iraftofits’ at cextern/cfitsio/lib/iraffits.c:889:5:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated before terminating nul copying 3 bytes from a string of the same length [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘hputcom’ at cextern/cfitsio/lib/iraffits.c:2088:6:
  /usr/include/aarch64-linux-gnu/bits/string_fortified.h:95:10: warning: ‘__builtin_strncpy’ output truncated before terminating nul copying 2 bytes from a string of the same length [-Wstringop-truncation]
     95 |   return __builtin___strncpy_chk (__dest, __src, __len,
        |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     96 |                                   __glibc_objsize (__dest));
        |                                   ~~~~~~~~~~~~~~~~~~~~~~~~~
  In function ‘strncpy’,
      inlined from ‘hputc’ at cextern/cfitsio/lib/iraffits.c:1930:2:
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/modkey.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/modkey.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/pliocomp.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/pliocomp.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcol.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcol.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolb.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolb.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcold.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcold.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcole.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcole.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoli.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcoli.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolj.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolj.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolk.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolk.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoll.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcoll.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcols.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcols.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolsb.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolsb.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolu.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolu.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolui.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolui.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluj.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcoluj.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluk.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcoluk.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putkey.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putkey.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/quantize.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/quantize.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/region.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/region.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/ricecomp.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/ricecomp.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/scalnull.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/scalnull.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/simplerng.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/simplerng.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/swapproc.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/swapproc.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcssub.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/wcssub.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcsutil.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/wcsutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/adler32.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/adler32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/crc32.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/crc32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/deflate.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/deflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/infback.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/infback.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inffast.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/inffast.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inflate.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/inflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inftrees.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/inftrees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/trees.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/trees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/uncompr.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/uncompr.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/zcompress.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/zcompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/zlib/zcompress.c: In function ‘uncompress2file’:
  cextern/cfitsio/zlib/zcompress.c:345:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    345 |             != (d_stream.total_out - bytes_out)) {
        |             ^~
  cextern/cfitsio/zlib/zcompress.c: In function ‘compress2file_from_mem’:
  cextern/cfitsio/zlib/zcompress.c:513:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    513 |             != (c_stream.total_out - bytes_out)) {
        |             ^~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/zuncompress.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/zuncompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/zlib/zuncompress.c: In function ‘write_buf’:
  cextern/cfitsio/zlib/zuncompress.c:581:27: warning: comparison of integer expressions of different signedness: ‘long int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
    581 |       if (bytes_out + cnt > *memsize)
        |                           ^
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/zutil.c -o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/zutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  creating /tmp/tmpaio3c0e9.build-lib/astropy/io
  creating /tmp/tmpaio3c0e9.build-lib/astropy/io/fits
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpgzmt5mz6.build-temp/astropy/io/fits/src/compressionmodule.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/buffers.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/cfileio.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/checksum.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/drvrfile.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/drvrmem.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/drvrnet.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/drvrsmem.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/editcol.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/edithdu.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/eval_f.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/eval_l.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/eval_y.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/fits_hcompress.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/fits_hdecompress.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/fitscore.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcol.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcolb.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcold.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcole.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcoli.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcolj.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcolk.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcoll.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcols.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcolsb.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcolui.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcoluj.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getcoluk.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/getkey.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/group.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/grparser.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/histo.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/imcompress.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/iraffits.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/modkey.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/pliocomp.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcol.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolb.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcold.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcole.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcoli.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolj.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolk.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcoll.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcols.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolsb.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolu.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcolui.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcoluj.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putcoluk.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/putkey.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/quantize.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/region.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/ricecomp.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/scalnull.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/simplerng.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/swapproc.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/wcssub.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/lib/wcsutil.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/adler32.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/crc32.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/deflate.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/infback.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/inffast.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/inflate.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/inftrees.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/trees.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/uncompr.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/zcompress.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/zuncompress.o /tmp/tmpgzmt5mz6.build-temp/cextern/cfitsio/zlib/zutil.o -o /tmp/tmpaio3c0e9.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.votable.tablewriter' extension
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/io/votable
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/io/votable/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/votable/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/votable/src/tablewriter.c -o /tmp/tmpgzmt5mz6.build-temp/astropy/io/votable/src/tablewriter.o
  astropy/io/votable/src/tablewriter.c: In function ‘write_tabledata’:
  astropy/io/votable/src/tablewriter.c:269:17: warning: ‘PyUnicode_AsUnicode’ is deprecated [-Wdeprecated-declarations]
    269 |                 if ((str_tmp = PyUnicode_AsUnicode(str_val)) == NULL) {
        |                 ^~
  In file included from /opt/miniconda3/envs/testbed/include/python3.9/unicodeobject.h:1026,
                   from /opt/miniconda3/envs/testbed/include/python3.9/Python.h:93,
                   from astropy/io/votable/src/tablewriter.c:12:
  /opt/miniconda3/envs/testbed/include/python3.9/cpython/unicodeobject.h:580:45: note: declared here
    580 | Py_DEPRECATED(3.3) PyAPI_FUNC(Py_UNICODE *) PyUnicode_AsUnicode(
        |                                             ^~~~~~~~~~~~~~~~~~~
  creating /tmp/tmpaio3c0e9.build-lib/astropy/io/votable
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpgzmt5mz6.build-temp/astropy/io/votable/src/tablewriter.o -o /tmp/tmpaio3c0e9.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.ascii.cparser' extension
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/io/ascii
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/io/ascii/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/cparser.c -o /tmp/tmpgzmt5mz6.build-temp/astropy/io/ascii/cparser.o -Wp,-w -Wno-unused-function
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/src/tokenizer.c -o /tmp/tmpgzmt5mz6.build-temp/astropy/io/ascii/src/tokenizer.o -Wp,-w -Wno-unused-function
  creating /tmp/tmpaio3c0e9.build-lib/astropy/io/ascii
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpgzmt5mz6.build-temp/astropy/io/ascii/cparser.o /tmp/tmpgzmt5mz6.build-temp/astropy/io/ascii/src/tokenizer.o -o /tmp/tmpaio3c0e9.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.bls._impl' extension
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/_impl.c -o /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms/bls/_impl.o -Wp,-w -Wno-unused-function
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/bls.c -o /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms/bls/bls.o -Wp,-w -Wno-unused-function
  creating /tmp/tmpaio3c0e9.build-lib/astropy/timeseries
  creating /tmp/tmpaio3c0e9.build-lib/astropy/timeseries/periodograms
  creating /tmp/tmpaio3c0e9.build-lib/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms/bls/_impl.o /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms/bls/bls.o -o /tmp/tmpaio3c0e9.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._stats' extension
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/stats
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/_stats.c -o /tmp/tmpgzmt5mz6.build-temp/astropy/stats/_stats.o -Wp,-w -Wno-unused-function
  creating /tmp/tmpaio3c0e9.build-lib/astropy/stats
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpgzmt5mz6.build-temp/astropy/stats/_stats.o -o /tmp/tmpaio3c0e9.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so
  building 'astropy.cosmology.scalar_inv_efuncs' extension
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/cosmology
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/cosmology/scalar_inv_efuncs.c -o /tmp/tmpgzmt5mz6.build-temp/astropy/cosmology/scalar_inv_efuncs.o -Wp,-w -Wno-unused-function
  creating /tmp/tmpaio3c0e9.build-lib/astropy/cosmology
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpgzmt5mz6.build-temp/astropy/cosmology/scalar_inv_efuncs.o -o /tmp/tmpaio3c0e9.build-lib/astropy/cosmology/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._utils' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/fits/_utils.c -o /tmp/tmpgzmt5mz6.build-temp/astropy/io/fits/_utils.o -Wp,-w -Wno-unused-function
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpgzmt5mz6.build-temp/astropy/io/fits/_utils.o -o /tmp/tmpaio3c0e9.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.lombscargle.implementations.cython_impl' extension
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c -o /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o -Wp,-w -Wno-unused-function
  creating /tmp/tmpaio3c0e9.build-lib/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpaio3c0e9.build-lib/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpgzmt5mz6.build-temp/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o -o /tmp/tmpaio3c0e9.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so
  copying /tmp/tmpaio3c0e9.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so -> astropy
  copying /tmp/tmpaio3c0e9.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so -> astropy/wcs
  copying /tmp/tmpaio3c0e9.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so -> astropy/convolution
  copying /tmp/tmpaio3c0e9.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so -> astropy/utils
  copying /tmp/tmpaio3c0e9.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpaio3c0e9.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpaio3c0e9.build-lib/astropy/modeling/_projections.cpython-39-aarch64-linux-gnu.so -> astropy/modeling
  copying /tmp/tmpaio3c0e9.build-lib/astropy/_erfa/ufunc.cpython-39-aarch64-linux-gnu.so -> astropy/_erfa
  copying /tmp/tmpaio3c0e9.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -> astropy/utils/xml
  copying /tmp/tmpaio3c0e9.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpaio3c0e9.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so -> astropy/io/votable
  copying /tmp/tmpaio3c0e9.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so -> astropy/io/ascii
  copying /tmp/tmpaio3c0e9.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/bls
  copying /tmp/tmpaio3c0e9.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpaio3c0e9.build-lib/astropy/cosmology/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so -> astropy/cosmology
  copying /tmp/tmpaio3c0e9.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpaio3c0e9.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/lombscargle/implementations
  Editable install will be performed using a meta path finder.

  Options like `package-data`, `include/exclude-package-data` or
  `packages.find.exclude/include` may have no effect.

  adding '__editable___astropy_4_0_dev3_finder.py'
  adding '__editable__.astropy-4.0.dev3.pth'
  creating '/tmp/pip-ephem-wheel-cache-mods2fx_/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4/tmpd9yfr1lu/.tmp-2lxp7exh/astropy-4.0.dev3-0.editable-cp39-cp39-linux_aarch64.whl' and adding '/tmp/tmpje7o1anbastropy-4.0.dev3-0.editable-cp39-cp39-linux_aarch64.whl' to it
  adding 'astropy-4.0.dev3.dist-info/LICENSE.rst'
  adding 'astropy-4.0.dev3.dist-info/METADATA'
  adding 'astropy-4.0.dev3.dist-info/WHEEL'
  adding 'astropy-4.0.dev3.dist-info/entry_points.txt'
  adding 'astropy-4.0.dev3.dist-info/top_level.txt'
  adding 'astropy-4.0.dev3.dist-info/RECORD'
  /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/setuptools/command/editable_wheel.py:348: InformationOnly: Editable installation.
  !!

          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************

  !!
    wheel_obj.write_files(unpacked)
  Building editable for astropy (pyproject.toml): finished with status 'done'
  Created wheel for astropy: filename=astropy-4.0.dev3-0.editable-cp39-cp39-linux_aarch64.whl size=5812 sha256=d0a062907ffd32aa7a88045107c84c3b70c04c2386adb7906142db178d622871
  Stored in directory: /tmp/pip-ephem-wheel-cache-mods2fx_/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4
Successfully built astropy
Installing collected packages: astropy
  Attempting uninstall: astropy
    Found existing installation: astropy 4.0.dev3
    Uninstalling astropy-4.0.dev3:
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fits2bitmap
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitscheck
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsdiff
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsheader
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsinfo
      Removing file or directory /opt/miniconda3/envs/testbed/bin/samp_hub
      Removing file or directory /opt/miniconda3/envs/testbed/bin/showtable
      Removing file or directory /opt/miniconda3/envs/testbed/bin/volint
      Removing file or directory /opt/miniconda3/envs/testbed/bin/wcslint
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable__.astropy-4.0.dev3.pth
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable___astropy_4_0_dev3_finder.py
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__pycache__/__editable___astropy_4_0_dev3_finder.cpython-39.pyc
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astropy-4.0.dev3.dist-info/
      Successfully uninstalled astropy-4.0.dev3
  changing mode of /opt/miniconda3/envs/testbed/bin/fits2bitmap to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitscheck to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsdiff to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsheader to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsinfo to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/samp_hub to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/showtable to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/volint to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/wcslint to 755
Successfully installed astropy-4.0.dev3
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
+ git checkout b750a0e6ee76fb6b8a099a4d16ec51977be46bf6 astropy/units/tests/test_quantity.py
Updated 0 paths from 0e9d85d
+ git apply -v -
Checking patch astropy/units/tests/test_quantity.py...
Applied patch astropy/units/tests/test_quantity.py cleanly.
+ pytest -rA astropy/units/tests/test_quantity.py
In /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/mpl-data/stylelib/classic.mplstyle: 'parseString' deprecated - use 'parse_string'
In /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/mpl-data/stylelib/classic.mplstyle: 'resetCache' deprecated - use 'reset_cache'
============================= test session starts ==============================
platform linux -- Python 3.9.25, pytest-7.4.0, pluggy-1.3.0
Matplotlib: 3.9.4
Freetype: 2.6.1

Running tests with Astropy version 4.0.dev3.
Running tests in astropy/units/tests/test_quantity.py.

Date: 2026-10-09T05:46:43

Platform: Linux-6.8.0-117-generic-aarch64-with-glibc2.35

Executable: /opt/miniconda3/envs/testbed/bin/python

Full Python Version: 
3.9.25 (main, Nov  3 2025, 22:33:42) 
[GCC 11.2.0]

encodings: sys: utf-8, locale: UTF-8, filesystem: utf-8
byteorder: little
float info: dig: 15, mant_dig: 15

Numpy: 1.25.2
Scipy: not available
Matplotlib: 3.9.4
h5py: not available
Pandas: not available
Cython: 0.29.34
Scikit-image: not available
astropy_helpers: 3.2.1
Using Astropy options: remote_data: none.

rootdir: /testbed
configfile: setup.cfg
plugins: mock-3.11.1, openfiles-0.5.0, hypothesis-6.82.6, cov-4.1.0, astropy-0.10.0, astropy-header-0.2.2, xdist-3.3.1, filter-subpackage-0.1.2, remotedata-0.4.0, doctestplus-1.0.0, arraydiff-0.5.0, mpl-0.18.0
collected 0 items / 2 errors

==================================== ERRORS ====================================
____________ ERROR collecting astropy/units/tests/test_quantity.py _____________
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: in from_call
    result: Optional[TResult] = func()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:372: in <lambda>
    call = CallInfo.from_call(lambda: list(collector.collect()), "collect")
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pytest_doctestplus/plugin.py:250: in collect
    module = import_path(fspath, root=self.config.rootpath)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/pathlib.py:565: in import_path
    importlib.import_module(module_name)
/opt/miniconda3/envs/testbed/lib/python3.9/importlib/__init__.py:127: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1030: in _gcd_import
    ???
<frozen importlib._bootstrap>:1007: in _find_and_load
    ???
<frozen importlib._bootstrap>:986: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:680: in _load_unlocked
    ???
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/assertion/rewrite.py:178: in exec_module
    exec(co, module.__dict__)
astropy/units/tests/test_quantity.py:27: in <module>
    import matplotlib.pyplot as plt
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/pyplot.py:55: in <module>
    import matplotlib.colorbar
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/colorbar.py:19: in <module>
    from matplotlib import _api, cbook, collections, cm, colors, contour, ticker
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/contour.py:15: in <module>
    from matplotlib.backend_bases import MouseButton
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/backend_bases.py:49: in <module>
    from matplotlib import (
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/text.py:18: in <module>
    from .textpath import TextPath, TextToPath  # noqa # Logically located here
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/textpath.py:12: in <module>
    from matplotlib.mathtext import MathTextParser
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/mathtext.py:22: in <module>
    from matplotlib import _api, _mathtext
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/_mathtext.py:45: in <module>
    ParserElement.enablePackrat()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pyparsing/util.py:472: in _inner
    warnings.warn(
E   pyparsing.warnings.PyparsingDeprecationWarning: 'enablePackrat' deprecated - use 'enable_packrat'
____________ ERROR collecting astropy/units/tests/test_quantity.py _____________
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: in from_call
    result: Optional[TResult] = func()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:372: in <lambda>
    call = CallInfo.from_call(lambda: list(collector.collect()), "collect")
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:531: in collect
    self._inject_setup_module_fixture()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:545: in _inject_setup_module_fixture
    self.obj, ("setUpModule", "setup_module")
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:310: in obj
    self._obj = obj = self._getobj()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:528: in _getobj
    return self._importtestmodule()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:617: in _importtestmodule
    mod = import_path(self.path, mode=importmode, root=self.config.rootpath)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/pathlib.py:565: in import_path
    importlib.import_module(module_name)
/opt/miniconda3/envs/testbed/lib/python3.9/importlib/__init__.py:127: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1030: in _gcd_import
    ???
<frozen importlib._bootstrap>:1007: in _find_and_load
    ???
<frozen importlib._bootstrap>:986: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:680: in _load_unlocked
    ???
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/assertion/rewrite.py:178: in exec_module
    exec(co, module.__dict__)
astropy/units/tests/test_quantity.py:27: in <module>
    import matplotlib.pyplot as plt
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/pyplot.py:55: in <module>
    import matplotlib.colorbar
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/colorbar.py:19: in <module>
    from matplotlib import _api, cbook, collections, cm, colors, contour, ticker
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/contour.py:15: in <module>
    from matplotlib.backend_bases import MouseButton
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/backend_bases.py:49: in <module>
    from matplotlib import (
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/text.py:18: in <module>
    from .textpath import TextPath, TextToPath  # noqa # Logically located here
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/textpath.py:12: in <module>
    from matplotlib.mathtext import MathTextParser
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/mathtext.py:22: in <module>
    from matplotlib import _api, _mathtext
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/matplotlib/_mathtext.py:45: in <module>
    ParserElement.enablePackrat()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pyparsing/util.py:472: in _inner
    warnings.warn(
E   pyparsing.warnings.PyparsingDeprecationWarning: 'enablePackrat' deprecated - use 'enable_packrat'
=========================== short test summary info ============================
ERROR astropy/units/tests/test_quantity.py - pyparsing.warnings.PyparsingDepr...
ERROR astropy/units/tests/test_quantity.py - pyparsing.warnings.PyparsingDepr...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 2 errors in 0.58s ===============================
+ git checkout b750a0e6ee76fb6b8a099a4d16ec51977be46bf6 astropy/units/tests/test_quantity.py
Updated 1 path from 0e9d85d

```
