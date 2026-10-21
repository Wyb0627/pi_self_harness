# Official SWE-bench Evaluator Feedback

This is hidden evaluator information from the rejected original Pi submission. The resulting repair is feedback-assisted and is not a standard one-submission SWE-bench prediction.

Instance: `astropy__astropy-14365`

## Report

```json
{
    "astropy__astropy-14365": {
        "patch_is_None": false,
        "patch_exists": true,
        "patch_successfully_applied": true,
        "resolved": false,
        "tests_status": {
            "FAIL_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]"
                ]
            },
            "PASS_TO_PASS": {
                "success": [
                    "astropy/io/ascii/tests/test_qdp.py::test_get_tables_from_qdp_file",
                    "astropy/io/ascii/tests/test_qdp.py::test_roundtrip[False]",
                    "astropy/io/ascii/tests/test_qdp.py::test_read_example",
                    "astropy/io/ascii/tests/test_qdp.py::test_roundtrip_example",
                    "astropy/io/ascii/tests/test_qdp.py::test_roundtrip_example_comma",
                    "astropy/io/ascii/tests/test_qdp.py::test_read_write_simple",
                    "astropy/io/ascii/tests/test_qdp.py::test_read_write_simple_specify_name",
                    "astropy/io/ascii/tests/test_qdp.py::test_get_lines_from_qdp"
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
cslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/dis.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/dis.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/flexed/wcsbth.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/flexed/wcsbth.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/flexed/wcspih.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/flexed/wcspih.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/flexed/wcsulex.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/flexed/wcsulex.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/flexed/wcsutrn.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/flexed/wcsutrn.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/lin.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/lin.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/log.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/log.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/prj.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/prj.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/spc.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/spc.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/sph.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/sph.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/spx.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/spx.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/tab.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/tab.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/wcs.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcs.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/wcserr.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcserr.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/wcsfix.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcsfix.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/wcshdr.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcshdr.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/wcsprintf.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcsprintf.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/wcsunits.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcsunits.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DECHO -DWCSTRIG_MACRO -DASTROPY_WCS_BUILD -D_GNU_SOURCE -DNDEBUG -DHAVE_SINCOS -UDEBUG -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -Icextern/wcslib/C -Iastropy/wcs/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/wcslib/C/wcsutil.c -o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcsutil.o -std=gnu99 -Wno-strict-prototypes -Wno-unused-function -Wno-unused-value -Wno-uninitialized
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/wcs
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/astropy_wcs.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/astropy_wcs_api.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/distortion.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/distortion_wrap.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/docstrings.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/pipeline.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/pyutil.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/sip.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/sip_wrap.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/str_list_proxy.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/unit_list_proxy.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/util.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/wcslib_auxprm_wrap.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/wcslib_celprm_wrap.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/wcslib_prjprm_wrap.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/wcslib_tabprm_wrap.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/wcslib_wrap.o /tmp/tmpj3odd3sh.build-temp/astropy/wcs/src/wcslib_wtbarr_wrap.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/cel.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/dis.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/flexed/wcsbth.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/flexed/wcspih.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/flexed/wcsulex.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/flexed/wcsutrn.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/lin.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/log.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/prj.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/spc.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/sph.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/spx.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/tab.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcs.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcserr.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcsfix.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcshdr.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcsprintf.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcsunits.o /tmp/tmpj3odd3sh.build-temp/cextern/wcslib/C/wcsutil.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.convolution._convolve' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/convolution
  creating /tmp/tmpj3odd3sh.build-temp/astropy/convolution/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/convolution/_convolve.c -o /tmp/tmpj3odd3sh.build-temp/astropy/convolution/_convolve.o -UNDEBUG -fPIC
  In file included from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/convolution/_convolve.c:698:
  /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  In file included from astropy/convolution/_convolve.c:703:
  astropy/convolution/src/convolve.h:88:19: warning: inline function ‘convolve3d’ declared but never defined
     88 | FORCE_INLINE void convolve3d(DTYPE * const result,
        |                   ^~~~~~~~~~
  astropy/convolution/src/convolve.h:74:19: warning: inline function ‘convolve2d’ declared but never defined
     74 | FORCE_INLINE void convolve2d(DTYPE * const result,
        |                   ^~~~~~~~~~
  astropy/convolution/src/convolve.h:60:19: warning: inline function ‘convolve1d’ declared but never defined
     60 | FORCE_INLINE void convolve1d(DTYPE * const result,
        |                   ^~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/convolution/src/convolve.c -o /tmp/tmpj3odd3sh.build-temp/astropy/convolution/src/convolve.o -UNDEBUG -fPIC
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/convolution
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/convolution/_convolve.o /tmp/tmpj3odd3sh.build-temp/astropy/convolution/src/convolve.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so
  building 'astropy.utils._compiler' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/utils
  creating /tmp/tmpj3odd3sh.build-temp/astropy/utils/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/utils/src/compiler.c -o /tmp/tmpj3odd3sh.build-temp/astropy/utils/src/compiler.o
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/utils
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/utils/src/compiler.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so
  building 'astropy.table._np_utils' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/table
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/table/_np_utils.c -o /tmp/tmpj3odd3sh.build-temp/astropy/table/_np_utils.o
  In file included from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/table/_np_utils.c:698:
  /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/table
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/table/_np_utils.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.table._column_mixins' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/table/_column_mixins.c -o /tmp/tmpj3odd3sh.build-temp/astropy/table/_column_mixins.o
  In file included from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/table/_column_mixins.c:696:
  /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  In file included from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:21,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/table/_column_mixins.c:696:
  /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/__multiarray_api.h:1463:1: warning: ‘_import_array’ defined but not used [-Wunused-function]
   1463 | _import_array(void)
        | ^~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/table/_column_mixins.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._fast_sigma_clip' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/stats
  creating /tmp/tmpj3odd3sh.build-temp/astropy/stats/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/src/compute_bounds.c -o /tmp/tmpj3odd3sh.build-temp/astropy/stats/src/compute_bounds.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/src/fast_sigma_clip.c -o /tmp/tmpj3odd3sh.build-temp/astropy/stats/src/fast_sigma_clip.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/src/wirth_select.c -o /tmp/tmpj3odd3sh.build-temp/astropy/stats/src/wirth_select.o
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/stats
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/stats/src/compute_bounds.o /tmp/tmpj3odd3sh.build-temp/astropy/stats/src/fast_sigma_clip.o /tmp/tmpj3odd3sh.build-temp/astropy/stats/src/wirth_select.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so
  building 'astropy.time._parse_times' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/time
  creating /tmp/tmpj3odd3sh.build-temp/astropy/time/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/time/src/parse_times.c -o /tmp/tmpj3odd3sh.build-temp/astropy/time/src/parse_times.o
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/time
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/time/src/parse_times.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so
  building 'astropy.utils.xml._iterparser' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/utils/xml
  creating /tmp/tmpj3odd3sh.build-temp/astropy/utils/xml/src
  creating /tmp/tmpj3odd3sh.build-temp/cextern/expat
  creating /tmp/tmpj3odd3sh.build-temp/cextern/expat/lib
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/utils/xml/src/iterparse.c -o /tmp/tmpj3odd3sh.build-temp/astropy/utils/xml/src/iterparse.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmlparse.c -o /tmp/tmpj3odd3sh.build-temp/cextern/expat/lib/xmlparse.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmlrole.c -o /tmp/tmpj3odd3sh.build-temp/cextern/expat/lib/xmlrole.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmltok.c -o /tmp/tmpj3odd3sh.build-temp/cextern/expat/lib/xmltok.o
  In file included from cextern/expat/lib/xmltok.c:55:
  cextern/expat/lib/xmltok_ns.c: In function ‘findEncodingNS’:
  cextern/expat/lib/xmltok.h:272:10: warning: ‘buf’ may be used uninitialized [-Wmaybe-uninitialized]
    272 |   (((enc)->utf8Convert)(enc, fromP, fromLim, toP, toLim))
        |   ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cextern/expat/lib/xmltok_ns.c:95:3: note: in expansion of macro ‘XmlUtf8Convert’
     95 |   XmlUtf8Convert(enc, &ptr, end, &p, p + ENCODING_MAX - 1);
        |   ^~~~~~~~~~~~~~
  cextern/expat/lib/xmltok.h:272:10: note: by argument 5 of type ‘const char *’ to ‘enum XML_Convert_Result(const ENCODING *, const char **, const char *, char **, const char *)’ {aka ‘enum XML_Convert_Result(const struct encoding *, const char **, const char *, char **, const char *)’}
    272 |   (((enc)->utf8Convert)(enc, fromP, fromLim, toP, toLim))
        |   ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cextern/expat/lib/xmltok_ns.c:95:3: note: in expansion of macro ‘XmlUtf8Convert’
     95 |   XmlUtf8Convert(enc, &ptr, end, &p, p + ENCODING_MAX - 1);
        |   ^~~~~~~~~~~~~~
  In file included from cextern/expat/lib/xmltok.c:1657:
  cextern/expat/lib/xmltok_ns.c:92:8: note: ‘buf’ declared here
     92 |   char buf[ENCODING_MAX];
        |        ^~~
  In file included from cextern/expat/lib/xmltok.c:55:
  cextern/expat/lib/xmltok_ns.c: In function ‘findEncoding’:
  cextern/expat/lib/xmltok.h:272:10: warning: ‘buf’ may be used uninitialized [-Wmaybe-uninitialized]
    272 |   (((enc)->utf8Convert)(enc, fromP, fromLim, toP, toLim))
        |   ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cextern/expat/lib/xmltok_ns.c:95:3: note: in expansion of macro ‘XmlUtf8Convert’
     95 |   XmlUtf8Convert(enc, &ptr, end, &p, p + ENCODING_MAX - 1);
        |   ^~~~~~~~~~~~~~
  cextern/expat/lib/xmltok.h:272:10: note: by argument 5 of type ‘const char *’ to ‘enum XML_Convert_Result(const ENCODING *, const char **, const char *, char **, const char *)’ {aka ‘enum XML_Convert_Result(const struct encoding *, const char **, const char *, char **, const char *)’}
    272 |   (((enc)->utf8Convert)(enc, fromP, fromLim, toP, toLim))
        |   ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cextern/expat/lib/xmltok_ns.c:95:3: note: in expansion of macro ‘XmlUtf8Convert’
     95 |   XmlUtf8Convert(enc, &ptr, end, &p, p + ENCODING_MAX - 1);
        |   ^~~~~~~~~~~~~~
  In file included from cextern/expat/lib/xmltok.c:1646:
  cextern/expat/lib/xmltok_ns.c:92:8: note: ‘buf’ declared here
     92 |   char buf[ENCODING_MAX];
        |        ^~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmltok_impl.c -o /tmp/tmpj3odd3sh.build-temp/cextern/expat/lib/xmltok_impl.o
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/utils/xml
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/utils/xml/src/iterparse.o /tmp/tmpj3odd3sh.build-temp/cextern/expat/lib/xmlparse.o /tmp/tmpj3odd3sh.build-temp/cextern/expat/lib/xmlrole.o /tmp/tmpj3odd3sh.build-temp/cextern/expat/lib/xmltok.o /tmp/tmpj3odd3sh.build-temp/cextern/expat/lib/xmltok_impl.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -Wl,--version-script=astropy/utils/xml/src/iterparse.map
  building 'astropy.io.votable.tablewriter' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/io
  creating /tmp/tmpj3odd3sh.build-temp/astropy/io/votable
  creating /tmp/tmpj3odd3sh.build-temp/astropy/io/votable/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/votable/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/votable/src/tablewriter.c -o /tmp/tmpj3odd3sh.build-temp/astropy/io/votable/src/tablewriter.o
  astropy/io/votable/src/tablewriter.c: In function ‘write_tabledata’:
  astropy/io/votable/src/tablewriter.c:270:30: warning: assignment discards ‘const’ qualifier from pointer target type [-Wdiscarded-qualifiers]
    270 |                 if ((str_tmp = PyUnicode_AsUTF8AndSize(str_val, &str_len)) == NULL) {
        |                              ^
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/io
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/io/votable
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/io/votable/src/tablewriter.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.ascii.cparser' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/io/ascii
  creating /tmp/tmpj3odd3sh.build-temp/astropy/io/ascii/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/cparser.c -o /tmp/tmpj3odd3sh.build-temp/astropy/io/ascii/cparser.o
  In file included from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/io/ascii/cparser.c:698:
  /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/src/tokenizer.c -o /tmp/tmpj3odd3sh.build-temp/astropy/io/ascii/src/tokenizer.o
  astropy/io/ascii/src/tokenizer.c: In function ‘push’:
  astropy/io/ascii/src/tokenizer.c:124:54: warning: comparison of integer expressions of different signedness: ‘long int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
    124 |     if (self->col_ptrs[col] - self->output_cols[col] >=
        |                                                      ^~
  astropy/io/ascii/src/tokenizer.c: In function ‘tokenize’:
  astropy/io/ascii/src/tokenizer.c:424:42: warning: comparison of integer expressions of different signedness: ‘size_t’ {aka ‘long unsigned int’} and ‘int’ [-Wsign-compare]
    424 |                     if (self->source_pos == -1
        |                                          ^~
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/io/ascii
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/io/ascii/cparser.o /tmp/tmpj3odd3sh.build-temp/astropy/io/ascii/src/tokenizer.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._tiled_compression._compression' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/io/fits
  creating /tmp/tmpj3odd3sh.build-temp/astropy/io/fits/_tiled_compression
  creating /tmp/tmpj3odd3sh.build-temp/astropy/io/fits/_tiled_compression/src
  creating /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio
  creating /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/fits/_tiled_compression/src/compression.c -o /tmp/tmpj3odd3sh.build-temp/astropy/io/fits/_tiled_compression/src/compression.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/fits/_tiled_compression/src/unquantize.c -o /tmp/tmpj3odd3sh.build-temp/astropy/io/fits/_tiled_compression/src/unquantize.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/fits_hcompress.c -o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/fits_hcompress.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/fits_hdecompress.c -o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/fits_hdecompress.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/pliocomp.c -o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/pliocomp.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/quantize.c -o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/quantize.o
  cextern/cfitsio/lib/quantize.c: In function ‘quick_select_float’:
  cextern/cfitsio/lib/quantize.c:3722:5: warning: this ‘if’ clause does not guard... [-Wmisleading-indentation]
   3722 |     if (hh <= median)
        |     ^~
  cextern/cfitsio/lib/quantize.c:3724:9: note: ...this statement, but the latter is misleadingly indented as if it were guarded by the ‘if’
   3724 |         if (hh >= median)
        |         ^~
  cextern/cfitsio/lib/quantize.c: In function ‘quick_select_short’:
  cextern/cfitsio/lib/quantize.c:3778:5: warning: this ‘if’ clause does not guard... [-Wmisleading-indentation]
   3778 |     if (hh <= median)
        |     ^~
  cextern/cfitsio/lib/quantize.c:3780:9: note: ...this statement, but the latter is misleadingly indented as if it were guarded by the ‘if’
   3780 |         if (hh >= median)
        |         ^~
  cextern/cfitsio/lib/quantize.c: In function ‘quick_select_int’:
  cextern/cfitsio/lib/quantize.c:3834:5: warning: this ‘if’ clause does not guard... [-Wmisleading-indentation]
   3834 |     if (hh <= median)
        |     ^~
  cextern/cfitsio/lib/quantize.c:3836:9: note: ...this statement, but the latter is misleadingly indented as if it were guarded by the ‘if’
   3836 |         if (hh >= median)
        |         ^~
  cextern/cfitsio/lib/quantize.c: In function ‘quick_select_longlong’:
  cextern/cfitsio/lib/quantize.c:3890:5: warning: this ‘if’ clause does not guard... [-Wmisleading-indentation]
   3890 |     if (hh <= median)
        |     ^~
  cextern/cfitsio/lib/quantize.c:3892:9: note: ...this statement, but the latter is misleadingly indented as if it were guarded by the ‘if’
   3892 |         if (hh >= median)
        |         ^~
  cextern/cfitsio/lib/quantize.c: In function ‘quick_select_double’:
  cextern/cfitsio/lib/quantize.c:3946:5: warning: this ‘if’ clause does not guard... [-Wmisleading-indentation]
   3946 |     if (hh <= median)
        |     ^~
  cextern/cfitsio/lib/quantize.c:3948:9: note: ...this statement, but the latter is misleadingly indented as if it were guarded by the ‘if’
   3948 |         if (hh >= median)
        |         ^~
  At top level:
  cextern/cfitsio/lib/quantize.c:3641:12: warning: ‘FnCompare_float’ defined but not used [-Wunused-function]
   3641 | static int FnCompare_float(const void *v1, const void *v2)
        |            ^~~~~~~~~~~~~~~
  cextern/cfitsio/lib/quantize.c:3628:12: warning: ‘FnCompare_int’ defined but not used [-Wunused-function]
   3628 | static int FnCompare_int(const void *v1, const void *v2)
        |            ^~~~~~~~~~~~~
  cextern/cfitsio/lib/quantize.c:3615:12: warning: ‘FnCompare_short’ defined but not used [-Wunused-function]
   3615 | static int FnCompare_short(const void *v1, const void *v2)
        |            ^~~~~~~~~~~~~~~
  cextern/cfitsio/lib/quantize.c:3494:12: warning: ‘FnNoise1_double’ defined but not used [-Wunused-function]
   3494 | static int FnNoise1_double
        |            ^~~~~~~~~~~~~~~
  cextern/cfitsio/lib/quantize.c:2487:12: warning: ‘FnNoise3_int’ defined but not used [-Wunused-function]
   2487 | static int FnNoise3_int
        |            ^~~~~~~~~~~~
  cextern/cfitsio/lib/quantize.c:2269:12: warning: ‘FnNoise3_short’ defined but not used [-Wunused-function]
   2269 | static int FnNoise3_short
        |            ^~~~~~~~~~~~~~
  cextern/cfitsio/lib/quantize.c: In function ‘fits_img_stats_short’:
  cextern/cfitsio/lib/quantize.c:510:41: warning: ‘ngood’ may be used uninitialized in this function [-Wmaybe-uninitialized]
    510 |                 if (ngoodpix) *ngoodpix = ngood;
        |                               ~~~~~~~~~~^~~~~~~
  cextern/cfitsio/lib/quantize.c: In function ‘fits_img_stats_int’:
  cextern/cfitsio/lib/quantize.c:569:41: warning: ‘ngood’ may be used uninitialized in this function [-Wmaybe-uninitialized]
    569 |                 if (ngoodpix) *ngoodpix = ngood;
        |                               ~~~~~~~~~~^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/ricecomp.c -o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/ricecomp.o
  cextern/cfitsio/lib/ricecomp.c: In function ‘fits_rcomp’:
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:267:21: note: in expansion of macro ‘putcbuf’
    267 |                     putcbuf(lbitbuffer & 0xff,buffer);
        |                     ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:270:25: note: in expansion of macro ‘putcbuf’
    270 |                         putcbuf(0, buffer);
        |                         ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:286:25: note: in expansion of macro ‘putcbuf’
    286 |                         putcbuf((lbitbuffer>>(-lbits_to_go)) & 0xff,buffer);
        |                         ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c: In function ‘fits_rcomp_short’:
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:498:21: note: in expansion of macro ‘putcbuf’
    498 |                     putcbuf(lbitbuffer & 0xff,buffer);
        |                     ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:500:25: note: in expansion of macro ‘putcbuf’
    500 |                         putcbuf(0, buffer);
        |                         ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:516:25: note: in expansion of macro ‘putcbuf’
    516 |                         putcbuf((lbitbuffer>>(-lbits_to_go)) & 0xff,buffer);
        |                         ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c: In function ‘fits_rcomp_byte’:
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:723:21: note: in expansion of macro ‘putcbuf’
    723 |                     putcbuf(lbitbuffer & 0xff,buffer);
        |                     ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:725:25: note: in expansion of macro ‘putcbuf’
    725 |                         putcbuf(0, buffer);
        |                         ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:741:25: note: in expansion of macro ‘putcbuf’
    741 |                         putcbuf((lbitbuffer>>(-lbits_to_go)) & 0xff,buffer);
        |                         ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c: In function ‘output_nbits’:
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:812:9: note: in expansion of macro ‘putcbuf’
    812 |         putcbuf(lbitbuffer & 0xff,buffer);
        |         ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:824:9: note: in expansion of macro ‘putcbuf’
    824 |         putcbuf((lbitbuffer>>(-lbits_to_go)) & 0xff,buffer);
        |         ^~~~~~~
  cextern/cfitsio/lib/ricecomp.c: In function ‘done_outputing_bits’:
  cextern/cfitsio/lib/ricecomp.c:70:48: warning: right-hand operand of comma expression has no effect [-Wunused-value]
     70 | #define putcbuf(c,mf)   ((*(mf->current)++ = c), 0)
        |                         ~~~~~~~~~~~~~~~~~~~~~~~^~~~
  cextern/cfitsio/lib/ricecomp.c:837:9: note: in expansion of macro ‘putcbuf’
    837 |         putcbuf(buffer->bitbuffer<<buffer->bits_to_go,buffer);
        |         ^~~~~~~
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/io/fits
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/io/fits/_tiled_compression
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/io/fits/_tiled_compression/src/compression.o /tmp/tmpj3odd3sh.build-temp/astropy/io/fits/_tiled_compression/src/unquantize.o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/fits_hcompress.o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/fits_hdecompress.o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/pliocomp.o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/quantize.o /tmp/tmpj3odd3sh.build-temp/cextern/cfitsio/lib/ricecomp.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/io/fits/_tiled_compression/_compression.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.bls._impl' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/timeseries
  creating /tmp/tmpj3odd3sh.build-temp/astropy/timeseries/periodograms
  creating /tmp/tmpj3odd3sh.build-temp/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/_impl.c -o /tmp/tmpj3odd3sh.build-temp/astropy/timeseries/periodograms/bls/_impl.o
  In file included from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/timeseries/periodograms/bls/_impl.c:698:
  /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/bls.c -o /tmp/tmpj3odd3sh.build-temp/astropy/timeseries/periodograms/bls/bls.o
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
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/timeseries
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/timeseries/periodograms
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/timeseries/periodograms/bls/_impl.o /tmp/tmpj3odd3sh.build-temp/astropy/timeseries/periodograms/bls/bls.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._stats' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/stats/_stats.c -o /tmp/tmpj3odd3sh.build-temp/./astropy/stats/_stats.o
  In file included from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/stats/_stats.c:698:
  /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/./astropy/stats/_stats.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._utils' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/io/fits/_utils.c -o /tmp/tmpj3odd3sh.build-temp/./astropy/io/fits/_utils.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/./astropy/io/fits/_utils.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.lombscargle.implementations.cython_impl' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpj3odd3sh.build-temp/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c -o /tmp/tmpj3odd3sh.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o
  In file included from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c:698:
  /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.cosmology.flrw.scalar_inv_efuncs' extension
  creating /tmp/tmpj3odd3sh.build-temp/astropy/cosmology
  creating /tmp/tmpj3odd3sh.build-temp/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/cosmology/flrw/scalar_inv_efuncs.c -o /tmp/tmpj3odd3sh.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/cosmology
  creating /tmp/tmpp4ywxmwg.build-lib/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.compiler_version' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/_compiler.c -o /tmp/tmpj3odd3sh.build-temp/astropy/_compiler.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpj3odd3sh.build-temp/astropy/_compiler.o -o /tmp/tmpp4ywxmwg.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so -> astropy/wcs
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so -> astropy/convolution
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so -> astropy/utils
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so -> astropy/time
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -> astropy/utils/xml
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so -> astropy/io/votable
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so -> astropy/io/ascii
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/io/fits/_tiled_compression/_compression.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits/_tiled_compression
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/bls
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/lombscargle/implementations
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so -> astropy/cosmology/flrw
  copying /tmp/tmpp4ywxmwg.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so -> astropy
  Editable install will be performed using a meta path finder.

  Options like `package-data`, `include/exclude-package-data` or
  `packages.find.exclude/include` may have no effect.

  adding '__editable___astropy_0_1_dev3_g7269fa3e3_d20260925_finder.py'
  adding '__editable__.astropy-0.1.dev3+g7269fa3e3.d20260925.pth'
  creating '/tmp/pip-ephem-wheel-cache-_xiuefda/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4/tmpifebwpqo/.tmp-fu_gk7x8/astropy-0.1.dev3+g7269fa3e3.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' and adding '/tmp/tmp3k0b2kaqastropy-0.1.dev3+g7269fa3e3.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' to it
  adding 'astropy-0.1.dev3+g7269fa3e3.d20260925.dist-info/LICENSE.rst'
  adding 'astropy-0.1.dev3+g7269fa3e3.d20260925.dist-info/METADATA'
  adding 'astropy-0.1.dev3+g7269fa3e3.d20260925.dist-info/WHEEL'
  adding 'astropy-0.1.dev3+g7269fa3e3.d20260925.dist-info/entry_points.txt'
  adding 'astropy-0.1.dev3+g7269fa3e3.d20260925.dist-info/scm_file_list.json'
  adding 'astropy-0.1.dev3+g7269fa3e3.d20260925.dist-info/scm_version.json'
  adding 'astropy-0.1.dev3+g7269fa3e3.d20260925.dist-info/top_level.txt'
  adding 'astropy-0.1.dev3+g7269fa3e3.d20260925.dist-info/RECORD'
  /tmp/pip-build-env-e8q4jelu/overlay/lib/python3.9/site-packages/setuptools/command/editable_wheel.py:348: InformationOnly: Editable installation.
  !!

          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************

  !!
    wheel_obj.write_files(unpacked)
  Building editable for astropy (pyproject.toml): finished with status 'done'
  Created wheel for astropy: filename=astropy-0.1.dev3+g7269fa3e3.d20260925-0.editable-cp39-cp39-linux_aarch64.whl size=19711 sha256=3c21d6036672f6b0dfa0c0d6b2e1b843482451b889d6740419e104dc98cc1835
  Stored in directory: /tmp/pip-ephem-wheel-cache-_xiuefda/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4
Successfully built astropy
Installing collected packages: astropy
  Attempting uninstall: astropy
    Found existing installation: astropy 0.1.dev3+g7269fa3e3.d20260925
    Uninstalling astropy-0.1.dev3+g7269fa3e3.d20260925:
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fits2bitmap
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitscheck
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsdiff
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsheader
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsinfo
      Removing file or directory /opt/miniconda3/envs/testbed/bin/samp_hub
      Removing file or directory /opt/miniconda3/envs/testbed/bin/showtable
      Removing file or directory /opt/miniconda3/envs/testbed/bin/volint
      Removing file or directory /opt/miniconda3/envs/testbed/bin/wcslint
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable__.astropy-0.1.dev3+g7269fa3e3.d20260925.pth
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable___astropy_0_1_dev3_g7269fa3e3_d20260925_finder.py
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__pycache__/__editable___astropy_0_1_dev3_g7269fa3e3_d20260925_finder.cpython-39.pyc
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astropy-0.1.dev3+g7269fa3e3.d20260925.dist-info/
      Successfully uninstalled astropy-0.1.dev3+g7269fa3e3.d20260925
  changing mode of /opt/miniconda3/envs/testbed/bin/fits2bitmap to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitscheck to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsdiff to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsheader to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsinfo to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/samp_hub to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/showtable to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/volint to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/wcslint to 755
Successfully installed astropy-0.1.dev3+g7269fa3e3.d20260925
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
+ git checkout 7269fa3e33e8d02485a647da91a5a2a60a06af61 astropy/io/ascii/tests/test_qdp.py
Updated 0 paths from fe91cbe
+ git apply -v -
Checking patch astropy/io/ascii/tests/test_qdp.py...
Applied patch astropy/io/ascii/tests/test_qdp.py cleanly.
+ pytest -rA astropy/io/ascii/tests/test_qdp.py
<frozen importlib._bootstrap>:228: RuntimeWarning: numpy.ndarray size changed, may indicate binary incompatibility. Expected 80 from C header, got 96 from PyObject
[1m============================= test session starts ==============================[0m
platform linux -- Python 3.9.25, pytest-7.4.0, pluggy-1.3.0

Running tests with Astropy version 0.1.dev3+g7269fa3e3.d20260925.
Running tests in astropy/io/ascii/tests/test_qdp.py.

Date: 2026-09-25T04:44:23

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
collected 9 items

astropy/io/ascii/tests/test_qdp.py [32m.[0m[32m.[0m[31mF[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31m                             [100%][0m

=================================== FAILURES ===================================
[31m[1m_____________________________ test_roundtrip[True] _____________________________[0m

tmp_path = PosixPath('/tmp/pytest-of-root/pytest-0/test_roundtrip_True_0')
lowercase = True

    @pytest.mark.parametrize("lowercase", [False, True])
    def test_roundtrip(tmp_path, lowercase):
        example_qdp = """
        ! Swift/XRT hardness ratio of trigger: XXXX, name: BUBU X-2
        ! Columns are as labelled
        READ TERR 1
        READ SERR 2
        ! WT -- hard data
        !MJD            Err (pos)       Err(neg)        Rate            Error
        53000.123456 2.37847222222222e-05    -2.37847222222222e-05   NO       0.212439
        55045.099887 1.14467592592593e-05    -1.14467592592593e-05   0.000000        0.000000
        NO NO NO NO NO
        ! WT -- soft data
        !MJD            Err (pos)       Err(neg)        Rate            Error
        53000.123456 2.37847222222222e-05    -2.37847222222222e-05   0.726155        0.583890
        55045.099887 1.14467592592593e-05    -1.14467592592593e-05   2.410935        1.393592
        NO NO NO NO NO
        ! WT -- hardness ratio
        !MJD            Err (pos)       Err(neg)        Rate            Error
        53000.123456 2.37847222222222e-05    -2.37847222222222e-05   -0.292553       -0.374935
        55045.099887 1.14467592592593e-05    -1.14467592592593e-05   0.000000        NO
        ! Add command, just to raise the warning.
        READ TERR 1
        ! WT -- whatever
        !MJD            Err (pos)       Err(neg)        Rate            Error
        53000.123456 2.37847222222222e-05    -2.37847222222222e-05   -0.292553       -0.374935
        NO 1.14467592592593e-05    -1.14467592592593e-05   0.000000        NO
        """
        if lowercase:
            example_qdp = lowercase_header(example_qdp)
    
        path = str(tmp_path / "test.qdp")
        path2 = str(tmp_path / "test2.qdp")
    
        with open(path, "w") as fp:
            print(example_qdp, file=fp)
        with pytest.warns(AstropyUserWarning) as record:
>           table = _read_table_qdp(path, names=["MJD", "Rate"], table_id=0)

[1m[31mastropy/io/ascii/tests/test_qdp.py[0m:93: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
[1m[31mastropy/io/ascii/qdp.py[0m:418: in _read_table_qdp
    tables = _get_tables_from_qdp_file(
[1m[31mastropy/io/ascii/qdp.py[0m:259: in _get_tables_from_qdp_file
    contents, ncol = _get_type_from_list_of_lines(lines, delimiter=delimiter)
[1m[31mastropy/io/ascii/qdp.py[0m:122: in _get_type_from_list_of_lines
    types = [_line_type(line, delimiter=delimiter) for line in lines]
[1m[31mastropy/io/ascii/qdp.py[0m:122: in <listcomp>
    types = [_line_type(line, delimiter=delimiter) for line in lines]
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

line = '53000.123456 2.37847222222222e-05    -2.37847222222222e-05   no       0.212439'
delimiter = None

    def _line_type(line, delimiter=None):
        """Interpret a QDP file line.
    
        Parameters
        ----------
        line : str
            a single line of the file
    
        Returns
        -------
        type : str
            Line type: "comment", "command", or "data"
    
        Examples
        --------
        >>> _line_type("READ SERR 3")
        'command'
        >>> _line_type(" \\n    !some gibberish")
        'comment'
        >>> _line_type("   ")
        'comment'
        >>> _line_type(" 21345.45")
        'data,1'
        >>> _line_type(" 21345.45 1.53e-3 1e-3 .04 NO nan")
        'data,6'
        >>> _line_type(" 21345.45,1.53e-3,1e-3,.04,NO,nan", delimiter=',')
        'data,6'
        >>> _line_type(" 21345.45 ! a comment to disturb")
        'data,1'
        >>> _line_type("NO NO NO NO NO")
        'new'
        >>> _line_type("NO,NO,NO,NO,NO", delimiter=',')
        'new'
        >>> _line_type("N O N NOON OON O")
        Traceback (most recent call last):
            ...
        ValueError: Unrecognized QDP line...
        >>> _line_type(" some non-comment gibberish")
        Traceback (most recent call last):
            ...
        ValueError: Unrecognized QDP line...
        """
        _decimal_re = r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
        _command_re = r"(?i:READ [TS]ERR(\s+[0-9]+)+)"
    
        sep = delimiter
        if delimiter is None:
            sep = r"\s+"
        _new_re = rf"NO({sep}NO)+"
        _data_re = rf"({_decimal_re}|NO|[-+]?nan)({sep}({_decimal_re}|NO|[-+]?nan))*)"
        _type_re = rf"^\s*((?P<command>{_command_re})|(?P<new>{_new_re})|(?P<data>{_data_re})?\s*(\!(?P<comment>.*))?\s*$"
        _line_type_re = re.compile(_type_re)
        line = line.strip()
        if not line:
            return "comment"
        match = _line_type_re.match(line)
    
        if match is None:
>           raise ValueError(f"Unrecognized QDP line: {line}")
[1m[31mE           ValueError: Unrecognized QDP line: 53000.123456 2.37847222222222e-05    -2.37847222222222e-05   no       0.212439[0m

[1m[31mastropy/io/ascii/qdp.py[0m:78: ValueError
==================================== PASSES ====================================
[36m[1m=========================== short test summary info ============================[0m
[32mPASSED[0m astropy/io/ascii/tests/test_qdp.py::[1mtest_get_tables_from_qdp_file[0m
[32mPASSED[0m astropy/io/ascii/tests/test_qdp.py::[1mtest_roundtrip[False][0m
[32mPASSED[0m astropy/io/ascii/tests/test_qdp.py::[1mtest_read_example[0m
[32mPASSED[0m astropy/io/ascii/tests/test_qdp.py::[1mtest_roundtrip_example[0m
[32mPASSED[0m astropy/io/ascii/tests/test_qdp.py::[1mtest_roundtrip_example_comma[0m
[32mPASSED[0m astropy/io/ascii/tests/test_qdp.py::[1mtest_read_write_simple[0m
[32mPASSED[0m astropy/io/ascii/tests/test_qdp.py::[1mtest_read_write_simple_specify_name[0m
[32mPASSED[0m astropy/io/ascii/tests/test_qdp.py::[1mtest_get_lines_from_qdp[0m
[31mFAILED[0m astropy/io/ascii/tests/test_qdp.py::[1mtest_roundtrip[True][0m - ValueError: Unrecognized QDP line: 53000.123456 2.37847222222222e-05    -2....
[31m========================= [31m[1m1 failed[0m, [32m8 passed[0m[31m in 0.03s[0m[31m ==========================[0m
+ git checkout 7269fa3e33e8d02485a647da91a5a2a60a06af61 astropy/io/ascii/tests/test_qdp.py
Updated 1 path from fe91cbe

```
