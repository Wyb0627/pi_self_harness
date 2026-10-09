# Official SWE-bench Evaluator Feedback

This is hidden evaluator information from the rejected original Pi submission. The resulting repair is feedback-assisted and is not a standard one-submission SWE-bench prediction.

Instance: `astropy__astropy-14539`

## Report

```json
{
    "astropy__astropy-14539": {
        "patch_is_None": false,
        "patch_exists": true,
        "patch_successfully_applied": true,
        "resolved": false,
        "tests_status": {
            "FAIL_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_identical_tables",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_table_data"
                ]
            },
            "PASS_TO_PASS": {
                "success": [
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_identical_headers",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_slightly_different_headers",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_common_keywords",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_keyword_count",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_keywords",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_keyword_values",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_keyword_comments",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_keyword_values_with_duplicate",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_asymmetric_duplicate_keywords",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_floating_point_rtol",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_floating_point_atol",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_ignore_blanks",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_ignore_blank_cards[HeaderDiff]",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_ignore_blank_cards[HDUDiff]",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_ignore_blank_cards[FITSDiff]",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_ignore_hdus",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_ignore_keyword_values",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_ignore_keyword_comments",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_trivial_identical_images",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_identical_within_relative_tolerance",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_identical_within_absolute_tolerance",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_identical_within_rtol_and_atol",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_not_identical_within_rtol_and_atol",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_identical_comp_image_hdus",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_dimensions",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_pixels",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_diff_empty_tables",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_ignore_table_fields",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_table_field_names",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_table_field_counts",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_different_table_rows",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_identical_files_basic",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_partially_identical_files1",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_partially_identical_files2",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_partially_identical_files3",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_diff_nans",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_file_output_from_path_string",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_file_output_overwrite_safety",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_file_output_overwrite_success",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_rawdatadiff_nodiff",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_rawdatadiff_dimsdiff",
                    "astropy/io/fits/tests/test_diff.py::TestDiff::test_rawdatadiff_bytesdiff",
                    "astropy/io/fits/tests/test_diff.py::test_fitsdiff_hdu_name",
                    "astropy/io/fits/tests/test_diff.py::test_fitsdiff_no_hdu_name",
                    "astropy/io/fits/tests/test_diff.py::test_fitsdiff_with_names",
                    "astropy/io/fits/tests/test_diff.py::test_rawdatadiff_diff_with_rtol"
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
cs/src/pyutil.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/sip.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/sip_wrap.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/str_list_proxy.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/unit_list_proxy.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/util.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/wcslib_auxprm_wrap.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/wcslib_celprm_wrap.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/wcslib_prjprm_wrap.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/wcslib_tabprm_wrap.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/wcslib_wrap.o /tmp/tmpp22gukgf.build-temp/astropy/wcs/src/wcslib_wtbarr_wrap.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/cel.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/dis.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/flexed/wcsbth.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/flexed/wcspih.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/flexed/wcsulex.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/flexed/wcsutrn.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/lin.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/log.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/prj.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/spc.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/sph.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/spx.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/tab.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/wcs.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/wcserr.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/wcsfix.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/wcshdr.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/wcsprintf.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/wcsunits.o /tmp/tmpp22gukgf.build-temp/cextern/wcslib/C/wcsutil.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.convolution._convolve' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/convolution
  creating /tmp/tmpp22gukgf.build-temp/astropy/convolution/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/convolution/_convolve.c -o /tmp/tmpp22gukgf.build-temp/astropy/convolution/_convolve.o -UNDEBUG -fPIC
  In file included from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/convolution/_convolve.c:698:
  /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/convolution/src/convolve.c -o /tmp/tmpp22gukgf.build-temp/astropy/convolution/src/convolve.o -UNDEBUG -fPIC
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/convolution
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/convolution/_convolve.o /tmp/tmpp22gukgf.build-temp/astropy/convolution/src/convolve.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so
  building 'astropy.utils._compiler' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/utils
  creating /tmp/tmpp22gukgf.build-temp/astropy/utils/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/utils/src/compiler.c -o /tmp/tmpp22gukgf.build-temp/astropy/utils/src/compiler.o
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/utils
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/utils/src/compiler.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so
  building 'astropy.table._np_utils' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/table
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/table/_np_utils.c -o /tmp/tmpp22gukgf.build-temp/astropy/table/_np_utils.o
  In file included from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/table/_np_utils.c:698:
  /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/table
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/table/_np_utils.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.table._column_mixins' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/table/_column_mixins.c -o /tmp/tmpp22gukgf.build-temp/astropy/table/_column_mixins.o
  In file included from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/table/_column_mixins.c:696:
  /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  In file included from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:21,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/table/_column_mixins.c:696:
  /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/__multiarray_api.h:1463:1: warning: ‘_import_array’ defined but not used [-Wunused-function]
   1463 | _import_array(void)
        | ^~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/table/_column_mixins.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._fast_sigma_clip' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/stats
  creating /tmp/tmpp22gukgf.build-temp/astropy/stats/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/src/compute_bounds.c -o /tmp/tmpp22gukgf.build-temp/astropy/stats/src/compute_bounds.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/src/fast_sigma_clip.c -o /tmp/tmpp22gukgf.build-temp/astropy/stats/src/fast_sigma_clip.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/src/wirth_select.c -o /tmp/tmpp22gukgf.build-temp/astropy/stats/src/wirth_select.o
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/stats
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/stats/src/compute_bounds.o /tmp/tmpp22gukgf.build-temp/astropy/stats/src/fast_sigma_clip.o /tmp/tmpp22gukgf.build-temp/astropy/stats/src/wirth_select.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so
  building 'astropy.time._parse_times' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/time
  creating /tmp/tmpp22gukgf.build-temp/astropy/time/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/time/src/parse_times.c -o /tmp/tmpp22gukgf.build-temp/astropy/time/src/parse_times.o
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/time
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/time/src/parse_times.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so
  building 'astropy.utils.xml._iterparser' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/utils/xml
  creating /tmp/tmpp22gukgf.build-temp/astropy/utils/xml/src
  creating /tmp/tmpp22gukgf.build-temp/cextern/expat
  creating /tmp/tmpp22gukgf.build-temp/cextern/expat/lib
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/utils/xml/src/iterparse.c -o /tmp/tmpp22gukgf.build-temp/astropy/utils/xml/src/iterparse.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmlparse.c -o /tmp/tmpp22gukgf.build-temp/cextern/expat/lib/xmlparse.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmlrole.c -o /tmp/tmpp22gukgf.build-temp/cextern/expat/lib/xmlrole.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmltok.c -o /tmp/tmpp22gukgf.build-temp/cextern/expat/lib/xmltok.o
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmltok_impl.c -o /tmp/tmpp22gukgf.build-temp/cextern/expat/lib/xmltok_impl.o
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/utils/xml
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/utils/xml/src/iterparse.o /tmp/tmpp22gukgf.build-temp/cextern/expat/lib/xmlparse.o /tmp/tmpp22gukgf.build-temp/cextern/expat/lib/xmlrole.o /tmp/tmpp22gukgf.build-temp/cextern/expat/lib/xmltok.o /tmp/tmpp22gukgf.build-temp/cextern/expat/lib/xmltok_impl.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -Wl,--version-script=astropy/utils/xml/src/iterparse.map
  building 'astropy.io.votable.tablewriter' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/io
  creating /tmp/tmpp22gukgf.build-temp/astropy/io/votable
  creating /tmp/tmpp22gukgf.build-temp/astropy/io/votable/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/votable/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/votable/src/tablewriter.c -o /tmp/tmpp22gukgf.build-temp/astropy/io/votable/src/tablewriter.o
  astropy/io/votable/src/tablewriter.c: In function ‘write_tabledata’:
  astropy/io/votable/src/tablewriter.c:270:30: warning: assignment discards ‘const’ qualifier from pointer target type [-Wdiscarded-qualifiers]
    270 |                 if ((str_tmp = PyUnicode_AsUTF8AndSize(str_val, &str_len)) == NULL) {
        |                              ^
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/io
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/io/votable
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/io/votable/src/tablewriter.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.ascii.cparser' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/io/ascii
  creating /tmp/tmpp22gukgf.build-temp/astropy/io/ascii/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/cparser.c -o /tmp/tmpp22gukgf.build-temp/astropy/io/ascii/cparser.o
  In file included from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/io/ascii/cparser.c:698:
  /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/src/tokenizer.c -o /tmp/tmpp22gukgf.build-temp/astropy/io/ascii/src/tokenizer.o
  astropy/io/ascii/src/tokenizer.c: In function ‘push’:
  astropy/io/ascii/src/tokenizer.c:124:54: warning: comparison of integer expressions of different signedness: ‘long int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
    124 |     if (self->col_ptrs[col] - self->output_cols[col] >=
        |                                                      ^~
  astropy/io/ascii/src/tokenizer.c: In function ‘tokenize’:
  astropy/io/ascii/src/tokenizer.c:424:42: warning: comparison of integer expressions of different signedness: ‘size_t’ {aka ‘long unsigned int’} and ‘int’ [-Wsign-compare]
    424 |                     if (self->source_pos == -1
        |                                          ^~
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/io/ascii
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/io/ascii/cparser.o /tmp/tmpp22gukgf.build-temp/astropy/io/ascii/src/tokenizer.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._tiled_compression._compression' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/io/fits
  creating /tmp/tmpp22gukgf.build-temp/astropy/io/fits/_tiled_compression
  creating /tmp/tmpp22gukgf.build-temp/astropy/io/fits/_tiled_compression/src
  creating /tmp/tmpp22gukgf.build-temp/cextern/cfitsio
  creating /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/fits/_tiled_compression/src/compression.c -o /tmp/tmpp22gukgf.build-temp/astropy/io/fits/_tiled_compression/src/compression.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/fits/_tiled_compression/src/unquantize.c -o /tmp/tmpp22gukgf.build-temp/astropy/io/fits/_tiled_compression/src/unquantize.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/fits_hcompress.c -o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/fits_hcompress.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/fits_hdecompress.c -o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/fits_hdecompress.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/pliocomp.c -o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/pliocomp.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/quantize.c -o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/quantize.o
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/ricecomp.c -o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/ricecomp.o
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
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/io/fits
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/io/fits/_tiled_compression
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/io/fits/_tiled_compression/src/compression.o /tmp/tmpp22gukgf.build-temp/astropy/io/fits/_tiled_compression/src/unquantize.o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/fits_hcompress.o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/fits_hdecompress.o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/pliocomp.o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/quantize.o /tmp/tmpp22gukgf.build-temp/cextern/cfitsio/lib/ricecomp.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/io/fits/_tiled_compression/_compression.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.bls._impl' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/timeseries
  creating /tmp/tmpp22gukgf.build-temp/astropy/timeseries/periodograms
  creating /tmp/tmpp22gukgf.build-temp/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/_impl.c -o /tmp/tmpp22gukgf.build-temp/astropy/timeseries/periodograms/bls/_impl.o
  In file included from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/timeseries/periodograms/bls/_impl.c:698:
  /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/bls.c -o /tmp/tmpp22gukgf.build-temp/astropy/timeseries/periodograms/bls/bls.o
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
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/timeseries
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/timeseries/periodograms
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/timeseries/periodograms/bls/_impl.o /tmp/tmpp22gukgf.build-temp/astropy/timeseries/periodograms/bls/bls.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._stats' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/stats/_stats.c -o /tmp/tmpp22gukgf.build-temp/./astropy/stats/_stats.o
  In file included from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/stats/_stats.c:698:
  /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/./astropy/stats/_stats.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._utils' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/io/fits/_utils.c -o /tmp/tmpp22gukgf.build-temp/./astropy/io/fits/_utils.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/./astropy/io/fits/_utils.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.lombscargle.implementations.cython_impl' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpp22gukgf.build-temp/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c -o /tmp/tmpp22gukgf.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o
  In file included from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c:698:
  /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.cosmology.flrw.scalar_inv_efuncs' extension
  creating /tmp/tmpp22gukgf.build-temp/astropy/cosmology
  creating /tmp/tmpp22gukgf.build-temp/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/cosmology/flrw/scalar_inv_efuncs.c -o /tmp/tmpp22gukgf.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/cosmology
  creating /tmp/tmpp8lu8gg0.build-lib/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.compiler_version' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/_compiler.c -o /tmp/tmpp22gukgf.build-temp/astropy/_compiler.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmpp22gukgf.build-temp/astropy/_compiler.o -o /tmp/tmpp8lu8gg0.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so -> astropy/wcs
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so -> astropy/convolution
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so -> astropy/utils
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so -> astropy/time
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -> astropy/utils/xml
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so -> astropy/io/votable
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so -> astropy/io/ascii
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/io/fits/_tiled_compression/_compression.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits/_tiled_compression
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/bls
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/lombscargle/implementations
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so -> astropy/cosmology/flrw
  copying /tmp/tmpp8lu8gg0.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so -> astropy
  Editable install will be performed using a meta path finder.

  Options like `package-data`, `include/exclude-package-data` or
  `packages.find.exclude/include` may have no effect.

  adding '__editable___astropy_0_1_dev3_gc0a24c1dc_d20260925_finder.py'
  adding '__editable__.astropy-0.1.dev3+gc0a24c1dc.d20260925.pth'
  creating '/tmp/pip-ephem-wheel-cache-_4v4f46w/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4/tmp3cwoe_t0/.tmp-744tjhio/astropy-0.1.dev3+gc0a24c1dc.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' and adding '/tmp/tmpsfjvnlpbastropy-0.1.dev3+gc0a24c1dc.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' to it
  adding 'astropy-0.1.dev3+gc0a24c1dc.d20260925.dist-info/LICENSE.rst'
  adding 'astropy-0.1.dev3+gc0a24c1dc.d20260925.dist-info/METADATA'
  adding 'astropy-0.1.dev3+gc0a24c1dc.d20260925.dist-info/WHEEL'
  adding 'astropy-0.1.dev3+gc0a24c1dc.d20260925.dist-info/entry_points.txt'
  adding 'astropy-0.1.dev3+gc0a24c1dc.d20260925.dist-info/scm_file_list.json'
  adding 'astropy-0.1.dev3+gc0a24c1dc.d20260925.dist-info/scm_version.json'
  adding 'astropy-0.1.dev3+gc0a24c1dc.d20260925.dist-info/top_level.txt'
  adding 'astropy-0.1.dev3+gc0a24c1dc.d20260925.dist-info/RECORD'
  /tmp/pip-build-env-0dlx6er0/overlay/lib/python3.9/site-packages/setuptools/command/editable_wheel.py:348: InformationOnly: Editable installation.
  !!

          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************

  !!
    wheel_obj.write_files(unpacked)
  Building editable for astropy (pyproject.toml): finished with status 'done'
  Created wheel for astropy: filename=astropy-0.1.dev3+gc0a24c1dc.d20260925-0.editable-cp39-cp39-linux_aarch64.whl size=19611 sha256=9ba952686a262fc5ff9d872b363c3886fabe8105b71b198f37a88bc5e204ed41
  Stored in directory: /tmp/pip-ephem-wheel-cache-_4v4f46w/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4
Successfully built astropy
Installing collected packages: astropy
  Attempting uninstall: astropy
    Found existing installation: astropy 0.1.dev3+gc0a24c1dc.d20260925
    Uninstalling astropy-0.1.dev3+gc0a24c1dc.d20260925:
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fits2bitmap
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitscheck
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsdiff
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsheader
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsinfo
      Removing file or directory /opt/miniconda3/envs/testbed/bin/samp_hub
      Removing file or directory /opt/miniconda3/envs/testbed/bin/showtable
      Removing file or directory /opt/miniconda3/envs/testbed/bin/volint
      Removing file or directory /opt/miniconda3/envs/testbed/bin/wcslint
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable__.astropy-0.1.dev3+gc0a24c1dc.d20260925.pth
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable___astropy_0_1_dev3_gc0a24c1dc_d20260925_finder.py
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__pycache__/__editable___astropy_0_1_dev3_gc0a24c1dc_d20260925_finder.cpython-39.pyc
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astropy-0.1.dev3+gc0a24c1dc.d20260925.dist-info/
      Successfully uninstalled astropy-0.1.dev3+gc0a24c1dc.d20260925
  changing mode of /opt/miniconda3/envs/testbed/bin/fits2bitmap to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitscheck to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsdiff to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsheader to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsinfo to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/samp_hub to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/showtable to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/volint to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/wcslint to 755
Successfully installed astropy-0.1.dev3+gc0a24c1dc.d20260925
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
+ git checkout c0a24c1dc957a3b565294213f435fefb2ec99714 astropy/io/fits/tests/test_diff.py
Updated 0 paths from b8e45d0
+ git apply -v -
Checking patch astropy/io/fits/tests/test_diff.py...
Applied patch astropy/io/fits/tests/test_diff.py cleanly.
+ pytest -rA astropy/io/fits/tests/test_diff.py
<frozen importlib._bootstrap>:228: RuntimeWarning: numpy.ndarray size changed, may indicate binary incompatibility. Expected 80 from C header, got 96 from PyObject
[1m============================= test session starts ==============================[0m
platform linux -- Python 3.9.25, pytest-7.4.0, pluggy-1.3.0

Running tests with Astropy version 0.1.dev3+gc0a24c1dc.d20260925.
Running tests in astropy/io/fits/tests/test_diff.py.

Date: 2026-09-25T05:40:57

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
collected 48 items

astropy/io/fits/tests/test_diff.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31mF[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31mF[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31m [ 77%]
[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31m                                                              [100%][0m

=================================== FAILURES ===================================
[31m[1m________________________ TestDiff.test_identical_tables ________________________[0m

self = <astropy.io.fits.tests.test_diff.TestDiff object at 0xecd5cb673790>

    def test_identical_tables(self):
        c1 = Column("A", format="L", array=[True, False])
        c2 = Column("B", format="X", array=[[0], [1]])
        c3 = Column("C", format="4I", dim="(2, 2)", array=[[0, 1, 2, 3], [4, 5, 6, 7]])
        c4 = Column("D", format="J", bscale=2.0, array=[0, 1])
        c5 = Column("E", format="A3", array=["abc", "def"])
        c6 = Column("F", format="E", unit="m", array=[0.0, 1.0])
        c7 = Column("G", format="D", bzero=-0.1, array=[0.0, 1.0])
        c8 = Column("H", format="C", array=[0.0 + 1.0j, 2.0 + 3.0j])
        c9 = Column("I", format="M", array=[4.0 + 5.0j, 6.0 + 7.0j])
        c10 = Column("J", format="PI(2)", array=[[0, 1], [2, 3]])
        c11 = Column("K", format="QJ(2)", array=[[0, 1], [2, 3]])
    
        columns = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11]
    
        ta = BinTableHDU.from_columns(columns)
        tb = BinTableHDU.from_columns([c.copy() for c in columns])
    
>       diff = TableDataDiff(ta.data, tb.data)

[1m[31mastropy/io/fits/tests/test_diff.py[0m:416: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
[1m[31mastropy/io/fits/diff.py[0m:1342: in __init__
    super().__init__(a, b)
[1m[31mastropy/io/fits/diff.py[0m:87: in __init__
    self._diff()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.diff.TableDataDiff object at 0xecd5de0bb220>

    def _diff(self):
        # Much of the code for comparing columns is similar to the code for
        # comparing headers--consider refactoring
        colsa = self.a.columns
        colsb = self.b.columns
    
        if len(colsa) != len(colsb):
            self.diff_column_count = (len(colsa), len(colsb))
    
        # Even if the number of columns are unequal, we still do comparison of
        # any common columns
        colsa = {c.name.lower(): c for c in colsa}
        colsb = {c.name.lower(): c for c in colsb}
    
        if "*" in self.ignore_fields:
            # If all columns are to be ignored, ignore any further differences
            # between the columns
            return
    
        # Keep the user's original ignore_fields list for reporting purposes,
        # but internally use a case-insensitive version
        ignore_fields = {f.lower() for f in self.ignore_fields}
    
        # It might be nice if there were a cleaner way to do this, but for now
        # it'll do
        for fieldname in ignore_fields:
            fieldname = fieldname.lower()
            if fieldname in colsa:
                del colsa[fieldname]
            if fieldname in colsb:
                del colsb[fieldname]
    
        colsa_set = set(colsa.values())
        colsb_set = set(colsb.values())
        self.common_columns = sorted(
            colsa_set.intersection(colsb_set), key=operator.attrgetter("name")
        )
    
        self.common_column_names = {col.name.lower() for col in self.common_columns}
    
        left_only_columns = {
            col.name.lower(): col for col in colsa_set.difference(colsb_set)
        }
        right_only_columns = {
            col.name.lower(): col for col in colsb_set.difference(colsa_set)
        }
    
        if left_only_columns or right_only_columns:
            self.diff_columns = (left_only_columns, right_only_columns)
            self.diff_column_names = ([], [])
    
        if left_only_columns:
            for col in self.a.columns:
                if col.name.lower() in left_only_columns:
                    self.diff_column_names[0].append(col.name)
    
        if right_only_columns:
            for col in self.b.columns:
                if col.name.lower() in right_only_columns:
                    self.diff_column_names[1].append(col.name)
    
        # If the tables have a different number of rows, we don't compare the
        # columns right now.
        # TODO: It might be nice to optionally compare the first n rows where n
        # is the minimum of the row counts between the two tables.
        if len(self.a) != len(self.b):
            self.diff_rows = (len(self.a), len(self.b))
            return
    
        # If the tables contain no rows there's no data to compare, so we're
        # done at this point. (See ticket #178)
        if len(self.a) == len(self.b) == 0:
            return
    
        # Like in the old fitsdiff, compare tables on a column by column basis
        # The difficulty here is that, while FITS column names are meant to be
        # case-insensitive, Astropy still allows, for the sake of flexibility,
        # two columns with the same name but different case.  When columns are
        # accessed in FITS tables, a case-sensitive is tried first, and failing
        # that a case-insensitive match is made.
        # It's conceivable that the same column could appear in both tables
        # being compared, but with different case.
        # Though it *may* lead to inconsistencies in these rare cases, this
        # just assumes that there are no duplicated column names in either
        # table, and that the column names can be treated case-insensitively.
        for col in self.common_columns:
            name_lower = col.name.lower()
            if name_lower in ignore_fields:
                continue
    
            cola = colsa[name_lower]
            colb = colsb[name_lower]
    
            for attr, _ in _COL_ATTRS:
                vala = getattr(cola, attr, None)
                valb = getattr(colb, attr, None)
                if diff_values(vala, valb):
                    self.diff_column_attributes.append(
                        ((col.name.upper(), attr), (vala, valb))
                    )
    
            arra = self.a[col.name]
            arrb = self.b[col.name]
    
            if np.issubdtype(arra.dtype, np.floating) and np.issubdtype(
                arrb.dtype, np.floating
            ):
                diffs = where_not_allclose(arra, arrb, rtol=self.rtol, atol=self.atol)
            elif "P" in col.format:
                diffs = (
                    [
                        idx
                        for idx in range(len(arra))
                        if not np.allclose(
                            arra[idx], arrb[idx], rtol=self.rtol, atol=self.atol
                        )
                    ],
                )
            else:
>               diffs = np.where(arra != arrb)
[1m[31mE               ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()[0m

[1m[31mastropy/io/fits/diff.py[0m:1463: ValueError
[31m[1m______________________ TestDiff.test_different_table_data ______________________[0m

self = <astropy.io.fits.tests.test_diff.TestDiff object at 0xecd5cb457ca0>

    def test_different_table_data(self):
        """
        Test diffing table data on columns of several different data formats
        and dimensions.
        """
    
        ca1 = Column("A", format="L", array=[True, False])
        ca2 = Column("B", format="X", array=[[0], [1]])
        ca3 = Column("C", format="4I", dim="(2, 2)", array=[[0, 1, 2, 3], [4, 5, 6, 7]])
        ca4 = Column("D", format="J", bscale=2.0, array=[0.0, 2.0])
        ca5 = Column("E", format="A3", array=["abc", "def"])
        ca6 = Column("F", format="E", unit="m", array=[0.0, 1.0])
        ca7 = Column("G", format="D", bzero=-0.1, array=[0.0, 1.0])
        ca8 = Column("H", format="C", array=[0.0 + 1.0j, 2.0 + 3.0j])
        ca9 = Column("I", format="M", array=[4.0 + 5.0j, 6.0 + 7.0j])
        ca10 = Column("J", format="PI(2)", array=[[0, 1], [2, 3]])
        ca11 = Column("K", format="QJ(2)", array=[[0, 1], [2, 3]])
    
        cb1 = Column("A", format="L", array=[False, False])
        cb2 = Column("B", format="X", array=[[0], [0]])
        cb3 = Column("C", format="4I", dim="(2, 2)", array=[[0, 1, 2, 3], [5, 6, 7, 8]])
        cb4 = Column("D", format="J", bscale=2.0, array=[2.0, 2.0])
        cb5 = Column("E", format="A3", array=["abc", "ghi"])
        cb6 = Column("F", format="E", unit="m", array=[1.0, 2.0])
        cb7 = Column("G", format="D", bzero=-0.1, array=[2.0, 3.0])
        cb8 = Column("H", format="C", array=[1.0 + 1.0j, 2.0 + 3.0j])
        cb9 = Column("I", format="M", array=[5.0 + 5.0j, 6.0 + 7.0j])
        cb10 = Column("J", format="PI(2)", array=[[1, 2], [3, 4]])
        cb11 = Column("K", format="QJ(2)", array=[[1, 2], [3, 4]])
    
        ta = BinTableHDU.from_columns(
            [ca1, ca2, ca3, ca4, ca5, ca6, ca7, ca8, ca9, ca10, ca11]
        )
        tb = BinTableHDU.from_columns(
            [cb1, cb2, cb3, cb4, cb5, cb6, cb7, cb8, cb9, cb10, cb11]
        )
    
>       diff = TableDataDiff(ta.data, tb.data, numdiffs=20)

[1m[31mastropy/io/fits/tests/test_diff.py[0m:574: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
[1m[31mastropy/io/fits/diff.py[0m:1342: in __init__
    super().__init__(a, b)
[1m[31mastropy/io/fits/diff.py[0m:87: in __init__
    self._diff()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.diff.TableDataDiff object at 0xecd5cb472b50>

    def _diff(self):
        # Much of the code for comparing columns is similar to the code for
        # comparing headers--consider refactoring
        colsa = self.a.columns
        colsb = self.b.columns
    
        if len(colsa) != len(colsb):
            self.diff_column_count = (len(colsa), len(colsb))
    
        # Even if the number of columns are unequal, we still do comparison of
        # any common columns
        colsa = {c.name.lower(): c for c in colsa}
        colsb = {c.name.lower(): c for c in colsb}
    
        if "*" in self.ignore_fields:
            # If all columns are to be ignored, ignore any further differences
            # between the columns
            return
    
        # Keep the user's original ignore_fields list for reporting purposes,
        # but internally use a case-insensitive version
        ignore_fields = {f.lower() for f in self.ignore_fields}
    
        # It might be nice if there were a cleaner way to do this, but for now
        # it'll do
        for fieldname in ignore_fields:
            fieldname = fieldname.lower()
            if fieldname in colsa:
                del colsa[fieldname]
            if fieldname in colsb:
                del colsb[fieldname]
    
        colsa_set = set(colsa.values())
        colsb_set = set(colsb.values())
        self.common_columns = sorted(
            colsa_set.intersection(colsb_set), key=operator.attrgetter("name")
        )
    
        self.common_column_names = {col.name.lower() for col in self.common_columns}
    
        left_only_columns = {
            col.name.lower(): col for col in colsa_set.difference(colsb_set)
        }
        right_only_columns = {
            col.name.lower(): col for col in colsb_set.difference(colsa_set)
        }
    
        if left_only_columns or right_only_columns:
            self.diff_columns = (left_only_columns, right_only_columns)
            self.diff_column_names = ([], [])
    
        if left_only_columns:
            for col in self.a.columns:
                if col.name.lower() in left_only_columns:
                    self.diff_column_names[0].append(col.name)
    
        if right_only_columns:
            for col in self.b.columns:
                if col.name.lower() in right_only_columns:
                    self.diff_column_names[1].append(col.name)
    
        # If the tables have a different number of rows, we don't compare the
        # columns right now.
        # TODO: It might be nice to optionally compare the first n rows where n
        # is the minimum of the row counts between the two tables.
        if len(self.a) != len(self.b):
            self.diff_rows = (len(self.a), len(self.b))
            return
    
        # If the tables contain no rows there's no data to compare, so we're
        # done at this point. (See ticket #178)
        if len(self.a) == len(self.b) == 0:
            return
    
        # Like in the old fitsdiff, compare tables on a column by column basis
        # The difficulty here is that, while FITS column names are meant to be
        # case-insensitive, Astropy still allows, for the sake of flexibility,
        # two columns with the same name but different case.  When columns are
        # accessed in FITS tables, a case-sensitive is tried first, and failing
        # that a case-insensitive match is made.
        # It's conceivable that the same column could appear in both tables
        # being compared, but with different case.
        # Though it *may* lead to inconsistencies in these rare cases, this
        # just assumes that there are no duplicated column names in either
        # table, and that the column names can be treated case-insensitively.
        for col in self.common_columns:
            name_lower = col.name.lower()
            if name_lower in ignore_fields:
                continue
    
            cola = colsa[name_lower]
            colb = colsb[name_lower]
    
            for attr, _ in _COL_ATTRS:
                vala = getattr(cola, attr, None)
                valb = getattr(colb, attr, None)
                if diff_values(vala, valb):
                    self.diff_column_attributes.append(
                        ((col.name.upper(), attr), (vala, valb))
                    )
    
            arra = self.a[col.name]
            arrb = self.b[col.name]
    
            if np.issubdtype(arra.dtype, np.floating) and np.issubdtype(
                arrb.dtype, np.floating
            ):
                diffs = where_not_allclose(arra, arrb, rtol=self.rtol, atol=self.atol)
            elif "P" in col.format:
                diffs = (
                    [
                        idx
                        for idx in range(len(arra))
                        if not np.allclose(
                            arra[idx], arrb[idx], rtol=self.rtol, atol=self.atol
                        )
                    ],
                )
            else:
>               diffs = np.where(arra != arrb)
[1m[31mE               ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()[0m

[1m[31mastropy/io/fits/diff.py[0m:1463: ValueError
==================================== PASSES ====================================
[36m[1m=========================== short test summary info ============================[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_identical_headers[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_slightly_different_headers[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_common_keywords[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_keyword_count[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_keywords[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_keyword_values[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_keyword_comments[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_keyword_values_with_duplicate[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_asymmetric_duplicate_keywords[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_floating_point_rtol[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_floating_point_atol[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_ignore_blanks[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_ignore_blank_cards[HeaderDiff][0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_ignore_blank_cards[HDUDiff][0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_ignore_blank_cards[FITSDiff][0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_ignore_hdus[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_ignore_keyword_values[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_ignore_keyword_comments[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_trivial_identical_images[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_identical_within_relative_tolerance[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_identical_within_absolute_tolerance[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_identical_within_rtol_and_atol[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_not_identical_within_rtol_and_atol[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_identical_comp_image_hdus[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_dimensions[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_pixels[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_diff_empty_tables[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_ignore_table_fields[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_table_field_names[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_table_field_counts[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_table_rows[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_identical_files_basic[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_partially_identical_files1[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_partially_identical_files2[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_partially_identical_files3[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_diff_nans[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_file_output_from_path_string[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_file_output_overwrite_safety[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_file_output_overwrite_success[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_rawdatadiff_nodiff[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_rawdatadiff_dimsdiff[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_rawdatadiff_bytesdiff[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mtest_fitsdiff_hdu_name[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mtest_fitsdiff_no_hdu_name[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mtest_fitsdiff_with_names[0m
[32mPASSED[0m astropy/io/fits/tests/test_diff.py::[1mtest_rawdatadiff_diff_with_rtol[0m
[31mFAILED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_identical_tables[0m - ValueError: The truth value of an array with more than one element is ambig...
[31mFAILED[0m astropy/io/fits/tests/test_diff.py::[1mTestDiff::test_different_table_data[0m - ValueError: The truth value of an array with more than one element is ambig...
[31m========================= [31m[1m2 failed[0m, [32m46 passed[0m[31m in 0.16s[0m[31m =========================[0m
+ git checkout c0a24c1dc957a3b565294213f435fefb2ec99714 astropy/io/fits/tests/test_diff.py
Updated 1 path from b8e45d0

```
