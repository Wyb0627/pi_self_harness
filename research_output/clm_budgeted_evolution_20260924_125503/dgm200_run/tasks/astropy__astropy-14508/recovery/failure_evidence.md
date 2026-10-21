# Official SWE-bench Evaluator Feedback

This is hidden evaluator information from the rejected original Pi submission. The resulting repair is feedback-assisted and is not a standard one-submission SWE-bench prediction.

Instance: `astropy__astropy-14508`

## Report

```json
{
    "astropy__astropy-14508": {
        "patch_is_None": false,
        "patch_exists": true,
        "patch_successfully_applied": true,
        "resolved": false,
        "tests_status": {
            "FAIL_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_floating_point_string_representation_card"
                ]
            },
            "PASS_TO_PASS": {
                "success": [
                    "astropy/io/fits/tests/test_header.py::test_shallow_copy",
                    "astropy/io/fits/tests/test_header.py::test_init_with_header",
                    "astropy/io/fits/tests/test_header.py::test_init_with_dict",
                    "astropy/io/fits/tests/test_header.py::test_init_with_ordereddict",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_rename_keyword",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_indexing_case[A]",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_indexing_case[a]",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_card_constructor_default_args",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_card_from_bytes",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_string_value_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_boolean_value_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_integer_value_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_floating_point_value_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_complex_value_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_card_image_constructed_too_long",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_constructor_filter_illegal_data_structures",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_keyword_too_long",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_illegal_characters_in_key",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_add_history",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_add_blank",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_comment",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_cards",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_card_created_by_fromstring",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_card_will_not_parse_numerical_value",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_equal_sign_after_column8",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_blank_keyword",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_specify_undefined_value",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_complex_number_using_string_input",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_fixable_non_standard_fits_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_fixable_non_fsc",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_undefined_value_using_string_input",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_undefined_keys_values",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_mislocated_equal_sign",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_equal_only_up_to_column_10",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_verify_invalid_equal_sign",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_fix_invalid_equal_sign",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_string_value",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_string_value_with_multiple_long_words",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_unicode_string",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_string_repr",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_blank_keyword_long_value",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_string_from_file",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_word_in_long_string_too_long",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_string_value_via_fromstring",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_continue_card_with_equals_in_value",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_final_continue_card_lacks_ampersand",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_final_continue_card_ampersand_removal_on_long_comments",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_card_creation",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_with_abbrev_value_indicator",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_not_warn",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_keyword_whitespace",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_verify_mixed_case_hierarch",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_missing_keyword",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_card_lookup",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_card_delete",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_card_insert_delete",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_create_and_update",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_short_hierarch_create_and_update",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_setitem_invalid",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_setitem_1tuple",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_setitem_2tuple",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_set_value_to_none",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_set_comment_only",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_iter",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_slice",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_slice_assignment",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_slice_delete",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_wildcard_slice",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_wildcard_with_hyphen",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_wildcard_slice_assignment",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_wildcard_slice_deletion",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_history",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_clear",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_clear_write[fitsext0]",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_clear_write[fitsext1]",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromkeys",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromkeys_with_value",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromkeys_with_value_and_comment",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromkeys_with_duplicates",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_items",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_iterkeys",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_itervalues",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_keys",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_list_like_pop",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_dict_like_pop",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_popitem",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_setdefault",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_from_dict",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_from_iterable",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_unique",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_unique_commentary",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_update",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_update_commentary",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_exact",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_count",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_append_use_blanks",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_append_keyword_only",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_insert_use_blanks",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_insert_before_keyword",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_remove",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_comments",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_comment_slices_and_filters",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_comment_slice_filter_assign",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_slicing",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_commentary",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_comparison",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_commentary_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_totxtfile[]",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_totxtfile[home_is_data]",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_totxtfile[home_is_data,",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_tofile[]",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_tofile[home_is_data]",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_tofile[home_is_data,",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_fromfile",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromtextfile",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromtextfile_with_end_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_append_end_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_end_cards",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_characters",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_unnecessary_move",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_float_cards",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_float_cards2",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_leading_zeros",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_assign_boolean",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_method_keyword_normalization",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_end_in_comment",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_assign_unicode",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_assign_non_ascii",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_strip_whitespace",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_keep_duplicate_history_in_orig_header",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_keyword_cards",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_fix_hierarch_with_invalid_value",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_assign_inf_nan",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_bool",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_numeric",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_newlines_in_commentary",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_commentary_card_appended_to_header",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromstring_bytes",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_set_keyword_with_space",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_strip",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_invalid_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_index_numpy_int",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_data_size",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_initialize_rvkc",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_parse_field_specifier",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_update_field_specifier",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_field_specifier_case_senstivity",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_get_rvkc_by_index",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_get_rvkc_by_keyword",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_get_rvkc_by_keyword_and_field_specifier",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_access_nonexistent_rvkc",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_update_rvkc",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_update_rvkc_2",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_raw_keyword_value",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_insert_after",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_delete",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_pattern_matching_keys",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_pattern_matching_key_deletion",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_successive_pattern_matching",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_in_cardlist_keys",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_in_cardlist_values",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_value_attribute",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_overly_permissive_parsing",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_overly_aggressive_rvkc_lookup",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_fitsheader_script",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_fitsheader_compressed_from_primary_image_ext",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_fitsheader_table_feature",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[wb]",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[wb+]",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[ab]",
                    "astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[ab+]",
                    "astropy/io/fits/tests/test_header.py::test_subclass"
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
0od.build-temp/astropy/utils/src/compiler.o
  creating /tmp/tmpufyklplh.build-lib/astropy/utils
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/utils/src/compiler.o -o /tmp/tmpufyklplh.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so
  building 'astropy.table._np_utils' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/table
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/table/_np_utils.c -o /tmp/tmp__oqk0od.build-temp/astropy/table/_np_utils.o
  In file included from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/table/_np_utils.c:698:
  /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmpufyklplh.build-lib/astropy/table
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/table/_np_utils.o -o /tmp/tmpufyklplh.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.table._column_mixins' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/table/_column_mixins.c -o /tmp/tmp__oqk0od.build-temp/astropy/table/_column_mixins.o
  In file included from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/table/_column_mixins.c:696:
  /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  In file included from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:21,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/table/_column_mixins.c:696:
  /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/__multiarray_api.h:1463:1: warning: ‘_import_array’ defined but not used [-Wunused-function]
   1463 | _import_array(void)
        | ^~~~~~~~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/table/_column_mixins.o -o /tmp/tmpufyklplh.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._fast_sigma_clip' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/stats
  creating /tmp/tmp__oqk0od.build-temp/astropy/stats/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/src/compute_bounds.c -o /tmp/tmp__oqk0od.build-temp/astropy/stats/src/compute_bounds.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/src/fast_sigma_clip.c -o /tmp/tmp__oqk0od.build-temp/astropy/stats/src/fast_sigma_clip.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/stats/src/wirth_select.c -o /tmp/tmp__oqk0od.build-temp/astropy/stats/src/wirth_select.o
  creating /tmp/tmpufyklplh.build-lib/astropy/stats
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/stats/src/compute_bounds.o /tmp/tmp__oqk0od.build-temp/astropy/stats/src/fast_sigma_clip.o /tmp/tmp__oqk0od.build-temp/astropy/stats/src/wirth_select.o -o /tmp/tmpufyklplh.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so
  building 'astropy.time._parse_times' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/time
  creating /tmp/tmp__oqk0od.build-temp/astropy/time/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/time/src/parse_times.c -o /tmp/tmp__oqk0od.build-temp/astropy/time/src/parse_times.o
  creating /tmp/tmpufyklplh.build-lib/astropy/time
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/time/src/parse_times.o -o /tmp/tmpufyklplh.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so
  building 'astropy.utils.xml._iterparser' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/utils/xml
  creating /tmp/tmp__oqk0od.build-temp/astropy/utils/xml/src
  creating /tmp/tmp__oqk0od.build-temp/cextern/expat
  creating /tmp/tmp__oqk0od.build-temp/cextern/expat/lib
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/utils/xml/src/iterparse.c -o /tmp/tmp__oqk0od.build-temp/astropy/utils/xml/src/iterparse.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmlparse.c -o /tmp/tmp__oqk0od.build-temp/cextern/expat/lib/xmlparse.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmlrole.c -o /tmp/tmp__oqk0od.build-temp/cextern/expat/lib/xmlrole.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmltok.c -o /tmp/tmp__oqk0od.build-temp/cextern/expat/lib/xmltok.o
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -DHAVE_EXPAT_CONFIG_H=1 -DBYTEORDER=1234 -DHAVE_UNISTD_H -Iastropy/utils/xml/src -Icextern/expat/lib -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/expat/lib/xmltok_impl.c -o /tmp/tmp__oqk0od.build-temp/cextern/expat/lib/xmltok_impl.o
  creating /tmp/tmpufyklplh.build-lib/astropy/utils/xml
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/utils/xml/src/iterparse.o /tmp/tmp__oqk0od.build-temp/cextern/expat/lib/xmlparse.o /tmp/tmp__oqk0od.build-temp/cextern/expat/lib/xmlrole.o /tmp/tmp__oqk0od.build-temp/cextern/expat/lib/xmltok.o /tmp/tmp__oqk0od.build-temp/cextern/expat/lib/xmltok_impl.o -o /tmp/tmpufyklplh.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -Wl,--version-script=astropy/utils/xml/src/iterparse.map
  building 'astropy.io.votable.tablewriter' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/io
  creating /tmp/tmp__oqk0od.build-temp/astropy/io/votable
  creating /tmp/tmp__oqk0od.build-temp/astropy/io/votable/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/votable/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/votable/src/tablewriter.c -o /tmp/tmp__oqk0od.build-temp/astropy/io/votable/src/tablewriter.o
  astropy/io/votable/src/tablewriter.c: In function ‘write_tabledata’:
  astropy/io/votable/src/tablewriter.c:270:30: warning: assignment discards ‘const’ qualifier from pointer target type [-Wdiscarded-qualifiers]
    270 |                 if ((str_tmp = PyUnicode_AsUTF8AndSize(str_val, &str_len)) == NULL) {
        |                              ^
  creating /tmp/tmpufyklplh.build-lib/astropy/io
  creating /tmp/tmpufyklplh.build-lib/astropy/io/votable
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/io/votable/src/tablewriter.o -o /tmp/tmpufyklplh.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.ascii.cparser' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/io/ascii
  creating /tmp/tmp__oqk0od.build-temp/astropy/io/ascii/src
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/cparser.c -o /tmp/tmp__oqk0od.build-temp/astropy/io/ascii/cparser.o
  In file included from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/io/ascii/cparser.c:698:
  /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/ascii/src/tokenizer.c -o /tmp/tmp__oqk0od.build-temp/astropy/io/ascii/src/tokenizer.o
  astropy/io/ascii/src/tokenizer.c: In function ‘push’:
  astropy/io/ascii/src/tokenizer.c:124:54: warning: comparison of integer expressions of different signedness: ‘long int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
    124 |     if (self->col_ptrs[col] - self->output_cols[col] >=
        |                                                      ^~
  astropy/io/ascii/src/tokenizer.c: In function ‘tokenize’:
  astropy/io/ascii/src/tokenizer.c:424:42: warning: comparison of integer expressions of different signedness: ‘size_t’ {aka ‘long unsigned int’} and ‘int’ [-Wsign-compare]
    424 |                     if (self->source_pos == -1
        |                                          ^~
  creating /tmp/tmpufyklplh.build-lib/astropy/io/ascii
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/io/ascii/cparser.o /tmp/tmp__oqk0od.build-temp/astropy/io/ascii/src/tokenizer.o -o /tmp/tmpufyklplh.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._tiled_compression._compression' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/io/fits
  creating /tmp/tmp__oqk0od.build-temp/astropy/io/fits/_tiled_compression
  creating /tmp/tmp__oqk0od.build-temp/astropy/io/fits/_tiled_compression/src
  creating /tmp/tmp__oqk0od.build-temp/cextern/cfitsio
  creating /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/fits/_tiled_compression/src/compression.c -o /tmp/tmp__oqk0od.build-temp/astropy/io/fits/_tiled_compression/src/compression.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/io/fits/_tiled_compression/src/unquantize.c -o /tmp/tmp__oqk0od.build-temp/astropy/io/fits/_tiled_compression/src/unquantize.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/fits_hcompress.c -o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/fits_hcompress.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/fits_hdecompress.c -o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/fits_hdecompress.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/pliocomp.c -o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/pliocomp.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/quantize.c -o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/quantize.o
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
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -Iastropy/io/fits/_tiled_compression/src -I/opt/miniconda3/envs/testbed/include/python3.9 -c cextern/cfitsio/lib/ricecomp.c -o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/ricecomp.o
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
  creating /tmp/tmpufyklplh.build-lib/astropy/io/fits
  creating /tmp/tmpufyklplh.build-lib/astropy/io/fits/_tiled_compression
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/io/fits/_tiled_compression/src/compression.o /tmp/tmp__oqk0od.build-temp/astropy/io/fits/_tiled_compression/src/unquantize.o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/fits_hcompress.o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/fits_hdecompress.o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/pliocomp.o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/quantize.o /tmp/tmp__oqk0od.build-temp/cextern/cfitsio/lib/ricecomp.o -o /tmp/tmpufyklplh.build-lib/astropy/io/fits/_tiled_compression/_compression.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.bls._impl' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/timeseries
  creating /tmp/tmp__oqk0od.build-temp/astropy/timeseries/periodograms
  creating /tmp/tmp__oqk0od.build-temp/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/_impl.c -o /tmp/tmp__oqk0od.build-temp/astropy/timeseries/periodograms/bls/_impl.o
  In file included from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from astropy/timeseries/periodograms/bls/_impl.c:698:
  /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/timeseries/periodograms/bls/bls.c -o /tmp/tmp__oqk0od.build-temp/astropy/timeseries/periodograms/bls/bls.o
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
  creating /tmp/tmpufyklplh.build-lib/astropy/timeseries
  creating /tmp/tmpufyklplh.build-lib/astropy/timeseries/periodograms
  creating /tmp/tmpufyklplh.build-lib/astropy/timeseries/periodograms/bls
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/timeseries/periodograms/bls/_impl.o /tmp/tmp__oqk0od.build-temp/astropy/timeseries/periodograms/bls/bls.o -o /tmp/tmpufyklplh.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.stats._stats' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/stats/_stats.c -o /tmp/tmp__oqk0od.build-temp/./astropy/stats/_stats.o
  In file included from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/stats/_stats.c:698:
  /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/./astropy/stats/_stats.o -o /tmp/tmpufyklplh.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so
  building 'astropy.io.fits._utils' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/io/fits/_utils.c -o /tmp/tmp__oqk0od.build-temp/./astropy/io/fits/_utils.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/./astropy/io/fits/_utils.o -o /tmp/tmpufyklplh.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so
  building 'astropy.timeseries.periodograms.lombscargle.implementations.cython_impl' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmp__oqk0od.build-temp/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c -o /tmp/tmp__oqk0od.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o
  In file included from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1822,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                   from /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4,
                   from ./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.c:698:
  /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
     17 | #warning "Using deprecated NumPy API, disable it with " \
        |  ^~~~~~~
  creating /tmp/tmpufyklplh.build-lib/astropy/timeseries/periodograms/lombscargle
  creating /tmp/tmpufyklplh.build-lib/astropy/timeseries/periodograms/lombscargle/implementations
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/./astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.o -o /tmp/tmpufyklplh.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so
  building 'astropy.cosmology.flrw.scalar_inv_efuncs' extension
  creating /tmp/tmp__oqk0od.build-temp/astropy/cosmology
  creating /tmp/tmp__oqk0od.build-temp/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/numpy/core/include -I/opt/miniconda3/envs/testbed/include/python3.9 -c ./astropy/cosmology/flrw/scalar_inv_efuncs.c -o /tmp/tmp__oqk0od.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o
  creating /tmp/tmpufyklplh.build-lib/astropy/cosmology
  creating /tmp/tmpufyklplh.build-lib/astropy/cosmology/flrw
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/./astropy/cosmology/flrw/scalar_inv_efuncs.o -o /tmp/tmpufyklplh.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so
  building 'astropy.compiler_version' extension
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -Wno-unused-result -Wsign-compare -DNDEBUG -O2 -Wall -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -I/opt/miniconda3/envs/testbed/include -fPIC -O2 -isystem /opt/miniconda3/envs/testbed/include -fPIC -I/opt/miniconda3/envs/testbed/include/python3.9 -c astropy/_compiler.c -o /tmp/tmp__oqk0od.build-temp/astropy/_compiler.o
  gcc -pthread -B /opt/miniconda3/envs/testbed/compiler_compat -shared -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib -Wl,-rpath,/opt/miniconda3/envs/testbed/lib -Wl,-rpath-link,/opt/miniconda3/envs/testbed/lib -L/opt/miniconda3/envs/testbed/lib /tmp/tmp__oqk0od.build-temp/astropy/_compiler.o -o /tmp/tmpufyklplh.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so
  copying /tmp/tmpufyklplh.build-lib/astropy/wcs/_wcs.cpython-39-aarch64-linux-gnu.so -> astropy/wcs
  copying /tmp/tmpufyklplh.build-lib/astropy/convolution/_convolve.cpython-39-aarch64-linux-gnu.so -> astropy/convolution
  copying /tmp/tmpufyklplh.build-lib/astropy/utils/_compiler.cpython-39-aarch64-linux-gnu.so -> astropy/utils
  copying /tmp/tmpufyklplh.build-lib/astropy/table/_np_utils.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpufyklplh.build-lib/astropy/table/_column_mixins.cpython-39-aarch64-linux-gnu.so -> astropy/table
  copying /tmp/tmpufyklplh.build-lib/astropy/stats/_fast_sigma_clip.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpufyklplh.build-lib/astropy/time/_parse_times.cpython-39-aarch64-linux-gnu.so -> astropy/time
  copying /tmp/tmpufyklplh.build-lib/astropy/utils/xml/_iterparser.cpython-39-aarch64-linux-gnu.so -> astropy/utils/xml
  copying /tmp/tmpufyklplh.build-lib/astropy/io/votable/tablewriter.cpython-39-aarch64-linux-gnu.so -> astropy/io/votable
  copying /tmp/tmpufyklplh.build-lib/astropy/io/ascii/cparser.cpython-39-aarch64-linux-gnu.so -> astropy/io/ascii
  copying /tmp/tmpufyklplh.build-lib/astropy/io/fits/_tiled_compression/_compression.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits/_tiled_compression
  copying /tmp/tmpufyklplh.build-lib/astropy/timeseries/periodograms/bls/_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/bls
  copying /tmp/tmpufyklplh.build-lib/astropy/stats/_stats.cpython-39-aarch64-linux-gnu.so -> astropy/stats
  copying /tmp/tmpufyklplh.build-lib/astropy/io/fits/_utils.cpython-39-aarch64-linux-gnu.so -> astropy/io/fits
  copying /tmp/tmpufyklplh.build-lib/astropy/timeseries/periodograms/lombscargle/implementations/cython_impl.cpython-39-aarch64-linux-gnu.so -> astropy/timeseries/periodograms/lombscargle/implementations
  copying /tmp/tmpufyklplh.build-lib/astropy/cosmology/flrw/scalar_inv_efuncs.cpython-39-aarch64-linux-gnu.so -> astropy/cosmology/flrw
  copying /tmp/tmpufyklplh.build-lib/astropy/compiler_version.cpython-39-aarch64-linux-gnu.so -> astropy
  Editable install will be performed using a meta path finder.

  Options like `package-data`, `include/exclude-package-data` or
  `packages.find.exclude/include` may have no effect.

  adding '__editable___astropy_0_1_dev3_ga3f4ae6cd_d20260925_finder.py'
  adding '__editable__.astropy-0.1.dev3+ga3f4ae6cd.d20260925.pth'
  creating '/tmp/pip-ephem-wheel-cache-vcq2kmwx/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4/tmp20sbm23v/.tmp-d00zyfds/astropy-0.1.dev3+ga3f4ae6cd.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' and adding '/tmp/tmpwnknv5otastropy-0.1.dev3+ga3f4ae6cd.d20260925-0.editable-cp39-cp39-linux_aarch64.whl' to it
  adding 'astropy-0.1.dev3+ga3f4ae6cd.d20260925.dist-info/LICENSE.rst'
  adding 'astropy-0.1.dev3+ga3f4ae6cd.d20260925.dist-info/METADATA'
  adding 'astropy-0.1.dev3+ga3f4ae6cd.d20260925.dist-info/WHEEL'
  adding 'astropy-0.1.dev3+ga3f4ae6cd.d20260925.dist-info/entry_points.txt'
  adding 'astropy-0.1.dev3+ga3f4ae6cd.d20260925.dist-info/scm_file_list.json'
  adding 'astropy-0.1.dev3+ga3f4ae6cd.d20260925.dist-info/scm_version.json'
  adding 'astropy-0.1.dev3+ga3f4ae6cd.d20260925.dist-info/top_level.txt'
  adding 'astropy-0.1.dev3+ga3f4ae6cd.d20260925.dist-info/RECORD'
  /tmp/pip-build-env-b9iiett0/overlay/lib/python3.9/site-packages/setuptools/command/editable_wheel.py:348: InformationOnly: Editable installation.
  !!

          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************

  !!
    wheel_obj.write_files(unpacked)
  Building editable for astropy (pyproject.toml): finished with status 'done'
  Created wheel for astropy: filename=astropy-0.1.dev3+ga3f4ae6cd.d20260925-0.editable-cp39-cp39-linux_aarch64.whl size=19597 sha256=cea242875e14bc7d0f0d9f244af3653a4abf95c621086c0316903010d74cc82a
  Stored in directory: /tmp/pip-ephem-wheel-cache-vcq2kmwx/wheels/7d/66/67/70d1ee2124ccf21d601c352e25cdca10f611f7c8b3f9ffb9e4
Successfully built astropy
Installing collected packages: astropy
  Attempting uninstall: astropy
    Found existing installation: astropy 0.1.dev3+ga3f4ae6cd.d20260925
    Uninstalling astropy-0.1.dev3+ga3f4ae6cd.d20260925:
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fits2bitmap
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitscheck
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsdiff
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsheader
      Removing file or directory /opt/miniconda3/envs/testbed/bin/fitsinfo
      Removing file or directory /opt/miniconda3/envs/testbed/bin/samp_hub
      Removing file or directory /opt/miniconda3/envs/testbed/bin/showtable
      Removing file or directory /opt/miniconda3/envs/testbed/bin/volint
      Removing file or directory /opt/miniconda3/envs/testbed/bin/wcslint
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable__.astropy-0.1.dev3+ga3f4ae6cd.d20260925.pth
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__editable___astropy_0_1_dev3_ga3f4ae6cd_d20260925_finder.py
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/__pycache__/__editable___astropy_0_1_dev3_ga3f4ae6cd_d20260925_finder.cpython-39.pyc
      Removing file or directory /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/astropy-0.1.dev3+ga3f4ae6cd.d20260925.dist-info/
      Successfully uninstalled astropy-0.1.dev3+ga3f4ae6cd.d20260925
  changing mode of /opt/miniconda3/envs/testbed/bin/fits2bitmap to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitscheck to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsdiff to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsheader to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/fitsinfo to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/samp_hub to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/showtable to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/volint to 755
  changing mode of /opt/miniconda3/envs/testbed/bin/wcslint to 755
Successfully installed astropy-0.1.dev3+ga3f4ae6cd.d20260925
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
+ git checkout a3f4ae6cd24d5ecdf49f213d77b3513dd509a06c astropy/io/fits/tests/test_header.py
Updated 0 paths from 36c2e27
+ git apply -v -
Checking patch astropy/io/fits/tests/test_header.py...
Applied patch astropy/io/fits/tests/test_header.py cleanly.
+ pytest -rA astropy/io/fits/tests/test_header.py
<frozen importlib._bootstrap>:228: RuntimeWarning: numpy.ndarray size changed, may indicate binary incompatibility. Expected 80 from C header, got 96 from PyObject
[1m============================= test session starts ==============================[0m
platform linux -- Python 3.9.25, pytest-7.4.0, pluggy-1.3.0

Running tests with Astropy version 0.1.dev3+ga3f4ae6cd.d20260925.
Running tests in astropy/io/fits/tests/test_header.py.

Date: 2026-09-25T05:31:10

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
collected 175 items

astropy/io/fits/tests/test_header.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31mF[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31m [ 20%]
[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31m [ 61%]
[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[31m     [100%][0m

=================================== FAILURES ===================================
[31m[1m______ TestHeaderFunctions.test_floating_point_string_representation_card ______[0m

self = <astropy.io.fits.tests.test_header.TestHeaderFunctions object at 0xea0d1f439c10>

    def test_floating_point_string_representation_card(self):
        """
        Ensures Card formats float values with the correct precision, avoiding
        comment truncation
    
        Regression test for https://github.com/astropy/astropy/issues/14507
        """
        k = "HIERARCH ABC DEF GH IJKLMN"
        com = "[m] abcdef ghijklm nopqrstu vw xyzab"
        c = fits.Card(k, 0.009125, com)
        expected_str = f"{k} = 0.009125 / {com}"
>       assert str(c)[: len(expected_str)] == expected_str

[1m[31mastropy/io/fits/tests/test_header.py[0m:151: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
[1m[31mastropy/io/fits/card.py[0m:213: in __str__
    return self.image
[1m[31mastropy/io/fits/card.py[0m:530: in image
    self._image = self._format_image()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = ('ABC DEF GH IJKLMN', 0.009125, '[m] abcdef ghijklm nopqrstu vw xyzab')

    def _format_image(self):
        keyword = self._format_keyword()
    
        value = self._format_value()
        is_commentary = keyword.strip() in self._commentary_keywords
        if is_commentary:
            comment = ""
        else:
            comment = self._format_comment()
    
        # equal sign string
        # by default use the standard value indicator even for HIERARCH cards;
        # later we may abbreviate it if necessary
        delimiter = VALUE_INDICATOR
        if is_commentary:
            delimiter = ""
    
        # put all parts together
        output = "".join([keyword, delimiter, value, comment])
    
        # For HIERARCH cards we can save a bit of space if necessary by
        # removing the space between the keyword and the equals sign; I'm
        # guessing this is part of the HIEARCH card specification
        keywordvalue_length = len(keyword) + len(delimiter) + len(value)
        if keywordvalue_length > self.length and keyword.startswith("HIERARCH"):
            if keywordvalue_length == self.length + 1 and keyword[-1] == " ":
                output = "".join([keyword[:-1], delimiter, value, comment])
            else:
                # I guess the HIERARCH card spec is incompatible with CONTINUE
                # cards
                raise ValueError(
                    f"The header keyword {self.keyword!r} with its value is too long"
                )
    
        if len(output) <= self.length:
            output = f"{output:80}"
        else:
            # longstring case (CONTINUE card)
            # try not to use CONTINUE if the string value can fit in one line.
            # Instead, just truncate the comment
            if isinstance(self.value, str) and len(value) > (self.length - 10):
                output = self._format_long_image()
            else:
>               warnings.warn(
                    "Card is too long, comment will be truncated.", VerifyWarning
                )
[1m[31mE               astropy.io.fits.verify.VerifyWarning: Card is too long, comment will be truncated.[0m

[1m[31mastropy/io/fits/card.py[0m:1038: VerifyWarning
==================================== PASSES ====================================
[32m[1m__________ TestHeaderFunctions.test_short_hierarch_create_and_update ___________[0m
----------------------------- Captured stdout call -----------------------------
[<class 'astropy.io.fits.verify.VerifyWarning'>]
[32m[1m__________ TestRecordValuedKeywordCards.test_fitsheader_table_feature __________[0m
----------------------------- Captured stderr call -----------------------------
WARNING: /testbed/astropy/io/fits/tests/data/zerowidth.fits: Extension DOES_NOT_EXIST not found. [astropy.io.fits.scripts.fitsheader]
WARNING: /testbed/astropy/io/fits/tests/data/zerowidth.fits (HDU AIPS FQ): Keyword DOES_NOT_EXIST not found. [astropy.io.fits.scripts.fitsheader]
------------------------------ Captured log call -------------------------------
[33mWARNING [0m astropy:fitsheader.py:214 /testbed/astropy/io/fits/tests/data/zerowidth.fits: Extension DOES_NOT_EXIST not found.
[33mWARNING [0m astropy:fitsheader.py:230 /testbed/astropy/io/fits/tests/data/zerowidth.fits (HDU AIPS FQ): Keyword DOES_NOT_EXIST not found.
[36m[1m=========================== short test summary info ============================[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mtest_shallow_copy[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mtest_init_with_header[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mtest_init_with_dict[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mtest_init_with_ordereddict[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_rename_keyword[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_indexing_case[A][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_indexing_case[a][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_card_constructor_default_args[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_card_from_bytes[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_string_value_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_boolean_value_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_long_integer_value_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_floating_point_value_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_complex_value_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_card_image_constructed_too_long[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_constructor_filter_illegal_data_structures[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_keyword_too_long[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_illegal_characters_in_key[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_add_history[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_add_blank[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_update[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_update_comment[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_commentary_cards[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_commentary_card_created_by_fromstring[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_commentary_card_will_not_parse_numerical_value[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_equal_sign_after_column8[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_blank_keyword[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_specify_undefined_value[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_complex_number_using_string_input[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_fixable_non_standard_fits_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_fixable_non_fsc[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_undefined_value_using_string_input[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_undefined_keys_values[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_mislocated_equal_sign[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_equal_only_up_to_column_10[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_verify_invalid_equal_sign[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_fix_invalid_equal_sign[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_long_string_value[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_long_string_value_with_multiple_long_words[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_long_unicode_string[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_long_string_repr[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_blank_keyword_long_value[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_long_string_from_file[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_word_in_long_string_too_long[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_long_string_value_via_fromstring[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_continue_card_with_equals_in_value[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_final_continue_card_lacks_ampersand[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_final_continue_card_ampersand_removal_on_long_comments[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_hierarch_card_creation[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_hierarch_with_abbrev_value_indicator[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_hierarch_not_warn[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_hierarch_keyword_whitespace[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_verify_mixed_case_hierarch[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_missing_keyword[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_hierarch_card_lookup[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_hierarch_card_delete[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_hierarch_card_insert_delete[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_hierarch_create_and_update[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_short_hierarch_create_and_update[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_setitem_invalid[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_setitem_1tuple[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_setitem_2tuple[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_set_value_to_none[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_set_comment_only[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_iter[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_slice[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_slice_assignment[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_slice_delete[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_wildcard_slice[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_wildcard_with_hyphen[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_wildcard_slice_assignment[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_wildcard_slice_deletion[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_history[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_clear[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_clear_write[fitsext0][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_clear_write[fitsext1][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_fromkeys[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_fromkeys_with_value[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_fromkeys_with_value_and_comment[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_fromkeys_with_duplicates[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_items[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_iterkeys[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_itervalues[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_keys[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_list_like_pop[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_dict_like_pop[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_popitem[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_setdefault[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_update_from_dict[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_update_from_iterable[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_extend[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_extend_unique[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_extend_unique_commentary[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_extend_update[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_extend_update_commentary[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_extend_exact[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_count[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_append_use_blanks[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_append_keyword_only[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_insert_use_blanks[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_insert_before_keyword[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_remove[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_comments[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_comment_slices_and_filters[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_comment_slice_filter_assign[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_commentary_slicing[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_update_commentary[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_commentary_comparison[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_long_commentary_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_totxtfile[][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_totxtfile[home_is_data][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_totxtfile[home_is_data, pathlib][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_tofile[][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_tofile[home_is_data][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_tofile[home_is_data, pathlib][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_fromfile[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_fromtextfile[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_fromtextfile_with_end_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_append_end_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_invalid_end_cards[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_invalid_characters[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_unnecessary_move[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_invalid_float_cards[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_invalid_float_cards2[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_leading_zeros[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_assign_boolean[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_method_keyword_normalization[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_end_in_comment[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_assign_unicode[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_assign_non_ascii[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_strip_whitespace[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_keep_duplicate_history_in_orig_header[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_invalid_keyword_cards[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_fix_hierarch_with_invalid_value[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_assign_inf_nan[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_update_bool[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_update_numeric[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_newlines_in_commentary[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_long_commentary_card_appended_to_header[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_fromstring_bytes[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_set_keyword_with_space[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_strip[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_update_invalid_card[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_index_numpy_int[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_header_data_size[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_initialize_rvkc[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_parse_field_specifier[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_update_field_specifier[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_field_specifier_case_senstivity[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_get_rvkc_by_index[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_get_rvkc_by_keyword[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_get_rvkc_by_keyword_and_field_specifier[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_access_nonexistent_rvkc[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_update_rvkc[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_update_rvkc_2[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_raw_keyword_value[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_rvkc_insert_after[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_rvkc_delete[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_pattern_matching_keys[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_pattern_matching_key_deletion[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_successive_pattern_matching[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_rvkc_in_cardlist_keys[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_rvkc_in_cardlist_values[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_rvkc_value_attribute[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_overly_permissive_parsing[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_overly_aggressive_rvkc_lookup[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_fitsheader_script[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_fitsheader_compressed_from_primary_image_ext[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_fitsheader_table_feature[0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_hdu_writeto_mode[wb][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_hdu_writeto_mode[wb+][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_hdu_writeto_mode[ab][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mTestRecordValuedKeywordCards::test_hdu_writeto_mode[ab+][0m
[32mPASSED[0m astropy/io/fits/tests/test_header.py::[1mtest_subclass[0m
[31mFAILED[0m astropy/io/fits/tests/test_header.py::[1mTestHeaderFunctions::test_floating_point_string_representation_card[0m - astropy.io.fits.verify.VerifyWarning: Card is too long, comment will be tru...
[31m======================== [31m[1m1 failed[0m, [32m174 passed[0m[31m in 0.34s[0m[31m =========================[0m
+ git checkout a3f4ae6cd24d5ecdf49f213d77b3513dd509a06c astropy/io/fits/tests/test_header.py
Updated 1 path from 36c2e27

```
