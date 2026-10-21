# Remote Restore and Resume

## 1. Clone the frozen handoff

```bash
git clone https://github.com/Wyb0627/pi_self_harness.git
cd pi_self_harness
handoff_commit="$(git log origin/main   --grep='docs(agent): checkpoint partial DGM-P2 experiment'   -n 1 --format=%H)"
test -n "$handoff_commit"
git checkout "$handoff_commit"
npm install --ignore-scripts
(cd pi-rollback && npm install --ignore-scripts)
python3 research_output/checkpoints/20261020_timeoutfix1_handoff/validate_checkpoint.py
```

Use Node `v26.5.0`; the frozen execution stack checks this version.

## 2. Restore external dependencies

The Git checkpoint intentionally excludes Docker images, the SWE-bench checkout,
the Python virtual environment, npm caches, and credentials.

```bash
git clone https://github.com/princeton-nlp/SWE-bench.git datasets/SWE-bench
git -C datasets/SWE-bench checkout dc4c087c2b9e4cefebf2e3d201d27e362d899e0f
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 -m pip install   -r research_output/checkpoints/20261020_timeoutfix1_handoff/frozen-execution-python-requirements.txt
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 -m venv   /tmp/pi-swebench-runtime
/tmp/pi-swebench-runtime/bin/python -m pip install --upgrade pip==26.1.2
/tmp/pi-swebench-runtime/bin/python -m pip install -r   research_output/checkpoints/20261020_timeoutfix1_handoff/swebench-runtime-requirements.txt
colima start --cpu 8 --memory 16 --disk 120
```

Install the official Python.org macOS Python 3.13.14 framework build. Before
resuming, verify
`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13` has SHA-256
`ee3c4103b97e32a98e98cfad7f6ca4d09b2ab2dc16f3d28e18b54a4a0244efe0`.
The first requirements file recreates the environment identity checked by
preflight; the second recreates the SWE-bench execution virtual environment.

The frozen D_evolve rows and preprocessing outputs are already in
`runtime/evolve-inputs/`. The tracked full manifest is
`research_output/clm_budgeted_evolution_20260924_125503/dgm_swebench_verified_200.v1.json`
with SHA-256 `3fb913fbc73a05c1f7cae3b708c976374632820b58377aab5de08b742f96c967`.
Do not materialize D_test before both searches seal.

## 3. Restore checkpoint directories

```bash
mkdir -p research_output/resumed_20261020_timeoutfix1
cp -R   research_output/checkpoints/20261020_timeoutfix1_handoff/dgm_seed20261014_v2_timeoutfix1   research_output/resumed_20261020_timeoutfix1/
cp -R   research_output/checkpoints/20261020_timeoutfix1_handoff/p2_seed20261014_v2_timeoutfix1   research_output/resumed_20261020_timeoutfix1/
```

The DGM checkpoint resumes at slot 4. It reuses the persisted mutation for slot
4, but reruns `django__django-10973` because the interrupted evaluator never
produced a complete observation. All 190 complete observations are cache-bound by
identity and observation hashes.

## 4. Inject credentials and start the local proxy

Obtain `ROLLBACK_ENDPOINT_API_KEY` through the user's secure channel. Do not save
it in the repository or command history.

```bash
read -s "ROLLBACK_ENDPOINT_API_KEY?Endpoint API key: "
export ROLLBACK_ENDPOINT_API_KEY
echo
export PYTHONUNBUFFERED=1
ca_bundle="$(mktemp /tmp/pi-timeoutfix1-ca.XXXXXX.pem)"
cp /etc/ssl/cert.pem "$ca_bundle"
security find-certificate -a -p /Library/Keychains/System.keychain >>"$ca_bundle"
chmod 600 "$ca_bundle"
SSL_CERT_FILE="$ca_bundle" /tmp/pi-swebench-runtime/bin/python   rollback_mvp/openai_buffered_sse_proxy.py   --host 127.0.0.1 --port 8765
```

Run the proxy in a dedicated terminal. Verify the variable is present without
printing it, `docker info` succeeds, and port 8765 accepts a connection.

## 5. Non-paid consistency checks

```bash
/tmp/pi-swebench-runtime/bin/python rollback_mvp/run_dgm_pi_evolution.py preflight   --run-id dgm-pilot-s20261014-v2-timeoutfix1   --output research_output/resumed_20261020_timeoutfix1/dgm_seed20261014_v2_timeoutfix1   --seed 20261014 --proposal-slots 10 --proposals-per-wave 2

/tmp/pi-swebench-runtime/bin/python rollback_mvp/run_dgm_pi_evolution.py preflight   --run-id p2-pilot-s20261014-v2-timeoutfix1   --output research_output/resumed_20261020_timeoutfix1/p2_seed20261014_v2_timeoutfix1   --seed 20261014 --proposal-slots 10 --proposals-per-wave 2 --enable-rf-clm
```

Repeat each preflight with `--execute` only after the key, proxy, and Docker are
ready.

## 6. Resume DGM, then P2

```bash
caffeinate -dimsu /tmp/pi-swebench-runtime/bin/python   rollback_mvp/run_dgm_pi_evolution.py search   --run-id dgm-pilot-s20261014-v2-timeoutfix1   --output research_output/resumed_20261020_timeoutfix1/dgm_seed20261014_v2_timeoutfix1   --seed 20261014 --proposal-slots 10 --proposals-per-wave 2   --confirm-paid-run I_APPROVE_DGM200_API_SPEND --execute
```

Confirm DGM produced a valid `search-seal.json`. Only then run:

```bash
caffeinate -dimsu /tmp/pi-swebench-runtime/bin/python   rollback_mvp/run_dgm_pi_evolution.py search   --run-id p2-pilot-s20261014-v2-timeoutfix1   --output research_output/resumed_20261020_timeoutfix1/p2_seed20261014_v2_timeoutfix1   --seed 20261014 --proposal-slots 10 --proposals-per-wave 2 --enable-rf-clm   --confirm-paid-run I_APPROVE_DGM200_API_SPEND --execute
```

Concurrency remains fixed at 1. The search token cap is already `null`, so the
current 70,678,467 search tokens do
not approach a search stop. The 80,000,000 caps are separate reserves for each
140-task endpoint scope; configured reservation is at most
`140 * 512,000 = 71,680,000` tokens per scope. Changing these frozen values would
change the config and protocol hashes, so this checkpoint preserves them.

## 7. Consume D_test only after both search seals

Only after both `search-seal.json` files exist, run:

```bash
caffeinate -dimsu /tmp/pi-swebench-runtime/bin/python   rollback_mvp/run_dgm_pi_evolution.py endpoint   --run-id dgm-pilot-s20261014-v2-timeoutfix1   --output research_output/resumed_20261020_timeoutfix1/dgm_seed20261014_v2_timeoutfix1   --seed 20261014 --proposal-slots 10 --proposals-per-wave 2   --confirm-paid-run I_APPROVE_DGM200_API_SPEND --execute

caffeinate -dimsu /tmp/pi-swebench-runtime/bin/python   rollback_mvp/run_dgm_pi_evolution.py endpoint   --run-id p2-pilot-s20261014-v2-timeoutfix1   --output research_output/resumed_20261020_timeoutfix1/p2_seed20261014_v2_timeoutfix1   --seed 20261014 --proposal-slots 10 --proposals-per-wave 2 --enable-rf-clm   --confirm-paid-run I_APPROVE_DGM200_API_SPEND --execute
```

These endpoint commands are the first operations allowed to materialize the
committed big-140 rows. Do not run either endpoint early. Remove the temporary CA
file after both arms finish.
