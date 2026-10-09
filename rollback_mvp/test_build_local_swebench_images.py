import unittest
from types import SimpleNamespace

from build_local_swebench_images import (
    add_pip_network_resilience,
    local_dockerfile,
)


class BuildLocalSwebenchImagesTest(unittest.TestCase):
    def test_adds_build_only_pip_settings_after_from(self):
        dockerfile = "FROM python:3.9\nRUN python -m pip install package\n"

        result = add_pip_network_resilience(dockerfile)

        self.assertEqual(
            result,
            "FROM python:3.9\n"
            "ARG PIP_DEFAULT_TIMEOUT=120\n"
            "ARG PIP_RETRIES=20\n"
            "RUN python -m pip install package\n",
        )

    def test_rejects_dockerfile_without_from(self):
        with self.assertRaisesRegex(ValueError, "no FROM"):
            add_pip_network_resilience("RUN true\n")

    def test_wheelhouse_is_available_to_instance_setup_and_evaluator(self):
        spec = SimpleNamespace(
            arch="arm64",
            platform="linux/arm64/v8",
            env_image_key="sweb.env.arm64.test:latest",
        )

        result = local_dockerfile(spec, use_wheelhouse=True)

        self.assertIn("COPY ./wheelhouse /root/pip-wheelhouse\n", result)
        self.assertIn("ENV PIP_NO_INDEX=1\n", result)
        self.assertIn("ENV PIP_FIND_LINKS=/root/pip-wheelhouse\n", result)
        self.assertIn("RUN /bin/bash /root/setup_local_repo.sh\n", result)


if __name__ == "__main__":
    unittest.main()
