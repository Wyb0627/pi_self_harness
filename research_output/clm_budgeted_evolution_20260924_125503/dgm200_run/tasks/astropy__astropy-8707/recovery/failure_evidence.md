# Official SWE-bench Evaluator Feedback

This is hidden evaluator information from the rejected original Pi submission. The resulting repair is feedback-assisted and is not a standard one-submission SWE-bench prediction.

Instance: `astropy__astropy-8707`

## Report

```json
{
    "astropy__astropy-8707": {
        "patch_is_None": false,
        "patch_exists": true,
        "patch_successfully_applied": true,
        "resolved": false,
        "tests_status": {
            "FAIL_TO_PASS": {
                "success": [],
                "failure": [
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_card_from_bytes"
                ]
            },
            "PASS_TO_PASS": {
                "success": [
                    "astropy/io/fits/tests/test_header.py::test_shallow_copy",
                    "astropy/io/fits/tests/test_header.py::test_init_with_header",
                    "astropy/io/fits/tests/test_header.py::test_init_with_dict",
                    "astropy/io/fits/tests/test_header.py::test_init_with_ordereddict"
                ],
                "failure": [
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_rename_keyword",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_card_constructor_default_args",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_string_value_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_boolean_value_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_integer_value_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_floating_point_value_card",
                    "astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_complex_value_card"
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
stresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959ca00>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_pattern_matching_key_deletion>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_pattern_matching_key_deletion is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
_ ERROR at setup of TestRecordValuedKeywordCards.test_successive_pattern_matching _

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf960864834c0>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959c700>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_successive_pattern_matching>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_successive_pattern_matching is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
__ ERROR at setup of TestRecordValuedKeywordCards.test_rvkc_in_cardlist_keys ___

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf960864833a0>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959c580>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_rvkc_in_cardlist_keys>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_in_cardlist_keys is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
_ ERROR at setup of TestRecordValuedKeywordCards.test_rvkc_in_cardlist_values __

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf9608646aa60>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959c790>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_rvkc_in_cardlist_values>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_in_cardlist_values is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
___ ERROR at setup of TestRecordValuedKeywordCards.test_rvkc_value_attribute ___

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf960862609d0>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959ce80>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_rvkc_value_attribute>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_value_attribute is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
_ ERROR at setup of TestRecordValuedKeywordCards.test_overly_permissive_parsing _

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf9608646a5e0>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959cf40>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_overly_permissive_parsing>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_overly_permissive_parsing is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
_ ERROR at setup of TestRecordValuedKeywordCards.test_overly_aggressive_rvkc_lookup _

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf96086260ca0>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959cd60>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_overly_aggressive_rvkc_lookup>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_overly_aggressive_rvkc_lookup is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
____ ERROR at setup of TestRecordValuedKeywordCards.test_fitsheader_script _____

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf9608646ab80>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959cc40>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_fitsheader_script>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_fitsheader_script is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
_ ERROR at setup of TestRecordValuedKeywordCards.test_fitsheader_table_feature _

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf9608646a5e0>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959ca60>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_fitsheader_table_feature>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_fitsheader_table_feature is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
___ ERROR at setup of TestRecordValuedKeywordCards.test_hdu_writeto_mode[wb] ___

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf960864d2af0>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf9609959adf0>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_hdu_writeto_mode[wb]>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[wb] is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
__ ERROR at setup of TestRecordValuedKeywordCards.test_hdu_writeto_mode[wb+] ___

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf96086483ee0>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf960995be550>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_hdu_writeto_mode[wb+]>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[wb+] is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
___ ERROR at setup of TestRecordValuedKeywordCards.test_hdu_writeto_mode[ab] ___

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf960861dcaf0>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf960995bef10>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_hdu_writeto_mode[ab]>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[ab] is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
__ ERROR at setup of TestRecordValuedKeywordCards.test_hdu_writeto_mode[ab+] ___

cls = <class '_pytest.runner.CallInfo'>
func = <function call_runtest_hook.<locals>.<lambda> at 0xf960861dcd30>
when = 'setup'
reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:157: in pytest_runtest_setup
    item.session._setupstate.setup(item)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:497: in setup
    raise exc
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/runner.py:494: in setup
    col.setup()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:1791: in setup
    self._request._fillfixtures()
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:566: in _fillfixtures
    item.funcargs[argname] = self.getfixturevalue(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:585: in getfixturevalue
    fixturedef = self._get_active_fixturedef(argname)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:607: in _get_active_fixturedef
    self._compute_fixture_value(fixturedef)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:693: in _compute_fixture_value
    fixturedef.execute(request=subrequest)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1069: in execute
    result = ihook.pytest_fixture_setup(fixturedef=self, request=request)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:1123: in pytest_fixture_setup
    result = call_fixture_func(fixturefunc, request, kwargs)
/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/fixtures.py:895: in call_fixture_func
    fixture_result = next(generator)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <astropy.io.fits.tests.test_header.TestRecordValuedKeywordCards object at 0xf960995befa0>
request = <SubRequest '_xunit_setup_method_fixture_TestRecordValuedKeywordCards' for <Function test_hdu_writeto_mode[ab+]>>

    @fixtures.fixture(
        autouse=True,
        scope="function",
        # Use a unique name to speed up lookup.
        name=f"_xunit_setup_method_fixture_{self.obj.__qualname__}",
    )
    def xunit_setup_method_fixture(self, request) -> Generator[None, None, None]:
        method = request.function
        if setup_method is not None:
            func = getattr(self, setup_name)
            _call_with_optional_argument(func, method)
            if emit_nose_setup_warning:
>               warnings.warn(
                    NOSE_SUPPORT_METHOD.format(
                        nodeid=request.node.nodeid, method="setup"
                    ),
                    stacklevel=2,
                )
E               pytest.PytestRemovedIn8Warning: Support for nose tests is deprecated and will be removed in a future release.
E               astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[ab+] is using nose-specific method: `setup(self)`
E               To remove this warning, rename it to `setup_method(self)`
E               See docs: https://docs.pytest.org/en/stable/deprecations.html#support-for-tests-written-for-nose

/opt/miniconda3/envs/testbed/lib/python3.9/site-packages/_pytest/python.py:898: PytestRemovedIn8Warning
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED astropy/io/fits/tests/test_header.py::test_shallow_copy
PASSED astropy/io/fits/tests/test_header.py::test_init_with_header
PASSED astropy/io/fits/tests/test_header.py::test_init_with_dict
PASSED astropy/io/fits/tests/test_header.py::test_init_with_ordereddict
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_rename_keyword
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_card_constructor_default_args
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_card_from_bytes
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_string_value_card
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_boolean_value_card
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_integer_value_card
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_floating_point_value_card
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_complex_value_card
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_card_image_constructed_too_long
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_constructor_filter_illegal_data_structures
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_keyword_too_long
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_illegal_characters_in_key
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_add_commentary
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_comment
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_cards
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_card_created_by_fromstring
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_card_will_not_parse_numerical_value
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_equal_sign_after_column8
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_blank_keyword
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_specify_undefined_value
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_complex_number_using_string_input
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_fixable_non_standard_fits_card
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_fixable_non_fsc
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_undefined_value_using_string_input
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_mislocated_equal_sign
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_equal_only_up_to_column_10
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_verify_invalid_equal_sign
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_fix_invalid_equal_sign
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_string_value
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_unicode_string
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_string_repr
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_blank_keyword_long_value
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_string_from_file
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_word_in_long_string_too_long
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_string_value_via_fromstring
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_continue_card_with_equals_in_value
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_final_continue_card_lacks_ampersand
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_final_continue_card_ampersand_removal_on_long_comments
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_card_creation
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_with_abbrev_value_indicator
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_keyword_whitespace
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_verify_mixed_case_hierarch
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_missing_keyword
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_card_lookup
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_card_delete
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_card_insert_delete
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_hierarch_create_and_update
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_short_hierarch_create_and_update
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_setitem_invalid
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_setitem_1tuple
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_setitem_2tuple
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_set_value_to_none
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_set_comment_only
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_iter
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_slice
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_slice_assignment
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_slice_delete
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_wildcard_slice
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_wildcard_with_hyphen
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_wildcard_slice_assignment
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_wildcard_slice_deletion
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_history
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_clear
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromkeys
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromkeys_with_value
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromkeys_with_value_and_comment
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromkeys_with_duplicates
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_items
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_iterkeys
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_itervalues
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_keys
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_list_like_pop
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_dict_like_pop
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_popitem
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_setdefault
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_from_dict
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_from_iterable
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_unique
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_unique_commentary
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_update
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_update_commentary
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_extend_exact
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_count
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_append_use_blanks
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_append_keyword_only
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_insert_use_blanks
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_insert_before_keyword
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_remove
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_comments
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_comment_slices_and_filters
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_comment_slice_filter_assign
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_slicing
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_commentary
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_commentary_comparison
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_long_commentary_card
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_totxtfile
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromtextfile
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromtextfile_with_end_card
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_append_end_card
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_end_cards
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_characters
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_unnecessary_move
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_float_cards
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_float_cards2
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_leading_zeros
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_assign_boolean
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_method_keyword_normalization
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_end_in_comment
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_assign_unicode
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_assign_non_ascii
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_strip_whitespace
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_keep_duplicate_history_in_orig_header
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_invalid_keyword_cards
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_fix_hierarch_with_invalid_value
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_assign_inf_nan
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_bool
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_update_numeric
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_newlines_in_commentary
ERROR astropy/io/fits/tests/test_header.py::TestHeaderFunctions::test_header_fromstring_bytes
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_initialize_rvkc
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_parse_field_specifier
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_update_field_specifier
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_field_specifier_case_senstivity
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_get_rvkc_by_index
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_get_rvkc_by_keyword
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_get_rvkc_by_keyword_and_field_specifier
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_access_nonexistent_rvkc
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_update_rvkc
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_update_rvkc_2
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_raw_keyword_value
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_insert_after
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_delete
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_pattern_matching_keys
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_pattern_matching_key_deletion
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_successive_pattern_matching
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_in_cardlist_keys
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_in_cardlist_values
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_rvkc_value_attribute
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_overly_permissive_parsing
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_overly_aggressive_rvkc_lookup
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_fitsheader_script
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_fitsheader_table_feature
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[wb]
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[wb+]
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[ab]
ERROR astropy/io/fits/tests/test_header.py::TestRecordValuedKeywordCards::test_hdu_writeto_mode[ab+]
======================== 4 passed, 148 errors in 7.14s =========================
+ git checkout a85a0747c54bac75e9c3b2fe436b105ea029d6cf astropy/io/fits/tests/test_header.py
Updated 1 path from a102106

```
