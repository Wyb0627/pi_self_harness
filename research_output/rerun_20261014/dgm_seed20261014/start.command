#!/bin/zsh

cd /Users/bytedance/codes/pi || exit 1

output="research_output/rerun_20261014/dgm_seed20261014"
mkdir -p "$output"
exec > >(tee -a "$output/terminal.log") 2>&1

printf '\033]0;DGM Pi pilot seed 20261014\007'
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] starting dgm-pilot-s20261014"
echo "commit: $(git rev-parse HEAD)"

(
	export ROLLBACK_ENDPOINT_API_KEY="$(
		security find-generic-password \
			-s pi.rollback-endpoint-api-key \
			-w
	)"
	export PYTHONUNBUFFERED=1

	/tmp/pi-swebench-runtime/bin/python \
		rollback_mvp/run_dgm_pi_evolution.py prepare \
		--run-id dgm-pilot-s20261014 \
		--output "$output" \
		--seed 20261014 \
		--proposal-slots 10 \
		--proposals-per-wave 2 &&
		/tmp/pi-swebench-runtime/bin/python \
			rollback_mvp/run_dgm_pi_evolution.py preflight \
			--run-id dgm-pilot-s20261014 \
			--output "$output" \
			--seed 20261014 \
			--proposal-slots 10 \
			--proposals-per-wave 2 \
			--execute &&
		caffeinate -dimsu \
			/tmp/pi-swebench-runtime/bin/python \
			rollback_mvp/run_dgm_pi_evolution.py search \
			--run-id dgm-pilot-s20261014 \
			--output "$output" \
			--seed 20261014 \
			--proposal-slots 10 \
			--proposals-per-wave 2 \
			--execute \
			--confirm-paid-run I_APPROVE_DGM200_API_SPEND
)

exit_code=$?
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] search exited with status $exit_code"
exec /bin/zsh -l
