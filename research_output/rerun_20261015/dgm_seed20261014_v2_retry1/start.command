#!/bin/zsh

cd /Users/bytedance/codes/pi || exit 1

output="research_output/rerun_20261015/dgm_seed20261014_v2_retry1"
source_run="research_output/rerun_20261014/dgm_seed20261014"
ca_bundle="$output/combined-ca.pem"
mkdir -p "$output"
exec > >(tee -a "$output/terminal.log") 2>&1

printf '\033]0;DGM Pi protocol-v2 retry1 seed 20261014\007'
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] starting dgm-pilot-s20261014-v2-retry1"
echo "commit: $(git rev-parse HEAD)"

proxy_pid=""
cleanup_proxy() {
	if [[ -n "$proxy_pid" ]] && kill -0 "$proxy_pid" 2>/dev/null; then
		kill "$proxy_pid"
		wait "$proxy_pid" 2>/dev/null
	fi
}
proxy_ready() {
	curl \
		--silent \
		--output /dev/null \
		--max-time 1 \
		http://127.0.0.1:8765/
}
trap cleanup_proxy EXIT INT TERM HUP

cp /etc/ssl/cert.pem "$ca_bundle"
security find-certificate \
	-a \
	-p \
	/Library/Keychains/System.keychain \
	>>"$ca_bundle"
chmod 600 "$ca_bundle"

if ! SSL_CERT_FILE="$ca_bundle" \
	/tmp/pi-swebench-runtime/bin/python \
	-c 'import urllib.request; urllib.request.urlopen("https://aicolate.tiktok-row.net/ai-gateway/openai/v1", timeout=10).read(1)'; then
	echo "Upstream TLS probe failed with the combined CA bundle."
	exit_code=1
elif proxy_ready; then
	echo "Port 8765 is already occupied; refusing an ambiguous proxy."
	exit_code=1
else
	SSL_CERT_FILE="$ca_bundle" \
		/tmp/pi-swebench-runtime/bin/python \
		rollback_mvp/openai_buffered_sse_proxy.py \
		--host 127.0.0.1 \
		--port 8765 \
		>"$output/proxy.log" 2>&1 &
	proxy_pid=$!
	for _ in {1..40}; do
		proxy_ready && break
		sleep 0.25
	done

	if ! proxy_ready; then
		echo "Local model proxy failed to start; see $output/proxy.log"
		exit_code=1
	else
		(
			export ROLLBACK_ENDPOINT_API_KEY="$(
				security find-generic-password \
					-s pi.rollback-endpoint-api-key \
					-w
			)"
			export PYTHONUNBUFFERED=1

			/tmp/pi-swebench-runtime/bin/python \
				rollback_mvp/run_dgm_pi_evolution.py prepare \
				--run-id dgm-pilot-s20261014-v2-retry1 \
				--output "$output" \
				--import-p0-from "$source_run" \
				--seed 20261014 \
				--proposal-slots 10 \
				--proposals-per-wave 2 &&
				/tmp/pi-swebench-runtime/bin/python \
					rollback_mvp/run_dgm_pi_evolution.py preflight \
					--run-id dgm-pilot-s20261014-v2-retry1 \
					--output "$output" \
					--seed 20261014 \
					--proposal-slots 10 \
					--proposals-per-wave 2 \
					--execute &&
				caffeinate -dimsu \
					/tmp/pi-swebench-runtime/bin/python \
					rollback_mvp/run_dgm_pi_evolution.py search \
					--run-id dgm-pilot-s20261014-v2-retry1 \
					--output "$output" \
					--seed 20261014 \
					--proposal-slots 10 \
					--proposals-per-wave 2 \
					--execute \
					--confirm-paid-run I_APPROVE_DGM200_API_SPEND
		)
		exit_code=$?
	fi
fi

cleanup_proxy
trap - EXIT INT TERM HUP
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] search exited with status $exit_code"
exec /bin/zsh -l
