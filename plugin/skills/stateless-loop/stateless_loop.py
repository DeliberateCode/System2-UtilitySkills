#!/usr/bin/env python3
"""Stateless loop: runs `claude -p` repeatedly until STATUS: CLEAN or max iterations."""

import argparse
import io
import subprocess
import sys
import threading


STOP_DIRECTIVE = (
    "\n\n---\n"
    "STOP CONDITION: When the task above is fully resolved and no further action "
    "is needed, output exactly this line on its own:\n"
    "STATUS: CLEAN\n"
    "If the task is NOT fully resolved, do NOT output STATUS: CLEAN. "
    "Describe what remains.\n"
    "---"
)


def _stream_and_capture(pipe, echo, buf):
    """Read lines from pipe, echo to the given stream, and collect in buf."""
    for line in iter(pipe.readline, ""):
        echo.write(line)
        echo.flush()
        buf.write(line)
    pipe.close()


def execute_stateless_loop(instruction, max_iterations=10):
    full_prompt = instruction + STOP_DIRECTIVE

    for i in range(1, max_iterations + 1):
        print(f"\n{'=' * 60}", flush=True)
        print(f"  Iteration {i}/{max_iterations}", flush=True)
        print(f"{'=' * 60}\n", flush=True)

        try:
            proc = subprocess.Popen(
                ["claude", "-p", full_prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout_buf = io.StringIO()
            stderr_buf = io.StringIO()

            out_thread = threading.Thread(
                target=_stream_and_capture,
                args=(proc.stdout, sys.stdout, stdout_buf),
            )
            err_thread = threading.Thread(
                target=_stream_and_capture,
                args=(proc.stderr, sys.stderr, stderr_buf),
            )

            out_thread.start()
            err_thread.start()

            proc.wait()
            out_thread.join()
            err_thread.join()

            captured_stdout = stdout_buf.getvalue()

            if "STATUS: CLEAN" in captured_stdout:
                print(f"\n{'=' * 60}", flush=True)
                print(f"  Resolved after {i} iteration(s).", flush=True)
                print(f"{'=' * 60}", flush=True)
                return 0

            if proc.returncode != 0:
                print(
                    f"\n[claude -p exited with code {proc.returncode}]",
                    flush=True,
                )

        except KeyboardInterrupt:
            print(f"\n\n[Interrupted by user at iteration {i}]", flush=True)
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
            return 130

        except Exception as e:
            print(f"\n[Error at iteration {i}]: {e}", flush=True)

    print(f"\n{'=' * 60}", flush=True)
    print(
        f"  Max iterations ({max_iterations}) reached without STATUS: CLEAN.",
        flush=True,
    )
    print(f"{'=' * 60}", flush=True)
    return 1


def main():
    parser = argparse.ArgumentParser(
        description="Run an instruction in a stateless claude -p loop.",
    )
    parser.add_argument(
        "instruction",
        help="The instruction to execute each iteration",
    )
    parser.add_argument(
        "--max_iterations",
        type=int,
        default=10,
        help="Maximum number of loop iterations (default: 10)",
    )
    args = parser.parse_args()
    sys.exit(execute_stateless_loop(args.instruction, args.max_iterations))


if __name__ == "__main__":
    main()
