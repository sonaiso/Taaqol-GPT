from __future__ import annotations

from sim_agent.f_experiment import run_f_experiment


def main() -> None:
    report = run_f_experiment()
    for result in report.results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{result.index:02d} {status} {result.code.value}")
    print(f"structural_valid={report.structural_valid}")
    print(f"ten_condition_passed={report.ten_condition_passed}")
    print(report.mapping_fingerprint)


if __name__ == "__main__":
    main()
