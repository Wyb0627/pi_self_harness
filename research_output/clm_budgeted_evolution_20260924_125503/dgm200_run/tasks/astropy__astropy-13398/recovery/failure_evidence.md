# Official SWE-bench Evaluator Feedback

This is hidden evaluator information from the rejected original Pi submission. The resulting repair is feedback-assisted and is not a standard one-submission SWE-bench prediction.

Instance: `astropy__astropy-13398`

## Report

```json
{
    "astropy__astropy-13398": {
        "patch_is_None": false,
        "patch_exists": true,
        "patch_successfully_applied": true,
        "resolved": false,
        "tests_status": {
            "FAIL_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_itrs_topo_to_altaz_with_refraction",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_itrs_topo_to_hadec_with_refraction",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_itrs_topo",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_itrs_straight_overhead"
                ]
            },
            "PASS_TO_PASS": {
                "success": [
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrs[icoo0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrs[icoo1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrs_dist_diff[gframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrs_dist_diff[gframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_to_altaz",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_to_hadec",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_itrs",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_itrs",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_cirs",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_hadec",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_precessed_geocentric",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_precessed_geocentric_different_obstime",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe2]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe3]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe4]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe2]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe3]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe4]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe2]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe3]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe4]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe2]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe3]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe4]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe2]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe3]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe4]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe2]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe3]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe4]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe2]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe3]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe4]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe2]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe3]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe4]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe0]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe1]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe2]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe3]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe4]",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_self_transform_closeby",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_teme_itrf",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_precessedgeocentric_loopback",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_teme_loopback",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_tete_transforms",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_straight_overhead",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::test_aa_high_precision_nodata",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::TestGetLocationGCRS::test_get_gcrs_posvel",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::TestGetLocationGCRS::test_tete_quick",
                    "astropy/coordinates/tests/test_intermediate_transformations.py::TestGetLocationGCRS::test_cirs_quick"
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
TD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoll.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcoll.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcols.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcols.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolsb.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcolsb.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolu.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcolu.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcolui.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcolui.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluj.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcoluj.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putcoluk.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcoluk.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/putkey.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putkey.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/quantize.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/quantize.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/region.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/region.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/region.c:988:1: warning: "/*" within comment [-Wcomment]
    988 | /*---------------------------------------------------------------------------*/
        |
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/ricecomp.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/ricecomp.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/scalnull.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/scalnull.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/simplerng.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/simplerng.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/swapproc.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/swapproc.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcssub.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/wcssub.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/wcsutil.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/wcsutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/zcompress.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/zcompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/zcompress.c: In function ‘uncompress2file’:
  cextern/cfitsio/lib/zcompress.c:347:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    347 |             != (d_stream.total_out - bytes_out)) {
        |             ^~
  cextern/cfitsio/lib/zcompress.c: In function ‘compress2file_from_mem’:
  cextern/cfitsio/lib/zcompress.c:515:13: warning: comparison of integer expressions of different signedness: ‘int’ and ‘long unsigned int’ [-Wsign-compare]
    515 |             != (c_stream.total_out - bytes_out)) {
        |             ^~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/zuncompress.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/zuncompress.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  cextern/cfitsio/lib/zuncompress.c: In function ‘write_buf’:
  cextern/cfitsio/lib/zuncompress.c:581:27: warning: comparison of integer expressions of different signedness: ‘long int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
    581 |       if (bytes_out + cnt > *memsize)
        |                           ^
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/adler32.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/adler32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/crc32.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/crc32.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/deflate.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/deflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/infback.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/infback.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inffast.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/inffast.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inflate.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/inflate.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/inftrees.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/inftrees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/trees.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/trees.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/uncompr.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/uncompr.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_UNISTD_H -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/cfitsio/lib -Icextern/cfitsio/zlib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/zlib/zutil.c -o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/zutil.o -Wno-declaration-after-statement -Wno-strict-prototypes -Wno-unused -Wno-uninitialized -Wno-unused-result -Wno-misleading-indentation -Wno-format-overflow
  creating /tmp/tmpk2_piuzd.build-lib/astropy/io
  creating /tmp/tmpk2_piuzd.build-lib/astropy/io/fits
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp93_32can.build-temp/astropy/io/fits/src/compressionmodule.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/buffers.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/cfileio.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/checksum.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/drvrfile.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/drvrmem.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/drvrnet.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/drvrsmem.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/editcol.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/edithdu.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/eval_f.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/eval_l.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/eval_y.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/fits_hcompress.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/fits_hdecompress.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/fitscore.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcol.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcolb.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcold.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcole.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcoli.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcolj.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcolk.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcoll.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcols.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcolsb.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcolui.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcoluj.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getcoluk.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/getkey.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/group.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/grparser.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/histo.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/imcompress.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/iraffits.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/modkey.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/pliocomp.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcol.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcolb.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcold.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcole.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcoli.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcolj.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcolk.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcoll.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcols.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcolsb.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcolu.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcolui.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcoluj.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putcoluk.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/putkey.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/quantize.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/region.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/ricecomp.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/scalnull.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/simplerng.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/swapproc.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/wcssub.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/wcsutil.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/zcompress.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/lib/zuncompress.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/adler32.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/crc32.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/deflate.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/infback.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/inffast.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/inflate.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/inftrees.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/trees.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/uncompr.o /tmp/tmp93_32can.build-temp/cextern/cfitsio/zlib/zutil.o -o /tmp/tmpk2_piuzd.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.votable.tablewriter' extension
  creating /tmp/tmp93_32can.build-temp/astropy/io/votable
  creating /tmp/tmp93_32can.build-temp/astropy/io/votable/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/votable/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/votable/src/tablewriter.c -o /tmp/tmp93_32can.build-temp/astropy/io/votable/src/tablewriter.o
  astropy/io/votable/src/tablewriter.c: In function ‘write_tabledata’:
  astropy/io/votable/src/tablewriter.c:270:30: warning: assignment discards ‘const’ qualifier from pointer target type [-Wdiscarded-qualifiers]
    270 |                 if ((str_tmp = PyUnicode_AsUTF8AndSize(str_val, &str_len)) == NULL) {
        |                              ^
  creating /tmp/tmpk2_piuzd.build-lib/astropy/io/votable
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp93_32can.build-temp/astropy/io/votable/src/tablewriter.o -o /tmp/tmpk2_piuzd.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.ascii.cparser' extension
  creating /tmp/tmp93_32can.build-temp/astropy/io/ascii
  creating /tmp/tmp93_32can.build-temp/astropy/io/ascii/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/cparser.c -o /tmp/tmp93_32can.build-temp/astropy/io/ascii/cparser.o
  In file included from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/io/ascii/cparser.c:698:
  /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/src/tokenizer.c -o /tmp/tmp93_32can.build-temp/astropy/io/ascii/src/tokenizer.o
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
  creating /tmp/tmpk2_piuzd.build-lib/astropy/io/ascii
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp93_32can.build-temp/astropy/io/ascii/cparser.o /tmp/tmp93_32can.build-temp/astropy/io/ascii/src/tokenizer.o -o /tmp/tmpk2_piuzd.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.bls._impl' extension
  creating /tmp/tmp93_32can.build-temp/astropy/timeseries
  creating /tmp/tmp93_32can.build-temp/astropy/timeseries/periodograms
  creating /tmp/tmp93_32can.build-temp/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/_impl.c -o /tmp/tmp93_32can.build-temp/astropy/timeseries/periodograms/bls/_impl.o
  In file included from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/timeseries/periodograms/bls/_impl.c:698:
  /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/bls.c -o /tmp/tmp93_32can.build-temp/astropy/timeseries/periodograms/bls/bls.o
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
  creating /tmp/tmpk2_piuzd.build-lib/astropy/timeseries
  creating /tmp/tmpk2_piuzd.build-lib/astropy/timeseries/periodograms
  creating /tmp/tmpk2_piuzd.build-lib/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp93_32can.build-temp/astropy/timeseries/periodograms/bls/_impl.o /tmp/tmp93_32can.build-temp/astropy/timeseries/periodograms/bls/bls.o -o /tmp/tmpk2_piuzd.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._stats' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/stats/_stats.c -o /tmp/tmp93_32can.build-temp/./astropy/stats/_stats.o
  In file included from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/stats/_stats.c:699:
  /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp93_32can.build-temp/./astropy/stats/_stats.o -o /tmp/tmpk2_piuzd.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._utils' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/io/fits/_utils.c -o /tmp/tmp93_32can.build-temp/./astropy/io/fits/_utils.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp93_32can.build-temp/./astropy/io/fits/_utils.o -o /tmp/tmpk2_piuzd.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.lombscargle.implementations.cython_impl' extension
  creating /tmp/tmp93_32can.build-temp/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmp93_32can.build-temp/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c -o /tmp/tmp93_32can.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o
  In file included from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c:698:
  /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmpk2_piuzd.build-lib/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpk2_piuzd.build-lib/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp93_32can.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o -o /tmp/tmpk2_piuzd.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.cosmology.flrw.scalar_inv_efuncs' extension
  creating /tmp/tmp93_32can.build-temp/astropy/cosmology
  creating /tmp/tmp93_32can.build-temp/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/cosmology/flrw/scalar_inv_efuncs.c -o /tmp/tmp93_32can.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o
  ./astropy/cosmology/flrw/scalar_inv_efuncs.c: In function ‘__pyx_f_7astropy_9cosmology_4flrw_17scalar_inv_efuncs_nufunc’:
  ./astropy/cosmology/flrw/scalar_inv_efuncs.c:6370:33: warning: comparison of integer expressions of different signedness: ‘unsigned int’ and ‘int’ [-Wsign-compare]
   6370 |   for (__pyx_t_4 = 0; __pyx_t_4 < __pyx_t_3; __pyx_t_4+=1) {
        |                                 ^
  creating /tmp/tmpk2_piuzd.build-lib/astropy/cosmology
  creating /tmp/tmpk2_piuzd.build-lib/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp93_32can.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o -o /tmp/tmpk2_piuzd.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.compiler_version' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/_compiler.c -o /tmp/tmp93_32can.build-temp/astropy/_compiler.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp93_32can.build-temp/astropy/_compiler.o -o /tmp/tmpk2_piuzd.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so
  copying /tmp/tmpk2_piuzd.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so -> astropy/wcs
  copying /tmp/tmpk2_piuzd.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so -> astropy/convolution
  copying /tmp/tmpk2_piuzd.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so -> astropy/utils
  copying /tmp/tmpk2_piuzd.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpk2_piuzd.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpk2_piuzd.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpk2_piuzd.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so -> astropy/time
  copying /tmp/tmpk2_piuzd.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -> astropy/utils/xml
  copying /tmp/tmpk2_piuzd.build-lib/astropy/io/fits/compression.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpk2_piuzd.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so -> astropy/io/votable
  copying /tmp/tmpk2_piuzd.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so -> astropy/io/ascii
  copying /tmp/tmpk2_piuzd.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/bls
  copying /tmp/tmpk2_piuzd.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpk2_piuzd.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpk2_piuzd.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/lombscargle/implementations
  copying /tmp/tmpk2_piuzd.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so -> astropy/cosmology/flrw
  copying /tmp/tmpk2_piuzd.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so -> astropy
  Editable install will be performed using a meta path finder.

  Options like `package-data`, `include/exclude-package-data` or
  `packages.find.exclude/include` may have no effect.

  adding '__editable___astropy_0_1_dev3_g6500928dc_d20260925_finder.py'
  adding '__editable__.astropy-0.1.dev3+g6500928dc.d20260925.pth'
  creating '/tmp/pip-ephem-wheel-cache-6aje9j09/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4/tmpgrlppjq5/.tmp-ii210v1z/astropy-0.1.dev3+g6500928dc.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' and adding '/tmp/tmpao27zes1astropy-0.1.dev3+g6500928dc.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' to it
  adding 'astropy-0.1.dev3+g6500928dc.d20260925.dist-info/LICENSE.rst'
  adding 'astropy-0.1.dev3+g6500928dc.d20260925.dist-info/METADATA'
  adding 'astropy-0.1.dev3+g6500928dc.d20260925.dist-info/WHEEL'
  adding 'astropy-0.1.dev3+g6500928dc.d20260925.dist-info/entry_points.txt'
  adding 'astropy-0.1.dev3+g6500928dc.d20260925.dist-info/scm_file_list.json'
  adding 'astropy-0.1.dev3+g6500928dc.d20260925.dist-info/scm_version.json'
  adding 'astropy-0.1.dev3+g6500928dc.d20260925.dist-info/top_level.txt'
  adding 'astropy-0.1.dev3+g6500928dc.d20260925.dist-info/RECORD'
  /tmp/pip-build-env-6g1ukco1/overlay/lib/python3.9/site-packages/setuptools/command/editable_wheel.py:348: InformationOnly: Editable installation.
  !!

          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************

  !!
    wheel_obj.write_files(unpacked)
  Building editable for astropy (pyproject.toml): finished with status 'done'
  Created wheel for astropy: filename=astropy-0.1.dev3+g6500928dc.d20260925-0.editable-cp39-cp39-linux_aarch64.whl size=19019 sha256=09e5d740bd2cdddcf4ad99c0b60c98c11bc91e46e98cf6a0b6fd66546dfbe005
  Stored in directory: /tmp/pip-ephem-wheel-cache-6aje9j09/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4
Successfully built astropy
Installing collected packages: astropy
  Attempting uninstall: astropy
    Found existing installation: astropy 0.1.dev3+g6500928dc.d20260925
    Uninstalling astropy-0.1.dev3+g6500928dc.d20260925:
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fits2bitmap
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitscheck
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsdiff
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsheader
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsinfo
      Removing file or directory /opt/miniconda3/envs/testbed/bin/samp_hub
      Removing file or directory /opt/miniconda3/envs/testbed/bin/showtable
      Removing file or directory /opt/miniconda3/envs/testbed/bin/volint
      Removing file or directory /opt/miniconda3/envs/testbed/bin/wcslint
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable__.astropy-0.1.dev3+g6500928dc.d20260925.pth
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable___astropy_0_1_dev3_g6500928dc_d20260925_finder.py
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__pycache__/__editable___astropy_0_1_dev3_g6500928dc_d20260925_finder.cpython-39.pyc
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astropy-0.1.dev3+g6500928dc.d20260925.dist-info/
      Successfully uninstalled astropy-0.1.dev3+g6500928dc.d20260925
  changing mode of /opt/miniconda3/envs/testbed/bin/fits2bitmap to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitscheck to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsdiff to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsheader to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsinfo to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/samp_hub to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/showtable to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/volint to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/wcslint to 755
Successfully installed astropy-0.1.dev3+g6500928dc.d20260925
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
+ git checkout 6500928dc0e57be8f06d1162eacc3ba5e2eff692 astropy/coordinates/tests/test_intermediate_transformations.py
Updated 0 paths from 059e0f8
+ git apply -v -
Checking patch astropy/coordinates/tests/test_intermediate_transformations.py...
Applied patch astropy/coordinates/tests/test_intermediate_transformations.py cleanly.
+ pytest -rA astropy/coordinates/tests/test_intermediate_transformations.py
<frozen importlib._bootstrap>:228: RuntimeWarning: numpy.ndarray size changed, may indicate binary incompatibility. Expected 80 from C header, got 96 from PyObject
============================= test session starts ==============================
platform linux -- Python 3.9.25, pytest-7.4.0, pluggy-1.3.0

Running tests with Astropy version 0.1.dev3+g6500928dc.d20260925.
Running tests in astropy/coordinates/tests/test_intermediate_transformations.py.

Date: 2026-09-25T02:08:34

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
plugins: mock-3.11.1, openfiles-0.5.0, cov-4.1.0, astropy-0.10.0, astropy-header-0.2.2, xdist-3.3.1, filter-subpackage-0.1.2, remotedata-0.4.0, doctestplus-1.0.0, arraydiff-0.5.0, hypothesis-6.46.7
collected 76 items

astropy/coordinates/tests/test_intermediate_transformations.py F......FF [ 11%]
..F......................................................ss..Fs....      [100%]

=================================== FAILURES ===================================
________________________________ test_icrs_cirs ________________________________

    def test_icrs_cirs():
        """
        Check a few cases of ICRS<->CIRS for consistency.
    
        Also includes the CIRS<->CIRS transforms at different times, as those go
        through ICRS
        """
        usph = golden_spiral_grid(200)
        dist = np.linspace(0., 1, len(usph)) * u.pc
        inod = ICRS(usph)
        iwd = ICRS(ra=usph.lon, dec=usph.lat, distance=dist)
    
        cframe1 = CIRS()
>       cirsnod = inod.transform_to(cframe1)  # uses the default time

astropy/coordinates/tests/test_intermediate_transformations.py:49: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
astropy/coordinates/baseframe.py:1202: in transform_to
    return trans(self, new_frame)
astropy/coordinates/transformations.py:1478: in __call__
    curr_coord = t(curr_coord, curr_toframe)
astropy/coordinates/transformations.py:1079: in __call__
    return supcall(fromcoord, toframe)
astropy/coordinates/builtin_frames/icrs_cirs_transforms.py:35: in icrs_to_cirs
    astrom = erfa_astrom.get().apco(cirs_frame)
astropy/coordinates/erfa_astrom.py:50: in apco
    xp, yp = get_polar_motion(obstime)
astropy/coordinates/builtin_frames/utils.py:47: in get_polar_motion
    xp, yp, status = iers_table.pm_xy(time, return_status=True)
astropy/utils/iers/iers.py:365: in pm_xy
    return self._interpolate(jd1, jd2, ['PM_x', 'PM_y'],
astropy/utils/iers/iers.py:392: in _interpolate
    mjd, utc = self.mjd_utc(jd1, jd2)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <IERS_B length=22066>
 year month  day    MJD      PM_x   ... e_UT1_UTC  e_LOD  e_dX_2000A e_dY_2000A
                ...  1.2e-05 6.7e-06    7.5e-05    7.6e-05
 2022     5    31 59730.0  0.149795 ...  1.17e-05 6.7e-06    7.5e-05    7.5e-05
jd1 = <Time object: scale='tt' format='jyear_str' value=J2000.000>, jd2 = 0.0

    def mjd_utc(self, jd1, jd2=0.):
        """Turn a time to MJD, returning integer and fractional parts.
    
        Parameters
        ----------
        jd1 : float, array, or `~astropy.time.Time`
            first part of two-part JD, or Time object
        jd2 : float or array, optional
            second part of two-part JD.
            Default is 0., ignored if jd1 is `~astropy.time.Time`.
    
        Returns
        -------
        mjd : float or array
            integer part of MJD
        utc : float or array
            fractional part of MJD
        """
        try:  # see if this is a Time object
            jd1, jd2 = jd1.utc.jd1, jd1.utc.jd2
        except Exception:
            pass
    
>       mjd = np.floor(jd1 - MJD_ZERO + jd2)
E       TypeError: unsupported operand type(s) for -: 'Time' and 'float'

astropy/utils/iers/iers.py:271: TypeError
___________________ test_itrs_topo_to_altaz_with_refraction ____________________

    def test_itrs_topo_to_altaz_with_refraction():
    
        loc = EarthLocation(lat=0*u.deg, lon=0*u.deg, height=0*u.m)
        usph = golden_spiral_grid(200)
        dist = np.linspace(1., 1000.0, len(usph)) * u.au
        icrs = ICRS(ra=usph.lon, dec=usph.lat, distance=dist)
        altaz_frame1 = AltAz(obstime = 'J2000', location=loc)
        altaz_frame2 = AltAz(obstime = 'J2000', location=loc, pressure=1000.0 * u.hPa,
                             relative_humidity=0.5)
        cirs_frame = CIRS(obstime = 'J2000', location=loc)
>       itrs_frame = ITRS(location=loc)

astropy/coordinates/tests/test_intermediate_transformations.py:207: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <ITRS Frame (obstime=J2000.000)>, copy = True, representation_type = None
differential_type = None, args = ()
kwargs = {'location': <EarthLocation (6378137., 0., 0.) m>}, values = {}
fnm = 'obstime'
fdefault = <Time object: scale='tt' format='jyear_str' value=J2000.000>

    def __init__(self, *args, copy=True, representation_type=None,
                 differential_type=None, **kwargs):
        self._attr_names_with_defaults = []
    
        self._representation = self._infer_representation(representation_type, differential_type)
        self._data = self._infer_data(args, copy, kwargs)  # possibly None.
    
        # Set frame attributes, if any
    
        values = {}
        for fnm, fdefault in self.get_frame_attr_names().items():
            # Read-only frame attributes are defined as FrameAttribute
            # descriptors which are not settable, so set 'real' attributes as
            # the name prefaced with an underscore.
    
            if fnm in kwargs:
                value = kwargs.pop(fnm)
                setattr(self, '_' + fnm, value)
                # Validate attribute by getting it. If the instance has data,
                # this also checks its shape is OK. If not, we do it below.
                values[fnm] = getattr(self, fnm)
            else:
                setattr(self, '_' + fnm, fdefault)
                self._attr_names_with_defaults.append(fnm)
    
        if kwargs:
>           raise TypeError(
                f'Coordinate frame {self.__class__.__name__} got unexpected '
                f'keywords: {list(kwargs)}')
E           TypeError: Coordinate frame ITRS got unexpected keywords: ['location']

astropy/coordinates/baseframe.py:319: TypeError
___________________ test_itrs_topo_to_hadec_with_refraction ____________________

    def test_itrs_topo_to_hadec_with_refraction():
    
        loc = EarthLocation(lat=0*u.deg, lon=0*u.deg, height=0*u.m)
        usph = golden_spiral_grid(200)
        dist = np.linspace(1., 1000.0, len(usph)) * u.au
        icrs = ICRS(ra=usph.lon, dec=usph.lat, distance=dist)
        hadec_frame1 = HADec(obstime = 'J2000', location=loc)
        hadec_frame2 = HADec(obstime = 'J2000', location=loc, pressure=1000.0 * u.hPa,
                             relative_humidity=0.5)
        cirs_frame = CIRS(obstime = 'J2000', location=loc)
>       itrs_frame = ITRS(location=loc)

astropy/coordinates/tests/test_intermediate_transformations.py:262: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <ITRS Frame (obstime=J2000.000)>, copy = True, representation_type = None
differential_type = None, args = ()
kwargs = {'location': <EarthLocation (6378137., 0., 0.) m>}, values = {}
fnm = 'obstime'
fdefault = <Time object: scale='tt' format='jyear_str' value=J2000.000>

    def __init__(self, *args, copy=True, representation_type=None,
                 differential_type=None, **kwargs):
        self._attr_names_with_defaults = []
    
        self._representation = self._infer_representation(representation_type, differential_type)
        self._data = self._infer_data(args, copy, kwargs)  # possibly None.
    
        # Set frame attributes, if any
    
        values = {}
        for fnm, fdefault in self.get_frame_attr_names().items():
            # Read-only frame attributes are defined as FrameAttribute
            # descriptors which are not settable, so set 'real' attributes as
            # the name prefaced with an underscore.
    
            if fnm in kwargs:
                value = kwargs.pop(fnm)
                setattr(self, '_' + fnm, value)
                # Validate attribute by getting it. If the instance has data,
                # this also checks its shape is OK. If not, we do it below.
                values[fnm] = getattr(self, fnm)
            else:
                setattr(self, '_' + fnm, fdefault)
                self._attr_names_with_defaults.append(fnm)
    
        if kwargs:
>           raise TypeError(
                f'Coordinate frame {self.__class__.__name__} got unexpected '
                f'keywords: {list(kwargs)}')
E           TypeError: Coordinate frame ITRS got unexpected keywords: ['location']

astropy/coordinates/baseframe.py:319: TypeError
_____________________________ test_cirs_itrs_topo ______________________________

    def test_cirs_itrs_topo():
        """
        Check basic CIRS<->ITRS topocentric transforms for round-tripping.
        """
        loc = EarthLocation(lat=0*u.deg, lon=0*u.deg, height=0*u.m)
        usph = golden_spiral_grid(200)
        cirs = CIRS(usph, obstime='J2000', location=loc)
        cirs6 = CIRS(usph, obstime='J2006', location=loc)
    
>       cirs2 = cirs.transform_to(ITRS(location=loc)).transform_to(cirs)

astropy/coordinates/tests/test_intermediate_transformations.py:359: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <ITRS Frame (obstime=J2000.000)>, copy = True, representation_type = None
differential_type = None, args = ()
kwargs = {'location': <EarthLocation (6378137., 0., 0.) m>}, values = {}
fnm = 'obstime'
fdefault = <Time object: scale='tt' format='jyear_str' value=J2000.000>

    def __init__(self, *args, copy=True, representation_type=None,
                 differential_type=None, **kwargs):
        self._attr_names_with_defaults = []
    
        self._representation = self._infer_representation(representation_type, differential_type)
        self._data = self._infer_data(args, copy, kwargs)  # possibly None.
    
        # Set frame attributes, if any
    
        values = {}
        for fnm, fdefault in self.get_frame_attr_names().items():
            # Read-only frame attributes are defined as FrameAttribute
            # descriptors which are not settable, so set 'real' attributes as
            # the name prefaced with an underscore.
    
            if fnm in kwargs:
                value = kwargs.pop(fnm)
                setattr(self, '_' + fnm, value)
                # Validate attribute by getting it. If the instance has data,
                # this also checks its shape is OK. If not, we do it below.
                values[fnm] = getattr(self, fnm)
            else:
                setattr(self, '_' + fnm, fdefault)
                self._attr_names_with_defaults.append(fnm)
    
        if kwargs:
>           raise TypeError(
                f'Coordinate frame {self.__class__.__name__} got unexpected '
                f'keywords: {list(kwargs)}')
E           TypeError: Coordinate frame ITRS got unexpected keywords: ['location']

astropy/coordinates/baseframe.py:319: TypeError
_________________________ test_itrs_straight_overhead __________________________

    def test_itrs_straight_overhead():
        """
        With a precise ITRS<->Observed transformation this should give Alt=90 exactly
    
        """
        t = Time('J2010')
        obj = EarthLocation(-1*u.deg, 52*u.deg, height=10.*u.km)
        home = EarthLocation(-1*u.deg, 52*u.deg, height=0.*u.km)
    
        # An object that appears straight overhead - FOR A GEOCENTRIC OBSERVER.
        itrs_geo = obj.get_itrs(t).cartesian
    
        # now get the Geocentric ITRS position of observatory
        obsrepr = home.get_itrs(t).cartesian
    
        # topocentric ITRS position of a straight overhead object
        itrs_repr = itrs_geo - obsrepr
    
        # create a ITRS object that appears straight overhead for a TOPOCENTRIC OBSERVER
>       itrs_topo = ITRS(itrs_repr, obstime=t, location=home)

astropy/coordinates/tests/test_intermediate_transformations.py:957: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <ITRS Coordinate (obstime=J2010.000): (x, y, z) in km
    (6.15567707, -0.10744774, 7.88010754)>
copy = True, representation_type = None, differential_type = None
args = (<CartesianRepresentation (x, y, z) in km
    (6.15567707, -0.10744774, 7.88010754)>,)
kwargs = {'location': <EarthLocation (3934.36115314, -68.67452938, 5002.80334548) km>}
values = {'obstime': <Time object: scale='tt' format='jyear_str' value=J2010.000>}
fnm = 'obstime'
fdefault = <Time object: scale='tt' format='jyear_str' value=J2000.000>
value = <Time object: scale='tt' format='jyear_str' value=J2010.000>

    def __init__(self, *args, copy=True, representation_type=None,
                 differential_type=None, **kwargs):
        self._attr_names_with_defaults = []
    
        self._representation = self._infer_representation(representation_type, differential_type)
        self._data = self._infer_data(args, copy, kwargs)  # possibly None.
    
        # Set frame attributes, if any
    
        values = {}
        for fnm, fdefault in self.get_frame_attr_names().items():
            # Read-only frame attributes are defined as FrameAttribute
            # descriptors which are not settable, so set 'real' attributes as
            # the name prefaced with an underscore.
    
            if fnm in kwargs:
                value = kwargs.pop(fnm)
                setattr(self, '_' + fnm, value)
                # Validate attribute by getting it. If the instance has data,
                # this also checks its shape is OK. If not, we do it below.
                values[fnm] = getattr(self, fnm)
            else:
                setattr(self, '_' + fnm, fdefault)
                self._attr_names_with_defaults.append(fnm)
    
        if kwargs:
>           raise TypeError(
                f'Coordinate frame {self.__class__.__name__} got unexpected '
                f'keywords: {list(kwargs)}')
E           TypeError: Coordinate frame ITRS got unexpected keywords: ['location']

astropy/coordinates/baseframe.py:319: TypeError
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrs[icoo0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrs[icoo1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrs_dist_diff[gframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrs_dist_diff[gframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_to_altaz
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_to_hadec
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_itrs
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_itrs
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_cirs
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_hadec
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_precessed_geocentric
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_precessed_geocentric_different_obstime
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe2]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe3]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_sunish[testframe4]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe2]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe3]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_moonish[testframe4]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe2]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe3]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_altaz_bothroutes[testframe4]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe2]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe3]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_moonish[testframe4]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe2]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe3]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_altaz_nodist[testframe4]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe2]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe3]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_icrs_moonish[testframe4]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe2]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe3]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_icrs_moonish[testframe4]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe2]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe3]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_gcrscirs_sunish[testframe4]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe0]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe1]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe2]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe3]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_altaz_moonish[testframe4]
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_gcrs_self_transform_closeby
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_teme_itrf
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_precessedgeocentric_loopback
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_teme_loopback
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_tete_transforms
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_straight_overhead
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::test_aa_high_precision_nodata
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::TestGetLocationGCRS::test_get_gcrs_posvel
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::TestGetLocationGCRS::test_tete_quick
PASSED astropy/coordinates/tests/test_intermediate_transformations.py::TestGetLocationGCRS::test_cirs_quick
SKIPPED [1] ../opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pytest_remotedata/plugin.py:85: need --remote-data option to run
SKIPPED [1] astropy/coordinates/tests/test_intermediate_transformations.py:817: requires jplephem
SKIPPED [1] astropy/coordinates/tests/test_intermediate_transformations.py:980: requires jplephem >= 2.15
FAILED astropy/coordinates/tests/test_intermediate_transformations.py::test_icrs_cirs
FAILED astropy/coordinates/tests/test_intermediate_transformations.py::test_itrs_topo_to_altaz_with_refraction
FAILED astropy/coordinates/tests/test_intermediate_transformations.py::test_itrs_topo_to_hadec_with_refraction
FAILED astropy/coordinates/tests/test_intermediate_transformations.py::test_cirs_itrs_topo
FAILED astropy/coordinates/tests/test_intermediate_transformations.py::test_itrs_straight_overhead
=================== 5 failed, 68 passed, 3 skipped in 0.57s ====================
+ git checkout 6500928dc0e57be8f06d1162eacc3ba5e2eff692 astropy/coordinates/tests/test_intermediate_transformations.py
Updated 1 path from 059e0f8

```
