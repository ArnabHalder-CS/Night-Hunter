# NIGHT HUNTER - HTTP Performance & Availability Benchmark
# Standard / Authorized HTTP Latency and Response-Time Diagnostics
# Similar to ApacheBench (ab) and standard uptime monitoring

import time
import threading

import requests

from core.logger import log_info, log_error


# =========================================================
# BENCHMARK SETTINGS
# =========================================================

MAX_DURATION = 300


# =========================================================
# WORKER
# =========================================================

def _stress_worker(
    url,
    stop_event,
    statistics,
    lock
):

    session = requests.Session()

    while not stop_event.is_set():

        try:

            start_time = time.perf_counter()

            response = session.get(
                url,
                timeout=5,
                allow_redirects=False
            )

            elapsed = (
                time.perf_counter() - start_time
            )

            with lock:

                statistics["requests"] += 1

                statistics["total_time"] += elapsed

                if response.status_code < 400:

                    statistics["successful"] += 1

                else:

                    statistics["failed"] += 1

        except requests.RequestException:

            with lock:

                statistics["requests"] += 1
                statistics["failed"] += 1

        except Exception:

            with lock:

                statistics["requests"] += 1
                statistics["failed"] += 1


# =========================================================
# HTTP PERFORMANCE BENCHMARK
# =========================================================

def run_load_benchmark(
    url,
    duration=60,
    workers=5
):
    # Never allow the session to exceed
    # the maximum authorized test duration.
    duration = min(
        int(duration),
        MAX_DURATION
    )

    # Keep concurrency deliberately bounded
    # for this lab-oriented testing module.
    workers = max(
        1,
        min(int(workers), 20)
    )

    statistics = {
        "requests": 0,
        "successful": 0,
        "failed": 0,
        "total_time": 0.0
    }

    stop_event = threading.Event()
    lock = threading.Lock()

    threads = []

    try:

        log_info(
            "========================================"
        )

        log_info(
            "NIGHT HUNTER HTTP BENCHMARK DIAGNOSTIC"
        )

        log_info(
            "========================================"
        )

        log_info(
            f"Target: {url}"
        )

        log_info(
            f"Duration: {duration} seconds"
        )

        log_info(
            f"Workers: {workers}"
        )

        log_info(
            "Test will stop automatically."
        )

        # -------------------------------------------------
        # Create workers
        # -------------------------------------------------

        for _ in range(workers):

            thread = threading.Thread(
                target=_stress_worker,
                args=(
                    url,
                    stop_event,
                    statistics,
                    lock
                ),
                daemon=True
            )

            threads.append(thread)

            thread.start()

        # -------------------------------------------------
        # Test timer
        # -------------------------------------------------

        start_time = time.monotonic()

        while True:

            elapsed = (
                time.monotonic() - start_time
            )

            if elapsed >= duration:

                break

            time.sleep(1)

            with lock:

                request_count = (
                    statistics["requests"]
                )

            log_info(
                f"Elapsed: {int(elapsed) + 1}s | "
                f"Requests: {request_count}"
            )

        # -------------------------------------------------
        # Stop all workers
        # -------------------------------------------------

        stop_event.set()

        for thread in threads:

            thread.join(
                timeout=2
            )

        # -------------------------------------------------
        # Calculate results
        # -------------------------------------------------

        with lock:

            total_requests = (
                statistics["requests"]
            )

            successful = (
                statistics["successful"]
            )

            failed = (
                statistics["failed"]
            )

            total_time = (
                statistics["total_time"]
            )

        if total_requests > 0:

            average_time = (
                total_time /
                total_requests
            ) * 1000

            requests_per_second = (
                total_requests /
                duration
            )

        else:

            average_time = 0
            requests_per_second = 0

        report = {
            "target": url,
            "duration_seconds": duration,
            "workers": workers,
            "total_requests": total_requests,
            "successful_requests": successful,
            "failed_requests": failed,
            "requests_per_second": round(
                requests_per_second,
                2
            ),
            "average_response_time_ms": round(
                average_time,
                2
            )
        }

        log_info(
            "========================================"
        )

        log_info(
            "STRESS TEST COMPLETED"
        )

        log_info(
            f"Total requests: {total_requests}"
        )

        log_info(
            f"Successful: {successful}"
        )

        log_info(
            f"Failed: {failed}"
        )

        log_info(
            f"Requests/sec: "
            f"{requests_per_second:.2f}"
        )

        log_info(
            f"Average response time: "
            f"{average_time:.2f} ms"
        )

        log_info(
            "========================================"
        )

        return report

    except KeyboardInterrupt:

        stop_event.set()

        log_info(
            "Stress test stopped manually."
        )

        for thread in threads:

            thread.join(
                timeout=2
            )

        return statistics

    except Exception as error:

        stop_event.set()

        log_error(
            f"Stress test failed: {error}"
        )

        return statistics


# Backward-compatible alias
run_stress_test = run_load_benchmark